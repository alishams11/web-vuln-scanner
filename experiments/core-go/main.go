package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"regexp"
	"strings"
	"sync"
	"time"
)

// Response is the output schema for each request
type Response struct {
	URL         string              `json:"url"`
	StatusCode  int                 `json:"status_code"`
	Headers     map[string][]string `json:"headers"`
	BodySnippet string              `json:"body_snippet"`
	DurationMs  float64             `json:"duration_ms"`
	Server      string              `json:"server,omitempty"`
	Title       string              `json:"title,omitempty"`
	Fingerprints []string           `json:"fingerprints,omitempty"`
	Error       string              `json:"error,omitempty"`
}

var titleRe = regexp.MustCompile(`(?is)<title[^>]*>(.*?)</title>`)

func extractTitle(body string) string {
	m := titleRe.FindStringSubmatch(body)
	if len(m) >= 2 {
		title := strings.TrimSpace(m[1])
		title = regexp.MustCompile(`\s+`).ReplaceAllString(title, " ")
		return title
	}
	return ""
}

func fingerprintFromHeadersAndBody(headers map[string][]string, body string) []string {
	var fps []string
	if serverVals, ok := headers["Server"]; ok && len(serverVals) > 0 {
		srv := strings.ToLower(serverVals[0])
		if strings.Contains(srv, "nginx") {
			fps = append(fps, "nginx")
		} else if strings.Contains(srv, "apache") {
			fps = append(fps, "apache")
		} else if strings.Contains(srv, "gunicorn") {
			fps = append(fps, "gunicorn")
		} else if strings.Contains(srv, "cloudflare") {
			fps = append(fps, "cloudflare")
		}
	}
	if xpb, ok := headers["X-Powered-By"]; ok && len(xpb) > 0 {
		val := strings.ToLower(strings.Join(xpb, " "))
		if strings.Contains(val, "php") {
			fps = append(fps, "php")
		}
		if strings.Contains(val, "express") {
			fps = append(fps, "express")
		}
	}

	lbody := strings.ToLower(body)
	if strings.Contains(lbody, "wp-content") || strings.Contains(lbody, "wordpress") {
		fps = append(fps, "wordpress")
	}
	if strings.Contains(lbody, "joomla") {
		fps = append(fps, "joomla")
	}
	if strings.Contains(lbody, "drupal") {
		fps = append(fps, "drupal")
	}
	if strings.Contains(lbody, "laravel") || strings.Contains(lbody, "csrf-token") {
		fps = append(fps, "laravel")
	}
	if strings.Contains(lbody, "static/ckeditor") {
		fps = append(fps, "ckeditor")
	}

	seen := map[string]bool{}
	out := []string{}
	for _, f := range fps {
		if f == "" {
			continue
		}
		if !seen[f] {
			seen[f] = true
			out = append(out, f)
		}
	}
	return out
}

// fetchURL performs the HTTP request and writes a Response to ch.
func fetchURL(client *http.Client, url string, wg *sync.WaitGroup, ch chan<- Response) {
	defer wg.Done()
	start := time.Now()

	fmt.Fprintf(os.Stderr, "[DEBUG] fetch start: %s\n", url)

	resp, err := client.Get(url)
	if err != nil {
		fmt.Fprintf(os.Stderr, "[DEBUG] fetch error: %s -> %v\n", url, err)
		ch <- Response{URL: url, Error: err.Error()}
		return
	}
	defer resp.Body.Close()

	bodyBytes, _ := io.ReadAll(io.LimitReader(resp.Body, 2048))
	body := string(bodyBytes)
	duration := time.Since(start).Seconds() * 1000

	server := ""
	if srv, ok := resp.Header["Server"]; ok && len(srv) > 0 {
		server = srv[0]
	}

	title := extractTitle(body)
	fps := fingerprintFromHeadersAndBody(resp.Header, body)

	res := Response{
		URL:         url,
		StatusCode:  resp.StatusCode,
		Headers:     resp.Header,
		BodySnippet: body,
		DurationMs:  duration,
		Server:      server,
		Title:       title,
		Fingerprints: fps,
	}

	fmt.Fprintf(os.Stderr, "[DEBUG] fetch done: %s status=%d dur=%.2fms title=%q fps=%v\n", url, res.StatusCode, res.DurationMs, res.Title, res.Fingerprints)
	ch <- res
}

func main() {
	concurrency := flag.Int("concurrency", 5, "maximum number of concurrent requests")
	rate := flag.Float64("rate", 2.0, "max requests per second")
	timeout := flag.Int("timeout", 10, "timeout per request (seconds)")
	flag.Parse()

	var urls []string
	if flag.NArg() > 0 {
		file, err := os.Open(flag.Arg(0))
		if err != nil {
			fmt.Fprintf(os.Stderr, "error opening file: %v\n", err)
			os.Exit(1)
		}
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			txt := strings.TrimSpace(scanner.Text())
			if txt != "" {
				urls = append(urls, txt)
			}
		}
		file.Close()
	} else {
		scanner := bufio.NewScanner(os.Stdin)
		for scanner.Scan() {
			txt := strings.TrimSpace(scanner.Text())
			if txt != "" {
				urls = append(urls, txt)
			}
		}
	}

	fmt.Fprintf(os.Stderr, "[DEBUG] total urls: %d\n", len(urls))
	if len(urls) == 0 {
		fmt.Fprintln(os.Stderr, "No URLs provided.")
		os.Exit(1)
	}

	client := &http.Client{Timeout: time.Duration(*timeout) * time.Second}
	sem := make(chan struct{}, *concurrency)
	rateInterval := time.Duration(float64(time.Second) / *rate)
	rateLimiter := time.NewTicker(rateInterval)
	defer rateLimiter.Stop()

	var wg sync.WaitGroup
	enc := json.NewEncoder(os.Stdout)

	// single encoder channel shared by all workers
	encCh := make(chan Response)
	go func() {
		for r := range encCh {
			_ = enc.Encode(r)
		}
	}()

	for _, u := range urls {
		u := u
		<-rateLimiter.C // enforce rate limit

		sem <- struct{}{}
		wg.Add(1)

		go func() {
			defer func() { <-sem }()
			fetchURL(client, u, &wg, encCh)
		}()
	}

	wg.Wait()
	// close encoder channel so encoder goroutine can finish
	close(encCh)
	fmt.Fprintln(os.Stderr, "[DEBUG] all done")
}


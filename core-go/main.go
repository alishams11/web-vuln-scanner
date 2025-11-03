package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"os"
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
	Error       string              `json:"error,omitempty"`
}

func main() {
	concurrency := flag.Int("concurrency", 5, "maximum number of concurrent requests")
	rate := flag.Float64("rate", 2.0, "max requests per second")
	timeout := flag.Int("timeout", 10, "timeout per request (seconds)")
	flag.Parse()

	var urls []string

	if flag.NArg() > 0 {
		// read from file
		file, err := os.Open(flag.Arg(0))
		if err != nil {
			fmt.Fprintf(os.Stderr, "error opening file: %v\n", err)
			os.Exit(1)
		}
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			urls = append(urls, strings.TrimSpace(scanner.Text()))
		}
		file.Close()
	} else {
		// read from stdin
		scanner := bufio.NewScanner(os.Stdin)
		for scanner.Scan() {
			urls = append(urls, strings.TrimSpace(scanner.Text()))
		}
	}

	client := &http.Client{Timeout: time.Duration(*timeout) * time.Second}
	sem := make(chan struct{}, *concurrency)
	rateLimiter := time.NewTicker(time.Duration(1e9 / *rate))
	defer rateLimiter.Stop()

	var wg sync.WaitGroup
	enc := json.NewEncoder(os.Stdout)

	for _, u := range urls {
		u := u
		<-rateLimiter.C // enforce rate limit

		sem <- struct{}{}
		wg.Add(1)

		go func() {
			defer wg.Done()
			defer func() { <-sem }()

			start := time.Now()
			resp, err := client.Get(u)
			res := Response{URL: u}

			if err != nil {
				res.Error = err.Error()
			} else {
				defer resp.Body.Close()
				res.StatusCode = resp.StatusCode
				res.Headers = resp.Header

				buf := make([]byte, 200)
				n, _ := resp.Body.Read(buf)
				res.BodySnippet = string(buf[:n])
			}

			res.DurationMs = float64(time.Since(start).Milliseconds())

			_ = enc.Encode(res)
		}()
	}

	wg.Wait()
}

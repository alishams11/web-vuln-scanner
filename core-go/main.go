package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
	"time"
)

type Response struct {
	URL        string              `json:"url"`
	StatusCode int                 `json:"status_code"`
	Headers    map[string][]string `json:"headers"`
	Body       string              `json:"body_snippet"`
	Duration   float64             `json:"duration_ms"`
	Error      string              `json:"error,omitempty"`
}

func fetchURL(url string, wg *sync.WaitGroup, ch chan<- Response) {
	defer wg.Done()
	start := time.Now()

	resp, err := http.Get(url)
	if err != nil {
		ch <- Response{URL: url, Error: err.Error()}
		return
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(io.LimitReader(resp.Body, 200)) 
	duration := time.Since(start).Seconds() * 1000

	ch <- Response{
		URL:        url,
		StatusCode: resp.StatusCode,
		Headers:    resp.Header,
		Body:       string(body),
		Duration:   duration,
	}
}

func main() {
	var urls []string


	if len(os.Args) > 1 {
		file, err := os.Open(os.Args[1])
		if err != nil {
			fmt.Fprintf(os.Stderr, "cannot open file: %v\n", err)
			os.Exit(1)
		}
		defer file.Close()
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			urls = append(urls, scanner.Text())
		}
	} else {
		scanner := bufio.NewScanner(os.Stdin)
		for scanner.Scan() {
			urls = append(urls, scanner.Text())
		}
	}

	if len(urls) == 0 {
		fmt.Fprintln(os.Stderr, "No URLs provided.")
		os.Exit(1)
	}

	ch := make(chan Response)
	var wg sync.WaitGroup

	for _, u := range urls {
		wg.Add(1)
		go fetchURL(u, &wg, ch)
	}

	go func() {
		wg.Wait()
		close(ch)
	}()

	encoder := json.NewEncoder(os.Stdout)
	for resp := range ch {
		encoder.Encode(resp)
	}
}


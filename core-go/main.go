package main

import (
	"encoding/json"
	"fmt"
	"os"
	"time"
)

type Response struct {
	URL      string  `json:"url"`
	Status   int     `json:"status"`
	Duration float64 `json:"duration_ms"`
	Host     string  `json:"host"`
	Ts       string  `json:"timestamp"`
}

func main() {
	now := time.Now().UTC().Format(time.RFC3339)
	out := []Response{
		{URL: "http://example.local/", Status: 200, Duration: 123.4, Host: "example.local", Ts: now},
	}
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	_ = enc.Encode(out)
	fmt.Println()
}


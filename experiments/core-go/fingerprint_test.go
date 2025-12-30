package main

import "testing"

func TestExtractTitle(t *testing.T) {
    html := "<html><head><title>  Test Title  </title></head><body>ok</body></html>"
    got := extractTitle(html)
    if got != "Test Title" {
        t.Fatalf("expected 'Test Title', got '%s'", got)
    }

    noTitle := "<html><head></head></html>"
    if extractTitle(noTitle) != "" {
        t.Fatalf("expected empty title for noTitle")
    }
}

func TestFingerprintFromHeadersAndBody(t *testing.T) {
    headers := map[string][]string{
        "Server":       {"nginx/1.18"},
        "X-Powered-By": {"Express"},
    }
    body := "<html>wp-content something</html>"
    fps := fingerprintFromHeadersAndBody(headers, body)
    want := map[string]bool{"nginx": true, "express": true, "wordpress": true}
    for _, f := range fps {
        if !want[f] {
            t.Fatalf("unexpected fingerprint: %s", f)
        }
        delete(want, f)
    }
    if len(want) != 0 {
        t.Fatalf("missing fingerprints: %v", want)
    }
}

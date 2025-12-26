import argparse
from pathlib import Path

from pywvs.templates.loaders import load_template
from pywvs.templates.runner import TemplateScanRunner
from pywvs.reporters.json_reporter import JSONReporter
from pywvs.reporters.html_reporter import HTMLReporter
from pywvs.auth.session import AuthSession


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="wvs",
        description="Web Vulnerability Scanner (template-driven)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser(
        "scan",
        help="Run a scan against a target using a template",
    )

    scan_parser.add_argument(
        "target",
        help="Target URL (e.g. https://example.com)",
    )

    scan_parser.add_argument(
        "-t",
        "--template",
        required=True,
        help="Path to template YAML (e.g. pywvs/templates/xss-reflected.yaml)",
    )

    scan_parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output file (report.json or report.html)",
    )

    scan_parser.add_argument(
        "-c",
        "--concurrency",
        type=int,
        default=5,
        help="Concurrency level (default: 5)",
    )

    scan_parser.add_argument(
        "--polite",
        action="store_true",
        help="Enable polite scanning mode (adds delay between requests)",
    )

    scan_parser.add_argument(
        "--user-agent",
        help="Custom User-Agent header",
    )

    scan_parser.add_argument(
        "--proxy",
        help="Proxy URL (e.g. http://127.0.0.1:8080)",
    )

    args = parser.parse_args()

    if args.command == "scan":
        template_path = Path(args.template)
        output_path = Path(args.output)

        if not template_path.exists():
            raise SystemExit(f"[!] Template not found: {template_path}")

        # load template
        template = load_template(template_path.name)

        # create auth / request session
        auth_session = AuthSession(
            polite=args.polite,
            user_agent=args.user_agent,
            proxy=args.proxy,
        )

        # run scan
        runner = TemplateScanRunner(
            concurrency=args.concurrency,
            auth_session=auth_session,
        )

        findings = runner.run(
            template=template,
            target=args.target,
        )

        # choose reporter
        if output_path.suffix == ".json":
            reporter = JSONReporter()
        elif output_path.suffix in (".html", ".htm"):
            reporter = HTMLReporter()
        else:
            raise SystemExit("[!] Output format must be .json or .html")

        reporter.write(findings, output_path)
        print(f"[+] Scan completed. Report saved to {output_path}")


if __name__ == "__main__":
    main()

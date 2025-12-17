from importlib import resources
import yaml
from .models import Template, TemplateRequest, Matcher


def load_template(name: str) -> Template:
    """
    Load a YAML template bundled inside pywvs.templates
    Example: load_template("xss-reflected.yaml")
    """
    with resources.files("pywvs.templates").joinpath(name).open(
        "r", encoding="utf-8"
    ) as f:
        raw = yaml.safe_load(f)

    # ---- requests ----
    requests = [
        TemplateRequest(
            method=r["method"],
            path=r["path"],
            payloads=r.get("payloads", {}),
        )
        for r in raw.get("requests", [])
    ]

    # ---- matchers ----
    matchers = []
    for m in raw.get("matchers", []):
        matcher = Matcher(
            type=m["type"],
            part=m.get("part", "body"),
            words=m.get("words"),
            regex=m.get("regex"),
            status=m.get("status"),
        )

        if not any([matcher.words, matcher.regex, matcher.status]):
            raise ValueError(
                f"Invalid matcher in template {name}: {m}"
            )

        matchers.append(matcher)

    return Template(
        id=raw["id"],
        name=raw["name"],
        severity=raw["severity"],
        requests=requests,
        matchers=matchers,
    )

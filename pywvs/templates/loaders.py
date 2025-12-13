from importlib import resources
import yaml
from .models import Template, TemplateRequest, Matcher


def load_template(name: str) -> Template:
    with resources.files("pywvs.templates").joinpath(name).open(
        "r", encoding="utf-8"
    ) as f:
        raw = yaml.safe_load(f)

    requests = [
        TemplateRequest(
            method=r["method"],
            path=r["path"],
            payloads=r.get("payloads", {})
        )
        for r in raw["requests"]
    ]

    matchers = [
        Matcher(
            type=m["type"],
            part=m.get("part", "body"),
            words=m.get("words"),
            regex=m.get("regex"),
            status=m.get("status"),
        )
        for m in raw["matchers"]
    ]

    return Template(
        id=raw["id"],
        name=raw["name"],
        severity=raw["severity"],
        requests=requests,
        matchers=matchers
    )

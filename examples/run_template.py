# examples/run_template.py
from pywvs.templates.engine import TemplateEngine
from pywvs.templates.loaders import load_template

engine = TemplateEngine()
tpl = load_template("xss-reflected.yaml")
findings = engine.run(tpl, "https://example.com")

for f in findings:
    print(f"[{f.severity.upper()}] {f.name} @ {f.target}")
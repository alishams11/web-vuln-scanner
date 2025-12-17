from pywvs.templates.loaders import load_template
from pywvs.templates.runner import TemplateScanRunner

runner = TemplateScanRunner()
template = load_template("xss-reflected.yaml")

findings = runner.run(
    template=template,
    target="https://example.com"
)

for f in findings:
    print(f)

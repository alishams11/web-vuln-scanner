from typing import List, Dict
from pywvs.modules.base import Finding


def is_ignored(finding: Finding, ignore_rules: List[Dict]) -> bool:
   
    for rule in ignore_rules:
        rule_type = rule.get("type")
        value = rule.get("value")

        if rule_type == "rule" and finding.id == value:
            return True

        if rule_type == "confidence" and finding.confidence == value:
            return True

        if rule_type == "url" and value in finding.target:
            return True

    return False

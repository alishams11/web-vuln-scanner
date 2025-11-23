from pywvs.modules.sqli import SQLiPassiveModule


def test_detects_mysql_error():
    module = SQLiPassiveModule()

    core_results = [
        {
            "url": "https://test.com/item?id=1",
            "body": "Warning: mysql_fetch_array() expects parameter 1 to be resource"
        }
    ]

    findings = module.scan("https://test.com", core_results)

    assert len(findings) == 1
    assert "mysql" in findings[0].evidence["error"]


def test_no_error_no_finding():
    module = SQLiPassiveModule()

    core_results = [
        {
            "url": "https://safe.com/",
            "body": "<html><title>OK</title></html>"
        }
    ]

    findings = module.scan("https://safe.com", core_results)
    assert len(findings) == 0

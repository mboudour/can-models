from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    study2_source = (ROOT / "app" / "abadi_study2_replication.py").read_text(encoding="utf-8")
    ess_source = (ROOT / "app" / "ess_cronos3_sogreen_case.py").read_text(encoding="utf-8")
    assert "d.r.abadi" not in study2_source
    assert "Dear Dr Abadi" not in study2_source
    assert "respondent-level" in ess_source
    assert "Results pending" in ess_source

    app = AppTest.from_file(str(ROOT / "app" / "app.py"))
    app.run(timeout=90)
    assert not app.exception, app.exception
    assert app.radio[0].value == "Abadi et al. Study 2 replication"
    assert any("Abadi et al.: public Study 2 replication" in element.value for element in app.header)
    assert any(metric.label == "Analysed Study 2 cases" and metric.value == "2,030" for metric in app.metric)
    assert any("Complete Abadi et al. replication ledger" in element.value for element in app.subheader)
    assert any("Study 1: 15-country access gate" in element.value for element in app.subheader)
    assert any("cross-sectional" in element.value for element in app.warning)
    assert len(app.download_button) >= 8

    app.radio[0].set_value("ESS CRONOS-3 / SoGreen Wave 6").run(timeout=90)
    assert any("ESS CRONOS-3 / SoGreen: Green Transition Attitude Network" in element.value for element in app.header)
    assert any(metric.label == "Approved CAN nodes" and metric.value == "21" for metric in app.metric)
    assert any(metric.label == "Public analysis state" and metric.value == "Results pending" for metric in app.metric)
    assert any("Results pending a publication gate" in element.value for element in app.warning)
    assert any(button.label == "Download Green Transition CAN configuration" for button in app.download_button)

    app.radio[0].set_value("Bring your own data").run(timeout=90)
    return_button = next(button for button in app.button if button.label == "← Return to Study 2 replication")
    return_button.click().run(timeout=90)
    assert app.radio[0].value == "Abadi et al. Study 2 replication"
    assert any("Abadi et al.: public Study 2 replication" in element.value for element in app.header)
    print("Streamlit Study 2, ESS publication-gate, and return-navigation smoke test passed.")


if __name__ == "__main__":
    main()

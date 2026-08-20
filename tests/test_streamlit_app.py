from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    study2_source = (ROOT / "app" / "abadi_study2_replication.py").read_text(encoding="utf-8")
    ess_source = (ROOT / "app" / "ess_cronos3_sogreen_case.py").read_text(encoding="utf-8")
    assert "d.r.abadi" not in study2_source
    assert "Dear Dr Abadi" not in study2_source
    assert "respondent-level" in ess_source
    assert "completed ESS counterpart" in ess_source
    ess_assets = ROOT / "app" / "assets" / "ess_cronos3_green_transition_w6"
    for asset_name in ["pooled_network.png", "top_node_strength.png", "country_density.png", "publication_gate_summary.csv", "country_nct_summary.json"]:
        assert (ess_assets / asset_name).is_file(), asset_name

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
    assert any(metric.label == "Green Transition nodes" and metric.value == "21" for metric in app.metric)
    assert any(metric.label == "Analysed ESS cases" and metric.value == "7,841" for metric in app.metric)
    assert any("Interpretive boundary" in element.value for element in app.warning)
    assert any("ESS scope" in element.label for element in app.tabs)
    assert any("RQ1 joint network" in element.label for element in app.tabs)
    assert any("Complete analysis ledger" in element.label for element in app.tabs)
    assert any(button.label == "Download Green Transition configuration" for button in app.download_button)

    app.radio[0].set_value("Pew ATP Wave 152 AI pathway").run(timeout=90)
    assert any("Pew American Trends Panel Wave 152: AI Attitude Network" in element.value for element in app.header)
    assert any(metric.label == "Pre-specified nodes" and metric.value == "15" for metric in app.metric)
    assert any("Results are intentionally not displayed" in element.value for element in app.warning)
    assert any("Pew scope" in element.label for element in app.tabs)
    assert any("Proposed RQ1 network" in element.label for element in app.tabs)
    assert any(button.label == "Download Wave 152 AI mapping manifest" for button in app.download_button)

    app.radio[0].set_value("Bring your own data").run(timeout=90)
    return_button = next(button for button in app.button if button.label == "← Return to Study 2 replication")
    return_button.click().run(timeout=90)
    assert app.radio[0].value == "Abadi et al. Study 2 replication"
    assert any("Abadi et al.: public Study 2 replication" in element.value for element in app.header)
    print("Streamlit Study 2, completed ESS case, Pew AI pathway, and return-navigation smoke test passed.")


if __name__ == "__main__":
    main()

from io import BytesIO
from pathlib import Path
import shutil

import pandas as pd
import yaml
from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "user_runs"


def main() -> None:
    source = ROOT / "data" / "raw" / "abadi_study2_2020" / "abadi_2023_four_country_study2.csv"
    sample = pd.read_csv(source, nrows=150)
    payload = sample.to_csv(index=False).encode("utf-8")

    before = set(RUNS.glob("run_*"))
    app = AppTest.from_file(str(ROOT / "app" / "app.py"))
    app.run(timeout=90)
    app.radio[0].set_value("Bring your own data").run(timeout=90)
    study_design = next(control for control in app.selectbox if control.label == "Study design")
    assert study_design.value == "Not specified"
    assert not any("Cross-sectional guardrail" in element.value for element in app.warning)
    app.file_uploader[0].upload("abadi_study2_subset.csv", payload, "text/csv").run(timeout=90)

    assert not app.exception, app.exception
    assert any(element.value == "Data preview" for element in app.subheader)
    assert len(app.multiselect) >= 2
    assert any("Coverage and placeholders" in element.value for element in app.header)

    create_button = next(button for button in app.button if button.label == "Create configuration and run bundle")
    create_button.click().run(timeout=90)
    assert not app.exception, app.exception
    after = set(RUNS.glob("run_*"))
    created = list(after - before)
    assert len(created) == 1, "Expected one user run bundle"
    run_dir = created[0]
    assert (run_dir / "config.yml").exists()
    assert (run_dir / "variable_profile.csv").exists()
    assert (run_dir / "manifest.json").exists()
    generated_config = yaml.safe_load((run_dir / "config.yml").read_text(encoding="utf-8"))
    assert generated_config["project"]["study_design"] == "Not specified"
    assert "will not assign a causal interpretation" in generated_config["project"]["interpretive_notice"]
    print("Streamlit upload, mapping, eligibility, and run-bundle test passed.")
    shutil.rmtree(run_dir)


if __name__ == "__main__":
    main()

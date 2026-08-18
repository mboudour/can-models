from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    app = AppTest.from_file(str(ROOT / "app" / "app.py"))
    app.run(timeout=90)
    assert not app.exception, app.exception
    assert app.radio[0].value == "ChatGPT case study"
    assert any("ChatGPT perceptions: worked CAN case study" in element.value for element in app.header)
    assert any(metric.label == "Complete CAN cases" and metric.value == "11,964" for metric in app.metric)
    assert len(app.download_button) >= 6
    print("Streamlit ChatGPT case-study smoke test passed.")


if __name__ == "__main__":
    main()

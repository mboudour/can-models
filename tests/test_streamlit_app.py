from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    app = AppTest.from_file(str(ROOT / "app" / "app.py"))
    app.run(timeout=60)
    assert not app.exception, app.exception
    assert len(app.file_uploader) == 1
    assert "CAN Models" in app.title[0].value
    assert "Upload a CSV or Excel file" in app.info[0].value
    print("Streamlit landing-page smoke test passed.")


if __name__ == "__main__":
    main()

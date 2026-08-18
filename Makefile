CONFIG ?= config/abadi_study2_public.yml
R ?= Rscript

.PHONY: setup validate example report streamlit test-app clean

setup:
	$(R) scripts/setup_environment.R

validate:
	$(R) scripts/validate_config.R --config $(CONFIG)

example:
	$(R) scripts/run_example.R --config $(CONFIG)

report:
	$(R) scripts/render_report.R --config $(CONFIG)

streamlit:
	streamlit run app/app.py

test-app:
	python3 tests/test_streamlit_app.py

clean:
	find new_computations -mindepth 1 ! -name '.gitkeep' -delete
	find figures -mindepth 1 ! -name '.gitkeep' -delete

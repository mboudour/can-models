# Official external datasets

This directory is reserved for datasets that must remain **local**. Its contents are ignored by Git, except for this instruction file. Do not add respondent-level files to GitHub, commit them, or expose them through the public Streamlit application.

## ESS CRONOS-3 Wave 6 / SoGreen

1. Download the official **CRONOS-3 Wave 6 main data set** and codebook from the [ESS Data Portal](https://ess.sikt.no/en/series/a46bcac5-b030-444b-9280-441ec97e1bce).
2. Extract the supplied ZIP into `data/external/ess_cronos3_sogreen/`.
3. The expected local files are:

```text
data/external/ess_cronos3_sogreen/CRON3w6e01.csv
data/external/ess_cronos3_sogreen/CRON3w6e01 codebook.html
```

4. Verify that the data file matches the source edition recorded by the worked case:

```bash
Rscript --vanilla scripts/verify_ess_cronos3_source.R
```

The baseline configuration expects the following SHA-256 fingerprint for `CRON3w6e01.csv`:

```text
0a3a647e1b530e33a0e542ce573e53aa4449fba49856af097bb1cdac15b3fe59
```

ESS recommends linking to its Data Portal rather than hosting ESS datasets on external websites. Its data are licensed under CC BY-NC-SA 4.0; preserve the current source citation and conditions of use. See the [ESS disclaimer](https://www.europeansocialsurvey.org/contact/disclaimer).

## Pew American Trends Panel Wave 152: AI and Human Enhancement

1. Create or sign in to a free account through the official [Pew Wave 152 dataset page](https://www.pewresearch.org/dataset/american-trends-panel-wave-152/). The download requires email verification and acceptance of the current [Pew Terms of Use](https://www.pewresearch.org/about/terms-and-conditions/).
2. Download the official respondent-level file and its accompanying documentation through that authorised account flow. Do not obtain a copied data file from an unofficial third party.
3. Create the following protected local directory and place the official file and documentation inside it:

```text
data/external/pew_atp_w152/
```

4. Before any analysis, record the filename and SHA-256 fingerprint and verify the exported column names and values against the public [final questionnaire](https://www.pewresearch.org/wp-content/uploads/sites/20/2025/03/pi_2025.04.03_us-public-and-ai-experts_questionnaire.pdf) and [topline](https://www.pewresearch.org/wp-content/uploads/sites/20/2025/03/pi_2025.04.03_us-public-and-ai-experts_topline.pdf).

The repository and Streamlit app intentionally do not bundle, display, or redistribute Pew respondent-level microdata. The questionnaire-derived 15-node mapping is recorded in `config/pew_atp_w152_ai_attitudes_manifest.yml`; it is a pre-analysis manifest, not an executed result configuration.

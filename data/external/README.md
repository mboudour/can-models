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

# ChatGPT example: CAN node dictionary

The public global ChatGPT survey is used as a fully configured example rather than as a claim that its content is substantively equivalent to the populism network studied by Abadi et al. The 30 nodes below are item-level, numerically coded survey responses selected to span behaviour, capability beliefs, governance, risk appraisal, satisfaction, evaluation, educational outcomes, labour-market beliefs, and affect.

| Node no. | Source variable | Output label | CAN domain |
|---:|---|---|---|
| 1 | Q15 | General ChatGPT use | Behaviour |
| 2 | Q19d | Provides information efficiently | Capability beliefs |
| 3 | Q19e | Provides reliable information | Capability beliefs |
| 4 | Q19g | Simplifies complex information | Capability beliefs |
| 5 | Q19h | Facilitates classroom learning | Capability beliefs |
| 6 | Q21a | International regulation is necessary | Governance evaluation |
| 7 | Q21c | University ethical guidelines are necessary | Governance evaluation |
| 8 | Q22b | May encourage cheating | Ethical and risk appraisal |
| 9 | Q22e | May mislead with inaccurate information | Ethical and risk appraisal |
| 10 | Q22f | May invade privacy | Ethical and risk appraisal |
| 11 | Q22j | May hinder learning by doing work | Ethical and risk appraisal |
| 12 | Q24e | Satisfied with level of assistance | Satisfaction |
| 13 | Q24f | Satisfied with information quality | Satisfaction |
| 14 | Q24g | Satisfied with information accuracy | Satisfaction |
| 15 | Q25a | Use is under my control | Attitude |
| 16 | Q25b | Use is interesting | Attitude |
| 17 | Q25c | Ability to use is important | Attitude |
| 18 | Q25d | Helps in everyday life | Attitude |
| 19 | Q26a | Enhances access to knowledge sources | Educational outcomes |
| 20 | Q26e | Increases study efficiency | Educational outcomes |
| 21 | Q26f | Increases motivation to study | Educational outcomes |
| 22 | Q27e | Enhances learning experience | Educational outcomes |
| 23 | Q27f | Improves skills | Educational outcomes |
| 24 | Q30a | Will reduce the number of jobs | Labour-market appraisal |
| 25 | Q30e | Will increase demand for AI skills | Labour-market appraisal |
| 26 | Q32b | Hopeful when using ChatGPT | Affect |
| 27 | Q32e | Calm when using ChatGPT | Affect |
| 28 | Q32j | Anxious when using ChatGPT | Affect |
| 29 | Q32l | Curious when using ChatGPT | Affect |
| 30 | Q32m | Excited when using ChatGPT | Affect |

## Analytic sample

The configured example filters to respondents who reported prior ChatGPT use (`Q13 = 1`). It contains **16,010** filtered records and **11,964** complete cases over the 30 configured nodes. Mardia’s diagnostic is calculated on a deterministic sample of 2,000 complete cases because the implementation has steep memory cost at the complete sample size; the core mixed graphical network continues to use all complete cases.

## Reuse note

A participant using the Streamlit interface does not need this question numbering or these domains. The app writes the same four-column mapping—source variable, node number, output label, and theoretical domain—for the participant’s own data. The logic is identical while the variable names are entirely user-defined.

## Source

Ravšelj et al. (2025). *Higher Education Students’ Early Perceptions of ChatGPT: Global Survey Data* (Version 2). Mendeley Data. [https://doi.org/10.17632/ymg9nsn6kn.2](https://doi.org/10.17632/ymg9nsn6kn.2)

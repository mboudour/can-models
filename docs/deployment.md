# Deployment guide

`can-models` supports two intentionally distinct publishing modes. Choose the mode based on whether users need to run the R-based CAN computations in the browser or only need an interface for uploading data, mapping variables, checking eligibility, and downloading a reproducible configuration.

| Mode | What users can do | Recommended host | Repository files |
|---|---|---|---|
| **A. Mapping-only Streamlit app** | Upload CSV/XLSX data, inspect columns and coding, map arbitrary variable names to CAN domains, obtain an eligibility matrix, and download a YAML run bundle | Streamlit Community Cloud | `app/app.py`, `requirements.txt` |
| **B. Full CAN analysis app** | Everything in Mode A plus R-side validation, MGM estimation, factor models, bootstrapping, NCT, country networks, clustering, and contextual analyses | A container-capable host | `Dockerfile`, `requirements.txt`, `renv.lock` |

## Mode A: Publish the mapping interface on Streamlit Community Cloud

This is the recommended immediate route for a shareable front end. Community Cloud supports Python requirements and Debian system dependencies, and it can deploy from either public or private GitHub repositories. It does **not** use this repository’s Dockerfile. The app therefore detects that `Rscript` is unavailable and automatically enters **mapping-only mode**: R-backed buttons are disabled, while configuration, data-profile, and eligibility features remain available.

1. Sign in at [share.streamlit.io](https://share.streamlit.io) with the GitHub account that owns `mboudour/can-models`.
2. In Community Cloud, open the `mboudour` workspace, or connect the GitHub account under **Settings → Linked accounts**. Because the repository is private, approve private-repository access and the associated GitHub authorization. Repository administrator permission is required for private deployment.
3. Select **Create app**. Choose repository `mboudour/can-models`, branch `master`, and entrypoint `app/app.py`.
4. Deploy with the repository-root `requirements.txt`. No secrets are required for the current mapping interface.
5. Test the deployed app with a non-sensitive small CSV. Confirm that it shows the data profile, the mapping interface, the CAN computation eligibility table, and the mapping-only notice after a run bundle is created.
6. Decide the sharing setting and communicate the privacy boundary to participants before collecting any data. Community Cloud hosts apps in the United States, and uploaded files are processed by the deployment. Do not invite users to upload identifiable or confidential data until an appropriate privacy and retention review has been completed.

Community Cloud will rebuild from `requirements.txt` when dependencies change and update from later Git pushes. It has shared resource limits and hibernates inactive apps, so it is appropriate for the lightweight mapping interface but not for exhaustive CAN runs on large datasets.

## Mode B: Deploy the full R-backed CAN app on a container host

Use this mode when participants must run the entire CAN workflow in a browser. The `Dockerfile` combines R, the locked `renv` package environment, and the Python Streamlit app. A host must allow Docker/container deployments and provide enough memory and CPU for the user’s selected analyses.

1. Create an account with a Docker-capable host such as Render, Railway, Fly.io, Google Cloud Run, AWS App Runner, or an institutional container platform.
2. Authorize the host to read the private `mboudour/can-models` GitHub repository.
3. Create a new service from the repository and choose **Dockerfile / container build**. The supplied Dockerfile is the build specification; no separate start command is required.
4. Set the service port to `8501` or configure the provider’s `PORT` mapping to the Streamlit command. The container exposes `8501` and has a health check at `/_stcore/health`.
5. Allocate resources based on the intended workload. The full primary ChatGPT example estimates a 30-node mixed graphical model over 11,964 complete cases; country comparisons and bootstrap diagnostics are materially more demanding. Begin with a private test deployment, Quick mode, a smaller test dataset, and a strict upload-size policy.
6. Configure privacy controls. The app stores each user run under `user_runs/` while it is active. For a production service, add scheduled deletion, authentication, HTTPS, usage limits, and—if data must persist—an encrypted storage policy before accepting participant uploads.
7. Use the provider’s logs and a simple test upload to confirm that `Rscript` is present. In full mode, the R-side **Validate configuration** and **Run core analysis** buttons become enabled automatically.

> **Computational guardrail.** Full bootstrapping and all pairwise country NCTs can take tens of minutes or longer. The app intentionally requires a confirmation before the full configured workflow begins, and it marks ineligible computations as placeholders instead of creating spurious results.

## Which mode to choose

Use **Mode A** if the immediate goal is a public or link-shared survey-data preparation tool. It solves the participant-facing variable-name issue: users map their own columns to the required CAN roles and retain a reproducible configuration.

Use **Mode B** if the goal is a complete online analysis service. It is the only deployment mode that can responsibly host the existing R implementation without trying to force its heavy mixed-language runtime into Community Cloud’s lightweight shared environment.

## References

[1] Streamlit. *App dependencies for your Community Cloud app*. [https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)

[2] Streamlit. *Quickstart: Streamlit Community Cloud*. [https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/quickstart](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/quickstart)

[3] Streamlit. *Status and limitations of Community Cloud*. [https://docs.streamlit.io/deploy/streamlit-community-cloud/status](https://docs.streamlit.io/deploy/streamlit-community-cloud/status)

[4] Streamlit. *Manage your app: app resources and limits*. [https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app)

[5] Streamlit. *Deploy Streamlit using Docker*. [https://docs.streamlit.io/deploy/tutorials/docker](https://docs.streamlit.io/deploy/tutorials/docker)

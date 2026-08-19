# Full local-analysis image: Python/Streamlit interface plus the R CAN engine.
# r2u provides binary CRAN packages for Ubuntu, avoiding a large fragile source restore.
FROM rocker/r2u:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    R_COMPILE_AND_INSTALL_PACKAGES=never

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    build-essential \
    gfortran \
    curl \
    git \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libgit2-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libglpk-dev \
    r-cran-readxl \
    r-cran-yaml \
    r-cran-digest \
    r-cran-jsonlite \
    r-cran-dplyr \
    r-cran-tidyr \
    r-cran-purrr \
    r-cran-tibble \
    r-cran-stringr \
    r-cran-readr \
    r-cran-ggplot2 \
    r-cran-qgraph \
    r-cran-bootnet \
    r-cran-networktools \
    r-cran-lavaan \
    r-cran-psych \
    r-cran-semtools \
    r-cran-gparotation \
    r-cran-igraph \
    r-cran-factoextra \
    r-cran-cluster \
    r-cran-rmarkdown \
    r-cran-knitr \
    r-cran-testthat \
    r-cran-withr \
    r-cran-scales \
    r-cran-renv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN python3 -m pip install --break-system-packages -r requirements.txt

COPY . .

# Do not restore renv.lock here: its package binaries are platform-specific.
# The bootstrap detects r2u-provided packages and installs only any CAN-specific
# CRAN dependencies not supplied as binaries, then records the environment.
RUN Rscript --vanilla scripts/setup_environment.R

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app/app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]

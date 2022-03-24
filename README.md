# Pubmed articles geocoder

Reading articles from CSV and querying bing API for affiliation geocoding.

## First usage

```
make virtualenv
source .venv/bin/activate
make install
```

## Example usage

```
source .venv/bin/activate
python -m pubmed_pelias_client --bing_key=bingapikey-xxxx data/last_20.csv
```

:warning: Following comes from python template used... Need to cleanup

## TODO

- save results to csv file
- cache geocoded results to a sqlite db for example
- Better nowhere filtering
- iterate through affiliations
- add verbose logs (every 1000 lines for example)

## Python Project Template

A low dependency and really simple to start project template for Python Projects.

See also

- [Flask-Project-Template](https://github.com/rochacbruno/flask-project-template/) for a full feature Flask project including database, API, admin interface, etc.
- [FastAPI-Project-Template](https://github.com/rochacbruno/fastapi-project-template/) The base to start an openapi project featuring: SQLModel, Typer, FastAPI, JWT Token Auth, Interactive Shell, Management Commands.

### HOW TO USE THIS TEMPLATE

> **DO NOT FORK** this is meant to be used from **[Use this template](https://github.com/rochacbruno/python-project-template/generate)** feature.

1. Click on **[Use this template](https://github.com/rochacbruno/python-project-template/generate)**
2. Give a name to your project  
   (e.g. `my_awesome_project` recommendation is to use all lowercase and underscores separation for repo names.)
3. Wait until the first run of CI finishes  
   (Github Actions will process the template and commit to your new repo)
4. If you want [codecov](https://about.codecov.io/sign-up/) Reports and Automatic Release to [PyPI](https://pypi.org)  
   On the new repository `settings->secrets` add your `PIPY_API_TOKEN` and `CODECOV_TOKEN` (get the tokens on respective websites)
5. Read the file [CONTRIBUTING.md](CONTRIBUTING.md)
6. Then clone your new project and happy coding!

> **NOTE**: **WAIT** until first CI run on github actions before cloning your new project.

### What is included on this template?

- 🖼️ Templates for starting multiple application types:
  - **Basic low dependency** Python program (default) [use this template](https://github.com/rochacbruno/python-project-template/generate)
  - **Flask** with database, admin interface, restapi and authentication [use this template](https://github.com/rochacbruno/flask-project-template/generate).
    **or Run `make init` after cloning to generate a new project based on a template.**
- 📦 A basic [setup.py](setup.py) file to provide installation, packaging and distribution for your project.  
  Template uses setuptools because it's the de-facto standard for Python packages, you can run `make switch-to-poetry` later if you want.
- 🤖 A [Makefile](Makefile) with the most useful commands to install, test, lint, format and release your project.
- 📃 Documentation structure using [mkdocs](http://www.mkdocs.org)
- 💬 Auto generation of change log using **gitchangelog** to keep a HISTORY.md file automatically based on your commit history on every release.
- 🐋 A simple [Containerfile](Containerfile) to build a container image for your project.  
  `Containerfile` is a more open standard for building container images than Dockerfile, you can use buildah or docker with this file.
- 🧪 Testing structure using [pytest](https://docs.pytest.org/en/latest/)
- ✅ Code linting using [flake8](https://flake8.pycqa.org/en/latest/)
- 📊 Code coverage reports using [codecov](https://about.codecov.io/sign-up/)
- 🛳️ Automatic release to [PyPI](https://pypi.org) using [twine](https://twine.readthedocs.io/en/latest/) and github actions.
- 🎯 Entry points to execute your program using `python -m <pubmed_pelias_client>` or `$ pubmed_pelias_client` with basic CLI argument parsing.
- 🔄 Continuous integration using [Github Actions](.github/workflows/) with jobs to lint, test and release your project on Linux, Mac and Windows environments.

> Curious about architectural decisions on this template? read [ABOUT_THIS_TEMPLATE.md](ABOUT_THIS_TEMPLATE.md)  
> If you want to contribute to this template please open an [issue](https://github.com/rochacbruno/python-project-template/issues) or fork and send a PULL REQUEST.

[❤️ Sponsor this project](https://github.com/sponsors/rochacbruno/)

<!--  DELETE THE LINES ABOVE THIS AND WRITE YOUR PROJECT README BELOW -->

---

# pubmed_pelias_client

[![codecov](https://codecov.io/gh/wayglem/pubmed-pelias-client/branch/main/graph/badge.svg?token=pubmed-pelias-client_token_here)](https://codecov.io/gh/wayglem/pubmed-pelias-client)
[![CI](https://github.com/wayglem/pubmed-pelias-client/actions/workflows/main.yml/badge.svg)](https://github.com/wayglem/pubmed-pelias-client/actions/workflows/main.yml)

Awesome pubmed_pelias_client created by wayglem

## Install it from PyPI

```bash
pip install pubmed_pelias_client
```

## Usage

```py
from pubmed_pelias_client import BaseClass
from pubmed_pelias_client import base_function

BaseClass().base_method()
base_function()
```

```bash
$ python -m pubmed_pelias_client
#or
$ pubmed_pelias_client
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

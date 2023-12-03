# Claritywave challenge
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/enfasis/cw_django_dev/ec2.yml?label=Workflow)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/bd9cd7f2b3404a1b84a7bf17c1ab9d4d)](https://app.codacy.com/gh/enfasis/cw_django_dev/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/bd9cd7f2b3404a1b84a7bf17c1ab9d4d)](https://app.codacy.com/gh/enfasis/cw_django_dev/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)


Author: CW-TEAM

# Setting up 

## Local Development

### Poetry
Setting up `.venv` enviroment with poetry for python 3.11
```sh
poetry config virtualenvs.in-project true
pyenv local 3.11.0
poetry shell 
poetry install 
```

This project uses `ruff` as a formatter and linter
``` sh
ruff check . --fix
ruff format .
```

### Testing
They are found in the `./tests/` path.
``` sh
pytest
```

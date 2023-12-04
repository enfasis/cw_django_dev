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

## Production 
Kubernetes configurations files are defined in `./deploy/`.

### About the current deployment
This project is deployed in an EC2 Instance running kubernetes cluster using [minikube](https://minikube.sigs.k8s.io/docs/) with a Postgres Database.
There are some security group rules to access the kubernetes cluster server and the app deployed. Given that this is a toy deployment there are some security and best practices concerns like `minikube` is not for production, but for now, it gets the job done. 

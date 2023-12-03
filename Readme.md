# Claritywave challenge

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

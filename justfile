init venv:
    poetry config virtualenvs.in-project true
    poetry install --no-root --with formatters,linters,tests 
    source .venv/bin/activate
    
install hooks:
    pre-commit install --hook-type pre-commit --hook-type pre-push

run checks:
    pre-commit run --all-files --hook-stage pre-commit
    pre-commit run --all-files --hook-stage pre-push

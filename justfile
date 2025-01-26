install:
    poetry install --no-root --with formatters,linters,tests
    pre-commit install --hook-type pre-commit --hook-type pre-push

send:
    pre-commit run --all-files --hook-stage pre-commit
    pre-commit run --all-files --hook-stage pre-push

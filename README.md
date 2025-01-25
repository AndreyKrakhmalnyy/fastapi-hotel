## Установка pre-commit для форматеров and pre-push для линтеров hooks:
    - pre-commit install --hook-type pre-commit --hook-type pre-push

## Запуск форматтеров и линтеров перед пушем:
    - pre-commit run --all-files --hook-stage pre-commit
    - pre-commit run --all-files --hook-stage pre-push

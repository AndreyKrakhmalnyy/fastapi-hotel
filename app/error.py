"""Модуль для обработки ошибок"""


class BaseSolutionException(Exception):
    """Базовый тип ошибок"""


class ServiceException(BaseSolutionException):
    "Тип ошибок при работе с сервисами"

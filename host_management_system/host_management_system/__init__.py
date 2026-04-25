from pymysql import install_as_MySQLdb

from .celery import celery_app


install_as_MySQLdb()

__all__ = ('celery_app',)

from sqlalchemy.orm import DeclarativeBase
#DeclarativeBase — это базовый класс SQLAlchemy для ORM-моделей.
#
# Он:
# 	•	хранит метаданные (metadata)
# 	•	регистрирует таблицы
# 	•	связывает Python-классы с таблицами БД

class Base(DeclarativeBase):
    pass

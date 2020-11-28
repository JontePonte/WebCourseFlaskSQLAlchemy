
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()


# Use:
# alembic revision --autogenerate -m 'Added last update'
# and
# alembic upgrade head
# to update database

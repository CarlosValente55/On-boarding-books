import pymysql

from secrets import MYSQL_CREDENTIALS
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
    MYSQL_CREDENTIALS['DB_USER'], MYSQL_CREDENTIALS['DB_PASSWORD'], MYSQL_CREDENTIALS['DB_HOST'], MYSQL_CREDENTIALS['DB_PORT'], MYSQL_CREDENTIALS['DB_NAME']))
session = sessionmaker(bind=engine)()


class Db():

    def store(self, country):
        session.add(country)

    def close_and_save(self):
        try:
            session.commit()
            return None
        except IntegrityError:
            session.rollback()
            return 'IntegrityError'

        except DataError:
            session.rollback()
            return 'DataError'


class Country(Db, Base):
    __tablename__ = "country_books"
    record_reference = Column(String(20), primary_key=True)
    country = Column(String(3), primary_key=True)

    def __init__(self, record_reference="", country=""):
        self.record_reference = record_reference
        self.country = country

    def create_sales_rights_table(self):
        if not engine.dialect.has_table(engine, "country_books"):
            metadata = MetaData(engine)
            Table("country_books", metadata,
                  Column('record_reference', String(14), primary_key=True),
                  Column('country', String(3), primary_key=True)
                  )
            metadata.create_all()

    def delete_sales_rights_table(self, table_name):
        if engine.dialect.has_table(engine, table_name):
            Country.__table__.drop(engine)

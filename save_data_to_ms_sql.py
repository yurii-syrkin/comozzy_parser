
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session
from sqlalchemy.orm.session import sessionmaker
import datetime

driver = 'SQL Server Native Client 11.0'
server = 'SERVER4'
database = 'camozzy_prices'
user = 'sa'
password = 'Aradmin!'

engine = create_engine(f'mssql://{user}:{password}@{server}/{database}?driver={driver}')
#mssql://sa:Syrkin_YV1983@Tyson/camozzy_parser?driver=SQL Server Native Client 11.0


base = declarative_base()

class Nomenclature(base):
    __tablename__ = 'Nomenclature'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    article = Column(String)
    weight = Column(Float)
    prices = relationship('Prices')

    def __repr__(self):
        return f'<Nomenclature {self.id} {self.article} {self.name}>'

class Prices(base):
    __tablename__ = 'Prices'
    id = Column(Integer, primary_key=True)
    period = Column(DateTime)
    nomenclature_id = Column(Integer, ForeignKey('Nomenclature.id'))
    price = Column(Float)

    def __repr__(self):
        return f'<Price {self.period} {self.price}>'


class Program_execution_status(base):
    __tablename__ = 'Program_execution_status'
    id = Column(Integer, primary_key=True)
    start_of_the_program = Column(DateTime)
    end_of_program_execution = Column(DateTime)
    time_of_the_last_transaction = Column(DateTime)
    program_execution_status = Column(VARCHAR(50))


def get_session():
    return scoped_session(sessionmaker(bind=engine))

def save_data(session, article, name, weight, price, date):

    q = session.query(Nomenclature).filter_by(article=article)
    finded_nomenclature = q.first()
    if finded_nomenclature == None:
        nomenclature = Nomenclature(article=article, name=name, weight=weight)
        session.add(nomenclature)
        session.commit()
        nomenclature_id = nomenclature.id
    else:
        nomenclature_id = finded_nomenclature.id

    price_data = Prices(period=date, nomenclature_id=nomenclature_id, price=price)

    session.add(price_data)
    session.commit()

base.metadata.create_all(engine)

##### testing

# session = get_session()
# save_data(session, '15651', 'ad;flkaf', 15.5, datetime.datetime.now())






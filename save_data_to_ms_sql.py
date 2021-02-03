
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session
from sqlalchemy.orm.session import sessionmaker
from datetime import datetime
from settings import USER_OF_DB, PASSWORD_OF_DB, SERVER, DATABASE, DRIVER

engine = create_engine(f'mssql://{USER_OF_DB}:{PASSWORD_OF_DB}@{SERVER}/{DATABASE}?driver={DRIVER}')
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

class Data_loading_errors(base):
    __tablename__ = 'Data_loading_errors'
    id = Column(Integer, primary_key=True)
    nomenclature_id = Column(Integer, ForeignKey('Nomenclature.id'))
    period = Column(DateTime)
    comment = Column(String)

class Program_execution_status(base):
    __tablename__ = 'Program_execution_status'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    program_execution_status = Column(VARCHAR(50))
    comments = Column(VARCHAR(150))

def get_session():
    return scoped_session(sessionmaker(bind=engine))

def get_price(nomenclature_id, date, session = None, all_data = False):
    if session == None:
        session = get_session()

    price_info = session.query(Prices).filter_by(nomenclature_id=nomenclature_id)
    price_dict = {}
    for str_price_info in price_info:
        period = str_price_info.period
        if period > date:
            continue
        if not 'period' in price_dict.keys() or period > price_dict['period']:
            price_dict['period'] = period
            price_dict['price'] = str_price_info.price
        else:
            continue

    if len(price_dict) == 0:
        if all_data == True:
            return None
        else:
            return 0
    elif all_data == True:
        return price_dict['price'], price_dict['period']
    else:
        return price_dict['price']

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
        if type(weight) == int and weight > 0:
            finded_nomenclature.weight = weight
            session.add(finded_nomenclature)
            session.commit()

    finded_price = get_price(nomenclature_id, datetime.now(), session=session, all_data=False)

    if finded_price == price:
        return

    price_data = Prices(period=date, nomenclature_id=nomenclature_id, price=price)

    session.add(price_data)
    session.commit()

def enter_data_about_the_download_error(session, article, name, comment):
    q = session.query(Nomenclature).filter_by(article=article)
    finded_nomenclature = q.first()
    if finded_nomenclature == None:
        nomenclature = Nomenclature(article=article, name=name)
        session.add(nomenclature)
        session.commit()
        nomenclature_id = nomenclature.id
    else:
        nomenclature_id = finded_nomenclature.id

    data_loading_errors = Data_loading_errors(nomenclature_id=nomenclature_id, period=datetime.now(), comment=comment)
    session.add(data_loading_errors)
    session.commit()

base.metadata.create_all(engine)





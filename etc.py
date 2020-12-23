from save_data_to_ms_sql import get_session, Prices


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
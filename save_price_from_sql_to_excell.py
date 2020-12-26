from save_data_to_ms_sql import get_price
from save_data_to_ms_sql import get_session, Nomenclature
import xlwt
from datetime import datetime

session = get_session()


new_workbook = xlwt.Workbook()
sheet_new_workbook = new_workbook.add_sheet('TDSheet')

q = session.query(Nomenclature)

finded_nomenclature = q.all()

row_number = 0
sheet_new_workbook.write(row_number, 0, 'Наименование')
sheet_new_workbook.write(row_number, 1, 'Артикул')
sheet_new_workbook.write(row_number, 2, 'Цена')
sheet_new_workbook.write(row_number, 3, 'Масса')


for nomenclature in finded_nomenclature:
    row_number += 1
    nomenclature_id = nomenclature.id
    nomenclature_article = nomenclature.article
    nomenclature_name = nomenclature.name
    weight = nomenclature.weight
    price = get_price(nomenclature_id=nomenclature_id, date=datetime.now(), session=session)
    sheet_new_workbook.write(row_number, 0, str(nomenclature_name))
    sheet_new_workbook.write(row_number, 1, str(nomenclature_article))
    sheet_new_workbook.write(row_number, 2, str(price))
    sheet_new_workbook.write(row_number, 3, str(weight))
    new_workbook.save('Цены Камоци из SQL.xls')




print("Сохранение данных в Excell успешно завершено")




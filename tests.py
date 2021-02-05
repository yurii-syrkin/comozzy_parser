'''Запрос для получения нулевых цен
USE [camozzy_prices]
GO

SELECT nomenclature.id,
		nomenclature.name,
		nomenclature.article,
		isnull(last_prices.price, 0) as price,
		last_prices.period
  FROM [dbo].[Nomenclature] as nomenclature
  LEFT JOIN (
  SELECT
	Prices.nomenclature_id,
	Prices.price,
	Prices.period
	from [dbo].[Prices]
	inner join (SELECT
      MAX([period]) as period
      ,[nomenclature_id]
  FROM [dbo].[Prices] as Prices
  GROUP BY [nomenclature_id]) as last_selection
  on last_selection.nomenclature_id = Prices.nomenclature_id and
  last_selection.period = Prices.period
  ) as last_prices on
  nomenclature.id = last_prices.nomenclature_id
  order by price
GO


'''

from main import Syte
from main import Nomenclature

def test_1():
    syte = Syte(False)
    nomenclature = Nomenclature(syte=syte, name='6708 6', article='6708 6')
    nomenclature.identify_indicators()
    print(f'Номенклатура: {str(nomenclature)}, цена {nomenclature.price}, масса {nomenclature.weight}')

test_1()
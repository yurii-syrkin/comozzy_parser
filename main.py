from time import sleep
import xlwt
from selenium import webdriver
from settings import SYTE_COMOZZY, LOGIN, PASSWORD
from selenium.webdriver.common.by import By
import re
import xlrd
import random

class Syte():
    def __init__(self):
        chromedriver = 'E:\Distrib\Browsers\chromedriver_win32\chromedriver.exe'
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')  # для открытия headless-браузера
        browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
        browser.maximize_window()

        browser.get(SYTE_COMOZZY)
        browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/span/a').click()

        login = browser.find_element_by_xpath('//*[@id="loginpopup"]/form/input[1]')
        login.send_keys(LOGIN)
        password = browser.find_element_by_xpath('//*[@id="loginpopup"]/form/input[2]')
        password.send_keys(PASSWORD)
        into_botton = browser.find_element_by_xpath('//*[@id="loginpopup"]/form/input[5]')
        into_botton.click()

        self.syte = browser

    def clear_order_list(self):
        for i in range(20):
            button_order_call_back = self.syte.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/a')#/html/body/div[2]/div[2]/div[1]
            button_order_call_back.click()

            cmarket_cart_item_delete_icon_remove = self.syte.find_elements(By.CLASS_NAME, 'cmarket_cart_item_delete.icon-remove')
            if len(cmarket_cart_item_delete_icon_remove) == 0:
                continue
            while True:
                cmarket_cart_item_delete_icon_remove_item = cmarket_cart_item_delete_icon_remove[0]
                for j in range(20):
                    try:
                        cmarket_cart_item_delete_icon_remove_item.click()
                    except BaseException:
                        continue
                    cmpopup = self.syte.find_elements_by_id('cmpopup')
                    if len(cmpopup) == 0:
                        continue
                    for k in range(20):
                        submit = cmpopup[0].find_elements(By.CLASS_NAME, 'ok')
                        if len(submit) == 0:
                            continue
                        submit[0].click()
                        break
                    break
                cmarket_cart_item_delete_icon_remove = self.syte.find_elements(By.CLASS_NAME, 'cmarket_cart_item_delete.icon-remove')
                if len(cmarket_cart_item_delete_icon_remove) <= 1:
                    break
            break

    def quit(self):
        self.syte.quit()

class Nomenclature():
    def __init__(self, **qwarg):
        self.syte = None
        self.name = ''
        self.article = ''
        self.price = None
        self.weight = None
        self.status = None
        self.comment = ''
        for parametr, value in qwarg.items():
            self.__dict__[parametr] = value

    def __str__(self):
        return f'{self.article} ({self.name})'

    def identify_indicators(self, key_for_search = None):
        if key_for_search == None:
            self.identify_indicators(self.article)
            if self.status != 'Ok':
                sleep(random.randrange(2,6))
                self.identify_indicators(self.name)
            return

        input_search = self.syte.syte.find_element_by_name('search')
        input_search.clear()
        input_search.send_keys(key_for_search)
        button_search = self.syte.syte.find_element_by_id('headsearchsubmit')
        button_search.click()
        table_strings = self.syte.syte.find_elements(By.CLASS_NAME, 'stock_available')
        table_strings = table_strings + self.syte.syte.find_elements(By.CLASS_NAME, 'stock_expect')
        if len(table_strings) == 0:
            i = 1
            for i in range(10):
                button_search = self.syte.syte.find_element_by_id('headsearchsubmit')
                button_search.click()
                table_strings = self.syte.syte.find_elements(By.CLASS_NAME, 'stock_available')
                table_strings = table_strings + self.syte.syte.find_elements(By.CLASS_NAME, 'stock_expect')
                if len(table_strings) > 0:
                    break
                sleep(10)

        for table_str in table_strings:
            children_elements = table_str.find_elements(By.TAG_NAME, 'div')
            regex = fr'^{key_for_search}$'
            if re.match(regex, children_elements[2].text) is None:
                continue
            price = children_elements[9].text
            price = price.replace(',', '.')
            if price.replace('.', '').isdigit():
                self.price = float(price)
            for i in range(10):
                botton_order_1 = children_elements[10].find_element(By.TAG_NAME, 'a')
                botton_order_1.click()
                form_order = self.syte.syte.find_elements(By.CLASS_NAME, 'popupbody')
                if len(form_order) == 0:
                    sleep(5)
                    continue
                for j in range(20):
                    botton_order_2 = self.syte.syte.find_elements(By.CLASS_NAME, 'imgsubmit')
                    if len(botton_order_2) == 0:
                        sleep(8)
                        continue
                    try:
                        botton_order_2[0].click()
                    except BaseException as exc:
                        continue
                    for g in range(20):
                        cmarket_cart_table = self.syte.syte.find_elements(By.CLASS_NAME, 'cmarket_cart_item.row.stock_available')
                        cmarket_cart_table = cmarket_cart_table + self.syte.syte.find_elements(By.CLASS_NAME, 'cmarket_cart_item.row.stock_expect.stock_order')
                        cmarket_cart_table = cmarket_cart_table + self.syte.syte.find_elements(By.CLASS_NAME, 'cmarket_cart_item.row.stock_expect')
                        if len(cmarket_cart_table) == 0:
                            continue
                        for cmarket_cart_table_str in cmarket_cart_table:
                            cmarket_cart_item_code = cmarket_cart_table_str.find_elements(By.CLASS_NAME,
                                'cmarket_cart_nn_container.cmarket_cart_jnote')
                            if len(cmarket_cart_item_code) == 0:
                                continue
                            nom_name = cmarket_cart_item_code[0].text
                            if re.match(regex, nom_name) is None:
                                continue
                            cmarket_cart_mass = cmarket_cart_table_str.find_elements(By.CLASS_NAME,
                                'cmarket_cart_sum_container.cmarket_cart_jnote.cmarket_cart_mulqty.cmarket_cart_mass')
                            if len(cmarket_cart_mass) == 0:
                                continue
                            weight = cmarket_cart_mass[0].text
                            weight = weight.replace(',', '.')
                            if weight.replace('.', '').isdigit():
                                weight = float(weight)
                                self.weight = weight
                                self.comment = f'Всё гуд. i = {i}, j = {j}'
                            else:
                                self.comment = f'Не удалось преобразовать значение массы {weight}'
                            break
                        break
                    break
                break

            if not self.price is None:
                self.status = 'Ok'

            self.syte.clear_order_list()
            break

def perform_crawler():
    syte = Syte()
    # nomenclature = Nomenclature(syte=syte.syte, name='V3MH-316-PP-025')
    workbook = xlrd.open_workbook('Цены Камоци Пневмоприводы.xls')
    sheet = workbook.sheet_by_index(0)
    new_workbook = xlwt.Workbook()
    sheet_new_workbook = new_workbook.add_sheet('TDSheet')

    sheet = workbook.sheet_by_index(0)

    for rownum in range(sheet.nrows):
        values = sheet.row_values(rownum)
        sheet_new_workbook.write(rownum, 0, values[0])
        sheet_new_workbook.write(rownum, 1, values[1])
        sheet_new_workbook.write(rownum, 2, values[2])
        sheet_new_workbook.write(rownum, 3, values[3])
        sheet_new_workbook.write(rownum, 4, values[4])
        sheet_new_workbook.write(rownum, 5, values[5])
        if rownum == 0:
            sheet_new_workbook.write(rownum, 6, values[6])
            sheet_new_workbook.write(rownum, 7, 'Масса')
            #sheet_new_workbook.write(rownum, 8, 'Комментарий')
        else:
            sleep(random.randrange(1, 10))
            name = values[3]
            article = values[4]
            nomenclature = Nomenclature(syte=syte, name=name, article=article)
            nomenclature.identify_indicators()
            if nomenclature.status == 'Ok':
                sheet_new_workbook.write(rownum, 6, nomenclature.price)
                if not nomenclature.weight is None:
                    sheet_new_workbook.write(rownum, 7, nomenclature.weight)
            #sheet_new_workbook.write(rownum, 8, nomenclature.comment)
        new_workbook.save('Цены Камоци Пневмоприводы (скаченные с сайта).xls')
        # if rownum > 20:
        #     break

    syte.quit()

def test():
    syte = Syte()
    nomenclature = Nomenclature(syte=syte, name='S6500 12-1/4', article='S6500 12-1/4')
    nomenclature.identify_indicators()
    print(f'Номенклатура: {str(nomenclature)}, цена {nomenclature.price}, масса {nomenclature.weight}')

if __name__ == '__main__':
    perform_crawler()
    #test()






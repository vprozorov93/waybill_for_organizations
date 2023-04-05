import time
from datetime import datetime as dt
import openpyxl as xl
import re
import os


def get_date_period(start_date, end_date):
    s, e = list(map(lambda x: int(dt.strptime(x, '%d.%m.%Y').timestamp()), [start_date, end_date]))
    return list(map(lambda x: dt.fromtimestamp(x).strftime('%d.%m.%Y'), range(s, e + 86400, 86400)))

def create_waybill(method:str='', params:dict=''):
    sample_wb = xl.load_workbook(filename='waybill_sample.xlsx')
    sample_ws1 = sample_wb['1']
    sample_ws2 = sample_wb['2']
    index_date = 1

    sample_fill_text = ['<date_start>', '<date_end>', '<serial_month_year>',
                        '<date_number>',
                        '<company_name, company_address, company_number, company_ogrn>',
                        '<delivery_type>', '<auto_name>', '<auto_number>',
                        '<driver_f_name>',
                        '<driver_license_card_serial_number>', '<car_class>',
                        '<driver_s_name>', '<company_name_and_department>',
                        '<dispetcher_s_name>', '<start_address>',
                        '<fuel_type>', '<fuel_code>', '<fuel_max_rate>']
    period = get_date_period(params['dates'][0], params['dates'][1])
    for date in period:
        ws1 = sample_wb.copy_worksheet(sample_ws1)
        ws2 = sample_wb.copy_worksheet(sample_ws2)
        ws1.title = f'{date}'
        ws2.title = f'{date}_2'
        index_date += 2

        for row in ws1.rows:
            for cell in row:
                for string in sample_fill_text:
                    if re.match(rf'{string}', str(cell.value)):
                        match string:
                            case '<date_start>':
                                cell.value = date
                            case '<date_end>':
                                if params['end_date'][0] == 1:
                                    cell.value = dt.fromtimestamp(
                                        int(dt.strptime(date,
                                                        '%d.%m.%Y').timestamp()) + 86400).strftime(
                                        '%d.%m.%Y')
                                elif params['end_date'][0] == 2:
                                    cell.value = date
                                else:
                                    cell.value = params['end_date'][1]
                            case '<serial_month_year>':
                                if params['driver'] == '':
                                    serial = 'РТ'
                                else:
                                    serial = params['driver'][-1]
                                monthyear = date.split('.')
                                cell.value = f'{serial}-{monthyear[1]}.{monthyear[2]}'
                            case '<date_number>':
                                cell.value = f"{date.split('.')[0]}"
                            case '<company_name, company_address, company_number, company_ogrn>':
                                cell.value = f"{params['company_settings']['company_name']}, {params['company_settings']['company_address']},\n" \
                                             f"{params['company_settings']['company_number']}, ОГРН {params['company_settings']['company_ogrn']}"
                            case '<delivery_type>':
                                cell.value = params['company_settings'][
                                    'delivery_type']
                            case '<auto_name>':
                                cell.value = params['car'][0]
                            case '<auto_number>':
                                cell.value = params['car'][1]
                            case '<driver_f_name>':
                                cell.value = '' if params['driver'] == '' else \
                                params['driver'][0]
                            case '<driver_license_card_serial_number>':
                                cell.value = '' if params[
                                                       'driver'] == '' else f'="{params["driver"][2]}"'
                            case '<car_class>':
                                cell.value = '' if params['driver'] == '' else \
                                params['driver'][3]
                            case '<driver_s_name>':
                                cell.value = '' if params['driver'] == '' else \
                                params['driver'][1]
                            case '<company_name_and_department>':
                                cell.value = f"{params['company_settings']['company_name']}, {params['company_settings']['delivery_department_title']}"
                            case '<dispetcher_s_name>':
                                cell.value = params['company_settings'][
                                    'dispatcher']
                            case '<start_address>':
                                cell.value = params['company_settings'][
                                    'start_address']
                            case '<fuel_type>':
                                cell.value = params['car'][2]
                            case '<fuel_code>':
                                cell.value = params['car'][4]
                            case '<fuel_max_rate>':
                                cell.value = params['car'][3]

        ws1.sheet_view.tabSelected = True
        ws2.sheet_view.tabSelected = True

    sample_wb.remove(sample_wb['1'])
    sample_wb.remove(sample_wb['2'])
    if method == 'save':
        sample_wb.save(os.path.join(os.getcwd(), 'waybills',
                                f"{'' if params['driver'] == '' else params['driver'][1]}_{params['car'][0]}_{period[0]}-{period[-1]}.xlsx".replace(' ', '_')))
    else:
        pass
    sample_wb.close()

def get_waybills(method, params:dict):
    create_waybill('print' if method == 'Напечатать' else 'save', params)


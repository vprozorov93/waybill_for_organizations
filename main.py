import os
import win32api
import win32print

def print_file():
    # os.startfile('waybills\waybill_Lada Largus_01.01.2023.xlsx', 'print')
    print(win32print.GetDefaultPrinter())
    # input('...')
    win32api.ShellExecute(0, 'printto', 'waybills\waybill_Lada Largus_01.01.2023.xlsx', '"%s"' % win32print.GetDefaultPrinter(), '.', 0)

print_file()
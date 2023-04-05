import sqlite3
import os
from typing import List, Any


class DBHandler:
    def __init__(self):
        self.path_dir = os.path.join(os.getcwd(), 'database')
        self.path_file = os.path.join(self.path_dir, 'waybill.db')

        try:
            os.mkdir(self.path_dir)
        except FileExistsError:
            pass

        self.sqlite_connection = sqlite3.connect(self.path_file)

        self.__create_drivers_table()
        self.__create_cars_table()

    def __create_drivers_table(self):
        cursor = self.sqlite_connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS drivers(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                fio_full TEXT NOT NULL,
                fio_short TEXT NOT NULL,
                license_num INTEGER NOT NULL,
                license_category TEXT NOT NULL,
                waybill_index TEXT NOT NULL);""")

        self.sqlite_connection.commit()
        cursor.close()

    def __create_cars_table(self):
        cursor = self.sqlite_connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS cars(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                gov_number TEXT NOT NULL,
                fuel_type TEXT NOT NULL,
                fuel_max_rate INTEGER NOT NULL,
                fuel_code TEXT NOT NULL);""")

        self.sqlite_connection.commit()
        cursor.close()

    def get_data(self, table: str, fullness: str = 'full') -> list[Any]:
        cursor = self.sqlite_connection.cursor()
        query_sample = f"""SELECT * FROM {table};"""

        match table:
            case 'cars':
                if fullness == 'short':
                    query_sample = query_sample.replace('*', 'id, gov_number')
            case 'drivers':
                if fullness == 'short':
                    query_sample = query_sample.replace('*', 'id, fio_short')

        data = cursor.execute(query_sample).fetchall()
        self.sqlite_connection.commit()
        cursor.close()

        return data

    def post_data(self, table: str, data: dict) -> None:
        cursor = self.sqlite_connection.cursor()
        sql = f"INSERT INTO {table} VALUES({('?,' * 6).strip(',')});"

        match table:
            case 'cars':
                data = (None, data['model'], data['gov_number'], data['fuel_type'],
                        data['fuel_max_rate'], data['fuel_code'])
            case 'drivers':
                data = (None, data['fio_full'], data['fio_short'],
                        data['license_num'], data['license_category'],
                        data['waybill_index'])

        cursor.execute(sql, data)
        self.sqlite_connection.commit()
        cursor.close()

    def delete_data(self, table, data_id) -> None:
        cursor = self.sqlite_connection.cursor()
        sql = f'DELETE FROM {table} WHERE id={data_id}'
        cursor.execute(sql)
        self.sqlite_connection.commit()
        cursor.close()

    def update_data(self, table, data) -> None:
        cursor = self.sqlite_connection.cursor()
        sql = f'UPDATE {table} SET * WHERE id = ?'

        match table:
            case 'cars':
                sql = sql.replace('*', 'model=?, gov_number=?, fuel_type=?, '
                                       'fuel_max_rate=?, fuel_code=?')
                data = (data['model'], data['gov_number'], data['fuel_type'],
                        data['fuel_max_rate'], data['fuel_code'], data['id'])
            case 'drivers':
                sql = sql.replace('*', 'fio_full=?, fio_short=?, '
                                       'license_num=?, license_category=?, '
                                       'waybill_index=?')
                data = (data['fio_full'], data['fio_short'],
                        data['license_num'], data['license_category'],
                        data['waybill_index'], data['id'])

        cursor.execute(sql, data)
        self.sqlite_connection.commit()
        cursor.close()

    def exit(self):
        self.sqlite_connection.close()


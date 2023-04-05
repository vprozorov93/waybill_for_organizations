# Формирование путевых листов для организаций

## О программе
Программа была создана в качестве пет-проекта, для изучения библиотки PyQt и QtDesigner, также программа решает задачу автоматизации создания нескольких путевых листов по Форме № 3 в соответствии с приказом Минтранса России	от 21.12.2018  №  467, которые требуются организациям для осуществления перевозок с помощью своего транспорта.

### Раздел Данные машин и водителей 
Программа имеет БД SQLite3, в которой хранятся записи о транспорте и водителях компании, с помощью интерфеса доступно редактирование/добавление/удаление записей в БД.

### Раздел Настройки
Прочие настройки организации задаются через JSON файл, редактируются в нем же. При необходимости можно легко реализовать сохранение изменений в JSON файле, если потребуется редактировать параметры компании через приложение. Данная функция мной не реализована, по причине избыточности для организации в которой я работаю, а также избыточности в целом, так как настрйоки организации редактируются крайне редко.

### Раздел Главное
В окне можно выбрать имеющегося водителя и автомобиль на котором он будет передвигаться, задать период формирования Путевых листов а также настройки даты окончания каждого путевого листа. При нажатии на кнопку Сохранить, программа сформирует xlsx файл, который в дальнейшем можно преобразовать в PDF средстави Excel и распечатать. Пребобразование в PDF требуется если вам необходима двухстороняя печать, в Excel добиться двухсторонней печати с нескольких листов довольно проблематично.

## Упаковка программы в исполяемый файл
0. Установите Python версии не ниже 3.10.4
1. Скопируйте репозиторий локально на ваш ПК
2. Создайте venv, для этого:
  - В cmd или terminal перейдите в папку куда были скопированы файлы из репозитория и выполните команду `python -m venv venv`, все следующие команды также должны быть выполены в дирректории с файлами из репозитория.
  - Активируйте vevn следующей командой:
    * `venv\Scripts\activate.bat` - для Windows;
    * `source venv/bin/activate` - для Linux и MacOS.
  - Установите все библиотеки из requirements.txt
3. Процесс упаковки:
  - Выполните команду `pip install pyinstaller`
  - Выполните команду `pyinstaller waybill.py`
  - В папке появится файл waybill.spec, найдите в нем строчку `console=True`, и измените значение на `False`. Это не обязательный пунтк, но в этом случае при запуске программы не будет открываться cmd или terminal, работа будет комфортнее.
  - Если выполнили предыдущий пункт, то выполните команду `pyinstaller waybill.spec`
  - В дирректорию `.../dist/waybill/` скопируйте папку `database`, `waybills` и файл `waybill_sample.xlsx`
4. Для запуска приложений перейдите в `.../dist/waybill/` и запустите исполняемый файл waybill

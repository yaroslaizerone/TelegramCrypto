import os, csv, re, chardet, dateparser
from core.models import Person, Region


def validate_data(data):
    # чистим заголовки
    headers = data.iloc[0]
    headers = headers.apply(lambda x: x.strip() if isinstance(x, str) else x)
    headers = headers.apply(lambda x: " ".join(x.split()) if isinstance(x, str) else x)
    data.columns = headers
    # чистим ячейки
    data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    data = data.applymap(lambda x: " ".join(x.split()) if isinstance(x, str) else x)
    # удаляю пустые строки и столбцы
    data.dropna(how="all", axis=1, inplace=True)
    data.dropna(how="all", inplace=True)
    data.fillna('', inplace=True)  # удаляю NaN
    data = data.iloc[
           1:]  # удаляю первую строку, потому что она дублируется с заголовком, не знаю как исправить пока что
    return data


def parse_person_data(person_data, attribute_name, value):
    if attribute_name == 'birth_date':
        dt = dateparser.parse(str(value))
        date_str = dt.strftime('%Y-%m-%d')
        date = dateparser.parse(date_str).date()
        person_data['birth_date'] = date.isoformat()
    elif attribute_name == 'fio':
        try:
            names = value.split(' ')
        except AttributeError:
            person_data['first_name'] = value
        else:
            if len(names) == 0:
                person_data['first_name'] = ''
            elif len(names) == 1:
                person_data['first_name'] = names[0]
            elif len(names) == 2:
                person_data['last_name'] = names[0]
                person_data['first_name'] = names[1]
            elif len(names) == 3:
                person_data['last_name'] = names[0]
                person_data['first_name'] = names[1]
                person_data['middle_name'] = names[2]
            else:
                person_data['last_name'] = names[0]
                person_data['first_name'] = names[1]
                person_data['middle_name'] = ' '.join(names[2:])
    elif attribute_name == 'phone':
        if not re.match(r'^7\d{10}$', str(value)):
            value = process_phone_number(str(value))
        if value != '':
            region_name = get_region_from_def_code(value)
            if region_name is not None:
                region, created = Region.objects.get_or_create(name=region_name)
                region.utc = UTC_DATA.get(region_name, '')
                region.save()
                person_data['region'] = region
        person_data['phone'] = value
    elif hasattr(Person, attribute_name):
        person_data[attribute_name] = value

    return person_data


def process_phone_number(phone):
    # Удаление лишних символов кроме цифр
    phone = re.sub(r'\D', '', phone)

    # Если символов 10, добавить 7 в начале
    if len(phone) == 10:
        phone = '7' + phone

    # Если начинается с 8, заменить на 7
    if phone.startswith('8'):
        phone = '7' + phone[1:]

    # Проверка длины номера телефона
    if len(phone) != 11:
        phone = ''

    return phone


def load_csv(filename):
    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    with open(filename, newline='', encoding=encoding) as csvfile:
        return list(csv.DictReader(csvfile, delimiter=';'))

def load_def_data():
    def_csv = load_csv(os.path.join(os.path.dirname(__file__), 'utils/DEF-9xx.csv'))
    def_data = {}
    for row in def_csv:
        def_code = int(row['АВС/ DEF'])
        if def_code not in def_data:
            def_data[def_code] = []
        def_data[def_code].append((int(row['От']), int(row['До']), row['Регион']))
    for code in def_data:
        def_data[code].sort()

    utc_csv = load_csv(os.path.join(os.path.dirname(__file__), 'utils/utc.csv'))
    utc_data = {}
    for row in utc_csv:
        region_name = row['region_name']
        utc = row['utc']
        utc_data[region_name] = utc

    return def_data, utc_data


DEF_DATA, UTC_DATA = load_def_data()


def get_region_from_def_code(phone_number):
    def_code = int(str(phone_number)[1:4])
    number = int(str(phone_number)[4:11])
    if def_code not in DEF_DATA:
        return None
    data = DEF_DATA[def_code]
    left, right = 0, len(data) - 1
    while left <= right:
        mid = (left + right) // 2
        if number < data[mid][0]:
            right = mid - 1
        elif number > data[mid][1]:
            left = mid + 1
        else:
            return data[mid][2]
    return None

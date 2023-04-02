class ColumnConfig:
    MAPPING = {
        'id': ('id', 'ID'),
        'last_name': ('last_name', 'Фамилия'),
        'first_name': ('first_name', 'Имя'),
        'middle_name': ('middle_name', 'Отчество'),
        'email': ('email', 'Электронная почта'),
        'phone': ('phone', 'Номер телефона'),
        'birth_date': ('birth_date', 'Дата рождения'),
        'address': ('address', 'Адрес'),
        'city': ('city', 'Город'),
        'region__name': ('region__name', 'Регион'),
        'region__utc': ('region__utc', 'UTC'),
    }

    @classmethod
    def get_column_name(cls, key):
        return cls.MAPPING.get(key)[0]

    @classmethod
    def get_header_name(cls, key):
        return cls.MAPPING.get(key)[1]

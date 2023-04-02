class PersonTableStatus:
    STATUS_NEW = 0
    STATUS_MATCHING = 1
    STATUS_PROCESSED = 2
    STATUS_COMPLETED = 3

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новый'),
        (STATUS_MATCHING, 'Сопоставлено'),
        (STATUS_PROCESSED, 'Обрабатывается'),
        (STATUS_COMPLETED, 'Выполнено'),
    ]

GENDER_CHOICES = (
    ('M', 'Мужской'),
    ('F', 'Женский'),
    ('U', 'Неопределен')
)

# Количество строк в Preview

PREVIEW_ROWS_LIMIT = 13
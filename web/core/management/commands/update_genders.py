from django.core.management.base import BaseCommand
from core.models import Person

def determine_gender(first_name, middle_name):
    if not first_name or not middle_name:
        return "U"
    # Окончания для имён и отчеств
    female_name_endings = ["а", "я", "ева", "ёва", "ина", "лина", "мина", "сина", "тина", "ша", "ла", "ица", "на", "ия", "айа", "уся", "тая", "рь", "ра", "зя"]
    male_name_endings = ["й", "ы", "н", "р", "л", "ь", "в", "г", "т", "у", "э", "о", "и", "е", "з", "д", "с", "ъ", "щ", "ц", "ш", "х", "ю", "ч", "б", "п", "м", "ф", "к", "ев", "ёв", "ин", "ченко", "лов", "хин", "чук", "чуков", "лин", "мин", "кин", "дзе", "айло", "дий", "ван", "ман", "мей", "пов", "рак", "рын", "тов", "чан", "чун", "чин", "чен", "шен", "шин", "ян", "рон", "кан", "кун", "кой", "ким"]
    female_patronymic_endings = ["вна", "чна", "шна", "щна", "хна", "гна", "кна", "нна", "мна", "рна", "пна", "фна", "тна", "сна", "льна", "ьевна", "евич", "евна", "ична", "ичична", "ылыевич", "евских", "кович", "акович", "тович", "икович", "ович", "никович", "ков", "инич", "ич", "ынович", "ыньич", "ьич"]
    male_patronymic_endings = ["вич", "чич", "шич", "щич", "хич", "гич", "кич", "нич", "мич", "рич", "пич", "фич", "тич", "сич", "льич"]

    # Проверка окончаний имени и отчества
    if any(first_name[-1] == ending for ending in female_name_endings) and any(middle_name[-3:] == ending for ending in female_patronymic_endings):
        return "F"
    elif any(first_name[-1] == ending for ending in male_name_endings) and any(middle_name[-3:] == ending for ending in male_patronymic_endings):
        return "M"
    else:
        return "U"


class Command(BaseCommand):
    help = 'Обновить поле пола для всех записей в таблице Person'

    def handle(self, *args, **options):
        persons = Person.objects.all()
        counter = 0
        male_count = 0
        female_count = 0
        undefined_count = 0

        for person in persons:
            gender = determine_gender(person.first_name, person.middle_name)
            person.gender = gender
            person.save()
            counter += 1
            print(f"{counter}. Обновлен пол для {person.first_name} {person.middle_name}: {gender}")

            if gender == 'M':
                male_count += 1
            elif gender == 'F':
                female_count += 1
            else:
                undefined_count += 1

        self.stdout.write(self.style.SUCCESS(f'Пол успешно обновлен для {counter} записей в таблице'))
        self.stdout.write(f'Мужчин: {male_count}, женщин: {female_count}, неопределено: {undefined_count}')

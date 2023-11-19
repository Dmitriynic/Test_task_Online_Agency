import requests
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from markmodel.models import CarMark, CarModel

class Command(BaseCommand):
    help = 'Parse XML from URL and update database'

    def handle(self, *args, **options):
        xml_file_url = "https://auto-export.s3.yandex.net/auto/price-list/catalog/cars.xml"

        # Путь для сохранения загруженного файла
        local_file_path = "../,,/../cars.xml"

        # Загрузка файла по ссылке
        response = requests.get(xml_file_url)
        with open(local_file_path, "wb") as f:
            f.write(response.content)

        # Удаляем предыдущие данные
        CarModel.objects.all().delete()
        CarMark.objects.all().delete()

        # Разбор локального XML-файла
        tree = ET.parse(local_file_path)
        root = tree.getroot()

        # Проход по элементам XML и создание объектов моделей
        for mark_elem in root.findall(".//mark"):
            mark_name = mark_elem.get("name")
            car_mark = CarMark.objects.create(name=mark_name)

            for model_elem in mark_elem.findall(".//model"):
                model_name = model_elem.text
                car_model = CarModel.objects.create(name=model_name, mark=car_mark)

        self.stdout.write(self.style.SUCCESS('Successfully parsed XML from URL and updated the database'))
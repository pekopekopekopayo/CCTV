import csv
from django.db import transaction
from app.settings import BASE_DIR
from django.core.management.base import BaseCommand
from models.cctv.models import Cctv


class Command(BaseCommand):
    def handle(self, *args, **options):
        csv_path = str(BASE_DIR) + "\\static\\csv\\cctv_info.csv"

        try:
            with transaction.atomic():
                Cctv.objects.all().delete()
                with open(csv_path, "r", encoding="utf-8") as file:
                    cctv_info = list(csv.reader(file))
                    for i in range(1, len(cctv_info)):
                        Cctv.objects.create(id=cctv_info[i][0], road_name=cctv_info[i][1])
                print("seed데이터 생성성공")
        except:
            print("seed데이터 생성실패")

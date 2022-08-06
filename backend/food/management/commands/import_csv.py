import csv
import os
from typing import Dict

from django.core.management.base import BaseCommand, CommandError
from food.models import Ingredient

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
    )
)

CSV_DIR = os.path.join(BASE_DIR, "data")
CSV_FILES = ("ingredients",)

FIELD_NAMES = {
    "ingredients": (
        "name",
        "measurement_unit",
    )
}


class Command(BaseCommand):
    help = "Import static csv data to DB"

    @staticmethod
    def clear_tables():
        Ingredient.objects.all().delete()

    @staticmethod
    def create_row(data: Dict, name: str):
        if name == "ingredients":
            Ingredient.objects.create(**data)

    def handle(self, *args, **options):
        self.clear_tables()

        for csv_filename in CSV_FILES:
            path_to_csv_file = f"{CSV_DIR}/{csv_filename}.csv"

            try:
                csv_file = open(path_to_csv_file, newline="")
            except OSError:
                raise CommandError('Failed to open "%s"' % path_to_csv_file)

            rows = csv.DictReader(csv_file, FIELD_NAMES[csv_filename])

            try:
                for row in list(rows):
                    self.create_row(row, csv_filename)
            except csv.Error as e:
                raise CommandError(
                    "file {}, line {}: {}".format(
                        path_to_csv_file, rows.line_num, e
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully imported "%s"' % csv_file.name
                )
            )

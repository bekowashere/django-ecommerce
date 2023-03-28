from django.core.management import BaseCommand, CommandError
from world.models import Currency
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/world/currency.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for crr in data:
            currency_code = crr['currency_code']
            currency_name = crr['currency_name']
            currency_symbol = crr['currency_symbol']

            try:
                currency = Currency(
                    currency_code=currency_code,
                    currency_name=currency_name,
                    currency_symbol=currency_symbol,

                )

                currency.save()

                self.stdout.write(self.style.SUCCESS(f'{currency_code} ({currency_symbol}) create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')
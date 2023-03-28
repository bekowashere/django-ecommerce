from django.core.management import BaseCommand, CommandError
from world.models import Country, Currency, Timezone
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '_data/world/countries.json'

        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)

        for country in data:
            name = country['name']
            iso3 = country['iso3']
            iso2 = country['iso2']
            numeric_code = country['numeric_code']
            phone_code = country['phone_code']
            capital = country['capital']
            region = country['region']
            subregion = country['subregion']
            latitude = country['latitude']
            longitude = country['longitude']

            # Timezone
            timezones = country['timezones']

            # Currency
            currency_code = country['currency']
            currency_name = country['currency_name']
            currency_symbol = country['currency_symbol']

            try:
                currency = Currency.objects.get(currency_code=currency_code)
            except Currency.DoesNotExist:
                currency = Currency(currency_code=currency_code, currency_name=currency_name, currency_symbol=currency_symbol)
                currency.save()

            try:
                country = Country(
                    name=name,
                    iso3=iso3,
                    iso2=iso2,
                    numeric_code=numeric_code,
                    phone_code=phone_code,
                    capital=capital,
                    currency=currency,
                    region=region,
                    subregion=subregion,
                    latitude=latitude,
                    longitude=longitude
                )

                country.save()

                # Timezones
                if len(timezones) > 0:
                    for timez in timezones:
                        zoneName = timez['zoneName']
                        gmtOffset = timez['gmtOffset']
                        gmtOffsetName = timez['gmtOffsetName']
                        abbreviation = timez['abbreviation']
                        tzName = timez['tzName']
                        
                        try:
                            timezone = Timezone.objects.get(abbreviation=abbreviation)
                        except:
                            timezone = Timezone(
                                zoneName=zoneName,
                                gmtOffset=gmtOffset,
                                gmtOffsetName=gmtOffsetName,
                                abbreviation=abbreviation,
                                tzName=tzName
                            )
                            timezone.save()
                        country.timezones.add(timezone)

                country.save()

                self.stdout.write(self.style.SUCCESS(f'{name} create successfully'))
            except Exception as e:
                raise CommandError(f'{e}')
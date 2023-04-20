from django.core.management import call_command
from django.core.management import BaseCommand, CommandError

# address gibi modellerde hata alıyoruz
def load_account_data():
    call_command("loaddata", "_fixtures/account/db_account_user_fixture.json")
    call_command("loaddata", "_fixtures/account/db_account_customeruser_fixture.json")
    call_command("loaddata", "_fixtures/account/db_account_address_fixture.json")
    call_command("loaddata", "_fixtures/account/db_account_selleruser_fixture.json")
    call_command("loaddata", "_fixtures/account/db_account_selleruserimage_fixture.json")


class Command(BaseCommand):
    def add_arguments(self, parser):

        parser.add_argument('-d', '--data', action='store_true', help="Run the projects with data")
        # runproject --data
        
    def handle(self, *args, **kwargs):
        data = kwargs['data']

        if data:
            call_command("makemigrations")
            call_command("migrate")
            call_command("add_currency")
            call_command("add_countries")

            # store
            call_command("add_ProductAttribute")
            call_command("add_ProductAttributeValue")
            call_command("add_ProductType")
            call_command("add_ProductTypeAttribute")

            # account
            # load_account_data()

            # all fixture.json
            # call_command("loaddata", "db_admin_fixture.json")
            self.stdout.write(self.style.SUCCESS(f'Project runs with data.'))
        else:
            call_command("makemigrations")
            call_command("migrate")
            call_command("add_currency")
            call_command("add_countries")
            self.stdout.write(self.style.SUCCESS(f'Project runs witout data.'))
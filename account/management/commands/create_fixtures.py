from django.core.management import call_command
from django.core.management import BaseCommand, CommandError
from io import StringIO
from pathlib import Path

def create_fixture(app_name, model_name=None):
    buf = StringIO()

    if model_name:
        model = f'{app_name}.{model_name}'
        filename = f'db_{app_name}_{model_name.lower()}_fixture.json'
        call_command('dumpdata', model, indent=4, format='json', stdout=buf)
        buf.seek(0)
        with open(Path.cwd().joinpath('_fixtures', app_name, filename), 'w') as f:
            f.write(buf.read())
    else:
        filename = f'db_{app_name}_fixture.json'
        call_command('dumpdata', app_name, indent=4, format='json', stdout=buf)
        buf.seek(0)
        with open(Path.cwd().joinpath('_fixtures', app_name, filename), 'w') as f:
            f.write(buf.read())

def create_account_fixture():
    create_fixture('account')
    create_fixture('account', 'User')
    create_fixture('account', 'CustomerUser')
    create_fixture('account', 'Address')
    create_fixture('account', 'SellerUser')
    create_fixture('account', 'SellerUserImage')

def create_app_fixture(app_name):
    if app_name == 'account':
        create_account_fixture()
    elif app_name == 'world':
        print('world create_app_fixture')
        pass
    else:
        raise CommandError('Invalid app name')


class Command(BaseCommand):
    def add_arguments(self, parser):

        parser.add_argument('-app', '--appname', type=str, help="Write a app name to create model fixtures")
        parser.add_argument('-a', '--all', action='store_true', help="Run the projects with data")
        
    def handle(self, *args, **kwargs):
        app_name = kwargs['appname']
        all_apps = kwargs['all']

        if app_name and all_apps:
            raise CommandError('Do not use commands together: --all and --appname. Choose one.')
        elif not app_name and not all_apps:
            raise CommandError('You must use at least one command: --all or --appname')
        else:
            if all_apps:
                create_account_fixture()
                self.stdout.write(self.style.SUCCESS(f'All data created successfully. (folder: _fixtures/)'))
            else:
                create_app_fixture(app_name)
                self.stdout.write(self.style.SUCCESS(f'{app_name} app data created successfully. (folder: _fixtures/{app_name}/)'))
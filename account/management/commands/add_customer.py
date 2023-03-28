from django.core.management import BaseCommand, CommandError
from account.models import User, CustomerUser

from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('email')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('password')

    def handle(self, *args, **options):
        email = options['email']
        first_name = options['first_name']
        last_name = options['last_name']
        password = options['password']

        # edit first_name & last_name for username
        _first_name = first_name.replace("ı", "i")
        _last_name = last_name.replace("ı", "i")

        ex = False
        new_username = slugify(f'c-{_first_name}{_last_name}')
        ex = User.objects.filter(username=new_username).exists()
        while ex:
            new_username = slugify(new_username + " " + get_random_string(9, "0123456789"))
            ex = User.objects.filter(username=new_username).exists()

        username = new_username

        messages = {'errors': []}

        if email == None:
            messages['errors'].append('Email can not be empty')
        if first_name == None:
            messages['errors'].append('First name can not be empty')
        if last_name == None:
            messages['errors'].append('Last name can not be empty')
        if password == None:
            messages['errors'].append('Password can not be empty')
        if User.objects.filter(email=email).exists():
            messages['errors'].append('Account already exists with this email')
        if User.objects.filter(username=username).exists():
            messages['errors'].append('Account already exists with this username')
        if len(messages['errors']) > 0:
            raise CommandError(f'Error: {messages["errors"]}')
        else:
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                is_customer=True,
            )

            customer = CustomerUser.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
            )

            customer.save()
            self.stdout.write(self.style.SUCCESS(f'Customer {email} added successfully '))
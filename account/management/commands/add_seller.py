from django.core.management import BaseCommand, CommandError
from account.models import User, SellerUser

from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('email')
        parser.add_argument('password')
        parser.add_argument('company_name')
        parser.add_argument('code')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        company_name = options['company_name']
        code = options['code']

        # USERNAME GENERATOR
        ex = False
        new_username = slugify(company_name)
        ex = User.objects.filter(username=new_username).exists()
        while ex:
            new_username = slugify(f"{new_username} {get_random_string(9, '0123456789')}")
            ex = User.objects.filter(username=new_username).exists()

        username = new_username
        seller_slug = new_username

        messages = {'errors': []}

        if email == None:
            messages['errors'].append('Email can not be empty')
        if password == None:
            messages['errors'].append('Password can not be empty')
        
        if company_name == None:
            messages['errors'].append('Company Name can not be empty')
        if SellerUser.objects.filter(company_name=company_name).exists():
            messages['errors'].append('Supplier already exists with this company name')
        
        if code == None:
            messages['errors'].append('Company code can not be empty')
        if SellerUser.objects.filter(code=code).exists():
            messages['errors'].append('Supplier already exists with this company code')

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
                is_supplier=True,
            )

            seller = SellerUser.objects.create(
                user=user,
                company_name=company_name,
                code=code,
                supplier_slug=seller_slug
            )

            seller.save()
            self.stdout.write(self.style.SUCCESS(f'Seller {company_name} added successfully '))
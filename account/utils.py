from django.utils.crypto import get_random_string

def generate_seller_code(company_name):
    company_code = company_name[0:4].strip().upper()
    return company_code

def generate_random_seller_code():
    company_code = get_random_string(4, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return company_code
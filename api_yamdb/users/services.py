import random


def generate_confirmation_code():
    code = random.randint(100000, 999999)
    return code

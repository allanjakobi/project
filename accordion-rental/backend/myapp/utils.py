import datetime

def calculate_reference_number(agreementId):
    year = datetime.datetime.now().year
    base_number = f"{year}{agreementId}"
    
    weights = [7, 3, 1]
    total = 0
    for i, digit in enumerate(reversed(base_number)):
        total += int(digit) * weights[i % len(weights)]
    
    control_digit = (10 - (total % 10)) % 10
    reference_number = f"{base_number}{control_digit}"
    
    return int(reference_number)

import hashlib

"""
Planning to add more here eventually, for now will be used for handling keys.
"""

# Set this to something unique.
pin = 'Mwanzo@#230101'


# Generate unique token from pin.  This adds a marginal amount of security.
def get_token():
    token = hashlib.sha224(pin.encode('utf-8'))
    return token.hexdigest()

# ByPass Function .
def get_price_token():
    price_token = hashlib.sha224(pin.encode('utf-8'))
    return token.hexdigest()
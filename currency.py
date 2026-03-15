"""
Currency Conversion Module for Modern Online Store
Primary Currency: South African Rand (ZAR)
"""

# Exchange rates relative to ZAR (1 ZAR = X foreign currency)
# These are example rates - in production, fetch from an API
EXCHANGE_RATES = {
    'ZAR': 1.0,       # South African Rand (Base)
    'USD': 0.053,     # US Dollar
    'EUR': 0.049,     # Euro
    'GBP': 0.042,     # British Pound
    'NGN': 82.5,      # Nigerian Naira
    'KES': 8.5,       # Kenyan Shilling
    'BWP': 0.72,      # Botswana Pula
    'NAD': 1.0,       # Namibian Dollar (pegged to ZAR)
    'SZL': 1.0,       # Swazi Lilangeni (pegged to ZAR)
    'LSL': 1.0,       # Lesotho Loti (pegged to ZAR)
}

CURRENCY_SYMBOLS = {
    'ZAR': 'R',
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'NGN': '₦',
    'KES': 'KSh',
    'BWP': 'P',
    'NAD': 'N$',
    'SZL': 'E',
    'LSL': 'L',
}

CURRENCY_NAMES = {
    'ZAR': 'South African Rand',
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'GBP': 'British Pound',
    'NGN': 'Nigerian Naira',
    'KES': 'Kenyan Shilling',
    'BWP': 'Botswana Pula',
    'NAD': 'Namibian Dollar',
    'SZL': 'Swazi Lilangeni',
    'LSL': 'Lesotho Loti',
}

DEFAULT_CURRENCY = 'ZAR'


def get_exchange_rate(from_currency, to_currency):
    """Get exchange rate between two currencies"""
    if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
        return 1.0
    
    # Convert to ZAR first, then to target currency
    zar_rate = 1 / EXCHANGE_RATES[from_currency]
    target_rate = EXCHANGE_RATES[to_currency]
    
    return zar_rate * target_rate


def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another"""
    if from_currency == to_currency:
        return amount
    
    rate = get_exchange_rate(from_currency, to_currency)
    return round(amount * rate, 2)


def format_currency(amount, currency):
    """Format amount with currency symbol"""
    symbol = CURRENCY_SYMBOLS.get(currency, currency)
    
    # Different formatting for different currencies
    if currency in ['ZAR', 'USD', 'EUR', 'GBP']:
        return f'{symbol}{amount:,.2f}'
    elif currency in ['NGN', 'KES']:
        return f'{symbol}{amount:,.0f}'
    else:
        return f'{symbol}{amount:,.2f}'


def get_currency_options():
    """Get list of currency options for dropdown"""
    return [
        {'code': code, 'name': name, 'symbol': CURRENCY_SYMBOLS.get(code, code)}
        for code, name in CURRENCY_NAMES.items()
    ]


def update_exchange_rates(rates_dict):
    """Update exchange rates (call this when fetching from API)"""
    global EXCHANGE_RATES
    EXCHANGE_RATES.update(rates_dict)


# Example function to fetch live rates (implement with your preferred API)
def fetch_live_rates(api_key=None):
    """
    Fetch live exchange rates from an API
    Recommended APIs:
    - ExchangeRate-API (https://www.exchangerate-api.com)
    - Fixer.io (https://fixer.io)
    - Open Exchange Rates (https://openexchangerates.org)
    """
    import requests
    
    if not api_key:
        return EXCHANGE_RATES
    
    try:
        # Example using ExchangeRate-API with ZAR as base
        response = requests.get(
            f'https://v6.exchangerate-api.com/v6/{api_key}/latest/ZAR'
        )
        data = response.json()
        
        if data.get('result') == 'success':
            rates = data.get('conversion_rates', {})
            # Filter to only our supported currencies
            filtered_rates = {k: v for k, v in rates.items() if k in EXCHANGE_RATES}
            return filtered_rates
    except Exception as e:
        print(f'Error fetching exchange rates: {e}')
    
    return EXCHANGE_RATES

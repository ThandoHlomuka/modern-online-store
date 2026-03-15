"""
Shipping Module for Modern Online Store
Primary Integration: Bobgo API
"""

import os
import requests
from datetime import datetime

# Bobgo API Configuration
BOBGO_API_BASE_URL = os.environ.get('BOBGO_API_URL', 'https://api.bobgo.co.za/v1')
BOBGO_API_KEY = os.environ.get('BOBGO_API_KEY', '')

# Shipping zones (South Africa focused)
SHIPPING_ZONES = {
    'gauteng': {
        'name': 'Gauteng',
        'provinces': ['Gauteng', 'Johannesburg', 'Pretoria', 'Soweto'],
        'base_rate': 65.00,
        'per_kg_rate': 15.00,
        'estimated_days': '1-2'
    },
    'western_cape': {
        'name': 'Western Cape',
        'provinces': ['Western Cape', 'Cape Town', 'Stellenbosch'],
        'base_rate': 85.00,
        'per_kg_rate': 18.00,
        'estimated_days': '2-3'
    },
    'kwazulu_natal': {
        'name': 'KwaZulu-Natal',
        'provinces': ['KwaZulu-Natal', 'Durban', 'Pietermaritzburg'],
        'base_rate': 80.00,
        'per_kg_rate': 17.00,
        'estimated_days': '2-3'
    },
    'eastern_cape': {
        'name': 'Eastern Cape',
        'provinces': ['Eastern Cape', 'Port Elizabeth', 'East London'],
        'base_rate': 90.00,
        'per_kg_rate': 20.00,
        'estimated_days': '3-4'
    },
    'other_sa': {
        'name': 'Other South Africa',
        'provinces': ['Free State', 'North West', 'Northern Cape', 'Mpumalanga', 'Limpopo'],
        'base_rate': 95.00,
        'per_kg_rate': 22.00,
        'estimated_days': '3-5'
    },
    'southern_africa': {
        'name': 'Southern Africa (SADC)',
        'countries': ['Namibia', 'Botswana', 'Lesotho', 'Eswatini', 'Zimbabwe', 'Mozambique', 'Zambia'],
        'base_rate': 250.00,
        'per_kg_rate': 45.00,
        'estimated_days': '5-10'
    },
    'international': {
        'name': 'International',
        'base_rate': 450.00,
        'per_kg_rate': 85.00,
        'estimated_days': '7-21'
    }
}

# Shipping methods
SHIPPING_METHODS = {
    'standard': {
        'name': 'Standard Shipping',
        'description': '5-7 business days',
        'multiplier': 1.0
    },
    'express': {
        'name': 'Express Shipping',
        'description': '2-3 business days',
        'multiplier': 1.5
    },
    'overnight': {
        'name': 'Overnight Delivery',
        'description': 'Next business day (selected areas)',
        'multiplier': 2.5
    },
    'bobgo_pudo': {
        'name': 'Bobgo Pudo Pickup',
        'description': 'Collect from nearest Pudo point',
        'multiplier': 0.7
    }
}


def get_shipping_zone(province, country='South Africa'):
    """Determine shipping zone based on location"""
    province_lower = province.lower() if province else ''
    country_lower = country.lower() if country else ''
    
    # Check if international
    if country_lower not in ['south africa', 'rsa', 'south africa']:
        # Check Southern Africa
        for zone_key, zone_data in SHIPPING_ZONES.items():
            if zone_key == 'southern_africa':
                countries = zone_data.get('countries', [])
                if any(c.lower() in country_lower for c in countries):
                    return zone_key, zone_data
        return 'international', SHIPPING_ZONES['international']
    
    # South Africa zones
    for zone_key, zone_data in SHIPPING_ZONES.items():
        if zone_key in ['southern_africa', 'international']:
            continue
        provinces = zone_data.get('provinces', [])
        if any(p.lower() in province_lower for p in provinces):
            return zone_key, zone_data
    
    # Default to other_sa
    return 'other_sa', SHIPPING_ZONES['other_sa']


def calculate_shipping_cost(zone_key, weight_kg=1, method='standard'):
    """Calculate shipping cost based on zone, weight, and method"""
    zone = SHIPPING_ZONES.get(zone_key, SHIPPING_ZONES['other_sa'])
    shipping_method = SHIPPING_METHODS.get(method, SHIPPING_METHODS['standard'])
    
    base_rate = zone['base_rate']
    per_kg_rate = zone['per_kg_rate']
    
    # Calculate cost
    cost = base_rate + (per_kg_rate * max(0, weight_kg - 1))
    
    # Apply method multiplier
    cost *= shipping_method['multiplier']
    
    return round(cost, 2)


def get_shipping_options(province, country='South Africa', weight_kg=1):
    """Get all available shipping options with pricing"""
    zone_key, zone_data = get_shipping_zone(province, country)
    
    options = []
    for method_key, method_data in SHIPPING_METHODS.items():
        # Skip overnight for international
        if method_key == 'overnight' and zone_key == 'international':
            continue
        
        cost = calculate_shipping_cost(zone_key, weight_kg, method_key)
        options.append({
            'key': method_key,
            'name': method_data['name'],
            'description': method_data['description'],
            'estimated_days': zone_data['estimated_days'],
            'cost': cost,
            'zone': zone_data['name']
        })
    
    return options


def bobgo_get_rates(origin_postal, destination_postal, weight_kg=1):
    """
    Fetch shipping rates from Bobgo API
    Note: This is a mock implementation - replace with actual API calls
    """
    if not BOBGO_API_KEY:
        # Return calculated rates if no API key
        return get_shipping_options('', '', weight_kg)
    
    try:
        response = requests.post(
            f'{BOBGO_API_BASE_URL}/rates',
            headers={
                'Authorization': f'Bearer {BOBGO_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'origin_postal_code': origin_postal,
                'destination_postal_code': destination_postal,
                'weight_kg': weight_kg
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('rates', [])
    except Exception as e:
        print(f'Bobgo API error: {e}')
    
    # Fallback to calculated rates
    return get_shipping_options('', '', weight_kg)


def bobgo_create_shipment(order_data):
    """
    Create shipment via Bobgo API
    """
    if not BOBGO_API_KEY:
        return {'success': False, 'error': 'Bobgo API key not configured'}
    
    try:
        response = requests.post(
            f'{BOBGO_API_BASE_URL}/shipments',
            headers={
                'Authorization': f'Bearer {BOBGO_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'sender': order_data.get('sender'),
                'recipient': order_data.get('recipient'),
                'parcel': order_data.get('parcel'),
                'service_type': order_data.get('service_type', 'standard')
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return {'success': True, 'data': response.json()}
        else:
            return {'success': False, 'error': response.text}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def bobgo_track_shipment(tracking_number):
    """
    Track shipment via Bobgo API
    """
    if not BOBGO_API_KEY:
        return {'success': False, 'error': 'Bobgo API key not configured'}
    
    try:
        response = requests.get(
            f'{BOBGO_API_BASE_URL}/track/{tracking_number}',
            headers={
                'Authorization': f'Bearer {BOBGO_API_KEY}'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return {'success': True, 'data': response.json()}
        else:
            return {'success': False, 'error': response.text}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_pudo_points(province, city):
    """
    Get nearby Bobgo Pudo pickup points
    """
    # This would normally call the Bobgo API
    # Returning mock data for demonstration
    return [
        {
            'id': 'PUDO001',
            'name': f'{city} Central Pudo',
            'address': f'123 Main Street, {city}, {province}',
            'hours': 'Mon-Fri: 8AM-6PM, Sat: 9AM-1PM',
            'distance_km': 2.5
        },
        {
            'id': 'PUDO002',
            'name': f'{city} Mall Pudo',
            'address': f'456 Shopping Centre, {city}, {province}',
            'hours': 'Mon-Sun: 9AM-7PM',
            'distance_km': 4.2
        }
    ]


# Shipping weight defaults (kg)
DEFAULT_WEIGHTS = {
    'Electronics': 1.5,
    'Accessories': 0.5,
    'Bags': 1.0,
    'Footwear': 1.2,
    'Clothing': 0.8,
    'Home': 2.0,
    'Other': 1.0
}


def estimate_order_weight(items):
    """Estimate total order weight based on items"""
    total_weight = 0
    
    for item in items:
        category = item.get('category', 'Other')
        quantity = item.get('quantity', 1)
        base_weight = DEFAULT_WEIGHTS.get(category, 1.0)
        total_weight += base_weight * quantity
    
    return round(total_weight, 2)

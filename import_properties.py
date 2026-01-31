"""
Property Data Import Script
This script imports property data from a CSV/text format into the MySQL database
"""

import mysql.connector
from datetime import datetime

# Database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Empty password
    'database': 'makemystayrealty'
}

# Property data to import (Updated with correct property names and map links)
properties_data = [
    {
        'property_name': 'Ashok PG Colive',
        'location': 'Btm 1st stage',
        'property_type': 'PG',
        'furnishing': 'fully_furnished',
        'private_price': None,
        'single_price': 9000,
        'double_price': None,
        'triple_price': None,
        'listing_type': 'rent',
        'is_available': 1,
        'phone': '9663634346',
        'map_link': 'https://maps.app.goo.gl/xGioX3jzEQHfy2wc7',
        'description': 'Experience comfortable living at Ashok PG Colive in Btm 1st stage. Fully furnished with modern amenities.'
    },
    {
        'property_name': 'Heaven coliving pg',
        'location': 'Kadubeesanahalli',
        'property_type': 'PG',
        'furnishing': 'fully_furnished',
        'private_price': None,
        'single_price': None,
        'double_price': None,
        'triple_price': None,
        'listing_type': 'rent',
        'is_available': 1,
        'phone': '9666832111',
        'map_link': 'https://maps.app.goo.gl/PX7S3UakFxZ8t5oQ9',
        'description': 'Premium living space in Kadubeesanahalli. Ideal for professionals looking for comfort and convenience.'
    },
    {
        'property_name': 'Chap & dona coliving',
        'location': 'Munnekollal',
        'property_type': 'PG',
        'furnishing': 'fully_furnished',
        'private_price': None,
        'single_price': 22000,
        'double_price': 11000,
        'triple_price': None,
        'listing_type': 'buy',
        'is_available': 1,
        'phone': '7993556221',
        'map_link': 'https://maps.app.goo.gl/bFjP7rZSGPzSMkZN6',
        'description': 'Luxury coliving in Munnekollal with top-notch facilities. A perfect blend of style and comfort.'
    },
    {
        'property_name': 'Urban coliving pg',
        'location': 'Munnekollal',
        'property_type': 'PG',
        'furnishing': 'fully_furnished',
        'private_price': None,
        'single_price': 22000,
        'double_price': 11000,
        'triple_price': None,
        'listing_type': 'rent',
        'is_available': 1,
        'phone': '7993556221',
        'map_link': 'https://maps.app.goo.gl/FNSSgCTCGpMUvFdi9',
        'description': 'Affordable and stylish coliving in Munnekollal. Designed for modern living.'
    },
    {
        'property_name': 'Kings & queens colive(B)',
        'location': 'Munnekollal',
        'property_type': 'PG',
        'furnishing': 'fully_furnished',
        'private_price': None,
        'single_price': 22000,
        'double_price': 11000,
        'triple_price': None,
        'listing_type': 'buy',
        'is_available': 1,
        'phone': '7993556221',
        'map_link': 'https://maps.app.goo.gl/NbcVi6GvULbCYrmj8',
        'description': 'Royal living experience in Munnekollal. Spacious rooms with premium furnishings.'
    },
    {
        'property_name': 'MK Comforts Co-Live',
        'location': 'Kundanahalli',
        'property_type': 'PG',
        'furnishing': 'fully_furnished',
        'private_price': None,
        'single_price': 16500,
        'double_price': 9000,
        'triple_price': 7000,
        'listing_type': 'rent',
        'is_available': 1,
        'phone': '9620845586',
        'map_link': 'https://maps.app.goo.gl/pnwm4D8XhgSd2uma9',
        'description': 'Comfortable and spacious PG in Kundanahalli. Great community and excellent services.'
    },
    {
        'property_name': 'Urban premium co living pg',
        'location': 'Nallurahalli',
        'property_type': 'PG',
        'furnishing': 'fully_furnished',
        'private_price': None,
        'single_price': 21000,
        'double_price': 11000,
        'triple_price': None,
        'listing_type': 'buy',
        'is_available': 1,
        'phone': '9666120076',
        'map_link': 'https://maps.app.goo.gl/rubnERvsVJt1qMpi6',
        'description': 'Premium co-living space in Nallurahalli. Experience the best in class living standards.'
    },
    {
        'property_name': 'At Home premium co living pg',
        'location': 'Bellandur',
        'property_type': 'PG',
        'furnishing': 'fully_furnished',
        'private_price': None,
        'single_price': None,
        'double_price': 12000,
        'triple_price': 9000,
        'listing_type': 'rent',
        'is_available': 1,
        'phone': '9849575475',
        'map_link': 'https://maps.app.goo.gl/Cq9t9SpH8vH8k1k68',
        'description': 'Feel at home in Bellandur with our premium amenities. Secure and peaceful environment.'
    },
    {
        'property_name': 'Sgr Enclave Homes',
        'location': 'Sarjapur',
        'property_type': '1BHK',
        'furnishing': 'fully_furnished',
        'private_price': 27000,
        'single_price': None,
        'double_price': None,
        'triple_price': None,
        'listing_type': 'buy',
        'is_available': 1,
        'phone': '9849575475',
        'map_link': 'https://maps.app.goo.gl/mobrcBykDqsvLQRE7',
        'description': 'Spacious 1BHK in Sarjapur. Perfect for families or individuals looking for their own space.'
    },
    {
        'property_name': 'Urban homes',
        'location': 'Munnekollal',
        'property_type': '1RK',
        'furnishing': 'fully_furnished',
        'private_price': 17000,
        'single_price': None,
        'double_price': None,
        'triple_price': None,
        'listing_type': 'rent',
        'is_available': 1,
        'phone': '9849575475',
        'map_link': 'https://maps.app.goo.gl/n3e2sFgDTnGPn9yi8',
        'description': 'Cozy 1RK studio in Munnekollal. Efficient and comfortable living solution.'
    }
]


def import_properties():
    """Import properties into the database"""
    try:
        # Connect to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # SQL insert query
        insert_query = """
        INSERT INTO properties 
        (property_name, location, property_type, furnishing, private_price, 
         single_price, double_price, triple_price, listing_type, is_available, phone, map_link, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        inserted_count = 0
        
        # Insert each property
        for prop in properties_data:
            values = (
                prop['property_name'],
                prop['location'],
                prop['property_type'],
                prop['furnishing'],
                prop['private_price'],
                prop['single_price'],
                prop['double_price'],
                prop['triple_price'],
                prop['listing_type'],
                prop['is_available'],
                prop['phone'],
                prop['map_link'],
                prop['description']
            )
            
            cursor.execute(insert_query, values)
            inserted_count += 1
            print(f"✅ Inserted: {prop['property_name']} - {prop['location']}")
        
        # Commit the transaction
        conn.commit()
        
        print(f"\n🎉 Successfully imported {inserted_count} properties!")
        
        # Close connection
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as error:
        print(f"❌ Error: {error}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def verify_import():
    """Verify the imported data"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT COUNT(*) as total FROM properties")
        result = cursor.fetchone()
        print(f"\n📊 Total properties in database: {result['total']}")
        
        cursor.execute("SELECT * FROM properties ORDER BY id DESC LIMIT 5")
        properties = cursor.fetchall()
        
        print("\n📋 Last 5 properties:")
        for prop in properties:
            print(f"  - {prop['property_name']} | {prop['location']} | {prop['property_type']}")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as error:
        print(f"❌ Error: {error}")


if __name__ == "__main__":
    print("🚀 Starting property import...\n")
    import_properties()
    verify_import()
    print("\n✅ Import complete!")

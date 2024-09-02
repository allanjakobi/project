import sqlite3

def insert_data():
    """ conn = sqlite3.connect('instance/mydatabase.db') """
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Insert data into models table
    cursor.execute('''
    INSERT INTO model (modelId, brand, model, keys, low, sb, bRows, fb, reedsR, reedsL, reeds_fb, range_fb, fb_low, regR, regL, height, width, weight, keyboard, newPrice, usedPrice)
    VALUES
    (1, 'Weltmeister', 'Stella', 26, 59, 40, 5, 0, 3, 4, 0, 0, 0, 5, 0, 34.5, 18, 6.2, 31.5, 1900.00, 900.00),
    (2, 'Menghini', 'Menghini40', 26, 59, 40, 5, 0, 2, 5, 0, 0, 0, 3, 0, 34.5, 18, 5.7, 31.5, 2500.00, 1200.00),
    (3, 'Walther', 'Teeny48', 26, 59, 48, 6, 0, 2, 3, 0, 0, 0, 3, 0, 35.5, 18, 5.8, 31.5, 1900.00, 1000.00),
    (4, 'Weltmeister', 'Rubin', 30, 55, 60, 5, 0, 2, 3, 0, 0, 0, 3, 0, 35.5, 18, 5.6, 31.5, 1900.00, 1000.00),
    (5, 'Harmona', 'Dolphin', 30, 55, 60, 5, 0, 2, 3, 0, 0, 0, 3, 0, 35.5, 18, 5.6, 31.5, 1900.00, 1000.00),
    (6, 'Excelsior', '301E', 26, 59, 48, 6, 0, 2, 4, 0, 0, 0, 3, 0, 35.5, 18, 6.0, 31.5, 2500.00, 1200.00)
''')


    # Insert data into rendipillid table
    cursor.execute('''
    INSERT INTO rendipillid (instrumentId, modelId, color, serial, info_est, info_eng, status, price_level)
    VALUES
    (1, 1, 'red', '07/02346', 'Mõned kollakad plekid lõõtsariidel, mõõdukad kulumisjäljed kastil.', 'Moderate wearing signs', 'available', 1),
    (2, 2, 'red', '11', '"Akordion on 100% töökorras, suuremaid kriimustusi ega deformatsioone ei ole. Üksikud vaevumärgatavad kasutusjäljed korpusel. Pillikast on korras, kuid rohkem kasutatud
"', 'Good shape, case a little bit more usedf', 'available', 1)
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_data()

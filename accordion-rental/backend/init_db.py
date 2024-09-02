import sqlite3

def init_db():
    conn = sqlite3.connect('db.sqlite3')
    """ conn = sqlite3.connect('instance/mydatabase.db') """
    cursor = conn.cursor()

    # Create model table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS model (
        modelId INTEGER PRIMARY KEY UNIQUE,
        brand TEXT,
        model TEXT,
        keys INTEGER,
        low INTEGER,
        sb INTEGER,
        bRows INTEGER,
        fb INTEGER,
        reedsR INTEGER,
        reedsL INTEGER,
        reeds_fb INTEGER,
        range_fb INTEGER,
        fb_low INTEGER,
        regR INTEGER,
        regL INTEGER,
        height REAL,
        width REAL,
        weight REAL,
        keyboard REAL,
        newPrice REAL,
        usedPrice REAL
    )
    ''')

    # Create rendipillid table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rendipillid (
        instrumentId INTEGER PRIMARY KEY,
        modelId INTEGER,
        color TEXT,
        serial TEXT,
        info_est TEXT,
        info_eng TEXT,
        status TEXT,
        price_level INTEGER DEFAULT 1,
        FOREIGN KEY (modelId) REFERENCES model(modelId),
        FOREIGN KEY (price_level) REFERENCES rates(rateId)
    )
    ''')

    # Create rates table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rates (
        rateId INTEGER PRIMARY KEY,
        description TEXT,
        rate REAL
    )
    ''')

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userId INTEGER PRIMARY KEY,
        firstName TEXT,
        lastName TEXT,
        country TEXT,
        province TEXT,
        municipality TEXT,
        settlement TEXT,
        street TEXT,
        house TEXT,
        apartment TEXT,
        phone TEXT,
        email TEXT UNIQUE,
        institution TEXT,
        teacher TEXT
    )
    ''')

    # Create agreements table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agreements (
        agreementId INTEGER PRIMARY KEY,
        referenceNr INTEGER,
        userId INTEGER,
        instrumentId INTEGER,
        startDate DATE,
        months INTEGER,
        rate INTEGER,
        info TEXT,
        status TEXT,
        FOREIGN KEY (userId) REFERENCES users(userId),
        FOREIGN KEY (instrumentId) REFERENCES rendipillid(instrumentId)
    )
    ''')

    # Create invoices table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY,
        date DATE,
        agreementId INTEGER,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY (agreementId) REFERENCES agreements(agreementId)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()

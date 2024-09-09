import sqlite3

def init_db():
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    # Create table for Model
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS model (
        modelId INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        keys INTEGER NOT NULL,
        low INTEGER NOT NULL,
        sb INTEGER NOT NULL,
        bRows INTEGER NOT NULL,
        fb INTEGER DEFAULT 0,
        reedsR INTEGER NOT NULL,
        reedsL INTEGER NOT NULL,
        reeds_fb INTEGER DEFAULT 0,
        range_fb INTEGER DEFAULT 0,
        fb_low INTEGER DEFAULT 0,
        regR INTEGER NOT NULL,
        regL INTEGER NOT NULL,
        height REAL DEFAULT 36,
        width REAL DEFAULT 18,
        length REAL DEFAULT 36,  -- fixed typo
        weight REAL NOT NULL,
        keyboard REAL NOT NULL,
        folds INTEGER,
        deep INTEGER,
        bass_start_notes TEXT,  -- Removed comma at the end
        newPrice REAL DEFAULT 2000,
        usedPrice REAL DEFAULT 1000
    );
    ''')

    # Create table for Rendipillid
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rendipillid (
        instrumentId INTEGER PRIMARY KEY AUTOINCREMENT,
        modelId_id INTEGER NOT NULL,
        color TEXT NOT NULL,
        serial TEXT NOT NULL,
        info_est TEXT NOT NULL,
        info_eng TEXT NOT NULL,
        status TEXT NOT NULL,
        price_level INTEGER DEFAULT 1,
        FOREIGN KEY (modelId_id) REFERENCES model (modelId),  -- Comma added
        FOREIGN KEY (price_level) REFERENCES rates (id)  -- Comma removed
    );
    ''')

    # Create table for Rates
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        rate REAL NOT NULL  -- Removed trailing comma
    );
    ''')

    # Create table for Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userId INTEGER PRIMARY KEY AUTOINCREMENT,
        firstName TEXT NOT NULL,
        lastName TEXT NOT NULL,
        country TEXT DEFAULT 'Estonia',
        province TEXT NOT NULL,
        municipality TEXT NOT NULL,
        settlement TEXT NOT NULL,
        street TEXT NOT NULL,
        house TEXT NOT NULL,
        apartment TEXT,  -- Fixed NULL constraint
        phone TEXT DEFAULT '+372',
        email TEXT UNIQUE NOT NULL,
        institution TEXT,
        teacher TEXT,
        language TEXT
    );
    ''')

    # Create table for Agreements
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agreements (
        agreementId INTEGER PRIMARY KEY AUTOINCREMENT,
        referenceNr INTEGER NOT NULL,
        userId INTEGER NOT NULL,
        instrumentId INTEGER NOT NULL,
        startDate DATE NOT NULL,
        months INTEGER NOT NULL,
        rate INTEGER NOT NULL,
        info TEXT,
        status TEXT NOT NULL,
        invoice_interval INTEGER DEFAULT 1,
        FOREIGN KEY (userId) REFERENCES users(userId) ON DELETE CASCADE,
        FOREIGN KEY (instrumentId) REFERENCES rendipillid(instrumentId) ON DELETE CASCADE
    );
    ''')

    # Create table for Invoices
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        agreementId_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (agreementId_id) REFERENCES agreements (agreementId)
    );
    ''')

    # Commit changes and close connection
    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()

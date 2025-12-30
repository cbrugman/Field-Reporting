import sqlite3
import os

DB_NAME = 'species.db'

# Check if we are running in an environment with a persistent volume mounted at /data
if os.path.exists('/data'):
    DB_NAME = '/data/species.db'
    # Optional: If the DB doesn't exist in /data but exists in current dir, copy it over (seeding)
    if not os.path.exists(DB_NAME) and os.path.exists('species.db'):
        import shutil
        print("Seeding database from image to persistent volume...")
        shutil.copy('species.db', DB_NAME)


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the schema."""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Species Table
    # - common_name: The primary identifier we match against (e.g., "Blue Jay")
    # - scientific_name: Optional, from Excel
    # - category: Plant, Animal, Fungi, etc.
    c.execute('''
        CREATE TABLE IF NOT EXISTS species (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            common_name TEXT NOT NULL,
            scientific_name TEXT,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(common_name)
        )
    ''')

    # Sightings Table
    # - source: Where this came from ("Excel Import", "Report 2024-09-01")
    # - count: Number of individuals (Excel = 1, Reports = N)
    c.execute('''
        CREATE TABLE IF NOT EXISTS sightings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            species_id INTEGER NOT NULL,
            date TEXT,
            count INTEGER DEFAULT 1,
            source TEXT,
            FOREIGN KEY (species_id) REFERENCES species (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} initialized.")

def get_or_create_species(common_name, scientific_name=None, category=None):
    """
    Looks up a species by common_name (case-insensitiveish logic handled by caller or basic lower()).
    If not found, creates it.
    Returns: species_id
    """
    clean_name = common_name.strip()
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Try find
    c.execute('SELECT id FROM species WHERE common_name = ? COLLATE NOCASE', (clean_name,))
    row = c.fetchone()
    
    if row:
        species_id = row['id']
        # Update category if provided (fixing previous Uncategorized entries)
        if category:
            c.execute('UPDATE species SET category = ? WHERE id = ?', (category, species_id))
            conn.commit()
    else:
        # Create
        c.execute('''
            INSERT INTO species (common_name, scientific_name, category)
            VALUES (?, ?, ?)
        ''', (clean_name, scientific_name, category))
        species_id = c.lastrowid
        conn.commit()
        print(f"Created new species: {clean_name}")
        
    conn.close()
    return species_id

def add_sighting(species_id, date, count, source):
    """Adds a sighting record."""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO sightings (species_id, date, count, source)
        VALUES (?, ?, ?, ?)
    ''', (species_id, date, count, source))
    
    conn.commit()
    conn.close()

def get_all_species():
    """Returns a list of all species sorted by category and name, with sighting counts."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT 
            s.*, 
            COUNT(si.id) as sightings_count, 
            COALESCE(SUM(si.count), 0) as total_individuals
        FROM species s
        LEFT JOIN sightings si ON s.id = si.species_id
        GROUP BY s.id
        ORDER BY s.category, s.common_name
    ''')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == '__main__':
    init_db()

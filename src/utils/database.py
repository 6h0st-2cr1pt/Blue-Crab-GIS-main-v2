import sqlite3
import os
import uuid
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="data/blue_crab.db"):
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.initialize_db()
    
    def get_connection(self):
        """Get a connection to the SQLite database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def initialize_db(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if we need to migrate the existing table
        cursor.execute("PRAGMA table_info(crab_data)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # If the old table exists with juvenile/adult columns, we need to migrate
        if 'juvenile_counts' in columns or 'adult_counts' in columns:
            print("Migrating database schema...")
            self.migrate_database(conn, cursor)
        
        # Create observers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS observers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            organization TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create locations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id TEXT PRIMARY KEY,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            location_name TEXT,
            region TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create new crab_data table (without juvenile_counts and adult_counts)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS crab_data_new (
            id TEXT PRIMARY KEY,
            date_month INTEGER NOT NULL,
            date_year INTEGER NOT NULL,
            male_counts INTEGER NOT NULL DEFAULT 0,
            female_counts INTEGER NOT NULL DEFAULT 0,
            population INTEGER NOT NULL,
            observer_id TEXT NOT NULL,
            location_id TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (observer_id) REFERENCES observers (id),
            FOREIGN KEY (location_id) REFERENCES locations (id),
            CHECK (male_counts + female_counts = population),
            CHECK (male_counts >= 0 AND female_counts >= 0),
            CHECK (population > 0),
            CHECK (date_month >= 1 AND date_month <= 12),
            CHECK (date_year >= 1900 AND date_year <= 2100)
        )
        ''')
        
        # If the new table was just created and old table exists, migrate data
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='crab_data'")
        old_table_exists = cursor.fetchone() is not None
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='crab_data_new'")
        new_table_exists = cursor.fetchone() is not None
        
        if old_table_exists and new_table_exists:
            # Check if new table is empty
            cursor.execute("SELECT COUNT(*) FROM crab_data_new")
            new_table_count = cursor.fetchone()[0]
            
            if new_table_count == 0:
                print("Migrating data from old table to new table...")
                # Migrate data from old table to new table
                cursor.execute('''
                INSERT INTO crab_data_new (
                    id, date_month, date_year, male_counts, female_counts, 
                    population, observer_id, location_id, created_at
                )
                SELECT 
                    id, date_month, date_year, 
                    COALESCE(male_counts, 0) as male_counts,
                    COALESCE(female_counts, 0) as female_counts,
                    population, observer_id, location_id, created_at
                FROM crab_data
                ''')
                
                # Drop old table and rename new table
                cursor.execute("DROP TABLE crab_data")
                cursor.execute("ALTER TABLE crab_data_new RENAME TO crab_data")
                print("Database migration completed successfully!")
        elif new_table_exists and not old_table_exists:
            # Just rename the new table to the correct name
            cursor.execute("ALTER TABLE crab_data_new RENAME TO crab_data")
        
        # Drop old crab_population table if it exists
        cursor.execute('DROP TABLE IF EXISTS crab_population')
        
        conn.commit()
        conn.close()
    
    def migrate_database(self, conn, cursor):
        """Migrate existing database to new schema"""
        try:
            # Create backup of existing data
            cursor.execute("CREATE TABLE crab_data_backup AS SELECT * FROM crab_data")
            
            # Drop the old table with constraints
            cursor.execute("DROP TABLE crab_data")
            
            print("Old table backed up and dropped successfully")
            
        except Exception as e:
            print(f"Migration step completed: {e}")
    
    # Observer methods
    def insert_observer(self, data):
        """Insert a new observer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        observer_id = data.get('id', str(uuid.uuid4())[:8])
        
        cursor.execute('''
        INSERT OR REPLACE INTO observers (id, name, email, organization)
        VALUES (?, ?, ?, ?)
        ''', (observer_id, data['name'], data.get('email', ''), data.get('organization', '')))
        
        conn.commit()
        conn.close()
        return observer_id
    
    def get_all_observers(self):
        """Get all observers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM observers ORDER BY name')
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                'id': row['id'],
                'name': row['name'],
                'email': row['email'],
                'organization': row['organization'],
                'created_at': row['created_at']
            })
        
        conn.close()
        return result
    
    # Location methods
    def insert_location(self, data):
        """Insert a new location"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        location_id = data.get('id', str(uuid.uuid4())[:8])
        
        cursor.execute('''
        INSERT OR REPLACE INTO locations (id, latitude, longitude, location_name, region)
        VALUES (?, ?, ?, ?, ?)
        ''', (location_id, data['latitude'], data['longitude'], 
              data.get('location_name', ''), data.get('region', '')))
        
        conn.commit()
        conn.close()
        return location_id
    
    def get_all_locations(self):
        """Get all locations"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM locations ORDER BY location_name')
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                'id': row['id'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'location_name': row['location_name'],
                'region': row['region'],
                'created_at': row['created_at']
            })
        
        conn.close()
        return result
    
    def find_or_create_location(self, latitude, longitude, location_name='', region=''):
        """Find existing location or create new one"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Try to find existing location within 0.001 degrees (approximately 100m)
        cursor.execute('''
        SELECT id FROM locations 
        WHERE ABS(latitude - ?) < 0.001 AND ABS(longitude - ?) < 0.001
        LIMIT 1
        ''', (latitude, longitude))
        
        row = cursor.fetchone()
        if row:
            conn.close()
            return row['id']
        
        # Create new location
        location_id = str(uuid.uuid4())[:8]
        cursor.execute('''
        INSERT INTO locations (id, latitude, longitude, location_name, region)
        VALUES (?, ?, ?, ?, ?)
        ''', (location_id, latitude, longitude, location_name, region))
        
        conn.commit()
        conn.close()
        return location_id
    
    # Crab data methods
    def insert_crab_data(self, data):
        """Insert a single crab data record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Generate ID if not provided
        crab_id = data.get('id', str(uuid.uuid4())[:8])
        
        # Convert month name to number if needed
        if isinstance(data['date_month'], str):
            month_map = {
                'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
            }
            data['date_month'] = month_map.get(data['date_month'].lower(), 1)
        
        # Validate population totals (only male + female now)
        if data['male_counts'] + data['female_counts'] != data['population']:
            raise ValueError("Male + Female counts must equal population")
        
        # Find or create observer
        observer_id = data.get('observer_id')
        if not observer_id and 'observer_name' in data:
            observer_id = self.insert_observer({
                'name': data['observer_name'],
                'email': data.get('observer_email', ''),
                'organization': data.get('observer_organization', '')
            })
        
        # Find or create location
        location_id = data.get('location_id')
        if not location_id:
            location_id = self.find_or_create_location(
                data['latitude'], 
                data['longitude'],
                data.get('location_name', ''),
                data.get('region', '')
            )
        
        cursor.execute('''
        INSERT INTO crab_data (
            id, date_month, date_year, male_counts, female_counts, 
            population, observer_id, location_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (crab_id, data['date_month'], data['date_year'], 
              data['male_counts'], data['female_counts'], 
              data['population'], observer_id, location_id))
        
        conn.commit()
        conn.close()
        return crab_id
    
    def insert_many_crab_data(self, data_list):
        """Insert multiple crab data records"""
        for data in data_list:
            self.insert_crab_data(data)
    
    def get_all_crab_data(self):
        """Get all crab data with observer and location information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT 
            cd.*,
            o.name as observer_name,
            o.email as observer_email,
            o.organization as observer_organization,
            l.latitude,
            l.longitude,
            l.location_name,
            l.region
        FROM crab_data cd
        LEFT JOIN observers o ON cd.observer_id = o.id
        LEFT JOIN locations l ON cd.location_id = l.id
        ORDER BY cd.date_year DESC, cd.date_month DESC
        ''')
        
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append({
                'id': row['id'],
                'date_month': row['date_month'],
                'date_year': row['date_year'],
                'male_counts': row['male_counts'],
                'female_counts': row['female_counts'],
                'population': row['population'],
                'observer_id': row['observer_id'],
                'observer_name': row['observer_name'],
                'observer_email': row['observer_email'],
                'observer_organization': row['observer_organization'],
                'location_id': row['location_id'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'location_name': row['location_name'],
                'region': row['region'],
                'created_at': row['created_at']
            })
        
        conn.close()
        return result
    
    def get_crab_data_by_id(self, crab_id):
        """Get crab data by ID with observer and location information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT 
            cd.*,
            o.name as observer_name,
            o.email as observer_email,
            o.organization as observer_organization,
            l.latitude,
            l.longitude,
            l.location_name,
            l.region
        FROM crab_data cd
        LEFT JOIN observers o ON cd.observer_id = o.id
        LEFT JOIN locations l ON cd.location_id = l.id
        WHERE cd.id = ?
        ''', (crab_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'date_month': row['date_month'],
                'date_year': row['date_year'],
                'male_counts': row['male_counts'],
                'female_counts': row['female_counts'],
                'population': row['population'],
                'observer_id': row['observer_id'],
                'observer_name': row['observer_name'],
                'observer_email': row['observer_email'],
                'observer_organization': row['observer_organization'],
                'location_id': row['location_id'],
                'latitude': row['latitude'],
                'longitude': row['longitude'],
                'location_name': row['location_name'],
                'region': row['region'],
                'created_at': row['created_at']
            }
        return None
    
    def update_crab_data(self, crab_id, data):
        """Update crab data record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Validate population totals
        if data['male_counts'] + data['female_counts'] != data['population']:
            raise ValueError("Male + Female counts must equal population")
        
        cursor.execute('''
        UPDATE crab_data SET
            date_month = ?, date_year = ?, male_counts = ?, 
            female_counts = ?, population = ?
        WHERE id = ?
        ''', (data['date_month'], data['date_year'], 
              data['male_counts'], data['female_counts'], 
              data['population'], crab_id))
        
        conn.commit()
        conn.close()
    
    def delete_crab_data(self, crab_id):
        """Delete crab data by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM crab_data WHERE id = ?', (crab_id,))
        
        conn.commit()
        conn.close()
    
    def get_analytics_data(self):
        """Get data for analytics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get monthly data
        cursor.execute('''
        SELECT 
            date_year, date_month,
            SUM(population) as total_population,
            SUM(male_counts) as total_males,
            SUM(female_counts) as total_females,
            COUNT(*) as record_count
        FROM crab_data
        GROUP BY date_year, date_month
        ORDER BY date_year, date_month
        ''')
        
        monthly_data = cursor.fetchall()
        
        # Get regional data
        cursor.execute('''
        SELECT 
            l.region,
            SUM(cd.population) as total_population,
            COUNT(*) as record_count
        FROM crab_data cd
        LEFT JOIN locations l ON cd.location_id = l.id
        GROUP BY l.region
        ORDER BY total_population DESC
        ''')
        
        regional_data = cursor.fetchall()
        
        # Get sex distribution
        cursor.execute('''
        SELECT 
            SUM(male_counts) as total_males,
            SUM(female_counts) as total_females
        FROM crab_data
        ''')
        
        sex_data = cursor.fetchone()
        
        conn.close()
        
        return {
            'monthly': [dict(row) for row in monthly_data],
            'regional': [dict(row) for row in regional_data],
            'sex_distribution': dict(sex_data) if sex_data else {'total_males': 0, 'total_females': 0}
        }
    
    def reset_database(self):
        """Reset the database by dropping and recreating all tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Drop all tables
        cursor.execute('DROP TABLE IF EXISTS crab_data')
        cursor.execute('DROP TABLE IF EXISTS crab_data_new')
        cursor.execute('DROP TABLE IF EXISTS crab_data_backup')
        cursor.execute('DROP TABLE IF EXISTS crab_population')
        cursor.execute('DROP TABLE IF EXISTS observers')
        cursor.execute('DROP TABLE IF EXISTS locations')
        
        conn.commit()
        conn.close()
        
        # Reinitialize
        self.initialize_db()
        print("Database reset completed successfully!")

    def delete_all_crab_data(self):
        """Delete all records from the crab_data table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM crab_data')
        conn.commit()
        conn.close()
import sqlite3

def init_db():
    conn = sqlite3.connect('resources.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            content TEXT NOT NULL,
            link TEXT NOT NULL,
            priority INTEGER DEFAULT 1
        )
    ''')
    
    # Insert sample data (funny cat picture links)
    sample_data = [
        ('CPT', 
         'Curious Paw Training (CPT) registration can be completed online', 
         'https://placekitten.com/200/300', 1),
        ('registration', 
         'Registration requires submitting a tuna treat preference form', 
         'https://placekitten.com/250/350', 2),
        ('deadline', 
         'Applications are accepted year-round - no deadlines for cat naps!', 
         'https://placekitten.com/300/400', 3),
        ('requirements', 
         'Must provide proof of purring ability and tail length measurement', 
         'https://placekitten.com/350/450', 2)
    ]
    
    cursor.executemany('''
        INSERT INTO resources (keyword, content, link, priority)
        VALUES (?, ?, ?, ?)
    ''', sample_data)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized with sample data!")

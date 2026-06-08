import sqlite3

# conn = sqlite3.connect(":memory:")

conn = sqlite3.connect("fitness_tracker.db")

c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON;")

tables_to_clean = ['clients', 'trainers']

def create_table(cursor, table_name, columns_sql):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});")

def delete_tables(cursor, table_names):
    for table_name in table_names:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

def insert_trainers(cursor):
    trainers = [('Josh', 'Cardio'),
            ('Jack', 'Cross'),
            ('Jared', 'Powerlifting')]
    query = "INSERT INTO trainers (name, specialty) VALUES (?, ?)"
    cursor.executemany(query, trainers)

def insert_clients(cursor):
    clients = [('Josh', 58.90, 3),
           ('Jacob', 63.50, 3),
           ('Dwayne', 70.50, 3),
           ('Alex', 98.00, 2),
           ('Jon', 101.20, 1),
           ('Sean', 98.30, 1)]
    query = "INSERT INTO clients (name, weight, trainer_id) VALUES (?, ?, ?)"
    cursor.executemany(query, clients)

def show_clients_with_trainers(cursor):
    cursor.execute("""
    SELECT clients.id, clients.name, clients.weight, trainers.name
    FROM clients
    INNER JOIN trainers ON clients.trainer_id = trainers.id;
    """)
    items = cursor.fetchall()

    for item in items:
        print(f"ID: {item[0]} | Client: {item[1]} | Weight: {item[2]} | Trainer: {item[3]}")

delete_tables(c, tables_to_clean)

create_table(c, "trainers", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, specialty TEXT")
create_table(c, "clients", "id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, weight REAL, trainer_id INTEGER, FOREIGN KEY (trainer_id) REFERENCES trainers(id)")

insert_trainers(c)
insert_clients(c)

show_clients_with_trainers(c)

conn.commit()
conn.close()
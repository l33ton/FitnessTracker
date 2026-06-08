import sqlite3

# conn = sqlite3.connect(":memory:")

conn = sqlite3.connect("fitness_tracker.db")

c = conn.cursor()

c.execute("PRAGMA foreign_keys = ON;")

c.execute("DROP TABLE IF EXISTS clients;")
c.execute("DROP TABLE IF EXISTS trainers;")

c.execute("""CREATE TABLE IF NOT EXISTS trainers (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT,
          specialty TEXT
          )
""")
c.execute("""CREATE TABLE IF NOT EXISTS clients (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT,
          weight REAL,
          trainer_id INTEGER,
          FOREIGN KEY (trainer_id) REFERENCES trainers(id)
          )
""")

trainers = [('Josh', 'Cardio'),
            ('Jack', 'Cross'),
            ('Jared', 'Powerlifting')]
clients = [('Josh', 58.90, 3),
           ('Jacob', 63.50, 3),
           ('Dwayne', 70.50, 3),
           ('Alex', 98.00, 2),
           ('Jon', 101.20, 1),
           ('Sean', 98.30, 1)]

c.executemany("INSERT INTO trainers (name, specialty) VALUES (?, ?)", trainers)
c.executemany("INSERT INTO clients (name, weight, trainer_id) VALUES (?, ?, ?)", clients)


c.execute("""
    SELECT clients.id, clients.name, clients.weight, trainers.name
    FROM clients
    INNER JOIN trainers ON clients.trainer_id = trainers.id;
""")
items = c.fetchall()

for item in items:
    print(f"ID: {item[0]} | Client: {item[1]} | Weight: {item[2]} | Trainer: {item[3]}")


conn.commit()
conn.close()
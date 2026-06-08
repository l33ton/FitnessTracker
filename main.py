from fastapi import FastAPI, Depends
from pydantic import BaseModel
import sqlite3
# ==================================================================================
# INITIALIZE THE APP
app = FastAPI(title="Fitness Tracker API")

# ==================================================================================
# PYDANTIC MODELS
class ClientCreate(BaseModel):
    name: str
    weight: float
    trainer_id: int

# ==================================================================================
# HELPER METHODS
def get_db():
    conn = sqlite3.connect("fitness_tracker.db")
    conn.execute("PRAGMA foreign_keys = ON;")

    try:
        yield conn
    finally:
        conn.close()
# ==================================================================================
# GENERAL ENDPOINTS
@app.get("/")
def home():
    return {"message": "Welcome to Fitness Tracker API"}

# ==================================================================================
# OPERATIONS WITH CLIENTS

@app.get("/clients")
def get_clients(db = Depends(get_db)):
    c = db.cursor()
    c.execute("SELECT id, name, weight FROM clients;")
    items = c.fetchall()

    return {"status": "success", 
            "total_clients": len(items), 
            "data": items}
@app.get("/clients/detailed")
def get_detailed_info_about_the_clients(db = Depends(get_db)):
    c = db.cursor()
    
    c.execute("""
    SELECT clients.id, clients.name, clients.weight, trainers.name
    FROM clients
    INNER JOIN trainers ON clients.trainer_id = trainers.id;
    """)
    items = c.fetchall()

    for item in items:
        print(f"ID: {item[0]} | Client: {item[1]} | Weight: {item[2]} | Trainer: {item[3]}")

    return {"status": "success",
            "data": } 

@app.get("/clients/filter-clients-by-trainer")
def filter_clients_by_trainer(trainer_id:int, db = Depends(get_db)):
    c = db.cursor()
    c.execute("SELECT id, name, weight FROM clients WHERE trainer_id = ?;", (trainer_id,))
    items = c.fetchall()

    return {
        "filtered_by_trainer_id": trainer_id,
        "count": len(items),
        "data": items
    }

@app.post("/clients/add")
def add(client_data: ClientCreate, db = Depends(get_db)):
    c = db.cursor()

    query = "INSERT INTO clients (name, weight, trainer_id) VALUES (?, ?, ?);"

    c.execute(query, (client_data.name, client_data.weight, client_data.trainer_id))

    db.commit()

    return {"status": "success", 
            "message": f"Client {client_data.name} successfully created"} 
            
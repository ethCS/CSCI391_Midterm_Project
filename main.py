from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from datetime import datetime
import sqlite3
import os

# === App instance ===
app = FastAPI(title="Car Maintenance Logger")

# === Database path ===
DB_PATH = "/media/volume/car-data/carlogger.db"  # change later if volume is different
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Create table if it doesn't exist
conn = sqlite3.connect(DB_PATH)
conn.execute("""
CREATE TABLE IF NOT EXISTS maintenance_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_name TEXT,
    make TEXT,
    model TEXT,
    year INTEGER,
    service TEXT,
    mileage INTEGER,
    notes TEXT,
    date TEXT
)
""")
conn.commit()
conn.close()

# === Routes ===
@app.get("/", response_class=HTMLResponse)
def home():
    # Display all maintenance logs in a simple HTML table
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT * FROM maintenance_logs ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()

    html = "<h1>Car Maintenance Logs</h1>"
    html += "<table border='1'><tr><th>ID</th><th>Owner</th><th>Make</th><th>Model</th><th>Year</th><th>Service</th><th>Mileage</th><th>Notes</th><th>Date</th></tr>"
    for row in rows:
        html += "<tr>" + "".join(f"<td>{item}</td>" for item in row) + "</tr>"
    html += "</table>"

    # Simple form to add new entries
    html += """
    <h2>Add New Entry</h2>
    <form action="/add" method="post">
        Owner Name: <input name="owner_name"><br>
        Car Make: <input name="make"><br>
        Car Model: <input name="model"><br>
        Year: <input name="year" type="number"><br>
        Service/Component: <input name="service"><br>
        Mileage: <input name="mileage" type="number"><br>
        Notes: <input name="notes"><br>
        <button type="submit">Add Entry</button>
    </form>
    """
    return html

@app.post("/add")
def add_entry(
    owner_name: str = Form(...),
    make: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    service: str = Form(...),
    mileage: int = Form(...),
    notes: str = Form("")
):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO maintenance_logs (owner_name, make, model, year, service, mileage, notes, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (owner_name, make, model, year, service, mileage, notes, date)
    )
    conn.commit()
    conn.close()
    return {"message": "Entry added successfully!"}

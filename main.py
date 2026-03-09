from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
import sqlite3
import os

app = FastAPI(title="Car Maintenance Logger")

DB_PATH = "/media/volume/car-data/carlogger.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

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

@app.get("/", response_class=HTMLResponse)
def home():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT * FROM maintenance_logs ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()

    html = """
    <html>
    <head>
        <title>Car Maintenance Logger</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-dark text-light">
    <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Car Maintenance Logs</h1>
        <a href="/" class="btn btn-secondary">Home</a>
    </div>
    <table class="table table-dark table-striped table-hover">
    <thead>
        <tr>
            <th>#</th>
            <th>Owner</th>
            <th>Make</th>
            <th>Model</th>
            <th>Year</th>
            <th>Service</th>
            <th>Mileage</th>
            <th>Notes</th>
            <th>Date</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
    """
    for i, row in enumerate(rows, start=1):
        html += "<tr>"
        html += f"<td>{i}</td>"
        for item in row[1:]:
            html += f"<td>{item}</td>"
        html += f"""
        <td>
            <a class="btn btn-warning btn-sm mb-1" href="/edit/{row[0]}">Edit</a>
            <form action="/delete/{row[0]}" method="post" style="display:inline;">
                <button class="btn btn-danger btn-sm">Delete</button>
            </form>
        </td>
        """
        html += "</tr>"

    html += """
    </tbody>
    </table>

    <div class="card bg-secondary p-3 mt-4">
    <h3>Add New Entry</h3>
    <form action="/add" method="post">
    <div class="row">
        <div class="col"><input class="form-control mb-2" name="owner_name" placeholder="Owner Name" required></div>
        <div class="col"><input class="form-control mb-2" name="make" placeholder="Car Make" required></div>
        <div class="col"><input class="form-control mb-2" name="model" placeholder="Car Model" required></div>
    </div>
    <div class="row">
        <div class="col"><input class="form-control mb-2" name="year" type="number" placeholder="Year" required></div>
        <div class="col"><input class="form-control mb-2" name="service" placeholder="Service / Component" required></div>
        <div class="col"><input class="form-control mb-2" name="mileage" type="number" placeholder="Mileage" required></div>
    </div>
    <input class="form-control mb-2" name="notes" placeholder="Notes (optional)">
    <button class="btn btn-primary">Add Entry</button>
    </form>
    </div>
    </div>
    </body>
    </html>
    """
    return html

@app.post("/add")
def add_entry(owner_name: str = Form(...), make: str = Form(...), model: str = Form(...), year: int = Form(...), service: str = Form(...), mileage: int = Form(...), notes: str = Form("")):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO maintenance_logs (owner_name, make, model, year, service, mileage, notes, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (owner_name, make, model, year, service, mileage, notes, date))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

@app.post("/delete/{entry_id}")
def delete_entry(entry_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM maintenance_logs WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

@app.get("/edit/{entry_id}", response_class=HTMLResponse)
def edit_page(entry_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT * FROM maintenance_logs WHERE id=?", (entry_id,))
    row = cursor.fetchone()
    conn.close()
    return f"""
    <html>
    <head><title>Edit Entry</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"></head>
    <body class="bg-dark text-light">
    <div class="container mt-4">
    <h2>Edit Entry</h2>
    <form action="/update/{entry_id}" method="post">
    <div class="row mb-2">
        <div class="col"><input class="form-control" name="owner_name" value="{row[1]}" required></div>
        <div class="col"><input class="form-control" name="make" value="{row[2]}" required></div>
        <div class="col"><input class="form-control" name="model" value="{row[3]}" required></div>
    </div>
    <div class="row mb-2">
        <div class="col"><input class="form-control" name="year" type="number" value="{row[4]}" required></div>
        <div class="col"><input class="form-control" name="service" value="{row[5]}" required></div>
        <div class="col"><input class="form-control" name="mileage" type="number" value="{row[6]}" required></div>
    </div>
    <input class="form-control mb-2" name="notes" value="{row[7]}">
    <button class="btn btn-primary">Update Entry</button>
    </form>
    <br><a class="btn btn-secondary" href="/">Home</a>
    </div>
    </body>
    </html>
    """

@app.post("/update/{entry_id}")
def update_entry(entry_id: int, owner_name: str = Form(...), make: str = Form(...), model: str = Form(...), year: int = Form(...), service: str = Form(...), mileage: int = Form(...), notes: str = Form("")):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE maintenance_logs SET owner_name=?, make=?, model=?, year=?, service=?, mileage=?, notes=? WHERE id=?", (owner_name, make, model, year, service, mileage, notes, entry_id))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)

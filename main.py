from datetime import datetime
from html import escape
from pathlib import Path
import os
import sqlite3

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="Car Maintenance Logger")

APP_DIR = Path(__file__).resolve().parent
LEGACY_DB_PATH = Path("/media/volume/car-data/carlogger.db")
DEFAULT_DB_PATH = LEGACY_DB_PATH if LEGACY_DB_PATH.exists() else APP_DIR / "carlogger.db"
DB_PATH = os.getenv("CAR_LOGGER_DB_PATH", str(DEFAULT_DB_PATH))
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

ROSE_PINE_CSS = """
<style>
    :root {
        color-scheme: dark;
        --base: #191724;
        --surface: #1f1d2e;
        --overlay: #26233a;
        --muted: #6e6a86;
        --subtle: #908caa;
        --text: #e0def4;
        --love: #eb6f92;
        --gold: #f6c177;
        --rose: #ebbcba;
        --pine: #31748f;
        --foam: #9ccfd8;
        --iris: #c4a7e7;
    }

    * { box-sizing: border-box; }

    body {
        margin: 0;
        font-family: Inter, "Segoe UI", sans-serif;
        background:
            radial-gradient(circle at top left, rgba(196, 167, 231, 0.18), transparent 0 30%),
            radial-gradient(circle at top right, rgba(235, 111, 146, 0.18), transparent 0 28%),
            linear-gradient(135deg, #15111f 0%, var(--base) 55%, #12101a 100%);
        color: var(--text);
        min-height: 100vh;
    }

    a { color: inherit; text-decoration: none; }

    .container {
        width: min(1180px, calc(100% - 2rem));
        margin: 0 auto;
        padding: 32px 0 48px;
    }

    .hero-card,
    .panel,
    .stat-card {
        background: rgba(31, 29, 46, 0.88);
        border: 1px solid rgba(224, 222, 244, 0.08);
        border-radius: 24px;
        box-shadow: 0 22px 48px rgba(8, 6, 16, 0.35);
        backdrop-filter: blur(18px);
    }

    .hero-card {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 18px;
        padding: 28px;
        margin-bottom: 18px;
    }

    .eyebrow {
        margin: 0 0 8px;
        color: var(--foam);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.78rem;
        font-weight: 700;
    }

    h1, h2, h3, p { margin-top: 0; }

    h1 {
        margin-bottom: 10px;
        font-size: clamp(2rem, 4vw, 2.8rem);
        line-height: 1.08;
    }

    .hero-subtitle,
    .panel-subtitle,
    .muted { color: var(--subtle); }

    .hero-actions,
    .form-actions,
    .table-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 14px;
        margin-bottom: 18px;
    }

    .stat-card {
        padding: 18px;
    }

    .stat-label {
        color: var(--subtle);
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }

    .stat-value {
        font-size: 1.7rem;
        font-weight: 700;
    }

    .layout-grid {
        display: grid;
        grid-template-columns: 1.1fr 0.9fr;
        gap: 18px;
    }

    .panel {
        padding: 22px;
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        align-items: start;
        margin-bottom: 16px;
    }

    .entry-form {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
    }

    .field,
    .field-full {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .field-full { grid-column: 1 / -1; }

    .field-label {
        color: var(--rose);
        font-size: 0.92rem;
        font-weight: 600;
    }

    input,
    textarea {
        width: 100%;
        border: 1px solid rgba(224, 222, 244, 0.09);
        background: rgba(38, 35, 58, 0.9);
        color: var(--text);
        border-radius: 14px;
        padding: 12px 14px;
        outline: none;
        transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
    }

    textarea {
        min-height: 96px;
        resize: vertical;
    }

    input:focus,
    textarea:focus {
        border-color: rgba(196, 167, 231, 0.65);
        box-shadow: 0 0 0 4px rgba(196, 167, 231, 0.14);
        transform: translateY(-1px);
    }

    .button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        border: none;
        border-radius: 999px;
        padding: 10px 16px;
        font-weight: 700;
        cursor: pointer;
        transition: transform 0.16s ease, opacity 0.16s ease, box-shadow 0.16s ease;
    }

    .button:hover { transform: translateY(-1px); opacity: 0.95; }

    .primary {
        background: linear-gradient(135deg, var(--iris), #9079f8);
        color: #15111f;
        box-shadow: 0 14px 28px rgba(196, 167, 231, 0.22);
    }

    .secondary {
        background: rgba(49, 116, 143, 0.2);
        color: var(--foam);
        border: 1px solid rgba(156, 207, 216, 0.16);
    }

    .warning {
        background: rgba(246, 193, 119, 0.18);
        color: var(--gold);
        border: 1px solid rgba(246, 193, 119, 0.18);
    }

    .danger {
        background: rgba(235, 111, 146, 0.16);
        color: var(--love);
        border: 1px solid rgba(235, 111, 146, 0.16);
    }

    .table-wrap {
        overflow-x: auto;
        border-radius: 18px;
        border: 1px solid rgba(224, 222, 244, 0.06);
        background: rgba(25, 23, 36, 0.6);
    }

    table {
        width: 100%;
        border-collapse: collapse;
        min-width: 780px;
    }

    th,
    td {
        padding: 14px 12px;
        text-align: left;
        vertical-align: top;
        border-bottom: 1px solid rgba(224, 222, 244, 0.06);
    }

    th {
        color: var(--foam);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        background: rgba(38, 35, 58, 0.82);
    }

    tbody tr:hover {
        background: rgba(38, 35, 58, 0.55);
    }

    .service-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        background: rgba(196, 167, 231, 0.14);
        color: var(--iris);
    }

    .badge-foam { background: rgba(156, 207, 216, 0.14); color: var(--foam); }
    .badge-gold { background: rgba(246, 193, 119, 0.14); color: var(--gold); }
    .badge-love { background: rgba(235, 111, 146, 0.14); color: var(--love); }

    .empty-state {
        padding: 30px 18px;
        text-align: center;
        color: var(--subtle);
    }

    @media (max-width: 920px) {
        .layout-grid {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 640px) {
        .container { width: min(100% - 1rem, 1180px); }
        .hero-card, .panel { padding: 18px; }
        .entry-form { grid-template-columns: 1fr; }
    }
</style>
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


with get_connection() as conn:
    conn.execute(
        """
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
        """
    )
    conn.commit()


def safe(value) -> str:
    return escape("" if value is None else str(value), quote=True)


def format_date(value: str | None) -> str:
    if not value:
        return "—"
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).strftime("%b %d, %Y • %I:%M %p")
        except ValueError:
            continue
    return safe(value)


def service_badge(service: str | None) -> str:
    label = (service or "Service").strip()
    lowered = label.lower()
    badge_class = "service-badge"

    if any(term in lowered for term in ("oil", "fluid", "filter")):
        badge_class += " badge-gold"
    elif any(term in lowered for term in ("tire", "wheel", "brake")):
        badge_class += " badge-love"
    elif any(term in lowered for term in ("inspection", "battery", "engine", "spark")):
        badge_class += " badge-foam"

    return f'<span class="{badge_class}">{safe(label)}</span>'


def render_shell(title: str, body: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{safe(title)}</title>
        {ROSE_PINE_CSS}
    </head>
    <body>
        <div class="container">
            {body}
        </div>
    </body>
    </html>
    """


def render_entry_form(action: str, submit_label: str, entry=None) -> str:
    entry = entry or {}
    return f"""
    <form class="entry-form" action="{safe(action)}" method="post">
        <label class="field">
            <span class="field-label">Owner Name</span>
            <input name="owner_name" placeholder="Jordan Lee" value="{safe(entry.get('owner_name', ''))}" required>
        </label>
        <label class="field">
            <span class="field-label">Service / Component</span>
            <input name="service" placeholder="Oil Change" value="{safe(entry.get('service', ''))}" required>
        </label>
        <label class="field">
            <span class="field-label">Car Make</span>
            <input name="make" placeholder="Subaru" value="{safe(entry.get('make', ''))}" required>
        </label>
        <label class="field">
            <span class="field-label">Car Model</span>
            <input name="model" placeholder="Outback" value="{safe(entry.get('model', ''))}" required>
        </label>
        <label class="field">
            <span class="field-label">Year</span>
            <input name="year" type="number" min="1900" max="2100" placeholder="2022" value="{safe(entry.get('year', ''))}" required>
        </label>
        <label class="field">
            <span class="field-label">Mileage</span>
            <input name="mileage" type="number" min="0" step="1" placeholder="45210" value="{safe(entry.get('mileage', ''))}" required>
        </label>
        <label class="field-full">
            <span class="field-label">Notes</span>
            <textarea name="notes" placeholder="Parts replaced, shop used, reminders, or follow-up items...">{safe(entry.get('notes', ''))}</textarea>
        </label>
        <div class="field-full form-actions">
            <button class="button primary" type="submit">{safe(submit_label)}</button>
            <a class="button secondary" href="/">Back Home</a>
        </div>
    </form>
    """


@app.get("/", response_class=HTMLResponse)
def home():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM maintenance_logs ORDER BY datetime(date) DESC, id DESC").fetchall()

    total_entries = len(rows)
    unique_vehicles = len({(row["make"], row["model"], row["year"]) for row in rows})
    service_types = len({row["service"] for row in rows if row["service"]})
    latest_service = format_date(rows[0]["date"]) if rows else "No entries yet"

    table_rows = ""
    for index, row in enumerate(rows, start=1):
        notes = safe(row["notes"]) if row["notes"] else '<span class="muted">No notes</span>'
        vehicle = f"{safe(row['year'])} {safe(row['make'])} {safe(row['model'])}"
        table_rows += f"""
        <tr>
            <td>{index}</td>
            <td><strong>{safe(row['owner_name'])}</strong></td>
            <td>{vehicle}</td>
            <td>{service_badge(row['service'])}</td>
            <td>{safe(row['mileage'])} mi</td>
            <td>{notes}</td>
            <td>{format_date(row['date'])}</td>
            <td>
                <div class="table-actions">
                    <a class="button warning" href="/edit/{row['id']}">Edit</a>
                    <form action="/delete/{row['id']}" method="post" onsubmit="return confirm('Delete this maintenance entry?');">
                        <button class="button danger" type="submit">Delete</button>
                    </form>
                </div>
            </td>
        </tr>
        """

    logs_section = f"""
    <section class="panel">
        <div class="panel-header">
            <div>
                <p class="eyebrow">Service history</p>
                <h2>Maintenance Timeline</h2>
                <p class="panel-subtitle">A darker, cleaner dashboard for tracking every repair and tune-up.</p>
            </div>
        </div>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Owner</th>
                        <th>Vehicle</th>
                        <th>Service</th>
                        <th>Mileage</th>
                        <th>Notes</th>
                        <th>Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows if table_rows else '<tr><td colspan="8"><div class="empty-state">No maintenance logs yet. Add your first entry to bring the dashboard to life.</div></td></tr>'}
                </tbody>
            </table>
        </div>
    </section>
    """

    body = f"""
    <section class="hero-card">
        <div>
            <p class="eyebrow">Ethan Elliott's</p>
            <h1>Vehicle Maintenance Logger</h1>
            <p class="hero-subtitle">Track every service visit, mileage milestone, and repair note.</p>
        </div>
        <div class="hero-actions">
            <a class="button primary" href="#new-entry">+ Add New Entry</a>
            <a class="button secondary" href="/">Refresh</a>
        </div>
    </section>

    <section class="stats-grid">
        <div class="stat-card"><div class="stat-label">Total Entries</div><div class="stat-value">{total_entries}</div></div>
        <div class="stat-card"><div class="stat-label">Vehicles Tracked</div><div class="stat-value">{unique_vehicles}</div></div>
        <div class="stat-card"><div class="stat-label">Service Types</div><div class="stat-value">{service_types}</div></div>
        <div class="stat-card"><div class="stat-label">Latest Update</div><div class="stat-value" style="font-size:1rem; line-height:1.4;">{latest_service}</div></div>
    </section>

    <section class="layout-grid">
        {logs_section}
        <section class="panel" id="new-entry">
            <div class="panel-header">
                <div>
                    <p class="eyebrow">Quick capture</p>
                    <h2>Add a New Entry</h2>
                    <p class="panel-subtitle">Log maintenance in seconds with a more modern form layout.</p>
                </div>
            </div>
            {render_entry_form('/add', 'Save Entry')}
        </section>
    </section>
    """
    return render_shell("Car Maintenance Logger", body)


@app.post("/add")
def add_entry(
    owner_name: str = Form(...),
    make: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    service: str = Form(...),
    mileage: int = Form(...),
    notes: str = Form(""),
):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO maintenance_logs (owner_name, make, model, year, service, mileage, notes, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (owner_name, make, model, year, service, mileage, notes, date),
        )
        conn.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/delete/{entry_id}")
def delete_entry(entry_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM maintenance_logs WHERE id = ?", (entry_id,))
        conn.commit()
    return RedirectResponse("/", status_code=303)


@app.get("/edit/{entry_id}", response_class=HTMLResponse)
def edit_page(entry_id: int):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM maintenance_logs WHERE id = ?", (entry_id,)).fetchone()

    if row is None:
        body = """
        <section class="hero-card">
            <div>
                <p class="eyebrow">Not found</p>
                <h1>Entry Missing</h1>
                <p class="hero-subtitle">That maintenance record no longer exists.</p>
            </div>
            <div class="hero-actions">
                <a class="button secondary" href="/">Return Home</a>
            </div>
        </section>
        """
        return HTMLResponse(render_shell("Entry Not Found", body), status_code=404)

    body = f"""
    <section class="hero-card">
        <div>
            <p class="eyebrow">Edit mode</p>
            <h1>Update Maintenance Entry</h1>
            <p class="hero-subtitle">Fine-tune the details while keeping the same clean Rose Pine styling.</p>
        </div>
        <div class="hero-actions">
            <a class="button secondary" href="/">Home</a>
        </div>
    </section>

    <section class="panel">
        <div class="panel-header">
            <div>
                <p class="eyebrow">Record details</p>
                <h2>Edit Service Log</h2>
                <p class="panel-subtitle">Adjust mileage, notes, or the service type and save instantly.</p>
            </div>
        </div>
        {render_entry_form(f'/update/{entry_id}', 'Update Entry', dict(row))}
    </section>
    """
    return render_shell("Edit Entry", body)


@app.post("/update/{entry_id}")
def update_entry(
    entry_id: int,
    owner_name: str = Form(...),
    make: str = Form(...),
    model: str = Form(...),
    year: int = Form(...),
    service: str = Form(...),
    mileage: int = Form(...),
    notes: str = Form(""),
):
    with get_connection() as conn:
        conn.execute(
            "UPDATE maintenance_logs SET owner_name = ?, make = ?, model = ?, year = ?, service = ?, mileage = ?, notes = ? WHERE id = ?",
            (owner_name, make, model, year, service, mileage, notes, entry_id),
        )
        conn.commit()
    return RedirectResponse("/", status_code=303)

# CSCI391_Midterm_Project
Midterm project for CSCI391 (Cloud Computing)

# Car Maintenance Logger

A simple cloud-native web application to log and track car maintenance tasks.  
Designed to be **easy to deploy**, **secure**, and **resilient** on Jetstream2 while demonstrating DevOps best practices.

---

## Features

- Add a maintenance entry for a car:
  - Owner Name
  - Car Make
  - Car Model
  - Year
  - Service/Component (Oil, Plugs, Tires, Brakes, etc.)
  - Mileage
  - Notes (optional)
  - Date (auto-filled by default)
- View all maintenance logs in a clean, list format
- Filter by car or component (optional enhancement)
- Persistent storage across server reboots

---

## Tech Stack

- **Python + Flask** – Lightweight web framework  
- **SQLite** – Single-file database, stored on mounted volume for persistence  
- **Gunicorn** – WSGI server for Flask  
- **Caddy** – Reverse proxy with HTTPS (via nip.io)  
- **systemd** – Ensures app runs continuously and auto-starts on reboot  
- **GitHub Actions** – Automates CI/CD deployment  

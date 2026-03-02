# Car Maintenance Logger

A simple cloud-native web application to log and track car maintenance tasks.  
Designed to meet the core requirements of the Cloud Computing Midterm Project.

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
- Entries persist across server reboots

---

## Core Project Requirements Covered

- **Secured Perimeter:** Only required ports are open (SSH, HTTP, HTTPS)  
- **GitOps Automation:** Push to `main` triggers CI/CD deployment via GitHub Actions  
- **Multi-Tenant Routing & SSL:** App served securely over HTTPS using Caddy and accessible via `nip.io` subdomain  
- **Resilience:** systemd ensures app runs continuously and database persists across reboots  

---

## Usage

1. Open your browser → `https://mycarlogger.<Will update with IP later>.nip.io`
2. Add new maintenance entries via the web form
3. View all entries in the dashboard
4. Reboot server → systemd auto-starts the app → entries remain intact
5. Push code updates → GitHub Actions auto-deploys changes to the live server

---

## Demo Workflow for Presentation

1. Add a maintenance entry  
2. Show entries on dashboard  
3. Reboot server → app auto-starts  
4. Refresh dashboard → data persists  
5. Push code change → GitHub Actions auto-deploys  

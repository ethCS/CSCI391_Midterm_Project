# Car Maintenance Logger

A simple cloud-native web application to log and track car maintenance tasks.  

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

1. Open your browser → "https://149.165.169.156.nip.io/"
2. Add new maintenance entries via the web form
3. View all entries in the dashboard
4. Reboot server → systemd auto-starts the app → entries remain intact
5. Push code updates → GitHub Actions auto-deploys changes to the live server

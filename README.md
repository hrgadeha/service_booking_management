# Service Booking Management

A custom Frappe app to manage service bookings, send booking confirmations via webhook and email, and track approval status.

## Requirements

- Frappe Framework: v15+
- Python 3.10+
- Node.js 18+
- Redis, MariaDB, yarn (standard Frappe setup)

## 🚀 Features

- Service Booking DocType with fields like:
  - Customer Name, Email
  - Service Type
  - Preferred Date & Time
  - Status (Requested, Approved, Completed)

- Auto-send confirmation email when booking is approved
- Push booking details to webhook endpoint via REST API
- Custom server-side method to expose booking details over API

## Installation

```bash
cd ~/frappe-bench/apps
bench get-app --branch main https://github.com/hrgadeha/service_booking_management.git
```


```bash
cd ~/frappe-bench
bench --site yoursite.local install-app service_booking_management
```

```bash
bench --site yoursite.local migrate
```

```bash
bench restart
```

## System Info

- OS : Ubunut 22.04
- Python : 3.10.12
- ERPNext : 15.55.0
- Frappe : 15.61.0
- Tools Used : VS Code, Digital Occean Droplet, Github

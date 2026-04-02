# Hospital Management System (H.M.S)

A full-featured Hospital Management System REST API built with Django and Django REST Framework.

---

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (SimpleJWT)
- **Containerization:** Docker
- **Documentation:** Swagger (drf-spectacular)

---

## Features

- JWT Authentication with access and refresh tokens
- Role-based permissions system
- UUID primary keys for security
- Filtering, searching, and ordering
- Pagination
- API documentation with Swagger
- Dockerized for easy deployment

---

## User Roles

| Role | Description |
|------|-------------|
| `admin` | Full access to everything |
| `supervisor` | Full billing access including refunds |
| `doctor` | Read access to patients and appointments, create doctor notes |
| `nurse` | Read access to patients, create and edit own nurse notes |
| `receptionist` | Assign patients to appointments, create and update invoices |
| `accountant` | Read only access to billing |
| `patient` | Access to own data only |
| `lab` | Create and update own lab results |
| `radiology` | Create and update own radiology results |

---

## Project Structure

```
src/
├── H_M_S/                  # Project settings and urls
├── accounts/               # Users, roles, JWT authentication
├── patients/               # Patient profiles
├── doctors/                # Doctor profiles and departments
├── appointments/           # Appointments and scheduling
├── billing/                # Invoices and payments
└── medical_records/        # Medical records, doctor notes, nurse notes, lab results
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/hospital-management-system.git
cd hospital-management-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r req.txt
```

4. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

5. Update the `.env` file with your settings:
```
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_NAME=hospital_db
DATABASE_USER=your_postgres_username
DATABASE_PASSWORD=your_postgres_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the server:
```bash
python manage.py runserver
```

---

### Running with Docker

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Run migrations inside the container:
```bash
docker-compose exec web python manage.py migrate
```

3. Create a superuser inside the container:
```bash
docker-compose exec web python manage.py createsuperuser
```

---

## API Documentation

After running the server, visit:
```
http://127.0.0.1:8000/api/docs/
```

---

## API Endpoints

### Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/accounts/register/` | Register a new user |
| POST | `/api/accounts/login/` | Login and get JWT tokens |
| GET | `/api/accounts/profile/` | Get current user profile |
| POST | `/api/token/refresh/` | Refresh access token |

### Patients
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/patients/` | List all patients |
| POST | `/api/patients/` | Create a new patient |
| GET | `/api/patients/{id}/` | Get patient details |
| PATCH | `/api/patients/{id}/` | Update patient |
| DELETE | `/api/patients/{id}/` | Delete patient |

### Doctors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/doctors/` | List all doctors |
| POST | `/api/doctors/` | Create a new doctor |
| GET | `/api/doctors/{id}/` | Get doctor details |
| GET | `/api/doctors/departments/` | List all departments |
| POST | `/api/doctors/departments/` | Create a new department |

### Appointments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/appointments/` | List all appointments |
| POST | `/api/appointments/` | Create a new appointment slot (admin only) |
| PATCH | `/api/appointments/{id}/` | Assign patient to slot (receptionist only) |
| DELETE | `/api/appointments/{id}/` | Delete appointment (admin only) |

### Billing
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/billing/` | List all invoices |
| POST | `/api/billing/` | Create a new invoice |
| PATCH | `/api/billing/{id}/` | Update invoice |
| POST | `/api/billing/items/` | Add item to invoice |

### Medical Records
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/medical_records/` | List all medical records |
| POST | `/api/medical_records/` | Create a new medical record |
| POST | `/api/medical_records/doctor-notes/` | Add doctor note |
| POST | `/api/medical_records/nurse-notes/` | Add nurse note |
| POST | `/api/medical_records/lab-results/` | Add lab result |

---

## Filtering & Search

### Patients
```
GET /api/patients/?search=ahmed
GET /api/patients/?blood_type=A+
GET /api/patients/?ordering=user__first_name
```

### Appointments
```
GET /api/appointments/?date_from=2026-01-01&date_to=2026-12-31
GET /api/appointments/?status=confirmed
GET /api/appointments/?is_available=true
```

### Billing
```
GET /api/billing/?status=unpaid
GET /api/billing/?date_from=2026-01-01&date_to=2026-12-31
GET /api/billing/?min_total=100&max_total=500
```

---

## Authentication

All endpoints except `register` and `login` require a JWT access token.

Include the token in the request header:
```
Authorization: Bearer your_access_token_here
```

Token lifespans:
- Access token: 15 minutes
- Refresh token: 1 day

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode (True/False) |
| `DATABASE_NAME` | PostgreSQL database name |
| `DATABASE_USER` | PostgreSQL username |
| `DATABASE_PASSWORD` | PostgreSQL password |
| `DATABASE_HOST` | PostgreSQL host |
| `DATABASE_PORT` | PostgreSQL port |
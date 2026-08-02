# TenantFlow

TenantFlow is a cloud-native, multi-tenant SaaS application built with Django. It empowers organizations to securely manage their employees, projects, tasks, and documents within a single, unified platform while ensuring strict data isolation between tenants.

## Features

- **Multi-Tenancy:** Secure data isolation using an organization-based architecture.
- **Role-Based Access Control:** Distinct roles and permissions for administrators, project managers, and employees.
- **Project & Task Management:** Create projects, assign tasks, manage task hierarchies (subtasks), and track statuses.
- **Document Storage:** Centralized document upload and management per organization.
- **Notifications:** Real-time in-app notifications and activity feeds.

## Tech Stack

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Frontend:** HTML5, Vanilla CSS, JavaScript
- **Infrastructure:** Docker, Docker Compose, AWS EC2
- **Static File Serving:** Whitenoise, Gunicorn

## Project Structure

- `apps/` - Core Django applications.
  - `accounts/` - Authentication flows (login, register).
  - `core/` - Shared utilities, base models, and common functionality.
  - `documents/` - Secure file upload and management.
  - `notifications/` - Activity tracking and system alerts.
  - `organizations/` - Multi-tenant isolation logic and tenant management.
  - `projects/` & `tasks/` - Core productivity and workflow features.
  - `users/` - User profile and employee management.
- `tenant_flow/` - Django project configuration, settings, and root URL routing.
- `static/` & `templates/` - Shared UI assets, CSS, JavaScript, and HTML layouts.

## Local Development Setup

The easiest way to run TenantFlow locally is using Docker.

**Prerequisites:** 
- Docker and Docker Compose installed on your machine.

1. **Clone the repository**
   ```bash
   git clone https://github.com/yashreddy1154/Tenant-Flow.git
   cd Tenant-Flow
   ```

2. **Boot the environment**
   ```bash
   docker-compose up --build
   ```
   *Note: This command automatically spins up the PostgreSQL database, applies all necessary Django migrations, collects static files, and boots the server.*

3. **Access the Application**
   Open your browser and navigate to `http://localhost:8000`.

## Production Deployment

TenantFlow is configured out-of-the-box for containerized deployment on Linux environments (e.g., AWS EC2). 

Production-ready configurations include:
- **Gunicorn** WSGI server integration.
- **Whitenoise** middleware for optimized static file serving without requiring NGINX.
- **Secure Environment Variables** for database credentials, secret keys, and debug toggles.

## Team

- Yash
- Dheeraj
- Nithin
- Bharath
# 🚧 TenantFlow (Under Construction)

> **Project Status:** 🚧 Under Development

TenantFlow is a cloud-native multi-tenant SaaS application built using **Django**. The platform allows multiple organizations to securely manage their employees, projects, tasks, and documents within a single application while keeping each organization's data isolated.

The goal of this project is to build a production-style application using modern development practices and technologies such as Django, PostgreSQL, Docker, and AWS.

---

# 🛠️ Tech Stack

- Python
- Django
- HTML
- CSS
- JavaScript
- PostgreSQL *(planned)*
- Docker *(planned)*
- AWS *(planned)*

---

# 📁 Project Structure

```
tenant_flow/
│
├── apps/
│   ├── accounts/
│   ├── core/
│   ├── documents/
│   ├── notifications/
│   ├── organizations/
│   ├── projects/
│   ├── tasks/
│   └── users/
│
├── requirements/
│
├── static/
├── templates/
├── media/
│
├── tenent_flow/
│
└── manage.py
```

---

# 📌 Folder Overview

### `apps/`
Contains all Django applications. Each app is responsible for one feature of the project.

- **accounts** → Authentication (Login, Register, Logout)
- **core** → Shared utilities, base classes, and common functionality
- **documents** → Document upload and management
- **notifications** → Email and in-app notifications
- **organizations** → Organization and tenant management
- **projects** → Project management
- **tasks** → Task management
- **users** → User profiles and employee information

---

### `templates/`

Stores shared HTML templates like `base.html`, common components, and error pages.

Each app also contains its own templates inside:

```
apps/<app_name>/templates/<app_name>/
```

This keeps every app independent and reusable.

---

### `static/`

Stores shared static files.

Each app can also have its own static files inside:

```
apps/<app_name>/static/<app_name>/
```

---

### `media/`

Stores uploaded files during development.

---

### `requirements/`

Contains project dependencies.

---

### `tenent_flow/`

Project configuration.

Contains:

- settings.py
- urls.py
- asgi.py
- wsgi.py

---

# 📖 Development Notes

- Each feature is developed inside its own Django app.
- Every app has its own `urls.py`.
- Templates and static files are organized per app for better maintainability.
- The project is being developed in a modular and scalable way.

---

# 👥 Team

- Yash
- Dheeraj
- Nithin
- Bharath
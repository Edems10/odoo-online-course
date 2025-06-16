# Online Course Odoo Module

A course management system built as an Odoo module. This module enables teachers to create and manage courses while allowing students to enroll and track their learning progress.

## Table of Contents

- [Project Structure](#📁project-structure)
- [How It Works](#how-it-works)
    - [Core Features](#core-features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
    - [1. Start the Project](#1-start-the-project)
    - [2. Access Odoo](#2-access-odoo)
    - [3. Create Database](#3-create-database)
    - [4. Install the Module](#4-install-the-module)
- [Using the Module](#using-the-module)
    - [Teacher Perspective](#teacher-perspective)
    - [Student Perspective](#student-perspective)
    - [Course States Explained](#course-states-explained)
- [Running Tests](#running-tests)
- [Troubleshooting](#troubleshooting)


## 📁Project Structure

```
online_course/
├── __manifest__.py
├── models/
│   ├── course.py                    # Course model
│   └── res_users.py                 # Extended user model for course functionality
├── services/
│   ├── course_services.py           # Business logic services (Security, Enrollment, State)
│   ├── user_services.py             # User-course relationship services
│   └── notification_factory.py      # User-friendly notification factory
├── validators/
│   └── course_validators.py         # Enrollment and price validation logic
├── static/
│   └── constants.py                 # Application constants and configuration
├── views/
│   ├── course_views.xml             # Course form, list, and kanban views
│   ├── res_users_views.xml          # User extensions with course smart buttons
│   └── menus.xml                    # Application menu structure
├── security/
│   ├── groups.xml                   # Teacher and student security groups
│   ├── record_rules.xml             # Data access rules per role
│   └── ir.model.access.csv          # Model access permissions
├── demo/
│   ├── users_demo.xml               # Demo teacher and student accounts
│   └── course_demo.xml              # Sample course data
└── tests/
    └── test_course.py               # Simple tests for basic functionality
```


## How It Works

This module extends Odoo's user management system to add course functionality:

### Core Features

- **Course Management**: Teachers can create, publish, manage and join courses  
- **Student Enrollment**: Self-enrollment system with validation
- **Role-Based Access**: Separate permissions for teachers, students, and administrators
- **Course Lifecycle**: Draft → Published → Closed → Archived states
- **Price Management**: Support for both free and paid courses
- **Smart Notifications**: Context-aware user feedback


## Prerequisites

- **Docker**: Container platform for running Odoo
- **Docker Compose**: Orchestration tool for multi-container applications


## Getting Started

### 1. Start the Project

```bash
docker-compose up -d
```


### 2. Access Odoo

Open your browser and navigate to: **http://localhost:8069/**

### 3. Create Database

1. Create a new database (or import an existing one)
2. **Important**: When creating the database, **tick the box "Load demonstration data"** for easier testing
3. Wait for the database creation to complete

### 4. Install the Module

1. Log in as the admin user
2. Go to **Settings** → **Activate Developer Mode**
3. Navigate to **Apps**
4. Filter by **Education** category
5. Find and install the **Online Courses** module

## Using the Module

### Teacher Perspective

Log out from admin and log in as a teacher:

- **Email**: `demo_sarah@example.com`
- **Password**: `demo123`

**Teacher Capabilities:**

- ✅ Create new courses
- ✅ Manage course details (name, description, price)
- ✅ Set courses as free or paid
- ✅ Control course states (draft/published/closed/archived)
- ✅ View and manage enrolled students
- ✅ Remove students from courses
- ✅ Access teaching analytics via smart buttons


### Student Perspective

Log in as a student:

- **Email**: `demo_alex@student.com`
- **Password**: `student123`

**Student Capabilities:**

- ✅ Browse and enroll in published courses
- ✅ View enrolled courses via smart buttons
- ✅ Unenroll from courses
- ✅ Access course materials and details
- ✅ Track learning progress


### Course States Explained

| State | Description | Teacher Actions | Student Actions |
| :-- | :-- | :-- | :-- |
| **Draft** | Course being prepared | Edit, Publish | None |
| **Published** | Open for enrollment | Manage, Close | Enroll, View |
| **Closed** | No new enrollments | Reopen, Archive | View only |
| **Archived** | Course ended | View only | View only |

## Running Tests

Execute the test suite with the following command:

```bash
docker-compose run --rm odoo odoo -c /etc/odoo/odoo.conf -d test_db --test-tags /online_course --stop-after-init -i online_course
```

This command will:

- Create a test database
- Install the module
- Run all module tests
- Stop the server after completion


## Troubleshooting

**Module not appearing in Apps?**

- Ensure developer mode is activated
- Update the app list
- Check the Education category filter

**Permission errors?**

- Verify user has correct group assignments
- Check if demo data was loaded
- Ensure proper user login

---

**Built with**: Odoo 18, Python 3.11+, PostgreSQL
**Maintainer**: Adam Mitrenga

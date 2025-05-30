 Project & Task Management API with Authentication

A modern and secure RESTful API for managing **Projects**, **Tasks**, and **Users** using **Flask**, **MySQL**, and **JWT**.
Includes role-based permissions (admin vs regular user) and powerful filtering options.

---

🚀 Features

🔐 Authentication & Authorization

* ✅ **User Registration & Login** with `is_admin` flag.
* 🔑 **JWT Token-based Security**
* 🔄 **Refresh Token Support**
* ❌ **Logout & Token Revocation**

👤 User Management

* Register as regular user or admin
* Only **admins** can:

  * Create/update/delete projects
  * Assign tasks

📁 Project Management

* Create, read, update, delete (CRUD) for projects
* Only **admins** can create or delete
* Regular users can **view projects** only if they are assigned to related tasks

📌 Task Management

* Create, assign, update, delete tasks
* **Project creators** can:

  * Create/edit/delete tasks
  * Edit delivery date
* **Assigned users** can only:

  * Update task status
* Filter tasks by:

  * `status`
  * `due_date`
  * `assigned_to`
  * `project_id`
* Search tasks by:

  * `title`
  * `description`
📧 Notifications

* Welcome email sent on login

---

## ⚙️ Tech Stack

* **Backend**: Python, Flask
* **Database**: MySQL
* **Authentication**: JWT (Access + Refresh Tokens)
* **Mail**: SMTP (Mailtrap or similar)
* **Tools**: Postman for API testing

---

🧲 API Overview

| Module   | Method | Endpoint             | Description                            |
| -------- | ------ | -------------------- | -------------------------------------- |
| Auth     | POST   | `/api/register`      | Register user (accepts `is_admin`)     |
| Auth     | POST   | `/api/login`         | Login and receive JWT tokens           |
| Auth     | POST   | `/api/logout`        | Logout and revoke token                |
| Projects | GET    | `/api/projects`      | List all accessible projects           |
| Projects | POST   | `/api/projects`      | Create a project (admin only)          |
| Projects | GET    | `/api/projects/<id>` | Get specific project by ID             |
| Projects | PUT    | `/api/projects/<id>` | Update a project (admin only)          |
| Projects | DELETE | `/api/projects/<id>` | Delete a project (admin only)          |
| Tasks    | GET    | `/api/tasks`         | List tasks (with filters)              |
| Tasks    | POST   | `/api/tasks`         | Create a task (project creator only)   |
| Tasks    | GET    | `/api/tasks/<id>`    | Get task by ID                         |
| Tasks    | PUT    | `/api/tasks/<id>`    | Update task (creator or assigned user) |
| Tasks    | DELETE | `/api/tasks/<id>`    | Delete task (creator only)             |

---
📦 Installation

1. Clone the repo

```bash
git clone https://github.com/Mahmoudyounes011/PythonTaskFirst.git
cd PythonTaskFirst
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
# OR
venv\Scripts\activate         # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```



Use the following **Postman collection naming conventions**:

🔑 Auth

* `POST /register` → `Register User`
* `POST /login` → `Login User`
* `POST /logout` → `Logout User`

📁 Projects

* `GET /projects` → `Get All Projects`
* `POST /projects` → `Create Project`
* `GET /projects/:id` → `Get Project by ID`
* `PUT /projects/:id` → `Update Project`
* `DELETE /projects/:id` → `Delete Project`
📌 Tasks

* `GET /tasks` → `Get Tasks (with filters)`
* `POST /tasks` → `Create Task`
* `GET /tasks/:id` → `Get Task by ID`
* `PUT /tasks/:id` → `Update Task`
* `DELETE /tasks/:id` → `Delete Task`

---



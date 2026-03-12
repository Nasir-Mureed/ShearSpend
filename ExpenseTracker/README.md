# Expense Tracker (Django)

A simple and efficient **Expense Tracking Web Application** built with **Django**.
This application allows users to manage their daily expenses, track spending, and organize expenses by partners.

---

##  Features

* User-based expense management
* Add, edit, and delete expenses
* Partner-based expense tracking
* Real-time form validation
* Change detection before saving edits
* Warning for unsaved changes
* Clean and responsive UI
* Secure Django authentication support

---

##  Tech Stack

**Backend**

* Python
* Django

**Frontend**

* HTML
* CSS
* Tailwind 
* JavaScript

**Database**

* SQLite (default Django database)

---

## 📂 Project Structure

```
ExpenseTracker/
│
├── ExpenseTracker/      # Main Django project
│
├── Expenses/            # Expense management app
│
├── Partners/            # Partner management app
│
├── Dashboard/           # Dashboard app
│
├── templates/           # Shared templates
│
├── manage.py
│
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/Nasir-Mureed/ShearSpend.git

```

### 2️⃣ Create virtual environment

```
python -m venv venv
```

### 3️⃣ Activate virtual environment

Linux / Mac

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

### 4️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 5️⃣ Apply migrations

```
python manage.py migrate
```

### 6️⃣ Create superuser

```
python manage.py createsuperuser
```

### 7️⃣ Run development server

```
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000
```

---

## 📊 Application Workflow

1. User logs into the system
2. User adds partners
3. User records expenses
4. Expenses are stored with:

   * Description
   * Amount
   * Partner
   * Date
5. Dashboard displays all recorded expenses

---

## 🔐 Security Features

* CSRF protection
* Django authentication system
* Input validation
* Form validation using JavaScript

---

## 👨‍💻 Author

**Muhammad Nasir**
BS Software Engineering Student

---

## 📜 License

This project is open source and available under the **MIT License**.

# 🏋️ IronFit Gym Management System (FastAPI)

## 📌 Project Overview

This project is a **Gym Management System API** built using **FastAPI**.
It provides endpoints to manage gym members, plans, memberships, attendance, class bookings, and advanced operations like filtering, sorting, searching, and pagination.

---

## 🚀 Features

### 🔹 Core Functionalities

* Manage gym members
* Create and manage membership plans
* Enroll members into plans
* Track attendance (check-in / check-out)
* Class booking system
* Freeze and reactivate memberships

---

### 🔹 Advanced Functionalities

* 🔍 Search (plans & memberships)
* 🔃 Sorting (price, name, duration, etc.)
* 📄 Pagination (plans & memberships)
* 🎯 Combined filtering + sorting + pagination (browse API)
* ❌ Error handling (invalid inputs, duplicates, etc.)

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Language:** Python
* **Server:** Uvicorn
* **API Docs:** Swagger UI (FastAPI built-in)

---

## 📂 Project Structure

```
project/
│
├── main.py             # Main FastAPI application
├── requirements.txt    # Dependencies
└── README.md           # Project documentation
|__Screenshots          
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone <your-repo-link>
cd project
```

### 2️⃣ Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run the server

```
python -m uvicorn main:app --reload
```

---

## 🌐 API Access

Open in browser:

```
http://127.0.0.1:8000/docs
```

👉 Interactive Swagger UI available

---

## 📊 API Endpoints

### 🏠 Home

* `GET /` → Welcome message

### 👥 Members

* `GET /members`
* `GET /members/{id}`
* `POST /members`

### 🧾 Memberships

* `POST /memberships`
* `GET /memberships/search`
* `GET /memberships/sort`
* `GET /memberships/page`
* `PUT /memberships/{id}/freeze`
* `PUT /memberships/{id}/reactivate`

### 📦 Plans

* `POST /plans`
* `PUT /plans/{id}`
* `DELETE /plans/{id}`
* `GET /plans/filter`
* `GET /plans/search`
* `GET /plans/sort`
* `GET /plans/page`
* `GET /plans/browse`

### 🏃 Attendance

* `POST /attendance/checkin`
* `POST /attendance/checkout`
* `GET /attendance`

### 🧘 Classes

* `POST /classes/book`
* `GET /classes/bookings`
* `DELETE /classes/cancel/{id}`

---

## ⚠️ Error Handling

* Duplicate plan → Error message
* Invalid plan_id → "Plan not found"
* Booking without membership → Error
* Deleting active plan → Blocked

---

## 📸 Screenshots

All API outputs are tested in Swagger UI and stored in the screenshots/ folder.

---

## 🎯 Learning Outcomes

* FastAPI fundamentals
* REST API design
* Data validation using Pydantic
* CRUD operations
* Filtering, sorting, pagination
* Real-world backend system design

---

## ✅ Conclusion

This project demonstrates a **complete backend system** for gym management using FastAPI with advanced features and clean API design.

---

## 👨‍💻 Author

Name: Narayanapuram.Akash                                                    
Project: FastAPI Application                                                                       
Internship: GenAI Internship                                                           
Guidance under @Innomatics Research Lab                                       

<div align="center">

# RideRentals 🚗
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/crackspy/RideRentals?color=black&label=Stable&logo=github)](https://github.com/crackspy/RideRentals/releases/latest/)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/crackspy/RideRentals?include_prereleases&label=Preview&logo=Github)](https://github.com/crackspy/RideRentals/releases/)

A full-stack car rental marketplace built with Django. RideRentals allows users to seamlessly browse and book vehicles, while providing a comprehensive dashboard for administrators to manage the platform.



## 🛠️ Made With
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

</div>

### 📸 Screenshots

| **Home** | **Explore Cars** |
| :---: | :---: |
| ![Home page Screenshot](https://raw.githubusercontent.com/crackspy/RideRentals/doc/screenshots/home_page.png) | ![Explore Cars Screenshot](https://raw.githubusercontent.com/crackspy/RideRentals/doc/screenshots/explore_cars.png) |
| **Login** | **Booking** |
| ![Login Page Screenshot](https://raw.githubusercontent.com/crackspy/RideRentals/doc/screenshots/login_page.png) | ![Booking Page Screenshot](https://raw.githubusercontent.com/crackspy/RideRentals/doc/screenshots/booking_page.png) |


---

## ✨ Key Features

| Feature | User | Admin |
| :--- | :---: | :---: |
| **Browse & Search Cars** | ✅ | N/A |
| **Date-Based Booking** | ✅ | N/A |
| **Email Confirmations** | ✅ | N/A |
| **Multiple Payment Options** | ✅ | N/A |
| **Full Car Management** | N/A | ✅ |
| **Booking & User Dashboard** | N/A | ✅ |
| **New Booking Notifications** | N/A | ✅ |

---

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | Python, Django |
| **Database** | PostgreSQL, SQLite3 |
| **Frontend** | HTML, CSS, JavaScript |
| **Hosting** | *(e.g., Heroku, AWS, DigitalOcean)* |

---

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites

* Python 3.13.3
* Git

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/crackspy/RideRentals.git
    cd RideRentals
    ```

2.  **Navigate to Project Directory**
    ```bash
    # The main project is nested. Navigate to the correct directory.
    cd code/RideRentals
    ```

3.  **Create and Activate Virtual Environment**
    ```bash
    python -m venv venv
    # On Windows: venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    ```

4.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set Up Environment Variables**
    Create a `.env` file in the `code/RideRentals` directory and add your credentials:
    ```env
    DEBUG=True
    EMAIL_HOST_USER=your-email@gmail.com
    EMAIL_HOST_PASSWORD=your-google-app-password
    ```
    *Note: For `EMAIL_HOST_PASSWORD`, it's recommended to use a Google App Password, not your regular account password.*

6.  **Run Database Migrations**
    ```bash
    python manage.py migrate
    ```

It has some data in db (car images, etc).
Default admin user:
```
username : admin
password : 123456
```

7.  **Create a Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

8.  **Run the Server**
    ```bash
    python manage.py runserver
    ```
    The application will be available at [`http://127.0.0.1:8000`](http://127.0.0.1:8000)

---

## 🗺️ Todo

-   [ ] Implement a user review and rating system.
-   [ ] Generate and email PDF booking receipts.
-   [ ] Add real-time notifications for users and admins.
-   [ ] Integrate a map view to see car locations.

---

## 📜 License

This project is distributed under the **MIT License**. See `LICENSE` for more information.

---

## 👤 Contact

Project Link: [https://github.com/crackspy/RideRentals](https://github.com/crackspy/RideRentals)
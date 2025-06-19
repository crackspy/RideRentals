# 🎉 RideRentals

**RideRentals** WebApp is global online marketplace that facilitates the renting of a wide range of vehicles built with **Django**.It allows users to browse, book cars seamlessly while providing an intuitive admin dashboard for rental cars.

## 🌟 Key Features

### 🖥️ User Side
- 🔍 Browse and search rental cars.
- 📅 Book cars with custom pickup date and return date.
- 💰 Choose payment method: **UPI/QR code** or **Cash on Event Day**.
- 📩 Receive email notifications for booking confirmations.

### ⚙️ Admin Side
- 🎛️ Manages car details, bookings, and users management via Django Admin.
- 📬 Get notified when a booking request is submitted.
- 📊 View booking details, user information, and payment status.

## 🛠️ Installation

Follow these steps to set up the project locally:

1. **Clone the Repository:**
```bash
git clone https://github.com/crackspy/RideRentals.git
cd RideRentals
```

2. **Create a Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd code/main/Ride_Rentals
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables:**
Create a `.env` file in code/main/RideRentals:
```
DEBUG=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

1. **Apply Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

1. **Create Superuser (Admin Account):**
```bash
python manage.py createsuperuser
```

1. **Run the Development Server:**
```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)


## 📦 Project Structure
```
├── Ride_Rentals     # Main project directory
├── mainapp          # Core app handling ride bookings and rentals
├── templates        # Frontend templates
├── static           # CSS, JS, images
├── media           # Uploaded ride images and documents
├── db.sqlite3       # Database for storing user and booking data
├── manage.py        # Django management script
└── requirements.txt # Project dependencies
```

## 🚀 Future Enhancements
- 📱 Add review and ratings option.
- 📜 Generate booking receipts.
- 🔔 Real-time notifications for admin and users.

## 🙌 Credits
- **Django** - Backend Framework
- **Postgresql or sqlite** - Backend Database
- **Html, css, javascript** - Frontend Styling


## 📜 License
This project is licensed under the **MIT License**. Feel free to use and modify it.

## 📞 Contact
For any queries or suggestions, contact:
- 🌐 Project GitHub: [https://github.com/crackspy/RideRentals](https://github.com/crackspy/RideRentals)
---

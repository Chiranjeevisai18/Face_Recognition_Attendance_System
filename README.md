# 🎥 Face Recognition Attendance System

A real-time face recognition attendance web app using **OpenCV**, **Streamlit**, and **face_recognition**.  
It supports live face detection, secure admin login, individual registration, multi-person detection, analytics, and CSV-based attendance tracking.

---

## 🚀 Features

- ✅ **Face Registration**
  - Register via webcam or upload image
  - Saves face data automatically

- ✅ **Live Face Attendance**
  - Real-time webcam attendance using OpenCV
  - Detects and marks multiple users
  - No duplicate attendance per day

- ✅ **Admin Dashboard (Sidebar)**
  - 🔐 Secure login system
  - 🧹 Reset today’s or all attendance data
  - 📥 Download attendance as CSV
  - 🚪 Logout functionality

- ✅ **Analytics Dashboard**
  - 📊 Per-user attendance stats (bar chart)
  - 📆 Daily attendance trend (line graph)

- ✅ **User Logs**
  - 📂 Per-user attendance history view


## 📁 Folder Structure
```
attendance_project/
├── app.py # Main application
├── Face_data/ # Stores registered face images
├── attendance.csv # CSV file for attendance logs
├── requirements.txt # Dependencies
└── screenshots/ # (Optional) for README visuals
```
---

## 📦 Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/face-attendance-app.git
cd face-attendance-app
```

### 2️⃣ Create and Activate Virtual Environment (Optional)
```bash

python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```
### 3️⃣ Install Required Packages
```bash

pip install -r requirements.txt
```
If requirements.txt is not available, manually install:

```bash
pip install streamlit opencv-python face_recognition numpy pandas matplotlib pillow
```
### ▶️ Run the App
```bash
streamlit run app.py
```
Open the link provided in the terminal to use the app in your browser.

## 🔐 Admin Panel
- Default password: admin123

- Login from sidebar to:

  - Clear today’s attendance

  - Reset all data

  - Download full CSV

  - Logout securely

- To change the password, edit:

```bash
ADMIN_PASSWORD = "admin123"
```
## 🌐 Deploy on Streamlit Cloud (Free Hosting)
- Push your project to GitHub

- Go to streamlit.io/cloud

- Click “New App”, connect to your GitHub repo, select app.py

  Your app is now live!

## 📚 Tech Stack
- Tool	Usage
- Streamlit	Web interface and dashboard
- OpenCV	Camera capture & face cropping
- face_recognition	Facial recognition & encoding
- Pandas	Attendance data management
- Matplotlib	Graph plotting for analytics
- Pillow	Image handling for uploads

## 📬 Future Enhancements
- SQLite or MongoDB backend support

- Mobile camera compatibility

- Email summary reports to admins

- UI improvements (themes, logos, animations)

## 🧾 Sample Attendance CSV Format
```csv
Name,Timestamp
john,2024-06-19 09:30:00
jane,2024-06-19 09:31:00
```
## 📄 License
- MIT License — you are free to use, modify, and distribute this software.

## 👨‍💻 Author
- Chiranjeevi Sai Moka
- 💼 GitHub - Chiranjeevisai18
- 📬 chiranjeevimoka@email.com


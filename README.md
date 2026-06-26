# 📧 Task 5 — Automated Bulk Email Sender with Templates

A Python CLI-based bulk email sending system built for **HK Academy Internship Task 5**. This project simulates real-world email marketing and notification systems using Gmail SMTP.

---

## 🎯 Objective

To develop a Python-based system that sends bulk emails automatically using reusable templates, personalized for each recipient.

---

## ⚙️ Features

- ✅ Send single emails via Gmail SMTP
- ✅ Load contacts from CSV file
- ✅ Bulk email sending to multiple recipients
- ✅ 3 pre-built email templates (Welcome, Reminder, Thank You)
- ✅ Personalized emails using `{name}` and `{company}` placeholders
- ✅ Email validation before sending
- ✅ Retry mechanism for failed emails
- ✅ Sent email history saved in JSON format
- ✅ Simple CLI menu system

---

## 📁 Project Structure

```
bulk email sender/
├── main.py          # Main application file
├── contacts.csv     # Recipient contact list
├── history.json     # Auto-generated sent email history
└── README.md        # Project documentation
```

---

## 🚀 How to Run

### Step 1 — Clone the Repository
```bash
git clone https://github.com/yourusername/HK-Task5-Automated-Bulk-Email-Sender.git
cd "bulk email sender"
```

### Step 2 — Setup Gmail App Password
1. Go to **Google Account → Security → 2-Step Verification → App Passwords**
2. Create a new App Password
3. Copy the 16-digit password

### Step 3 — Update Credentials in main.py
Open `main.py` and update lines 7-8:
```python
SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD  = "your16digitpassword"
```

### Step 4 — Run the Application
```bash
python main.py
```

---

## 📋 Menu Options

```
[1] Send Email          → Send a single email manually
[2] Load Contacts & Bulk Send → Send to all contacts in CSV
[3] Choose Template     → Pick and use a pre-built template
[4] View History        → See all sent/failed email logs
[5] Exit
```

---

## 📄 contacts.csv Format

```csv
name,email,company
Ali Khan,ali@example.com,HK Academy
Sara Malik,sara@example.com,HK Academy
```

---

## 📬 Email Templates

| # | Template | Subject |
|---|----------|---------|
| 1 | Welcome | Welcome to HK Academy! |
| 2 | Reminder | Reminder: Upcoming Session |
| 3 | Thank You | Thank You from HK Academy |

---

## 🔒 Security Note

- Uses **Gmail App Password** (not your actual Gmail password)
- Enable **2-Step Verification** on Gmail before generating App Password
- Never share your App Password publicly

---

## 🛠️ Built With

- Python 3
- smtplib (built-in)
- csv (built-in)
- json (built-in)
- re (built-in)
- datetime (built-in)

> No external libraries required!
> click here for demo video
> https://drive.google.com/file/d/1qAH-kRC9wfUbe3lB2_EvltokstqYIiil/view?usp=drive_link

---

## 👩‍💻 Developed By

**Areesha Fatima**
HK Academy Python Developer Internship — Task 5

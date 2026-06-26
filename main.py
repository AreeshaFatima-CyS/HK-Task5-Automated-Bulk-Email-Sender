import smtplib
import json
import csv
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
# ---- config ----
SENDER_EMAIL = "areeshahere03@gmail.com"   
APP_PASSWORD  = "gdjh mvoq omie pqvc"   
HISTORY_FILE  = "history.json"
CONTACTS_FILE = "contacts.csv"
# ---- email templates ----
templates = {
    "1": {
        "name": "Welcome",
        "subject": "Welcome to HK Academy!",
        "body": "Hello {name},\n\nWelcome to {company}! We are glad to have you on board.\n\nBest regards,\nHK Academy Team"
    },
    "2": {
        "name": "Reminder",
        "subject": "Reminder: Upcoming Session",
        "body": "Hello {name},\n\nThis is a reminder about your upcoming session at {company}.\n\nPlease be on time!\n\nBest regards,\nHK Academy Team"
    },
    "3": {
        "name": "Thank You",
        "subject": "Thank You from HK Academy",
        "body": "Hello {name},\n\nThank you for being part of {company}. We appreciate your support!\n\nBest regards,\nHK Academy Team"
    }
}
 
# ---- helper: validate email format ----
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email.strip().lower()) is not None
 
# ---- load history from json ----
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []
 
# ---- save one record to history ----
def save_to_history(email, subject, status):
    history = load_history()
    record = {
        "email": email,
        "subject": subject,
        "status": status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    history.append(record)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
 
# ---- actually send one email via smtp ----
def send_single_email(to_email, subject, body, retries=2):
    to_email = to_email.strip().lower()
 
    if not is_valid_email(to_email):
        print(f"  [!] Skipping invalid email: {to_email}")
        save_to_history(to_email, subject, "Failed - Invalid Email")
        return
 
    attempt = 0
    while attempt <= retries:
        try:
            msg = MIMEMultipart()
            msg["From"]    = SENDER_EMAIL
            msg["To"]      = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
 
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
 
            print(f"  [+] Sent to {to_email}")
            save_to_history(to_email, subject, "Sent")
            return
 
        except smtplib.SMTPAuthenticationError:
            print("  [!] Auth failed — check your email/app password in config.")
            save_to_history(to_email, subject, "Failed - Auth Error")
            return
 
        except smtplib.SMTPConnectError:
            print("  [!] Connection error — check your internet.")
            save_to_history(to_email, subject, "Failed - Connection Error")
            return
 
        except Exception as e:
            attempt += 1
            if attempt > retries:
                print(f"  [!] Failed after {retries+1} tries: {e}")
                save_to_history(to_email, subject, f"Failed - {str(e)}")
            else:
                print(f"  [~] Retrying ({attempt}/{retries})...")
 
 
# ---- menu 1: send email manually ----
def menu_send_email():
    print("\n--- Send Email ---")
    to_email = input("Recipient email: ").strip()
    subject  = input("Subject: ").strip()
    body     = input("Message body: ").strip()
 
    if not subject or not body:
        print("[!] Subject and body cannot be empty.")
        return
 
    send_single_email(to_email, subject, body)
 
 
# ---- menu 2: load contacts from csv ----
def menu_load_contacts():
    print("\n--- Load Contacts from CSV ---")
 
    if not os.path.exists(CONTACTS_FILE):
        print(f"[!] '{CONTACTS_FILE}' not found. Creating a sample file...")
        # create sample contacts.csv so user has example
        sample = [
            ["name", "email", "company"],
            ["Ali Khan", "ali@example.com", "HK Academy"],
            ["Sara Malik", "sara@example.com", "HK Academy"],
        ]
        with open(CONTACTS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(sample)
        print(f"[+] Sample '{CONTACTS_FILE}' created. Fill it with real contacts and try again.")
        return
 
    contacts = []
    with open(CONTACTS_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            contacts.append(row)
 
    if not contacts:
        print("[!] CSV file is empty.")
        return
 
    print(f"\n[+] {len(contacts)} contact(s) loaded:")
    for c in contacts:
        print(f"    - {c.get('name', 'N/A')} | {c.get('email', 'N/A')} | {c.get('company', 'N/A')}")
 
    choice = input("\nSend email to all contacts? (y/n): ").strip().lower()
    if choice != "y":
        return
 
    # pick a template
    template = menu_choose_template(return_template=True)
    if not template:
        return
 
    print("\n[~] Sending emails...")
    for contact in contacts:
        name    = contact.get("name", "User")
        email   = contact.get("email", "")
        company = contact.get("company", "HK Academy")
 
        # replace placeholders
        body    = template["body"].replace("{name}", name).replace("{company}", company)
        subject = template["subject"]
 
        send_single_email(email, subject, body)
 
    print("\n[+] Bulk sending done!")
 
 
# ---- menu 3: choose template ----
def menu_choose_template(return_template=False):
    print("\n--- Email Templates ---")
    for key, t in templates.items():
        print(f"  {key}. {t['name']} — {t['subject']}")
 
    choice = input("\nChoose template number: ").strip()
 
    if choice not in templates:
        print("[!] Invalid choice.")
        return None
 
    selected = templates[choice]
    print(f"\n[+] Template selected: {selected['name']}")
    print(f"    Subject : {selected['subject']}")
    print(f"    Body    :\n{selected['body']}")
 
    if return_template:
        return selected
 
    # if called from menu directly, ask to send manually
    use_it = input("\nSend this template to someone? (y/n): ").strip().lower()
    if use_it == "y":
        to_email = input("Recipient email: ").strip()
        name     = input("Recipient name: ").strip()
        company  = input("Company name: ").strip() or "HK Academy"
 
        body = selected["body"].replace("{name}", name).replace("{company}", company)
        send_single_email(to_email, selected["subject"], body)
 
 
# ---- menu 4: view history ----
def menu_view_history():
    print("\n--- Sent Email History ---")
    history = load_history()
 
    if not history:
        print("[!] No history found yet.")
        return
 
    print(f"{'#':<4} {'Email':<30} {'Subject':<30} {'Status':<20} {'Time'}")
    print("-" * 100)
    for i, record in enumerate(history, 1):
        print(f"{i:<4} {record['email']:<30} {record['subject']:<30} {record['status']:<20} {record['timestamp']}")
 
 
# ---- main menu loop ----
def main():
    print("=" * 45)
    print("   Automated Bulk Email Sender — HK Academy")
    print("=" * 45)
 
    while True:
        print("\n[1] Send Email")
        print("[2] Load Contacts & Bulk Send")
        print("[3] Choose Template")
        print("[4] View History")
        print("[5] Exit")
 
        choice = input("\nEnter choice: ").strip()
 
        if choice == "1":
            menu_send_email()
        elif choice == "2":
            menu_load_contacts()
        elif choice == "3":
            menu_choose_template()
        elif choice == "4":
            menu_view_history()
        elif choice == "5":
            print("\n[+] Goodbye!")
            break
        else:
            print("[!] Invalid option. Try again.")
 
 
if __name__ == "__main__":
    main()
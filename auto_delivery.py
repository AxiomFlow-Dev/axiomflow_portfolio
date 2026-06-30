import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv #Added this import

# 📁 Calculate paths relative to this script (root folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "config", ".env")
ATTACHEMENT_PATH = os.path.join(BASE_DIR, "outputs", "multi_page_quotes.xlsx")

# 🔐Load the environment variables from the specific config folder
load_dotenv(ENV_PATH)

#Grab credentials
EMAIL_SENDER = os.getenv("EMAIL_USER")
EMAIL_PASSWAORD = os.getenv("EMAIL_PASS")

print("✉️ Preparing the secure automated email delivery system...")

#1. Setup the connection configurations
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "axiomflow.engine@gmail.com"
receiver_email = "selvanexgamer@gmail.com"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] =receiver_email
message["Subject"] = "Automated Weekly Scraped Data Delievery"

body = """
Hello,

This is an automated delievry of your weekly requested data extraction asset.
The live scraper has finished executing, compiled the raw records, and applied your branded corporate styling rules.

Please find the attached spreadsheet containing the latest extracted data rows.

Best regards
Your Automated Python engine 🤖
"""
message.attach(MIMEText(body, "plain"))

file_name = "multi_page_quotes.xlsx"

if os.path.exists(ATTACHEMENT_PATH):
    with open(ATTACHEMENT_PATH, "rb") as attachement:
        part =  MIMEBase("application", "octet-stream")
        part.set_payload(attachement.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {os.path.basename(ATTACHEMENT_PATH)} ",
    )
    message.attach(part)
    print("📎 Spreadsheet file successfully mapped and attached to message package.")
else:
    print("❌ Error: The excel file could not be located on disk.")

print("🏁 System engine prepared. Waiting for server validation link...")

# 2. Establish connection and send the email
try:
    print("🚀 Connecting to secure server...")
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Upgrade connection to secure TLS encryption
    
    # Log in using your business email and your 16-character App Password
    server.login("axiomflow.engine@gmail.com", "tkqyuxauzyepbiwd")
    
    print("🔒 Server authenticated successfully. Transmitting payload...")
    
    # Send the package
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("🚀 Success! The automated shipment has been delivered.")

except Exception as e:
    print(f"❌ Critical Error during transmission: {e}")

finally:
    server.quit()
    print("🔌 Server connection closed cleanly.")
import os
import socket
import smtplib
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Ensure IPv4 resolution in WSL environments to prevent timeouts
_orig_getaddrinfo = socket.getaddrinfo
def _ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _ipv4_getaddrinfo


class NotificationManager:
    def __init__(self):
        # Email setup (SMTP)
        self.smtp_address = os.environ.get("EMAIL_PROVIDER_SMTP_ADDRESS", "smtp.gmail.com")
        self.email = os.environ.get("MY_EMAIL") or os.environ.get("TEST_EMAIL_ADDRESS")
        raw_password = os.environ.get("MY_EMAIL_PASSWORD") or os.environ.get("TEST_EMAIL_PASSWORD", "")
        self.email_password = raw_password.replace(" ", "") if raw_password else ""

        # Twilio setup
        self.twilio_sid = os.environ.get("TWILIO_SID") or os.environ.get("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.twilio_virtual_number = os.environ.get("TWILIO_VIRTUAL_NUMBER") or os.environ.get("TWILIO_PHONENUMBER")
        self.twilio_verified_number = os.environ.get("TWILIO_VERIFIED_NUMBER") or os.environ.get("TEST_PHONENUMBER")
        self.whatsapp_number = os.environ.get("TWILIO_WHATSAPP_NUMBER", "+14155238886")

        if self.twilio_sid and self.twilio_auth_token and not self.twilio_sid.startswith("your_"):
            self.client = Client(self.twilio_sid, self.twilio_auth_token)
        else:
            self.client = None

        # Telegram setup
        self.telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    def send_emails(self, email_list, email_body):
        """
        Sends an email alert to all customer emails in email_list via SMTP.
        """
        if not self.email or not self.email_password or self.email.startswith("your_") or self.email_password.startswith("your_"):
            print("Email credentials not configured in .env. Skipping email delivery.")
            return

        try:
            with smtplib.SMTP(self.smtp_address, 587, timeout=15) as connection:
                connection.starttls()
                connection.login(user=self.email, password=self.email_password)
                for email in email_list:
                    connection.sendmail(
                        from_addr=self.email,
                        to_addrs=email,
                        msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                    )
            print(f"Deal alert emails sent to {len(email_list)} recipient(s)!")
        except Exception as e:
            print(f"Error sending email: {e}")

    def send_telegram(self, message_body):
        """
        Sends an instant push alert message to Telegram via Bot API.
        """
        if not self.telegram_bot_token or not self.telegram_chat_id or self.telegram_bot_token == "your_bot_token_here":
            print("Telegram credentials not configured. Please add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to .env.")
            return

        telegram_url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message_body,
        }

        try:
            response = requests.post(url=telegram_url, json=payload, timeout=10)
            if response.status_code == 200:
                print("Telegram flight deal alert sent successfully!")
            else:
                print(f"Failed to send Telegram message. Response: {response.text}")
        except Exception as e:
            print(f"Error sending Telegram message: {e}")

    def send_sms(self, message_body):
        """
        Sends an SMS message through Twilio.
        """
        if not self.client:
            print("Twilio credentials not configured. SMS not sent.")
            return
        message = self.client.messages.create(
            from_=self.twilio_virtual_number,
            body=message_body,
            to=self.twilio_verified_number,
        )
        print(f"SMS sent successfully! SID: {message.sid}")

    def send_whatsapp(self, message_body):
        """
        Sends a WhatsApp message through Twilio.
        """
        if not self.client:
            print("Twilio credentials not configured. WhatsApp message not sent.")
            return
        message = self.client.messages.create(
            from_=f"whatsapp:{self.whatsapp_number}",
            body=message_body,
            to=f"whatsapp:{self.twilio_verified_number}",
        )
        print(f"WhatsApp message sent successfully! SID: {message.sid}")
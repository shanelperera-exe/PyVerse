from flask import Flask, render_template, request
import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.environ["MY_TEST_EMAIL"]
EMAIL_PASSWORD = os.environ["EMAIL_SENDER_PASSWORD"]
SMTP_ADDRESS = os.environ["MY_SMTP_ADDRESS"]

posts_url = "https://api.npoint.io/357777370cdad88c4223"
blog_response = requests.get(url=posts_url)
blog_response.raise_for_status()
posts = blog_response.json()

def receive_data():
    data = request.form

    name = data["name"]
    email = data["email"]
    phone_number = data["phone"]
    message = data["message"]

    send_email(name, email, phone_number, message)

    return "<h1>Successfully sent your message</h1>"

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP(SMTP_ADDRESS, 587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=email,
            msg=email_message
        )

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        receive_data()
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

@app.route("/post/<int:index>")
def view_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)
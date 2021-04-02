from flask import Flask, render_template, request
import requests
import smtplib

posts = requests.get("https://api.npoint.io/f196852caaea93ffe048").json()
OWN_EMAIL = "oiji2504@gmail.com"
OWN_PASSWORD = "password"

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'GET':
        return render_template("contact.html", msg_sent = False)
    else:
        data = request.form
        # print(data["name"])
        # print(data["email"])
        # print(data["phone"])
        # print(data["message"])
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent = True)


# @app.route("/form-entry", methods= ["POST"])
# def receive_data():
#     data = request.form
#     print(data["name"])
#     print(data["email"])
#     print(data["phone"])
#     print(data["message"])
#     return "<h1>Successfully sent your message</h1>"

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)

if __name__ == "__main__":
    app.run(debug=True)

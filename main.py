from flask import Flask, render_template, request
import requests
import smtplib

blog_url = "BLOG_ENDPOINT"
posts = requests.get(url=blog_url).json()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject: New Message from Blog!\n\n" \
                    f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:\n\t{message}"
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user="EMAIL@gmail.com", password="PWD")
        connection.sendmail(from_addr="EMAIL@gmail.com", to_addrs="EMAIL@gmail.com", msg=email_message)


@app.route("/post/<int:index>")
def show_post(index):
    return render_template("post.html", all_posts=posts, blog_id=index)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import requests
import smtplib

blog_url = "BLOG URL"
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
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user="EMAIL", password="PASSWORD")
            connection.sendmail(
                from_addr="EMAIL",
                to_addrs="EMAIL",
                msg=f"Subject: New Message from Blog!\n\nName: {data['name']}"
                    f"\nEmail: {data['email']}\nPhone: {data['phone']}\nMessage:\n\t{data['message']}")

        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    return render_template("post.html", all_posts=posts, blog_id=index)


if __name__ == "__main__":
    app.run(debug=True)

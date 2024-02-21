from flask import Flask, render_template, request
import smtplib

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route("/success", methods=["POST"])
def receive_data():
    firstname = request.form["firstname"]
    lastname = request.form['lastname']
    email = request.form["email"]
    subject = request.form["subject"]
    desc = request.form["desc"]

    my_email = ""
    password = ""

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email, 
            to_addrs=[f"{email}"],
            msg=f"Subject:{subject}\n\n{desc}\nKind regards,\n{firstname}{lastname}"
        )

    return f"Success! Review your email below \n\n Hi {firstname} {lastname}, <br> just confirming your email is {email} and heading {subject} <br> {desc}"


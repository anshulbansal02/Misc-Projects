# Imports
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeSerializer, BadSignature
import sqlite3

# Initialize App
app = Flask(__name__)

conn = sqlite3.connect('database.sqlite')

# Database.sqlite file contains a Subscribers table with two columns (Name TEXT, Email TEXT).
c = conn.cursor()
print('Opened database successfully')


# Configure Mail App
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='anshul.bansal950@gmail.com',
    MAIL_PASSWORD="Flaskwebapp16"
)

# Initialize Mail App
mail = Mail(app)


# Opens the index page of the website
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

v_name = ""


# Takes the Email and Name from the HTML Form
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == "POST":
        global v_name
        v_name = request.form['vname']
        v_email = request.form['vemail']
        s = URLSafeSerializer("secret-key")
        encrypted_url = s.dumps(v_email)
        return send_mail(v_name, v_email, encrypted_url)

    else:
        return redirect(url_for("/"))


# Email Function
def send_mail(name, email, serial_key):
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    for v_email in (email,):
        c.execute("SELECT * FROM Subscribers WHERE Email = ?", (v_email,))
        data_exists = c.fetchone()
        if data_exists:
            return render_template('indata.html')
        else:
            msg = Message('You Have Got A Mail', sender='anshul.bansal950@gmail.com', recipients=[email])
            msg.html = render_template('email.html', name=name, serial_key=serial_key, v_email=email)
            mail.send(msg)
            return render_template('confirm.html', v_email=email)


# De-serialize the key and store the info in database
@app.route("/<key>")
def confirm(key):
    try:
        s = URLSafeSerializer('secret-key')
        v_email = s.loads(key)
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute("INSERT INTO Subscribers(Name, Email) VALUES (?, ?)", (v_name, v_email))
        conn.commit()
        c.close()
        return render_template('registered.html', name=v_name)
    except BadSignature:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

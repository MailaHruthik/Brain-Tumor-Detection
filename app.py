from flask import Flask, render_template, request, redirect, url_for, session,jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import model
from email.message import EmailMessage
import smtplib
import ssl

app = Flask(__name__)
app.secret_key = 'xyzsdfg'
app.config['UPLOAD_FOLDER'] = 'uploads'  # Configure upload folder

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'

mysql = MySQL(app)

# Your email credentials
email_sender = 'bab502bab@gmail.com'
email_password = "xkch gwen tfvy seli"
email_recipient = "mhruthik7@gmail.com"

@app.route('/')
def home():
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            message = 'Logged in successfully !'
            return redirect(url_for('dashboard'))
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        elif not userName or not password or not email:
            message = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s)', (userName, email, password,))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html', message=message)

@app.route('/dashboard')
def dashboard():
    if 'name' in session:
        username = session['name']
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'loggedin' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            image_path = f'uploads/{image_file.filename}'
            image_file.save(image_path)

            loaded_model = model.load_model("Classification.h5")  # Rename the variable
            prediction = model.predict_tumor(image_path, loaded_model)

            return render_template('result.html', prediction=prediction)
        else:
            return redirect(url_for('home'))
        

@app.route('/video_chat')
def video_chat():
    return render_template('video_chat.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Email content
        subject = "Patient Ready for Video Chat"
        body = "https://mailadoctor.000webhostapp.com/"

        # Create email message
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_recipient
        em['Subject'] = subject
        em.set_content(body)

        # SMTP connection
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_recipient, em.as_string())

        # Return success response
        return jsonify({'success': True, 'message': 'Email sent successfully'})
    except Exception as e:
        # Return error response
        return jsonify({'success': False, 'error': str(e)})

@app.route('/help')
def help():
    return render_template('help.html')


if __name__ == '__main__':
    app.run(debug=True)

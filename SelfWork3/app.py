from flask import Flask, render_template, request, jsonify, session
from models import db, Book, Order
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SECRET_KEY'] = 'student-key-2026'
db.init_app(app)

with app.app_context():
    db.create_all()
    if not Book.query.first():
        db.session.add(Book(title="Kobzar", author="T. Shevchenko", price=300.0))
        db.session.commit()

@app.route('/')
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    books = Book.query.all()
    res = f"<h1>BookStore</h1><p>Session ID: {session['user_id']}</p><ul>"
    for b in books:
        res += f"<li>{b.title} ({b.author}) - {b.price} UAH</li>"
    return res + "</ul>"

@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{"title": b.title, "author": b.author, "price": b.price} for b in books])

if __name__ == '__main__':
    app.run(debug=True)

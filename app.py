"""
A basic web app that asks the user to rate their experience shopping with a fake Lexus dealership
"""

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev': 
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://moses:#Dragon21@localhost/Python-Flask-Tutorial'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    # def __init__(self, customer, dealer, rating, comments):
    def __init__(self, **kwargs):
        self.customer = kwargs['customer']
        self.dealer = kwargs['dealer']
        self.rating = kwargs['rating']
        self.comments = kwargs['comments']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']

        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')

        # Save the user's feedback to the db unless they've already submitted a survey. In that case, inform them that their feedback has already been submitted.
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer=customer, dealer=dealer, rating=rating, comments=comments)
            db.session.add(data)
            db.session.commit()

            return render_template('success.html')
        else:
            return render_template('index.html', message='You have already submitted feedback')

if __name__ == "__main__":
    app.run()

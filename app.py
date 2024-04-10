from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import numpy as np
import pickle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/db'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class PlayoffData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    League = db.Column(db.String(50))
    Year = db.Column(db.Integer)
    OBP = db.Column(db.Float)
    SLG = db.Column(db.Float)
    BA = db.Column(db.Float)
    Playoffs = db.Column(db.Boolean)
    G = db.Column(db.Integer)
    OOBP = db.Column(db.Float)
    OSLG = db.Column(db.Float)
    RD = db.Column(db.Integer)

with open('svc_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def predict_playoffs():
    if request.method == 'POST':
        data = {
            'League': float(request.form['League']),
            'Year': int(request.form['Year']),
            'OBP': float(request.form['OBP']),
            'SLG': float(request.form['SLG']),
            'BA': float(request.form['BA']),
            'G': int(request.form['G']),
            'OOBP': float(request.form['OOBP']),
            'OSLG': float(request.form['OSLG']),
            'RD': int(request.form['RD'])
        }

        features = np.array([data['Year'], data['OBP'], data['SLG'], data['BA'], data['G'], data['OOBP'], data['OSLG'], data['RD'], data['League']]).reshape(1, -1)
        print("Input Features:", features)

        prediction = model.predict(features)[0]
        print("Predicted Playoff Status:", prediction)

        new_entry = PlayoffData(League=data['League'], Year=data['Year'], OBP=data['OBP'], SLG=data['SLG'], BA=data['BA'],
                                Playoffs=prediction, G=data['G'], OOBP=data['OOBP'], OSLG=data['OSLG'], RD=data['RD'])
        db.session.add(new_entry)
        db.session.commit()

        return render_template('result.html', prediction=prediction)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)

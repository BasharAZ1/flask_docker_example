import os
from flask import Flask, request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pandas as pd
from flask import jsonify
import pickle

db_username = os.environ['DB_USERNAME']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_uri = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
print(f"Connecting db @{db_uri}")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy()
db.init_app(app)

class BaseballData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    League = db.Column(db.String(50))
    Year = db.Column(db.Integer)
    OBP = db.Column(db.Float)
    SLG = db.Column(db.Float)
    BA = db.Column(db.Float)
    Playoffs = db.Column(db.Integer)
    G = db.Column(db.Integer)
    OOBP = db.Column(db.Float)
    OSLG = db.Column(db.Float)
    RD = db.Column(db.Integer)


def load_model_components():
    global svm_model
    with open('svm_model.pkl', 'rb') as f:
        svm_model = pickle.load(f)

@app.route('/')
def homepage():
    return render_template("index.html")
@app.route('/predict', methods=['POST'])
def predict():
    load_model_components()

    league = request.form['league']
    if league=='NL':
        league=1
    else:
        league=0   
    year = request.form['year']
    obp = request.form['obp']
    slg = request.form['slg']
    ba = request.form['ba']
    g = request.form['g']
    oobp = request.form['oobp']
    oslg = request.form['oslg']
    rd = request.form['rd']
    input_data = pd.DataFrame({

        'Year': [year],
        'OBP': [obp],
        'SLG': [slg],
        'BA': [ba],
        'G': [g],
        'OOBP': [oobp],
        'OSLG': [oslg],
        'RD': [rd],
        'League_NL': [league],
    })
    prediction = svm_model.predict(input_data)
    baseball_data = BaseballData(
        League='NL' if league == 1 else 'AL',
        Year=int(year),
        OBP=float(obp),
        SLG=float(slg),
        BA=float(ba),
        Playoffs=int(prediction),
        G=int(g),
        OOBP=float(oobp),
        OSLG=float(oslg),
        RD=int(rd)
    )
    db.session.add(baseball_data)
    db.session.commit()
    return render_template('result.html', prediction=prediction)
    
  

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5555)
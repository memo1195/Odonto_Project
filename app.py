from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# App Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/odonto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model

class Tratamiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable =False)

    def __repr__(self):
        return 'Tratamiento id: ' + str(self.id)

class Estado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable =False)

    def __repr__(self):
        return 'Estado id: ' + str(self.id)


db.create_all()

# Routes
@app.route('/')
def index():
    tratamientos = Tratamiento.query.order_by(Tratamiento.id).all()
    estados = Estado.query.order_by(Estado.id).all()

    return render_template('index.html',tratamientos=tratamientos,estados=estados)


if __name__ == "__main__":
    app.run(debug=True)
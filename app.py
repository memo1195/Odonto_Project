from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# App Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/odonto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model

# Tratamiento
class Tratamiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable =False)

    def __repr__(self):
        return 'Tratamiento id: ' + str(self.id)

# Estado
class Estado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable =False)

    def __repr__(self):
        return 'Estado id: ' + str(self.id)

# Lugar
class Lugar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable =False)
    estado_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Lugar id: ' + str(self.id)

# Cita
class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dentista_id = db.Column(db.Integer)
    nombre_paciente = db.Column(db.String(50), nullable=False)
    tel_paciente = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer, default=0)
    estado_id = db.Column(db.Integer ,nullable=False)
    lugar = db.Column(db.String(50))
    tratamiento_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Cita id: ' + str(self.id)

# Dentista
class Dentista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tel = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return 'Dentista id: ' + str(self.id)


db.create_all()

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre_paciente = request.form['nombre_paciente']
        tel_paciente = request.form['tel_paciente']
        # Tomamos los str
        tratamiento = request.form['tratamiento']
        estado = request.form['estado']
        # Los convertimos a Int
        tratamiento_id=Tratamiento.query.filter_by(nombre=tratamiento).first().id
        estado_id=Estado.query.filter_by(nombre=estado).first().id
        # Creamos la nueva cita
        nueva_cita = Cita(nombre_paciente=nombre_paciente,tel_paciente=tel_paciente,tratamiento_id=tratamiento_id,estado_id=estado_id)
        db.session.add(nueva_cita)
        db.session.commit() 
        return redirect('/')
    else:
        tratamientos = Tratamiento.query.order_by(Tratamiento.id).all()
        estados = Estado.query.order_by(Estado.id).all()
        return render_template('index.html',tratamientos=tratamientos,estados=estados)


if __name__ == "__main__":
    app.run(debug=True)
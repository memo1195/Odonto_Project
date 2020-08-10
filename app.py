from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# App Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/odonto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

############

# Model #

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

# Status_cita
class Status_cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(50), unique=True, nullable =False)

    def __repr__(self):
        return self.desc

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
    # [0=Libre, 1=Pendiente, 2=Confirmada, 3=Cancelada]
    status_id = db.Column(db.Integer, default=1)
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

# Creamos la DB
db.create_all()

############

# Routes #

# Index
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # Cuando se agrega una nueva cita

        # Asignamos valores del form
        nombre_paciente = request.form['nombre_paciente']
        tel_paciente = request.form['tel_paciente']
        tratamiento_id=request.form['tratamiento_id']
        estado_id=request.form['estado_id']

        # Creamos la nueva cita
        nueva_cita = Cita(nombre_paciente=nombre_paciente,tel_paciente=tel_paciente,tratamiento_id=tratamiento_id,estado_id=estado_id)

        # La agregamos a la DB
        db.session.add(nueva_cita)
        db.session.commit() 

        # F5
        return redirect('/')
    else: # Cuando no se intenta agregar una nueva cita

        # Cargamos las traducciones para el form
        tratamientos = Tratamiento.query.order_by(Tratamiento.id).all()
        estados = Estado.query.order_by(Estado.id).all()

        # Se carga la pagina
        return render_template('index.html',tratamientos=tratamientos,estados=estados)

# Buscar Paciente
@app.route('/paciente_search', methods=['GET', 'POST'])
def paciente_search():

    if request.method == 'POST': # Cuando se aplica el filtro

        # Cargamos las traducciones por ID para el form
        tratamientos = Tratamiento.query.order_by(Tratamiento.id).all()
        estados = Estado.query.order_by(Estado.id).all()
        status_citas = Status_cita.query.order_by(Status_cita.id).all()

        # Asignamos los valores del form a las variables
        tratamiento_id = request.form['tratamiento_id']
        estado_id = request.form['estado_id']

        # Creamos los filtros con las variables
        filter_tratamiento = (Cita.tratamiento_id == tratamiento_id)
        filter_estado = (Cita.estado_id == estado_id)
        filter_status = (Cita.status_id == 1) | (Cita.status_id ==4)

        # Unimos los filtros en uno solo
        if (tratamiento_id == 'default') and (estado_id == 'default'):
            filter_citas = filter_status
        elif tratamiento_id == 'default':
            filter_citas = filter_status & filter_estado
        elif estado_id == 'default':
            filter_citas = filter_status & filter_tratamiento
        else:
            filter_citas = filter_status & filter_tratamiento & filter_estado
        
        # Filtramos todas las citas con nuestro filtro creado
        citas = Cita.query.filter(filter_citas).all()

        return render_template('paciente_search.html',citas=citas, tratamientos=tratamientos, estados=estados, status_citas=status_citas)
    
    else: # Cuando se abre la pagina sin aplicar filtro

        # Cargamos las traducciones para el form
        tratamientos = Tratamiento.query.order_by(Tratamiento.id).all()
        estados = Estado.query.order_by(Estado.id).all()
        status_citas = Status_cita.query.order_by(Status_cita.id).all()

        # Cargamos todas las citas que esten libres o canceladas
        citas = Cita.query.filter((Cita.status_id == 1) | (Cita.status_id ==4)).all()

        return render_template('paciente_search.html',citas=citas, tratamientos=tratamientos, estados=estados, status_citas=status_citas)


if __name__ == "__main__":
    app.run(debug=True)       
from flask import Flask, request, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password123@localhost:5432/EmployeeDB"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] =  False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Employees(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())

    #def __init__(self, name, email, phone):
        #self.name = name
        #self.email = email
        #self.phone = phone

    def __repr__(self):
        return f"<Employee {self.name}>"


@app.route('/')
def index():
    employees = Employees.query.order_by(Employees.id).all()
    return render_template('index.html', employees = employees)

@app.route('/create/', methods = ('GET','POST'))
def create():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        employees = Employees(name = name, email = email, phone = phone)
        db.session.add(employees)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/update/<int:id>')
def update(id):
    employees = Employees.query.get_or_404(id)
    return render_template('update.html', employees = employees)

@app.route('/edit/', methods = ["POST"])
def edit():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    #employees = Employees(name = name, email = email, phone = phone)
    existing_employee = Employees.query.get(id)
    #existing_employee = Employees(name = name, email = email, phone = phone)
    existing_employee.name = name
    existing_employee.email = email
    existing_employee.phone = phone
    #existing_employee = employees
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    employees = Employees.query.get_or_404(id)
    db.session.delete(employees)
    db.session.commit()
    return redirect(url_for('index'))

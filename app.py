from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    usn = db.Column(db.String(20), nullable=False)
    branch = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    section = db.Column(db.Integer())
    dob = db.Column(db.Date)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    students = Students.query.all()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        usn = request.form['usn']
        branch = request.form['branch']
        semester = request.form['semester']
        section = request.form['section']
        dob_str = request.form['dob']
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        print(f"nme is: {name}, usn is: {usn}, branch is: {branch}, semester is: {semester}, section is: {section}, dob is: {dob}")
        new_student = Students(name=name, usn=usn, branch=branch, semester=semester, section=section, dob=dob)
        print("new_task: {}".format(new_student))
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('add_student'))
    return render_template('add_student.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Students.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.usn = request.form['usn']
        student.branch =request.form['branch']
        student.semester = request.form['semester']
        student.section = request.form['section']
        dob_str = request.form['dob'].strip()
        student.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Students.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})

if __name__ == "__main__":
    app.run(debug=True)

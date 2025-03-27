from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Employee, Attendance
from app import db
from datetime import datetime, date

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('department')
        
        if not name or not email or not department:
            flash('All fields are required!')
            return redirect(url_for('main.employees'))
        
        existing_employee = Employee.query.filter_by(email=email).first()
        if existing_employee:
            flash('Email already exists!')
            return redirect(url_for('main.employees'))
        
        new_employee = Employee(name=name, email=email, department=department)
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee added successfully!')
        
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

@bp.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        action = request.form.get('action')
        
        if not employee_id or not action:
            flash('Invalid request!')
            return redirect(url_for('main.attendance'))
        
        employee = Employee.query.get(employee_id)
        if not employee:
            flash('Employee not found!')
            return redirect(url_for('main.attendance'))
        
        today = date.today()
        
        if action == 'check_in':
            # Check if already checked in today
            existing_attendance = Attendance.query.filter_by(
                employee_id=employee_id, 
                date=today,
                check_out=None
            ).first()
            
            if existing_attendance:
                flash('Already checked in!')
                return redirect(url_for('main.attendance'))
            
            new_attendance = Attendance(employee_id=employee_id)
            db.session.add(new_attendance)
            db.session.commit()
            flash('Checked in successfully!')
            
        elif action == 'check_out':
            # Find the latest attendance record without checkout
            attendance_record = Attendance.query.filter_by(
                employee_id=employee_id, 
                date=today,
                check_out=None
            ).first()
            
            if not attendance_record:
                flash('No check-in record found!')
                return redirect(url_for('main.attendance'))
            
            attendance_record.check_out = datetime.utcnow()
            db.session.commit()
            flash('Checked out successfully!')
    
    employees = Employee.query.all()
    today_attendance = Attendance.query.filter_by(date=date.today()).all()
    return render_template('attendance.html', employees=employees, attendance=today_attendance)

@bp.route('/reports')
def reports():
    employees = Employee.query.all()
    department = request.args.get('department')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Attendance.query
    
    if department:
        query = query.join(Employee).filter(Employee.department == department)
    
    if start_date:
        query = query.filter(Attendance.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    
    if end_date:
        query = query.filter(Attendance.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    attendance_data = query.all()
    
    departments = db.session.query(Employee.department).distinct().all()
    departments = [d[0] for d in departments]
    
    return render_template('reports.html', 
                           attendance=attendance_data, 
                           employees=employees,
                           departments=departments)

@bp.route('/api/attendance', methods=['GET'])
def api_attendance():
    attendance_data = Attendance.query.all()
    result = []
    
    for record in attendance_data:
        employee = Employee.query.get(record.employee_id)
        data = {
            'id': record.id,
            'employee_id': record.employee_id,
            'employee_name': employee.name,
            'department': employee.department,
            'date': record.date.strftime('%Y-%m-%d'),
            'check_in': record.check_in.strftime('%H:%M:%S'),
            'check_out': record.check_out.strftime('%H:%M:%S') if record.check_out else None
        }
        result.append(data)
    
    return jsonify(result)
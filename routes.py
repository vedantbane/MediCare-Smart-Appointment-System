import logging
from datetime import datetime, date, time
from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from models import User, Appointment, DoctorSchedule

@app.before_request
def make_session_permanent():
    session.permanent = True

def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current logged-in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

@app.route('/')
def index():
    """Main landing page"""
    current_user = get_current_user()
    if current_user:
        # User is logged in, show dashboard
        if current_user.role == 'doctor':
            return render_template('index.html', 
                                 current_user=current_user,
                                 show_doctor_dashboard=True)
        else:
            return render_template('index.html', 
                                 current_user=current_user,
                                 show_patient_dashboard=True)
    else:
        # User not logged in, show auth forms
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Handle login form submission"""
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    user_type = request.form.get('userType', 'patient')
    
    if not email or not password:
        flash('Please enter both email and password.', 'error')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(email=email, role=user_type).first()
    
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['user_role'] = user.role
        flash(f'Welcome back, {user.name}!', 'success')
        logging.info(f"User {email} logged in successfully")
        return redirect(url_for('index'))
    else:
        flash('Invalid email or password.', 'error')
        return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    """Handle signup form submission"""
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    user_type = request.form.get('signupUserType', 'patient')
    specialization = request.form.get('specialization', '').strip()
    license_number = request.form.get('licenseNumber', '').strip()
    
    # Validation
    if not all([name, email, password, confirm_password]):
        flash('Please fill in all required fields.', 'error')
        return redirect(url_for('index'))
    
    if password != confirm_password:
        flash('Passwords do not match.', 'error')
        return redirect(url_for('index'))
    
    if len(password) < 6:
        flash('Password must be at least 6 characters long.', 'error')
        return redirect(url_for('index'))
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('An account with this email already exists.', 'error')
        return redirect(url_for('index'))
    
    # Doctor-specific validation
    if user_type == 'doctor':
        if not specialization or not license_number:
            flash('Specialization and license number are required for doctors.', 'error')
            return redirect(url_for('index'))
    
    # Create new user
    try:
        user = User(
            name=name,
            email=email,
            role=user_type,
            specialization=specialization if user_type == 'doctor' else None,
            license_number=license_number if user_type == 'doctor' else None
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Auto login after signup
        session['user_id'] = user.id
        session['user_role'] = user.role
        
        flash(f'Account created successfully! Welcome to MediCare, {name}!', 'success')
        logging.info(f"New user created: {email} as {user_type}")
        return redirect(url_for('index'))
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating user: {e}")
        flash('An error occurred while creating your account. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Handle logout"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/book_appointment', methods=['POST'])
@login_required
def book_appointment():
    """Handle appointment booking"""
    current_user = get_current_user()
    if current_user.role != 'patient':
        flash('Only patients can book appointments.', 'error')
        return redirect(url_for('index'))
    
    doctor_id = request.form.get('doctor_id')
    appointment_date = request.form.get('appointment_date')
    appointment_time = request.form.get('appointment_time')
    reason = request.form.get('reason', '').strip()
    
    if not all([doctor_id, appointment_date, appointment_time]):
        flash('Please fill in all appointment details.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Parse date and time
        app_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        app_time = datetime.strptime(appointment_time, '%H:%M').time()
        
        # Check if appointment date is in the future
        if app_date < date.today():
            flash('Appointment date must be in the future.', 'error')
            return redirect(url_for('index'))
        
        # Check if doctor exists
        doctor = User.query.filter_by(id=doctor_id, role='doctor').first()
        if not doctor:
            flash('Selected doctor not found.', 'error')
            return redirect(url_for('index'))
        
        # Check for existing appointment at same time
        existing = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=app_date,
            appointment_time=app_time,
            status='scheduled'
        ).first()
        
        if existing:
            flash('This time slot is already booked. Please choose another time.', 'error')
            return redirect(url_for('index'))
        
        # Create appointment
        appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=doctor_id,
            appointment_date=app_date,
            appointment_time=app_time,
            reason=reason,
            status='scheduled'
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash(f'Appointment booked successfully with Dr. {doctor.name} for {app_date} at {app_time}!', 'success')
        logging.info(f"Appointment booked: Patient {current_user.id} with Doctor {doctor_id}")
        
    except ValueError:
        flash('Invalid date or time format.', 'error')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error booking appointment: {e}")
        flash('An error occurred while booking your appointment. Please try again.', 'error')
    
    return redirect(url_for('index'))

@app.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    current_user = get_current_user()
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check if user has permission to cancel this appointment
    if current_user.role == 'patient' and appointment.patient_id != current_user.id:
        flash('You can only cancel your own appointments.', 'error')
        return redirect(url_for('index'))
    
    if current_user.role == 'doctor' and appointment.doctor_id != current_user.id:
        flash('You can only cancel appointments with your patients.', 'error')
        return redirect(url_for('index'))
    
    try:
        appointment.status = 'cancelled'
        appointment.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Appointment cancelled successfully.', 'info')
        logging.info(f"Appointment {appointment_id} cancelled by user {current_user.id}")
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error cancelling appointment: {e}")
        flash('An error occurred while cancelling the appointment.', 'error')
    
    return redirect(url_for('index'))

@app.route('/complete_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def complete_appointment(appointment_id):
    """Mark an appointment as completed (doctors only)"""
    current_user = get_current_user()
    if current_user.role != 'doctor':
        flash('Only doctors can mark appointments as completed.', 'error')
        return redirect(url_for('index'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.doctor_id != current_user.id:
        flash('You can only complete your own appointments.', 'error')
        return redirect(url_for('index'))
    
    try:
        appointment.status = 'completed'
        appointment.notes = request.form.get('notes', '')
        appointment.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Appointment marked as completed.', 'success')
        logging.info(f"Appointment {appointment_id} completed by doctor {current_user.id}")
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error completing appointment: {e}")
        flash('An error occurred while updating the appointment.', 'error')
    
    return redirect(url_for('index'))

@app.context_processor
def inject_data():
    """Inject common data into all templates"""
    from datetime import date
    current_user = get_current_user()
    data = {'current_user': current_user, 'today': date.today}
    
    if current_user:
        if current_user.role == 'patient':
            # Get patient's appointments
            data['patient_appointments'] = Appointment.query.filter_by(
                patient_id=current_user.id
            ).order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).all()
            
            # Get all doctors for booking
            data['doctors'] = User.query.filter_by(role='doctor').all()
            
        elif current_user.role == 'doctor':
            # Get doctor's appointments
            data['doctor_appointments'] = Appointment.query.filter_by(
                doctor_id=current_user.id
            ).order_by(Appointment.appointment_date.asc(), Appointment.appointment_time.asc()).all()
    
    return data

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('index.html'), 500

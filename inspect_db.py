from app import app, db, models
from models import User, Appointment

def inspect():
    with app.app_context():
        print("-" * 50)
        print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("-" * 50)

        # List Users
        users = User.query.all()
        print(f"\nUsers ({len(users)}):")
        if not users:
            print("  No users found.")
        for u in users:
            print(f"  [ID: {u.id}] {u.name} | Role: {u.role} | Email: {u.email}")
        
        print("-" * 30)

        # List Appointments
        appointments = Appointment.query.all()
        print(f"\nAppointments ({len(appointments)}):")
        if not appointments:
            print("  No appointments found.")
        for a in appointments:
            print(f"  [ID: {a.id}] {a.appointment_date} {a.appointment_time} | Status: {a.status}")

        print("\n" + "-" * 50)

if __name__ == "__main__":
    inspect()

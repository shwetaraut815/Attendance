from app import create_app, db
from app.models import Employee, Attendance

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Employee': Employee, 'Attendance': Attendance , }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
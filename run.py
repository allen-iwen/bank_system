from app import create_app, db
from app.models import User, Customer, Manager, MatchingRecord
from app.utils.data_generator import generate_test_data, clear_test_data

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Customer': Customer,
        'Manager': Manager,
        'MatchingRecord': MatchingRecord,
        'generate_test_data': generate_test_data,
        'clear_test_data': clear_test_data
    }

if __name__ == '__main__':
    app.run(debug=True)
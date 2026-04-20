from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# In-memory "database"
students = []
next_id = 1


# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 500


# Get all students
@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(students), 200


# Get student by ID
@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    for student in students:
        if student['id'] == student_id:
            return jsonify(student), 200
    return jsonify({'error': 'Student not found'}), 404


# Add new student
@app.route('/api/students', methods=['POST'])
def add_student():
    global next_id

    data = request.get_json()

    # Check required fields
    if not data or 'name' not in data or 'grade' not in data:
        return jsonify({'error': 'Missing fields'}), 400

    new_student = {
        'id': next_id,
        'name': data['name'],
        'grade': data['grade']
    }

    students.append(new_student)
    next_id += 1

    return jsonify(new_student), 201


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
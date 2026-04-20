import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING']=True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

def test_get_all_students(client):
    response = client.get('/api/students')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data,list)

# 3. Get non-existent student → should return 404
def test_get_non_existent_student(client):
    response = client.get('/api/students/9999')
    assert response.status_code == 404


# 4. Add valid student → should return 201 and correct name
def test_add_valid_student(client):
    student = {
        "name": "Memoona",
        "grade": "A"
    }

    response = client.post('/api/students', json=student)
    assert response.status_code == 201

    data = response.get_json()
    assert data['name'] == "Memoona"


# 5. Add student with missing field → should return 400
def test_add_student_missing_field(client):
    student = {
        "name": "Sara"
    }

    response = client.post('/api/students', json=student)
    assert response.status_code == 400
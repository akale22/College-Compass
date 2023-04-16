from flask import Blueprint, request, jsonify, make_response
import json
from src import db


students = Blueprint('students', __name__)


# Get all of the information for a student
@students.route('/<ID>', methods=['GET'])
def get_student_info(ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Students WHERE StudentID = {0}'.format(ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get favorites colleges for a specific student
@students.route('/<ID>/favoritedColleges', methods=['GET'])
def get_student_favorite_colleges(ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT CollegeId FROM StudentsFavoritedColleges WHERE StudentID = {0}'.format(ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get the student's college preferences
@students.route('/<ID>/collegePreferences', methods=['GET'])
def get_student_college_preferences(ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT GreekLife, Size, Temperature FROM CollegePreferences WHERE StudentID = {0}'.format(ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get the corresponding student's parents' financial income
@students.route('/<ID>/studentParentIncome', methods=['GET'])
def get_student_parent_income(ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT Income FROM Parents WHERE StudentID = {0}'.format(ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@students.route('')
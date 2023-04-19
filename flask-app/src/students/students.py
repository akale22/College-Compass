from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

students = Blueprint('students', __name__)

# Get the corresponding student's information
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

# Get the corresponding student's parents' financial income
@students.route('/<ID>/parentIncome', methods=['GET'])
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

# Get the corresponding student's college preferences
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

# Update the corresponding student's college preferences
@students.route('/<ID>/collegePreferences', methods=['PUT'])
def update_student_preferences(ID):
    the_data = request.json

    greek_life = the_data['Greek_Life']
    size = the_data['Size']
    temp = the_data['Temperature']

    the_query = 'UPDATE CollegePreferences SET GreekLife = %s, Size = %s, Temperature = %s WHERE StudentID = %s;'

    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query, (greek_life, size, temp, ID))
    db.get_db().commit()

    return "Successfully updated student preferences!"


# Get the corresponding student's favorites colleges
@students.route('/<ID>/favoritedColleges', methods=['GET'])
def get_student_favorite_colleges(ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT CollegeName, C.CollegeID, EnrollmentSize, AcceptanceRate FROM StudentsFavoritedColleges SFC JOIN Colleges C ON SFC.CollegeID = C.CollegeID WHERE StudentID = {0}'.format(ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add to the corresponding student's list of favorited colleges
@students.route('/<ID>/favoritedColleges', methods=['POST'])
def add_favorite_colleges(ID):
    the_data = request.json

    college_id = the_data['CollegeID']

    the_query = 'INSERT into StudentsFavoritedColleges (StudentID, CollegeID) VALUES (%s, %s);'

    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query, (ID, college_id))
    db.get_db().commit()

    return "Successfully added a college to a student's favorited list!"

# Delete from the corresponding student's list of favorite colleges
@students.route('/<ID>/favoritedColleges', methods=['DELETE'])
def delete_favorite_colleges(ID):
    the_data = request.json

    college_id = the_data['CollegeID']

    the_query = 'DELETE FROM StudentsFavoritedColleges WHERE StudentID = %s AND CollegeID = %s;'

    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query, (ID, college_id))
    db.get_db().commit()

    return "Successfully deleted a college from a student's favorited list!"

# Get the corresponding student's high school information
@students.route('/<ID>/HighSchool', methods=['GET'])
def get_student_HighSchool(ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT HighSchoolName, SchoolRank, Size FROM Students JOIN HighSchool on Students.SchoolID = HighSchool.SchoolID WHERE StudentID = {0}'.format(ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all the students, necessary for logging in as a particular student
@students.route('/', methods=['GET'])
def get_all_students():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT DISTINCT StudentID as label, StudentID as value FROM Students ORDER BY StudentID')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

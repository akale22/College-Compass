from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db

colleges = Blueprint('colleges', __name__)

# getting college information
@colleges.route('/<ID>', methods=['GET'])
def get_college_info(ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Colleges WHERE CollegeID = {0}'.format(ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get department information
@colleges.route('/<ID>/departments', methods=['GET'])
def get_college_departments(ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT DeptName, DeptRank, DeptDescription FROM Colleges JOIN Departments WHERE Colleges.CollegeID = {0} ORDER BY DeptRank'.format(ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get course information
@colleges.route('/<ID>/courses', methods=['GET'])
def get_college_courses(ID):
    cursor = db.get_db().cursor() 
    # get college departments, have to join on colleges
    cursor.execute('SELECT CourseName, CourseDescription, Credits FROM Colleges JOIN Departments D JOIN Courses on D.DeptCode = Courses.DeptCode WHERE Colleges.CollegeID = {0}'.format(ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all colleges with query params:
@colleges.route('/', methods=['GET'])
def get_all_colleges():
    cursor = db.get_db().cursor()
    # been messing around with this and the only real thing you can filter by in a college is the enrollmentSize, so you might
    # as well just pass it through the url instead of query paramters tho idk

    # default value if the user does not supply a paramter
    enrollmentSize = request.args.get('enrollmentSize', 10000000)
    # enrollmentSize = request.args.to_dict()['enrollmentSize']
    the_query ='SELECT * FROM Colleges WHERE EnrollmentSize < ' + str(enrollmentSize)

    cursor.execute(the_query)
    current_app.logger.info(the_query)

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

#another route to get how many students are viewing a college:

# Add a new course to a college
@colleges.route('/<ID>/newCourse', methods=['POST'])
def add_new_course(ID):
    the_data = request.json
    dept_id = the_data['DeptCode']
    credits = the_data['Credits']
    courseName = the_data['CourseName']
    courseDescription = the_data['CourseDescription']
    tempCourseID = 'SELECT MAX(CourseID) FROM Courses'
    cursor = db.get_db().cursor()
    cursor.execute(tempCourseID)

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    courseID = json_data[0]["MAX(CourseID)"]
    if courseID is None:
        courseID = 1
    else:
        courseID = int(courseID) + 1

    the_query = 'INSERT into Courses (CourseID, DeptCode, Credits, CourseName, CourseDescription) VALUES (%s, %s, %s, %s, %s);'
    current_app.logger.info(the_query)
    cursor = db.get_db().cursor()
    cursor.execute(the_query, (courseID, dept_id, credits, courseName, courseDescription))
    db.get_db().commit()

    return "Successfully added a course to a college!"

@colleges.route('/<ID>/studentsInterested', methods=['GET'])
def get_interested_students(ID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT studentID FROM StudentsFavoritedColleges WHERE CollegeID = {0}'.format(ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add a new department to a college
@colleges.route('/<ID>/newDepartment', methods=['POST'])
def add_new_department(ID):
    the_data = request.json
    deptName = the_data["DeptName"]
    deptRank = the_data["DeptRank"]
    deptDescription = the_data["DeptDescription"]

    tempDeptCode = 'SELECT MAX(DeptCode) FROM Departments WHERE CollegeID = %s'
    print(tempDeptCode)
    cursor = db.get_db().cursor()
    cursor.execute(tempDeptCode, (ID))


    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
        
    deptCode = json_data[0]["MAX(DeptCode)"]
    if deptCode is None:
        deptCode = 1
    else:
        deptCode = int(deptCode) + 1

    the_query = 'INSERT into Departments (DeptName, DeptCode, CollegeID, DeptRank, DeptDescription) VALUES (%s, %s, %s, %s, %s);'
    current_app.logger.info(the_query)
    cursor = db.get_db().cursor()
    cursor.execute(the_query, (deptName, deptCode, ID, deptRank, deptDescription))
    db.get_db().commit()

    return "Successfully added a department to a college!"


# Add a new college to the college list if it is not already there
@colleges.route('/newCollege', methods=['POST'])
def add_new_college():
    the_data = request.json
    college_name = the_data['CollegeName']
    enrollment_size = the_data['EnrollmentSize']
    acceptance_rate = the_data['AcceptanceRate']

    tempCollegeID = 'SELECT MAX(CollegeID) FROM Colleges'
    cursor = db.get_db().cursor()
    cursor.execute(tempCollegeID)

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    college_id = str(json_data[0]["MAX(CollegeID)"])
    college_id = int(college_id) + 1

    the_query = 'INSERT INTO Colleges (CollegeName, EnrollmentSize, AcceptanceRate, CollegeID) VALUES (%s, %s, %s, %s);'
    current_app.logger.info(the_query)
    cursor = db.get_db().cursor()
    cursor.execute(the_query, (college_name, enrollment_size, acceptance_rate, college_id))
    db.get_db().commit()

    return "Successfully added a new college!"

# Delete a department
@colleges.route('/<ID>/departments', methods=['DELETE'])
def delete_department(ID):
    the_data = request.json
    dept_code = the_data['DeptCode']
    the_query = 'DELETE FROM Departments WHERE CollegeID = %s AND DeptCode = %s;'

    current_app.logger.info(the_query)
    cursor = db.get_db().cursor()
    cursor.execute(the_query, (ID, dept_code))
    db.get_db().commit()

    return "Successfully deleted a department!"

# Update the college's info
@colleges.route('/<ID>/updateInfo', methods=['PUT'])
def update_college_info(ID):
    the_data = request.json

    college_name = the_data['CollegeName']
    enrollment_size = the_data['EnrollmentSize']
    acceptance_rate = the_data['AcceptanceRate']

    the_query = 'UPDATE Colleges SET CollegeName = %s, EnrollmentSize = %s, AcceptanceRate = %s WHERE CollegeID = %s;'

    current_app.logger.info(the_query)

    cursor = db.get_db().cursor()
    cursor.execute(the_query, (college_name, enrollment_size, acceptance_rate, ID))
    db.get_db().commit()

    return "Successfully updated college info!"

# Delete a course -- doesn't delete based on CollegeID
@colleges.route('/<ID>/courses', methods=['DELETE'])
def delete_course(ID):
    the_data = request.json
    dept_code = the_data['DeptCode']
    course_id = the_data['CourseID']
    the_query = 'DELETE FROM Courses WHERE DeptCode = %s and CourseID = %s;'

    current_app.logger.info(the_query)
    cursor = db.get_db().cursor()
    cursor.execute(the_query, (dept_code, course_id))
    db.get_db().commit()

    return "Successfully deleted a course!"
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


colleges = Blueprint('colleges', __name__)

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

#just realized we don't have a name for any of the departments so not sure if just a desciption makes sense
@colleges.route('/<ID>/departments', methods=['GET'])
def get_college_departments(ID):
    cursor = db.get_db().cursor()

    cursor.execute('SELECT DeptRank, DeptDescription  FROM Colleges JOIN Departments WHERE Colleges.CollegeID = {0} ORDER BY DeptRank'.format(ID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@colleges.route('/<ID>/courses', methods=['GET'])
def get_college_courses(ID):
    cursor = db.get_db().cursor()

    #get college departments, have to join on colleges
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

#get all colleges with query params:
@colleges.route('/', methods=['GET'])
def get_all_colleges():
    cursor = db.get_db().cursor()
    #been messing around with this and the only real thing you can filter by in a college is the enrollmentSize, so you might
    #as well just pass it through the url instead of query paramters tho idk

    #default value if the user does not supply a paramter
    enrollmentSize = request.args.get('enrollmentSize', 10000000)
    #enrollmentSize = request.args.to_dict()['enrollmentSize']
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


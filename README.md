# College Compass

College Compass was created with the purpose of providing students an opportunity to view and favorite specific colleges, and for colleges to view prospective students that are interested in them.

## Overview of code:

### db:

Within our db directory we have two .sql files that get created with the docker compose:

**college-compass-db:**

This file contains information to create the CollegeCompass database, and grant permissions for web access, and creates the structure for each of our 16 tables

**college-compass-data:**

This file contains the insert statements for each of those tables of various amounts of mockaroo data

### flask-app:

This directory contains two blueprints colleges and students each for our user personas  

**colleges.py**

Contains all the routes necessary for a college user persona and includes at least one route for each the main HTTP methods: GET, PUT, POST, DELETE
Within this file contains the routes to get meta data about a specific college, add and delete new courses/departments for a college, and update necessary information about the college

**students.py**

Contains all the routes necessary for a student user persona and also includes at least one route for each the main HTTP methods: GET, PUT, POST, DELETE
Within the file contains routes to get necessary information about the student who accessed the route, such as their highschool and statistics, and options to modify their preferences and add and delete favorited colleges

Each route within flask-app queries the CollegeCompass database from our db folder and uses MYSQL to query for data in the necessary tables.

### Thunder-Test:

This directory contains all the tests for each of the routes created within the flask-app directory, and over 32 in total (at least 1 for each route).

## College Compass Appsmith

Within our [appsmith repo](https://github.com/akale22/College-Compass-Appsmith) contains the front end of the application.

### Pages:

**Home Page:** Here users select how they would like to use the app, either as a College or a Student, and then get directed to their respective profile pages

**Student Profile Page:** Students can select their studentID to login and then their information will be generated about the selected student. Students can update their existing preferences using a PUT request API call or navigate to Saved Colleges Page to add or remove their favorited colleges

**Update Saved Colleges Page:** Here users can search through the list of all colleges and add their selected college to their favorite colleges List using a POST API call, or delete an existing preference using a DELETE API call.

**Update College Preferences Page:** Here users can update their specific college preferences regaridng Greek Life, Size, and Temperature using a PUT API call.

Colleges similarly have their own ProfilePage(**College Profile Page**), and can also navigate to **Update College Info Page** to update and modify their information on the college to better advertise themselves to prospective students.

## How to setup and start the containers

**Important** - you need Docker Desktop installed

1. Clone this repository.
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL.
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp.
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`. To run in detached mode, run `docker compose up -d`.

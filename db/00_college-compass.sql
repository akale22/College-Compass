DROP DATABASE IF EXISTS CollegeCompass;
CREATE DATABASE CollegeCompass;

USE CollegeCompass;

grant all privileges on CollegeCompass.* to 'webapp'@'%';
flush privileges;


DROP TABLE IF EXISTS HighSchool;
CREATE TABLE HighSchool
(
    HighSchoolName VARCHAR(50) NOT NULL,
    Size INT NOT NULL,
    SchoolRank INT NOT NULL, 
    SchoolID INT PRIMARY KEY    
);

DROP TABLE IF EXISTS Counselors;
CREATE TABLE Counselors
(
    FirstName VARCHAR(20) NOT NULL,
    LastName VARCHAR(20) NOT NULL,
    CounselorID INT PRIMARY KEY
);

DROP TABLE IF EXISTS Colleges;
CREATE TABLE Colleges
(
    CollegeName VARCHAR(60) NOT NULL,
    EnrollmentSize INT NOT NULL,
    AcceptanceRate VARCHAR(4) NOT NULL,
    CollegeID INT PRIMARY KEY
);

DROP TABLE IF EXISTS Departments;
CREATE TABLE Departments
(
    DeptName VARCHAR(10) NOT NULL,
    DeptCode INT NOT NULL,
    CollegeID INT NOT NULL,
    DeptRank INT NOT NULL,
    DeptDescription VARCHAR(700) NOT NULL,
    CONSTRAINT departmentsPK PRIMARY KEY (DeptCode, CollegeID),
    CONSTRAINT departmentsFK FOREIGN KEY (CollegeID) REFERENCES Colleges(CollegeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS Courses;
CREATE TABLE Courses
(
    CourseID INT NOT NULL,
    DeptCode INT NOT NULL,
    Credits INT NOT NULL,
    CourseName VARCHAR(30) NOT NULL,
    CourseDescription VARCHAR(700) NOT NULL,
    CONSTRAINT coursesPK PRIMARY KEY (CourseID, DeptCode),
    CONSTRAINT coursesFK FOREIGN KEY (DeptCode) REFERENCES Departments(DeptCode)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS FinancialPackages;
CREATE TABLE FinancialPackages
(
    FFCode INT NOT NULL,
    CollegeID INT NOT NULL,
    LowerRange INT NOT NULL,
    UpperRange INT NOT NULL,
    AmountOfAid FLOAT NOT NULL,
    NumSemesters INT NOT NULL,
    CONSTRAINT financialPackagePK PRIMARY KEY (FFCode, CollegeID),
    CONSTRAINT financialPackageFK FOREIGN KEY (CollegeID) REFERENCES Colleges(CollegeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS Scholarships;
CREATE TABLE Scholarships
(
    SSCode INT NOT NULL,
    FFCode INT NOT NULL,
    ScholarshipName VARCHAR(50) NOT NULL,
    ScholarshipDescription VARCHAR(700) NOT NULL,
    Amount INT NOT NULL,
    CONSTRAINT scholarshipsPK PRIMARY KEY (SSCode, FFCode),
    CONSTRAINT scholarshipsFK FOREIGN KEY (FFCode) REFERENCES FinancialPackages(FFCode)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS Students;
CREATE TABLE Students
(
    StudentID INT PRIMARY KEY,
    SchoolID INT NOT NULL,
    CounselorID INT NOT NULL,
    FirstName VARCHAR(20) NOT NULL,
    LastName VARCHAR(20) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    CurrentYear INT NOT NULL,
    DesiredMajor VARCHAR(50) NOT NULL,
    DesiredMinor VARCHAR(50),
    SAT INT,
    ACT INT,
    GPA FLOAT,
    PhoneNumber BIGINT NOT NULL,
    CONSTRAINT studentsFK1 FOREIGN KEY (SchoolID) REFERENCES HighSchool(SchoolID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT studentsFK2 FOREIGN KEY (CounselorID) REFERENCES Counselors(CounselorID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


DROP TABLE IF EXISTS Parents;
CREATE TABLE Parents
(
    ParentName VARCHAR(25) NOT NULL,
    StudentID INT NOT NULL,
    Income INT NOT NULL,
    SchoolAttended VARCHAR(20) NOT NULL,
    NumChildren INT NOT NULL,
    CONSTRAINT parentsPK PRIMARY KEY (ParentName, StudentID),
    CONSTRAINT parentsFK FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS StudentsFavoritedColleges;
CREATE TABLE StudentsFavoritedColleges
(
    StudentID INT NOT NULL,
    CollegeID INT NOT NULL,
    CONSTRAINT stuColPK PRIMARY KEY (CollegeID, StudentID),
    CONSTRAINT stuColFK1 FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT stuColFK2 FOREIGN KEY (CollegeID) REFERENCES Colleges(CollegeID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS AlumniChats;
CREATE TABLE AlumniChats
(
    StudentID INT NOT NULL,
    AlumniID INT NOT NULL,
    CounselorID INT NOT NULL,
    AlumniName VARCHAR(50) NOT NULL,
    AlumniEmail VARCHAR(50) NOT NULL,
    CONSTRAINT alumniChatsPK PRIMARY KEY (StudentID, AlumniID),
    CONSTRAINT alumniChatsFK FOREIGN KEY (CounselorID) REFERENCES Counselors(CounselorID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS AlumChatContent;
CREATE TABLE AlumChatContent
(
    Content VARCHAR(400) NOT NULL,
    StudentID INT NOT NULL,
    AlumniID INT NOT NULL,
    CONSTRAINT alumChatContentPK PRIMARY KEY (Content, StudentID, AlumniID),
    CONSTRAINT alumChatContentFK FOREIGN KEY (StudentID, AlumniID) REFERENCES AlumniChats(StudentID, AlumniID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS CollegePreferences;
CREATE TABLE CollegePreferences
(
    CPID INT NOT NULL,
    StudentID INT NOT NULL,
    GreekLife VARCHAR(10) NOT NULL,
    Size VARCHAR(10) NOT NULL,
    Temperature VARCHAR(10) NOT NULL,
    CONSTRAINT preferencesPK PRIMARY KEY (CPID, StudentID),
    CONSTRAINT preferencesFK FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS CollegePrefLocation;
CREATE TABLE CollegePrefLocation
(
    Location VARCHAR(50) NOT NULL,
    CPID INT NOT NULL,
    CONSTRAINT prefLocationPK PRIMARY KEY (Location, CPID),
    CONSTRAINT prefLocationFK FOREIGN KEY (CPID) REFERENCES CollegePreferences(CPID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS AdmissionsPlan;
CREATE TABLE AdmissionsPlan
(
    AdmissionsID INT NOT NULL,
    CounselorID INT NOT NULL,
    CONSTRAINT admissionsPlanPK PRIMARY KEY (AdmissionsID, CounselorID),
    CONSTRAINT admissionsPlanFK FOREIGN KEY (CounselorID) REFERENCES Counselors(CounselorID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

DROP TABLE IF EXISTS AdmissionsPlanColleges;
CREATE TABLE AdmissionsPlanColleges
(
    CollegeID INT NOT NULL,
    Category VARCHAR(6) NOT NULL,
    AdmissionsID INT NOT NULL,
    CONSTRAINT adminPlanCollPK PRIMARY KEY (CollegeID, AdmissionsID, Category),
    CONSTRAINT adminPlanCollFK FOREIGN KEY (AdmissionsID) REFERENCES AdmissionsPlan(AdmissionsID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

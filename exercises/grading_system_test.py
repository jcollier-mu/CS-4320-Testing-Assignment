import pytest
import System
import Student

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem

@pytest.fixture
def sgoggins():
    gradingSystem = System.System()
    gradingSystem.load_data()
    username = "goggins"
    password = "augurrox"
    gradingSystem.login(username,password)
    return gradingSystem

def test_login(grading_system):
    username = "hdjsr7"
    password = "pass1234"
    grading_system.login(username,password)
    assert isinstance(grading_system.usr, Student.Student)

def test_check_password(grading_system):
    #is not robust to different forms of the same password
    #FAILS
    username = "hdjsr7"
    password = "pass1234"
    assert grading_system.check_password(username, password.upper())
    assert grading_system.check_password(username, password.capitalize())
    assert grading_system.check_password(username, password + " ")

def test_change_grade(grading_system):
    username = "calyam"
    password = "#yeet"
    grading_system.login(username, password)
    grading_system.usr.change_grade("hdjsr7", "cloud_computing", "assignment1", 0)
    grading_system.reload_data()
    assert grading_system.users["hdjsr7"]['courses']["cloud_computing"]["assignment1"]['grade'] == 0

def test_create_assignment(sgoggins):
    sgoggins.usr.create_assignment("assignment3", "2/2/20", "databases")
    sgoggins.reload_data()
    assert sgoggins.courses["databases"]["assignments"].get("assignment3", 'N/A') != 'N/A'
    assert sgoggins.courses["databases"]["assignments"]["assignment3"].get("due_date", "N/A") == "2/2/20"

def test_add_student(sgoggins, grading_system):
    #FAILS
    sgoggins.usr.add_student("james", "databases")
    sgoggins.reload_data()
    # no password parameter provided in Professor.add_student()
    grading_system.login("james", "")

def test_drop_student(sgoggins):
    #designed to fail
    sgoggins.usr.drop_student("akend3", "comp_sci")
    sgoggins.reload_data()
    sgoggins.users["akend3"]['courses']['comp_sci']

def test_submit_assignment(grading_system):
    username = "hdjsr7"
    password = "pass1234"
    grading_system.login(username, password)
    grading_system.usr.submit_assignment("databases", "assignment1", "Test", "3/1/2022")
    grading_system.reload_data()
    assert grading_system.users["hdjsr7"]["courses"]["databases"]["assignment1"]["submission"] == "Test"
    assert grading_system.users["hdjsr7"]["courses"]["databases"]["assignment1"]["submission_date"] == "3/1/2022"

def test_check_ontime(grading_system):
    #FAILS
    username = "hdjsr7"
    password = "pass1234"
    grading_system.login(username, password)
    assert grading_system.usr.check_ontime("1/6/2022", "3/1/2022") == False
    assert grading_system.usr.check_ontime("3/1/2022", "2/28/2022") == True

def test_check_grades(grading_system):
    username = "akend3"
    password = "123454321"
    grading_system.login(username, password)
    grades = grading_system.usr.check_grades("databases")
    assert grades[0][1] == 23
    assert grades[1][1] == 46

def test_view_assignments(grading_system):
    #FAILS
    username = "akend3"
    password = "123454321"
    grading_system.login(username, password)
    assignments = grading_system.usr.view_assignments("databases")
    # check due dates
    assert assignments[0][1] == "1/6/20"
    assert assignments[1][1] == "2/6/20"


## Designing my own tests

def test_drop_student_in_course_not_taught(sgoggins):
    # professors should not be able to alter student data for courses they don't teach
    # FAILS
    sgoggins.usr.drop_student("yted91", "cloud_computing")
    sgoggins.reload_data()
    assert sgoggins.users["yted91"]['courses'].get("cloud_computing", "N/A") != "N/A"

def test_create_assignment_in_course_not_taught(sgoggins):
    # professors and TAs should not be able to alter assignments for courses they don't teach
    # FAILS
    sgoggins.usr.create_assignment("assignment3", "3/2/20", "cloud_computing")
    sgoggins.reload_data()
    assert sgoggins.courses["cloud_computing"]["assignments"].get("assignment3", 'N/A') == 'N/A'

def test_check_grades_in_course_not_taught(grading_system):
    # professors and TAs should not be able to see grades for students and courses they don't teach
    # FAILS
    grading_system.login("saab", "boomr345")
    grades = grading_system.usr.check_grades("akend3", "databases")
    assert len(grades) == 0

def test_change_grade_in_course_not_taught(sgoggins):
    # professors and TAs should not be able to alter grades for students and courses they don't teach
    # FAILS
    sgoggins.usr.change_grade("hdjsr7", "cloud_computing", "assignment1", 0)
    sgoggins.reload_data()
    assert sgoggins.users["hdjsr7"]['courses']["cloud_computing"]["assignment1"]['grade'] != 0

def test_create_then_submit(sgoggins, grading_system):
    # a larger test
    # for whether a new assignment can be created by a professor then whether a student can submit in one test
    # FAILS
    sgoggins.usr.create_assignment("assignment4", "3/2/2022", "software_engineering")
    sgoggins.reload_data()
    grading_system.login("yted91", "imoutofpasswordnames")
    # key error!
    grading_system.usr.submit_assignment("software_engineering", "assignment4", "Test", "3/1/2022")
    assert grading_system.users["yted91"]["courses"]["software_engineering"]["assignment4"]["submission"] == "Test"
    assert grading_system.users["yted91"]["courses"]["software_engineering"]["assignment4"]["submission_date"] == "3/1/2022"






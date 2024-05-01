import random
from utils import *
from repository import StudentRepository
from dto import Student, Subject
from collections import defaultdict
from main import FormatCodes

def register_student():
    print(f"\t{FormatCodes.OKGREEN}Student Sign Up")
    is_valid = False
    email_id = input(f"\t{FormatCodes.ENDC}Email: ").lower() #formatcodes.endc is used to changing the default colour to terminal defaults because earlier we used green.
    password = input(f"\t{FormatCodes.ENDC}Password: ")
    if validate_regex(get_value("email"), email_id):
        if (validate_regex(get_value("password"), password)):
            is_valid = True
            print(f"\t{FormatCodes.WARNING}email and password formats acceptable")
        else:
            print(f"\t{FormatCodes.FAIL}Incorrect email or password Format")
    else:
        print(f"\t{FormatCodes.FAIL}Incorrect email or password Format")
    
    if(is_valid):
        first_name = input(f"\t{FormatCodes.ENDC}Name: ")
        repo = StudentRepository()
        student_id = 0 # It will be overwritten inside the function call. 
        new_student = Student(student_id,first_name,email_id,password,[])
        print(repo.add_student(new_student))
        return
    else: 
        register_student()

def login_student():
    print(f'\t{FormatCodes.OKGREEN}Student Sign In')
    email_id = input(f"\t{FormatCodes.ENDC}Email: ").lower()
    password = input(f"\t{FormatCodes.ENDC}Password: ")
    if validate_regex(get_value("email"), email_id):
        if (validate_regex(get_value("password"), password)):
            print(f"\t{FormatCodes.WARNING}email and password formats acceptable")
            repo = StudentRepository()
            logged_student = repo.login_student(email_id, password)
            if(logged_student is not None):
                while True:
                    choice = input(f"\t\t{FormatCodes.OKCYAN}Student Course Menu (c/e/r/s/x):{FormatCodes.ENDC} : ").lower()
                    if choice == 'c':
                        change_password(logged_student, repo)
                    elif choice == 'e':
                        enrol_subject(logged_student,repo)
                    elif choice == 'r':
                        remove_subject(logged_student,repo)
                    elif choice == 's':
                        show_subjects(logged_student, repo)
                    elif choice == 'x':
                        break
                    else:
                        print(f"\t\t{FormatCodes.FAIL}Invalid option, please try again.")
                        login_student()
            else:   
                print(f"\t{FormatCodes.FAIL}Student does not exist")
                login_student()
        else:
            print(f"\t{FormatCodes.FAIL}Incorrect email or password Format")
            login_student()
    else:
        print(f"\t{FormatCodes.FAIL}Incorrect email or password Format")
        login_student()
    

def enrol_subject(student,repo):
    subject_id = input(f"\t\t{FormatCodes.WARNING}Enrolling in Subject: ")
    is_valid = False 
    max_enrollement = 4
    if (len(student.subjects) >=4):
        print(f'\t\t{FormatCodes.FAIL}Students are allowed to enrol in {max_enrollement} subjects')
        login_student()
    elif(validate_subjectid(subject_id)):
        mark = random.randint(25, 100)
        if mark < 50 :
            grade = 'Z'
        elif 50 <= mark < 65:
            grade = 'P'
        elif 65 <= mark < 75:
            grade = 'C'
        elif 75 <= mark < 85:
            grade = 'D'
        else:
            grade = 'HD'
        subjects = student.subjects
        subjects.append(Subject(subject_id, mark, grade))
        repo.update_student(student.student_id, **{'subjects': subjects})
        is_valid = True
    else: 
        print(f"\t\t{FormatCodes.FAIL}Invalid Subject ID format")
    
    if is_valid:
        print(f"\t\t{FormatCodes.WARNING}You are now enrolled in {len(subjects)} out of {max_enrollement} subjects")
    else : 
        enrol_subject(student,repo)

def change_password(student,repo):
    print(f"\t\t{FormatCodes.WARNING}Updating Password")
    is_valid = False
    new_password = input(f'\t\t{FormatCodes.ENDC}New Password: ')
    confirm_new_password = input(f'\t\t{FormatCodes.ENDC}Confirm New Password: ')
    if (new_password==confirm_new_password):
        repo.update_student(student.student_id, **{'password': new_password})
        is_valid = True
    else:
        print(f"\t\t{FormatCodes.FAIL}Password do not match - try again")
        change_password(student,repo)

def remove_subject(student, repo):
    max_subjects = 4
    drop_subject_id = input(f'\t\t{FormatCodes.ENDC}Remove Subject by ID: ')
    print(f"\t\t{FormatCodes.WARNING}Dropping Subject - {drop_subject_id}")
    student.remove_subject(f"{drop_subject_id}")
    repo.update_student(student.student_id, **{'subjects': student.subjects})
    print(f"\t\t{FormatCodes.WARNING}You are now enrolled in {len(student.subjects)} out of {max_subjects} subjects")

def show_subjects(student, repo):
   print(f"\t\t{FormatCodes.WARNING}Showing {len(student.subjects)} subjects")
   for subject in student.subjects:
       print(f"\t\t{FormatCodes.ENDC}Subject::{subject.subject_id} -- mark = {subject.mark} -- grade = {subject.grade}")

def clear_database():
    print(f"\t\t{FormatCodes.WARNING} Clearing students database") 
    choice = input(f'\t\t{FormatCodes.FAIL}Are you sure you want to clear the database (Y)ES / (N)O: ').lower()
    if choice == 'y':
        with open('students.data', 'w') as file :
            pass

def grade_grouping():
    print(f"\t\t{FormatCodes.WARNING}Grade Grouping")
    repo = StudentRepository()
    grade_groups = defaultdict(list)
    for student in repo.students:
        full_name = f"{student.first_name.capitalize()}"
        for subject in student.subjects:
            student_info = f"{full_name} :: {student.student_id} -- GRADE: {subject.grade} - MARK: {subject.mark}"
            grade_groups[subject.grade].append(student_info)
    
    # Print the result grouped by grade
    for grade in sorted(grade_groups):
        print(f"\t\t{FormatCodes.ENDC}{grade} --> [{', '.join(grade_groups[grade])}]")

def pass_fail_distribution():
    print(f"\t\t{FormatCodes.WARNING}PASS/FAIL Partition")
    repo = StudentRepository()
    pass_groups = defaultdict(list)
    fail_groups = defaultdict(list)
    for student in repo.students:
        full_name = f"{student.first_name.capitalize()}"
        for subject in student.subjects:
            student_info = f"{full_name} :: {student.student_id} -- Subject ID: {subject.subject_id} -- GRADE: {subject.grade} - MARK: {subject.mark}"
            if subject.mark >= 50:
                pass_groups['Pass'].append(student_info)
            else:
                fail_groups['Fail'].append(student_info)
    
    # Print the result grouped by grade
    for mark in sorted(pass_groups):
        print(f"\t\t{FormatCodes.ENDC}Pass --> [{', '.join(pass_groups[mark])}]")
    for mark in sorted(fail_groups):
        print(f"\t\t{FormatCodes.ENDC}Fail --> [{', '.join(fail_groups[mark])}]")

def delete_student_by_id():
    repo = StudentRepository()
    student_id = input(f'\t\t{FormatCodes.ENDC}Remove by ID: ').lower()
    student_id = f"{int(student_id):06d}"
    print(repo.delete_student(student_id))

def display_students():
    print(f"\t\t{FormatCodes.WARNING}Student List")
    repo = StudentRepository()
    for student in repo.students:
        full_name = f"{student.first_name.capitalize()}"
        print(f"\t\t{FormatCodes.ENDC}{full_name} :: {student.student_id} -- Email: {student.email}")

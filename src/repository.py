from dto import Student
import json
from main import FormatCodes
class StudentRepository:
    def __init__(self, filename = 'students.data'):
        self.filename = filename
        self.students = []  
        self.students = self.load_students()
        self.id_gen = self.id_generator()

    def id_generator(self):
        # Start from the next number after the highest current ID
        current_max_id = max((int(student.student_id) for student in self.students), default=0)
        next_id = current_max_id + 1
        while next_id < 1000000:
            yield f"{next_id:06}"
            next_id += 1

    def add_student(self, student):
        if any(s.email == student.email for s in self.students):
            return f"\t{FormatCodes.FAIL}Student {student.first_name} {student.last_name} already exists"
        student.student_id =  next(self.id_gen)
        self.students.append(student)
        self.save_students()
        return f"\t{FormatCodes.OKGREEN}Student added successfully"

    def get_student(self, student_id):
        student_id = f"{student_id:06}"
        for student in self.students:
            if student.student_id == student_id:
                return student
        return "Student not found."

    def login_student(self, email_id, password, **kwargs):
        for student in self.students:
            if ((student.email == email_id) & (student.password == password)):
                return student
        return None


    def update_student(self, student_id, **kwargs):
        for student in self.students:
            if student.student_id == student_id:
                for key, value in kwargs.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                self.save_students()
                return "Student updated successfully."
        return "Student not found."

    def delete_student(self, student_id):
        for i, student in enumerate(self.students):
            if student.student_id == student_id:
                del self.students[i]
                self.save_students()
                return f"\t\t{FormatCodes.WARNING}Removing Student {student_id} Account"
        return f"\t\t{FormatCodes.FAIL}Student {student_id} does not exist"
    
    def save_students(self):
        with open(self.filename, 'w') as file :
            json.dump([student.to_dict() for student in self.students], file, indent=4)

    def load_students(self):
        try:
            with open(self.filename, 'r') as file:
                file_contents = file.read()
                if not file_contents:
                    return []
                data = json.loads(file_contents)
                return [Student(**student) for student in data]

        except FileNotFoundError:
            # If the file does not exist, create it and return an empty list
            self.save_students()
            return []
        
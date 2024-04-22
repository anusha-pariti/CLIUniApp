def dict_to_subject(subject_dict):
    return Subject(**subject_dict)


class Student:
    def __init__(self, student_id, first_name, last_name, email, password, subjects):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.subjects = [dict_to_subject(subj) if isinstance(subj, dict) else subj for subj in subjects]

    def __str__(self):
        return f"Student ID: {self.student_id}, Name: {self.first_name} {self.last_name}, Email: {self.email}, Subjects : {self.subjects}"
    
    def remove_subject(self, subject_id):
        self.subjects = [subject for subject in self.subjects if subject.subject_id != subject_id]

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "subjects": [subject.to_dict() for subject in self.subjects]
        }
    
class Subject:
    def __init__(self, subject_id, mark, grade):
        self.subject_id = subject_id
        self.mark = mark 
        self.grade = grade
    
    def __str__(self):
        return f"Subject ID: {self.subject_id}, Mark: {self.mark}, Grade: {self.grade}"
    
    def to_dict(self):
        return {
            "subject_id": self.subject_id,
            "mark": self.mark,
            "grade": self.grade
        }
    
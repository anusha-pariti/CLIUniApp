from services import *

# ANSI escape codes for colors and formatting
class FormatCodes:
    HEADER = '\033[95m'  # Purple
    OKBLUE = '\033[94m'  # Blue
    OKCYAN = '\033[96m'  # Cyan
    OKGREEN = '\033[92m'  # Green
    WARNING = '\033[93m'  # Yellow
    FAIL = '\033[91m'  # Red
    ENDC = '\033[0m'  # Reset to default
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main_menu():
    while True:
        choice = input(f"{FormatCodes.OKBLUE}{FormatCodes.BOLD}University System: (A)dmin, (S)tudent, or X{FormatCodes.ENDC} :").upper()

        if choice == 'A':
            admin_menu()
        elif choice == 'S':
            student_menu()
        elif choice == 'X':
            print(f"{FormatCodes.WARNING}{FormatCodes.BOLD}Thank You{FormatCodes.ENDC}")
            break
        else:
            print("Invalid option, please try again.")

def student_menu():
    while True:
        choice = input(f"\t{FormatCodes.OKCYAN}Student System (l/r/x):{FormatCodes.ENDC} : ").lower()
        if choice == 'l':
            login_student()
        elif choice == 'r':
            register_student()
        elif choice == 'x':
            break
        else:
            print("Invalid option, please try again.")


def admin_menu():
    while True :
        choice = input(f"\t{FormatCodes.OKCYAN}Admin System (c/g/p/r/s/x):{FormatCodes.ENDC} : ").lower()
        if choice == 'c':
            clear_database()
        elif choice == 'g':
            grade_grouping()
        elif choice == 'p':
            pass_fail_distribution()
        elif choice == 'r':
            delete_student_by_id()
        elif choice == 's':
            display_students()
        elif choice == 'x':
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main_menu()

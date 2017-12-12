from sync_database import *
from admin import *
from user import *


if __name__ == '__main__':
    sync_from_user()
    sync_from_main()
    sync_from_age()
    while True:
        print("\n\n******* WELCOME ********\n1.USER\n2.ADMIN\n3.EXIT")
        choice = check_input("enter the option :", 1)
        if choice == 1:
            user()
        elif choice == 2:
            admin()
            sync_to_main()
        elif choice == 3:
            print("***Thank You***")
            exit(0)
        else:
            print("---re_enter the choice_____")
            continue

def check_password():

    password = "secure123"


    enteredPass = input("Please enter your password: ")


    if enteredPass == password:
        print("Welcome!")
    else:
        print("Did you forget your password?")

def main():

    check_password()
    print("Thank you for using our system!")

if __name__ == "__main__":
    main()

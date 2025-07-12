
EMERGENCY_CONTACT = "911"
ORGANIZATION_PHONE = "123-456-7890"

def gather_profile():
    """
    Prompt the user for their details and print a formatted profile.
    """
    print("Hello! Welcome to our volunteer program.")
    print("Let's set up your profile.\n")
    

    phone_number = input("1) Your phone number: ")
    age_input = input("2) Your age: ")
    # Validate age is an integer
    try:
        age = int(age_input)
    except ValueError:
        print("That doesn't look like a number. I'll set your age to 18.")
        age = 18
    
    academic_background = input("3) Academic background (e.g., High School, College, etc.): ")
    availability = input("4) Availability (Weekdays, Weekends, or Both): ")


    print("\n" + "=" * 40)
    print("Volunteer Profile")
    print("=" * 40)
    print(f"• Phone Number       : {phone_number}")
    print(f"• Age                : {age}")
    print(f"• Academic Background: {academic_background}")
    print(f"• Availability       : {availability}")
    

    print("\nImportant Contacts")
    print("-" * 40)
    print(f"Emergency: {EMERGENCY_CONTACT}")
    print(f"Our Office: {ORGANIZATION_PHONE}")
    

    print("\nThank you for sharing your details! We're excited to have you on board.")

if __name__ == "__main__":
    gather_profile()

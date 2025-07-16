import random

def cake_order(size, *args, **kwargs):
    
    print("\nOrder Details:")
    print(f"- Cake Size: {size}")

    if args:
        print("- Cake Details:")
        for detail in args:
            print(f"  * {detail}")

    if kwargs:
        print("- Optional Details:")
        for key, value in kwargs.items():
            print(f"  * {key.capitalize()}: {value}")


if __name__ == "__main__":
    print("Welcome to the Cake Ordering System!\n")

    size = input("Enter cake size (small, medium, large): ").strip()

    print("\nEnter cake details (e.g., flavor, layers). Type 'done' when finished:")
    cake_details = []
    while True:
        detail = input("Detail: ").strip()
        if detail.lower() == "done":
            break
        if detail:
            cake_details.append(detail)

    print("\nEnter optional details (e.g., drinks=Juice, delivery=Home). Type 'done' when finished:")
    optional_details = {}
    while True:
        entry = input("Optional detail (key=value): ").strip()
        if entry.lower() == "done":
            break
        if "=" in entry:
            key, value = entry.split("=", 1)
            optional_details[key.strip()] = value.strip()
        else:
            print("Invalid format. Use key=value.")

    if "captain_reward" not in optional_details:
        reward = random.randint(3, 10)
        optional_details["captain_reward"] = f"{reward} USD"

    cake_order(size, *cake_details, **optional_details)

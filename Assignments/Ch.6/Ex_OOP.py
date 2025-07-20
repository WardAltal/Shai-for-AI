# Task 1 & 2: Shape, Rectangle, Circle with area and print_info methods

class Shape:
    def area(self):
        return 0

    def print_info(self):
        print(f"Shape: Unknown, Area: {self.area()}")

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def print_info(self):
        print(f"Shape: Rectangle, Width: {self.width}, Height: {self.height}, Area: {self.area()}")

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

    def print_info(self):
        print(f"Shape: Circle, Radius: {self.radius}, Area: {self.area()}")

# Task 3: BankAccount with encapsulation

class BankAccount:
    def __init__(self, account_number, initial_balance=0):
        self.__account_number = account_number
        self.__balance = initial_balance

    def get_account_number(self):
        return self.__account_number

    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited: {amount}, New Balance: {self.__balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
        elif amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew: {amount}, New Balance: {self.__balance}")
        else:
            print("Insufficient balance!")

# Task 4: Animal, Dog, Cat with speak()

class Animal:
    def speak(self):
        print("I don't know what I say!")

class Dog(Animal):
    def speak(self):
        print("Woof Woof!")

class Cat(Animal):
    def speak(self):
        print("Meow Meow!")

# Task 5: Polymorphic animal_speak function

def animal_speak(animal):
    animal.speak()

# Task 6: Car class with encapsulation for speed

class Car:
    def __init__(self, color):
        self.color = color
        self.__speed = 0

    def accelerate(self):
        self.__speed += 10
        print(f"Accelerated. Current speed: {self.__speed}")

    def get_speed(self):
        return self.__speed

# Example usage (optional for testing)

if __name__ == "__main__":
    print("--- Task 1 & 2 ---")
    r = Rectangle(5, 10)
    c = Circle(7)
    r.print_info()
    c.print_info()

    print("\n--- Task 3 ---")
    acc = BankAccount("12345678", 100)
    print(f"Account Number: {acc.get_account_number()}")
    print(f"Initial Balance: {acc.get_balance()}")
    acc.deposit(50)
    acc.withdraw(30)
    acc.withdraw(-90)
    acc.withdraw(200)

    print("\n--- Task 4 & 5 ---")
    x = Animal()
    dog = Dog()
    cat = Cat()
    animal_speak(x)
    animal_speak(dog)
    animal_speak(cat)

    print("\n--- Task 6 ---")
    car = Car("Black")
    print(f"Car Color: {car.color}")
    car.accelerate()
    car.accelerate()
    print(f"Current Speed: {car.get_speed()}")

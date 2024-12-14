# This script contains intentional code smells for testing purposes.

class SampleClass:
    def __init__(self, name, age, address, phone, email, job, salary):
        self.name = name
        self.age = age
        self.address = address
        self.phone = phone
        self.email = email
        self.job = job
        self.salary = salary

    def large_function(self):
        # A large function with many lines of code
        print("Starting large function")
        for i in range(10):  # Nested loop level 1
            for j in range(5):  # Nested loop level 2
                for k in range(3):  # Nested loop level 3
                    print(f"Processing {i}, {j}, {k}")
                    if i == 5:
                        if j == 2:
                            if k == 1:  # Deeply nested if-else blocks
                                print("Reached a critical condition")

        total = 0
        for i in range(100):  # Magic number
            total += i
        print("Total:", total)

        self.helper_function(1, 2, 3, 4, 5, 6)  # Too many arguments passed
        return total

    def helper_function(self, a, b, c, d, e, f):
        # Function with many parameters
        result = a + b + c + d + e + f
        return result

    def another_large_function(self):
        # A function with too many return statements
        if self.age < 18:
            return "Underage"
        elif self.age < 25:
            return "Youth"
        elif self.age < 40:
            return "Adult"
        elif self.age < 60:
            return "Middle-aged"
        else:
            return "Senior"

def utility_function():
    # A function with high cyclomatic complexity
    x = 5
    if x > 0:
        if x < 10:
            if x % 2 == 0:
                print("X is an even number less than 10")
            else:
                print("X is an odd number less than 10")
        else:
            print("X is greater than or equal to 10")
    else:
        print("X is non-positive")

    for i in range(10):  # Magic number
        for j in range(5):  # Nested loop
            print(i + j)

# Duplicate code blocks (intentional duplication)
def duplicate_block():
    print("This is a duplicate block")
    print("This is a duplicate block")
    print("This is a duplicate block")

def duplicate_block_2():
    print("This is a duplicate block")
    print("This is a duplicate block")
    print("This is a duplicate block")
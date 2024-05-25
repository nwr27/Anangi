class Person:
    def __init__(self, name, age, is_student):
        self.name = name
        self.age = age
        self.is_student = is_student

    def introduce(self):
        if self.is_student == False:
            addText=""
        else:
            addText=f"I am a student"
        return f"Hello, my name is {self.name} and I am {self.age} years old. {addText}"


# Membuat objek dari kelas Person
john = Person("John", 30, 1)

print(john.introduce())  # Output: Hello, my name is John and I am 30 years old.

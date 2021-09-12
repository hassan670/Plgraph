class Student:
    name = ""

    def __init__(self, name):
        self.name = name

    def print_(self):
        return self.name

if __name__=="__main__":
    S = Student("Hassan Mubiru")
    print()

from abc import ABC, abstractmethod

class Parent(ABC):

    def __init__(self):
        pass

    def run(self):
        self.check()

    @abstractmethod
    def check(self):
        pass


class Child(Parent):

    def check(self):
        print("test")

test = Child()
test.run()



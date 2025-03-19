import ZODB
import ZODB.FileStorage
import transaction
import persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOBTree  # Můžete použít místo PersistentMapping

# Define persistent classes (zůstává stejné)
class Person(persistent.Persistent):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.friends = PersistentList()
        self.address = PersistentMapping()

    def greet(self):
        print(f"Hello, my name is {self.name}")

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r}, friends={self.friends!r}, address={self.address!r})"


class Employee(Person):
    def __init__(self, name, age, position, salary):
        super().__init__(name, age)
        self.position = position
        self.salary = salary

    def raise_salary(self, percentage):
        self.salary += self.salary * (percentage / 100)

    def __repr__(self):
        return f"Employee(name={self.name!r}, age={self.age!r}, position={self.position!r}, salary={self.salary!r})"


if __name__ == '__main__':
    storage = ZODB.FileStorage.FileStorage('mydata.fs')
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root()
    
    if 'people' not in root:
        print("Initializing database...")
        root.people = PersistentMapping()

        john = Person("John Doe", 30)
        john.address['street'] = "123 Main St"
        john.address['city'] = "Anytown"
        root.people['john'] = john  # Ukládáme do root.people

        eva = Employee("Eva Dvořáková", 25, "Programmer", 50000)
        root.people['eva'] = eva  # Ukládáme do root.people

        transaction.commit()
        print("Database initialized.")
    else:
        print("Database already initialized.")

    connection.close()
    db.close()
    storage.close()
    print("Database initialization complete.")
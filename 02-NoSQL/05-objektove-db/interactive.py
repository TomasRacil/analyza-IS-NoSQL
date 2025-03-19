import ZODB
import ZODB.FileStorage
import transaction
import persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from init_db import Person, Employee

# --- Database connection ---
storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

print("Connected to ZODB database.")
print("Available objects:")
print("  - root (the root object)")
print("  - root.people (a dictionary of people and employees)")
print("  - Person (the Person class)")
print("  - Employee (the Employee class)")
print("  - transaction (the transaction manager)")
print("  - connection, db, storage (for advanced use)")
print("\nUse transaction.commit() to commit changes.")
print("Use transaction.abort() to abort changes.")
print("Use connection.close() to close the connection (when you're done).\n")
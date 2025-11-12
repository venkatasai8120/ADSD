import sqlite3

connection = None

# -----------------------------
# INITIALIZATION
# -----------------------------
def initialize(database_file):
    global connection
    connection = sqlite3.connect(database_file, check_same_thread=False)
    connection.execute("PRAGMA foreign_keys = 1")
    connection.row_factory = sqlite3.Row


# -----------------------------
# PETS
# -----------------------------
def get_pets():
    cursor = connection.cursor()
    cursor.execute("""
        SELECT pet.id, pet.name, pet.age, pet.owner, pet.kind_id,
               kind.name AS kind_name, kind.food, kind.sound
        FROM pet 
        JOIN kind ON pet.kind_id = kind.id
    """)
    pets = cursor.fetchall()
    pets = [dict(pet) for pet in pets]
    return pets


def get_pet(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pet WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row:
        return dict(row)
    return None


def create_pet(data):
    try:
        data["age"] = int(data.get("age", 0))
    except:
        data["age"] = 0
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO pet(name, age, kind_id, owner) VALUES (?,?,?,?)""",
        (data["name"], data["age"], data["kind_id"], data["owner"]),
    )
    connection.commit()


def update_pet(id, data):
    try:
        data["age"] = int(data.get("age", 0))
    except:
        data["age"] = 0
    cursor = connection.cursor()
    cursor.execute(
        """UPDATE pet SET name=?, age=?, kind_id=?, owner=? WHERE id=?""",
        (data["name"], data["age"], data["kind_id"], data["owner"], id),
    )
    connection.commit()


def delete_pet(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM pet WHERE id = ?", (id,))
    connection.commit()


# -----------------------------
# KINDS
# -----------------------------
def get_kinds():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM kind")
    kinds = cursor.fetchall()
    return [dict(kind) for kind in kinds]


def get_kind(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM kind WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row:
        return dict(row)
    return None


def create_kind(data):
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO kind(name, food, sound) VALUES (?,?,?)""",
        (data["name"], data["food"], data["sound"]),
    )
    connection.commit()


def update_kind(id, data):
    cursor = connection.cursor()
    cursor.execute(
        """UPDATE kind SET name=?, food=?, sound=? WHERE id=?""",
        (data["name"], data["food"], data["sound"], id),
    )
    connection.commit()


def delete_kind(id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM kind WHERE id = ?", (id,))
    connection.commit()


# -----------------------------
# TEST SETUP (optional)
# -----------------------------
def setup_test_database():
    initialize("test_pets.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS pet")
    cursor.execute("DROP TABLE IF EXISTS kind")

    cursor.execute("""
        CREATE TABLE kind (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            food TEXT,
            sound TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE pet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            kind_id INTEGER,
            age INTEGER,
            owner TEXT,
            FOREIGN KEY (kind_id) REFERENCES kind (id)
        )
    """)

    cursor.executemany(
        "INSERT INTO kind(name, food, sound) VALUES (?, ?, ?)",
        [("dog", "dogfood", "bark"), ("cat", "catfood", "meow")]
    )
    connection.commit()

    pets = [
        {"name": "dorothy", "kind_id": 1, "age": 9, "owner": "greg"},
        {"name": "suzy", "kind_id": 1, "age": 9, "owner": "greg"},
        {"name": "casey", "kind_id": 2, "age": 9, "owner": "greg"},
        {"name": "heidi", "kind_id": 2, "age": 15, "owner": "david"},
    ]
    for pet in pets:
        create_pet(pet)

    print("✅ Test database setup complete.")


# -----------------------------
# MANUAL TEST
# -----------------------------
if __name__ == "__main__":
    setup_test_database()
    pets = get_pets()
    print("Pets:", pets)
    kinds = get_kinds()
    print("Kinds:", kinds)
    print("done.")

import psycopg2
from connect import get_connection
import csv

# Create the phone_book table
conn = get_connection()
cur = conn.cursor()

sql_create_table = """
CREATE TABLE IF NOT EXISTS phone_book (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(15) NOT NULL
)
"""
cur.execute(sql_create_table)
conn.commit()
print("Table phone_book created")

# Insert a single contact
def insert_contact(name, phone):
    """Insert a single contact into phone_book"""
    sql = "INSERT INTO phone_book (name, phone) VALUES (%s, %s) RETURNING id;"
    cur.execute(sql, (name, phone))
    contact_id = cur.fetchone()[0]
    conn.commit()
    return contact_id

# Insert contacts from CSV
with open("contacts.csv", newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        name, phone = row
        cur.execute("INSERT INTO phone_book (name, phone) VALUES (%s, %s);", (name, phone))
conn.commit()
print("Contacts from CSV inserted")

# Query and show all contacts
def show_contacts():
    cur.execute("SELECT * FROM phone_book ORDER BY id;")
    rows = cur.fetchall()
    for r in rows:
        print(r)

print("All contacts:")
show_contacts()

# Update a contact
def update_contact(contact_id, name=None, phone=None):
    """Update name and/or phone for a contact by ID"""
    fields = []
    values = []
    if name:
        fields.append("name = %s")
        values.append(name)
    if phone:
        fields.append("phone = %s")
        values.append(phone)
    if not fields:
        return
    values.append(contact_id)
    sql = f"UPDATE phone_book SET {', '.join(fields)} WHERE id = %s"
    cur.execute(sql, tuple(values))
    conn.commit()
    print(f"Contact {contact_id} updated")

# Example: update contact ID 1
update_contact(1, phone="87011111111")

# Delete a contact
def delete_contact(contact_id):
    """Delete a contact by ID"""
    sql = "DELETE FROM phone_book WHERE id = %s"
    cur.execute(sql, (contact_id,))
    conn.commit()
    print(f"Contact {contact_id} deleted")

# Example: delete contact ID 2
# delete_contact(2)

# 7. Close cursor and connection
cur.close()
conn.close()
print("Database connection closed")
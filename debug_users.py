from app import create_app, db
from app.models.user import User
from app.models.battalion import Battalion
import sys

app = create_app()

with app.app_context():
    with open('debug_output.txt', 'w') as f:
        f.write("--- USERS ---\n")
        users = User.query.all()
        for u in users:
            f.write(f"User: {u.username}, ID: {u.id}, IsAdmin: {u.is_admin}, IsBnAdmin: {u.is_battalion_admin}, BnID: {u.battalion_id}\n")

        f.write("\n--- BATTALIONS ---\n")
        bns = Battalion.query.all()
        for b in bns:
            f.write(f"Bn Name: {b.name}, DB_ID: {b.id}, Bn_Number: {b.battalion_number}\n")
    print("Debug output written to debug_output.txt")

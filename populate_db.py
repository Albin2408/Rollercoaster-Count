import csv
from app import db, create_app
from models import Rollercoaster

app = create_app()

def populate_database():
    with app.app_context():
        with open('coaster_db.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                coaster = Rollercoaster(
                    name=row['coaster_name'],
                    location=row['Location'],
                    speed=row['Speed'],
                    status=row['Status'],
                    opening_date=row['Opening date'],
                    manufacturer=row['Manufacturer'],
                    model=row['Model'],
                    height=row['Height'],
                    cost=row['Cost'],
                    ridden=False,  # Set default value for 'ridden'
                    user_id=1  # Default user ID for now, you can change this later
                )
                db.session.add(coaster)
            db.session.commit()

if __name__ == "__main__":
    populate_database()
    print("Database populated!")

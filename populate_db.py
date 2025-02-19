import csv
from app import db, create_app
from models import Rollercoaster

app = create_app()

def populate_database():
    with app.app_context():
        with open('coaster_db.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    coaster = Rollercoaster(
                        name=row['coaster_name'],
                        location=row['Location'],
                        speed=row.get('speed_mph', None),
                        status=row.get('Status', 'Unknown'),
                        opening_date=row.get('opening_date_clean', None),
                        manufacturer=row.get('Manufacturer', 'Unknown'),
                        model=row.get('Model', None),
                        height=row.get('height_ft', None),
                        cost=row.get('Cost', None)
                    )
                    db.session.add(coaster)
                except KeyError as e:
                    print(f"Missing column in CSV: {e}")
            db.session.commit()
            print("Database populated successfully!")

if __name__ == "__main__":
    populate_database()

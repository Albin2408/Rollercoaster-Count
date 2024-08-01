from app import db, create_app

app = create_app()
app.app_context().push()

# Drop all tables to ensure the schema is updated
db.drop_all()
# Create all tables
db.create_all()
print("Database initialized!")

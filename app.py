from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)

    # Application Configurations
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Prevents unnecessary warnings

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import Models (Ensuring Tables Exist Before Running)
    from models import User, Rollercoaster

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Fetches user by ID

    # Register Blueprints (Routes)
    from routes import main
    app.register_blueprint(main)

    # Ensure database tables are created if they don't exist
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

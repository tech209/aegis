from flask import Flask
import os

def create_app():
    app = Flask(__name__, 
                template_folder=os.path.abspath("templates"), 
                static_folder=os.path.abspath("static"))  # ✅ Explicitly set static folder
    
    from app.routes import routes
    app.register_blueprint(routes)

    print("Flask is looking for static files in:", app.static_folder)  # Debugging line
    return app

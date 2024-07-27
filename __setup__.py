from flask import Flask
from dashboards import dashboards_bp
from notebooks import notebooks_bp

def setup(app: Flask):
    app.register_blueprint(dashboards_bp())
    app.register_blueprint(notebooks_bp())

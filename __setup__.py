from flask import Flask
from dashboards import dashboards_bp

def setup(app: Flask):
    print("aaa")
    app.register_blueprint(dashboards_bp())
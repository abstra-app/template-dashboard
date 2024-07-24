from flask import Blueprint
from .templates import page
from abstra.tables import select_by_id, select
from dataclasses import dataclass
from datetime import datetime
from dateutil.parser import parse

@dataclass
class Department:
    id: int
    name: str
    created_at: datetime

    @staticmethod
    def from_dict(d):
        return Department(d["id"], d["name"], parse(d["created_at"]))

    @property
    def people(self):
        return map(Person.from_dict, select("people", where={'department_id': self.id}))

    @staticmethod
    def all():
        return map(Department.from_dict, select("departments"))

@dataclass
class Person:
    id: int
    name: str
    department_id: int
    created_at: datetime

    @staticmethod
    def from_dict(d):
        return Person(d["id"], d["name"], d["department_id"], parse(d["created_at"]))

    def department(self):
        return Department.from_dict(select_by_id("departments", self.department_id))

def dashboards_bp():
    bp = Blueprint('dashboards', __name__, url_prefix='/dashboards')
    
    @bp.route('/')
    def index():
        departments = Department.all()
        return page.render(title="Dashboards", departments=departments)
    
    return bp
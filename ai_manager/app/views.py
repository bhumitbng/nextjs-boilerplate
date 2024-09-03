from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from . import appbuilder, db
from .models import Employee, PerformanceData, Goal

class EmployeeModelView(ModelView):
    datamodel = SQLAInterface(Employee)
    list_columns = ['name', 'email']

class PerformanceDataModelView(ModelView):
    datamodel = SQLAInterface(PerformanceData)
    list_columns = ['employee', 'date', 'performance_score', 'tasks_completed']

class GoalModelView(ModelView):
    datamodel = SQLAInterface(Goal)
    list_columns = ['employee', 'description']

appbuilder.add_view(EmployeeModelView, "Employees", icon="fa-users", category="Management")
appbuilder.add_view(PerformanceDataModelView, "Performance Data", icon="fa-chart-line", category="Management")
appbuilder.add_view(GoalModelView, "Goals", icon="fa-bullseye", category="Management")
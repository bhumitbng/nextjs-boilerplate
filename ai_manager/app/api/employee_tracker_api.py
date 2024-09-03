from flask_appbuilder.api import BaseApi, expose
from .. import appbuilder
from ..models import db, Employee, PerformanceData, Goal
from employee_tracker import EmployeeTracker
import pandas as pd

class EmployeeTrackerApi(BaseApi):
    tracker = EmployeeTracker()

    @expose('/performance', methods=['POST'])
    def add_performance(self):
        if not self.request.json:
            return self.response_400('Invalid data')
        
        data = self.request.json
        employee = db.session.query(Employee).get(data['employee_id'])
        if not employee:
            return self.response_404('Employee not found')
        
        performance_data = PerformanceData(
            employee=employee,
            date=data['date'],
            performance_score=data['metrics']['performance_score'],
            tasks_completed=data['metrics']['tasks_completed'],
            hours_worked=data['metrics'].get('hours_worked', 0)
        )
        db.session.add(performance_data)
        db.session.commit()
        
        self.tracker.add_performance_data(data['employee_id'], data['date'], data['metrics'])
        return self.response(200, {'status': 'success'})

    @expose('/predict/<int:employee_id>', methods=['GET'])
    def predict_performance(self, employee_id):
        employee = db.session.query(Employee).get(employee_id)
        if not employee:
            return self.response_404('Employee not found')
        
        performance_data = db.session.query(PerformanceData).filter_by(employee_id=employee_id).all()
        if not performance_data:
            return self.response_400('Not enough data for prediction')
        
        for pd in performance_data:
            self.tracker.add_performance_data(employee_id, pd.date.isoformat(), {
                'performance_score': pd.performance_score,
                'tasks_completed': pd.tasks_completed,
                'hours_worked': pd.hours_worked
            })
        
        self.tracker.train_model()
        future_dates = pd.date_range(start=performance_data[-1].date, periods=30)
        predictions = self.tracker.predict_performance(employee_id, future_dates)
        
        feature_importance = self.tracker.get_feature_importance()
        
        return self.response(200, {
            'predictions': predictions.to_dict(orient='records'),
            'feature_importance': feature_importance.to_dict(orient='records')
        })

appbuilder.add_api(EmployeeTrackerApi)
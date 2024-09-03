import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

class EmployeeTracker:
    def __init__(self):
        self.performance_data = pd.DataFrame()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='mean')

    def add_performance_data(self, employee_id, date, metrics):
        new_data = pd.DataFrame({'employee_id': [employee_id], 'date': [date], **metrics})
        self.performance_data = pd.concat([self.performance_data, new_data], ignore_index=True)

    def preprocess_data(self, data):
        # Convert date to numerical features
        data['date'] = pd.to_datetime(data['date'])
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.month
        data['day'] = data['date'].dt.day
        data = data.drop('date', axis=1)

        # One-hot encode categorical variables
        data = pd.get_dummies(data, columns=['employee_id'])

        # Impute missing values
        data = pd.DataFrame(self.imputer.fit_transform(data), columns=data.columns)

        # Scale numerical features
        numerical_columns = data.select_dtypes(include=[np.number]).columns
        data[numerical_columns] = self.scaler.fit_transform(data[numerical_columns])

        return data

    def train_model(self):
        if len(self.performance_data) < 10:
            raise ValueError("Not enough data to train the model")

        data = self.preprocess_data(self.performance_data.copy())
        X = data.drop('performance_score', axis=1)
        y = data['performance_score']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        print(f"Model trained. Train R2: {train_score:.2f}, Test R2: {test_score:.2f}")

    def predict_performance(self, employee_id, future_dates):
        if len(self.performance_data) < 10:
            raise ValueError("Not enough data to make predictions")

        future_data = pd.DataFrame({
            'employee_id': [employee_id] * len(future_dates),
            'date': future_dates
        })

        all_data = pd.concat([self.performance_data, future_data], ignore_index=True)
        processed_data = self.preprocess_data(all_data)

        future_processed_data = processed_data.iloc[-len(future_dates):]
        predictions = self.model.predict(future_processed_data.drop('performance_score', axis=1))

        return pd.DataFrame({'date': future_dates, 'predicted_score': predictions})

    def get_feature_importance(self):
        if not hasattr(self.model, 'feature_importances_'):
            raise ValueError("Model has not been trained yet")

        data = self.preprocess_data(self.performance_data.copy())
        feature_importance = pd.DataFrame({
            'feature': data.drop('performance_score', axis=1).columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        return feature_importance

# Usage example
tracker = EmployeeTracker()
tracker.add_performance_data('EMP001', '2023-01-01', {'performance_score': 85, 'tasks_completed': 10, 'hours_worked': 40})
tracker.add_performance_data('EMP001', '2023-02-01', {'performance_score': 88, 'tasks_completed': 12, 'hours_worked': 42})
# Add more data...

tracker.train_model()
future_dates = pd.date_range(start='2023-03-01', periods=30)
predictions = tracker.predict_performance('EMP001', future_dates)
print(predictions)

feature_importance = tracker.get_feature_importance()
print(feature_importance)
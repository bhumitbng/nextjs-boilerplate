from flask import Flask, jsonify, request
from flask_cors import CORS
from meeting_summarizer import MeetingSummarizer
from employee_tracker import EmployeeTracker

app = Flask(__name__)
CORS(app)

summarizer = MeetingSummarizer()
tracker = EmployeeTracker()

@app.route('/api/summarize', methods=['POST'])
def summarize_meeting():
    text = request.json['text']
    summary = summarizer.summarize_text(text)
    return jsonify({'summary': summary})

@app.route('/api/employee/performance', methods=['POST'])
def add_performance():
    data = request.json
    tracker.add_performance_data(data['employee_id'], data['date'], data['metrics'])
    return jsonify({'status': 'success'})

@app.route('/api/employee/predict/<employee_id>', methods=['GET'])
def predict_performance(employee_id):
    predictions = tracker.predict_performance(employee_id)
    return jsonify(predictions.to_dict(orient='records'))

@app.route('/api/team/performance', methods=['GET'])
def get_team_performance():
    # Mock data for now
    team_performance = [
        {'date': '2023-01', 'performance': 85},
        {'date': '2023-02', 'performance': 88},
        {'date': '2023-03', 'performance': 92},
    ]
    return jsonify(team_performance)

@app.route('/api/employee/<employee_id>', methods=['GET'])
def get_employee_data(employee_id):
    # Mock data for now
    performance_data = {'score': 88, 'tasksCompleted': 12}
    goals = [
        'Complete project X by end of Q2',
        'Improve communication skills',
        'Learn new technology Y',
    ]
    return jsonify({'performanceData': performance_data, 'goals': goals})

if __name__ == '__main__':
    app.run(debug=True)
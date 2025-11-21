from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# configuring the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tasks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# defining how a task is going to be stored in the db
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.description}>"

# create (or update) the db
with app.app_context():
    db.create_all()

# defining the api endpoints
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    description = data.get('description')

    # invalid requisition
    if not description:
        return jsonify({'error': 'Description is required'}), 400
    
    new_task = Task(description=description)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'description': new_task.description, 'completed': new_task.completed}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'description': task.description, 'completed': task.completed} for task in tasks])

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    task.completed = True
    db.session.commit()
    return jsonify({'id': task.id, 'description': task.description, 'completed': task.completed})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 204

if __name__ == '__main__':
    app.run(debug=True)
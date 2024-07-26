from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello')
def hello():
    new_user = User(name="User")
    db.session.add(new_user)
    db.session.commit()
    return 'Hello, User!'

@app.route('/goodbye')
def goodbye():
    user = User.query.filter_by(name="User").first()
    db.session.delete(user)
    db.session.commit()
    return 'Goodbye, User!'

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'name': user.name} for user in users]
    return jsonify(users_list)

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({'id': user.id, 'name': user.name})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/user', methods=['POST'])
def create_user():
    name = request.json.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'name': new_user.name}), 201

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'})
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


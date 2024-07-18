from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# [* INITIALIZES THE APP/DATABASE *]
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sensitivity.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
# [* MODELS FOR THE DATABASE *]
class Recoil_Param(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    x_sens = db.Column(db.Integer, unique=False, nullable=False)
    y_sens = db.Column(db.Integer, unique=False, nullable=False)
    smooth = db.Column(db.Float, unique=False, nullable=False)
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'x_sens': self.x_sens,
            'y_sens': self.y_sens,
            'smooth': self.smooth
        }
### [* API LOGIC STARTS HERE *] ###

@app.before_request
def create_tables():
    db.create_all()

@app.get('/api/get')
def get_obj():
    try:
        obj_list = Recoil_Param.query.all()
        return jsonify([obj.to_json() for obj in obj_list])
    except Exception as e:
        return jsonify({"message": str(e)}), 500
@app.get('/api/get/<int:id>')
def get_item(id):
    try:
        obj_list = Recoil_Param.query.all()
        return jsonify([obj.to_json() for obj in obj_list][id - 1])
    except Exception as e:
        print(e)


@app.get('/api/getbyname/<name>')
def get_item_by_name(name):
    try:
        obj_list = Recoil_Param.query.all()
        item = [obj.to_json() for obj in obj_list]
        for i in item:
            if i["name"] == name:
                return i


    except Exception as e:
        return jsonify({'message': 'Name not found'}), 400


@app.post('/api/post')
def post_obj():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid JSON"}), 400

    id = data.get('id')
    name = data.get('name')
    x_sens = data.get('x_sens')
    y_sens = data.get('y_sens')
    smooth = data.get('smooth')

    new_obj = Recoil_Param(id=id, name=name, x_sens=x_sens,y_sens=y_sens,smooth=smooth)
    try:
        db.session.add(new_obj)
        db.session.commit()
        return jsonify({
            'id': id,
            'name': name,
            'x_sens': x_sens,
            'y_sens': y_sens,
            'smooth': smooth,
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400

# [* Note to self change debug to false when deploying *]

if __name__ == "__main__":
    app.run(debug=True)
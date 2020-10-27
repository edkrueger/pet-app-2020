from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

app = Flask(__name__)

pets = []

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_CONN")

db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    age = db.Column(db.Integer)

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }

db.create_all()

@app.route("/")
def main():
    "The app is up!"

@app.route("/add_pet", methods=["POST"])
def add_pet():
    try:

        name = request.json.get("name")
        age = int(request.json.get("age"))
        new_pet = Pet(name=name, age=age)

        db.session.add(new_pet)
        db.session.commit()

        return {"msg": "Success"}

    except Exception as e:
        return {"error": str(e)}

@app.route("/update", methods=["POST"])
def update():

    try:
        pet_id = int(request.args.get("id"))

        new_age = request.json.get("age")
        new_name = request.json.get("name")

        pet = Pet.query.filter(Pet.id == pet_id).first()

        if new_age:
            pet.age = int(new_age)
        if new_name:
            pet.name = new_name

        db.session.commit()

        return {"msg": "Success"}
    
    except Exception as e:
        return {"error": str(e)}

@app.route("/delete_pet")
def delete_pet():

    try:
        pet_id = int(request.args.get("id"))

        pet = Pet.query.filter(Pet.id == pet_id).first()

        db.session.delete(pet)
        db.session.commit()
        
        return {"msg": "Success"}
    except Exception as e:
        return {"error": str(e)}


def show(min_age=None, max_age=None, name=None):
    
    q = Pet.query

    if min_age:
        q = q.filter(Pet.age >= int(min_age))

    if max_age:
        q = q.filter(Pet.age <= int(max_age))

    if name:
        q = q.filer(Pet.name == name)

    pets = q.all()
    return jsonify([pet.to_dict() for pet in pets])


@app.route("/search")
def query_by_age():

    min_age = request.args.get("min_age")
    max_age = request.args.get("max_age")
    name = request.args.get("name")

    q = Pet.query

    if min_age:
        q = q.filter(Pet.age >= int(min_age))

    if max_age:
        q = q.filter(Pet.age <= int(max_age))

    if name:
        q = q.filter(Pet.name == name)

    pets = q.all()
    return jsonify([pet.to_dict() for pet in pets])


if __name__ == "__main__":
    app.run(debug=True)


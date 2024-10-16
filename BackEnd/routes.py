from app import app,db
from flask import request, jsonify
from model import Friend


# get all friends
@app.route('/api/friends', methods=['GET'])
def get_friends():
    friends = Friend.query.all()
    return jsonify([friend.to_json() for friend in friends])


# create a friend
@app.route('/api/friends', methods=['POST'])
def create_friend():
    try:
        data = request.json

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")

        #set validation of the input fields
        if not name or not role or not description or not gender:
            return jsonify({"msg": "All fields are required"}), 400

        if len(name) > 100 or len(description) > 2000:
            return jsonify({"msg": "Invalid input"}), 400

        if gender not in ["male", "female"]:
            return jsonify({"msg": "Invalid gender"}), 400

        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None

        new_friend = Friend(name=name, role=role, description=description, gender=gender, img_url=img_url)

        db.session.add(new_friend)

        db.session.commit()

        return jsonify({"msg": "Friend created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500


#Delete a friend
@app.route('/api/friends/<int:friend_id>', methods=['DELETE'])
def delete_friend(friend_id):
    try:
        friend = Friend.query.get(friend_id)
        if friend is None:
            return jsonify({"msg": "Friend not found"}), 404

        db.session.delete(friend)
        db.session.commit()

        return jsonify({"msg": "Friend deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500


@app.route('/api/friends/<int:friend_id>', methods=['PATCH'])
def update_friend(friend_id):
    try:
        # Retrieve the friend object by ID
        friend = Friend.query.get(friend_id)
        if friend is None:
            return jsonify({"msg": "Friend not found"}), 404

        data = request.json

        # Extract fields from the request data
        name = data.get("name", friend.name)
        role = data.get("role", friend.role)
        description = data.get("description", friend.description)
        gender = data.get("gender", friend.gender)

        # Validate input fields
        if not name or not role or not description or not gender:
            return jsonify({"msg": "All fields are required"}), 400

        if len(name) > 100 or len(description) > 2000:
            return jsonify({"msg": "Invalid length input"}), 400

        if gender not in ["male", "female"]:
            return jsonify({"msg": "Invalid gender"}), 400

        # Update the friend's details
        friend.name = name
        friend.role = role
        friend.description = description
        friend.gender = gender
        
        # Commit the changes to the database
        db.session.commit()
        return jsonify({"msg": "Friend updated successfully"}), 200
    except Exception as e:
        # Roll back changes in case of error
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

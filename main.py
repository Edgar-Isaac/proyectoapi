from flask import jsonify,request
from flask_pymongo import pymongo
from app import create_app
from bson.json_util import dumps
import db_config as db

app = create_app()

@app.route('/api/stands/')
def show_stands():
    all_stands=dumps(list(db.db.stands_jojo.find()))
    return all_stands

@app.route('/api/stand/<string:tarot_number>',methods=['GET'])
def show_a_stand(tarot_number):
    stand=dumps(db.db.stands_jojo.find_one({"tarot_number":tarot_number}))
    if  stand == 'null':
        return jsonify({
            "status":400,
            "message":"Stand not found"
        })
    else: 
        return stand

@app.route('/api/new_stand/',methods=['POST'])
def add_new_stand():
    if len(request.json) == 5:

        db.db.stands_jojo.insert_one({
            "tarot_number": request.json["tarot_number"],
            "name":request.json["name"],
            "user_name":request.json["user_name"],
            "reference": request.json["reference"],
            "img": request.json["img"]
        })
    else:
        return jsonify({
            "ERROR":"ERROR",
            "message":f"{request.json['name']}You're missing something"
        

    })

    return jsonify({
        "status":200,
        "message": "A new Stand was added with success",
        "lenght":f"{len(request.json)}"
    })

@app.route('/api/stand/update/<string:tarot_number>/',methods=['PUT'])
def update_stand(tarot_number):
    if db.db.stands_jojo.find_one({'tarot_number':tarot_number}):
        db.db.stands_jojo.update_one({'tarot_number':tarot_number},
        {'$set':{
            "tarot_number": request.json["tarot_number"],
            "name":request.json["name"],
            "user_name":request.json["user_name"],
            "reference": request.json["reference"],
            "img": request.json["img"]    
        }})
    else:
        return jsonify ({'status':400, "message": f"Stand #{tarot_number} not found"})
    return jsonify ({'status':200, "message": f"The stand #{tarot_number} of the list was updated"})

@app.route('/api/stand/del/<string:tarot_number>/',methods=['DELETE'])
def delete_stand(tarot_number):
    if db.db.stands_jojo.find_one({'tarot_number':tarot_number}):
        db.db.stands_jojo.delete_one({'tarot_number':tarot_number})

    else:
        return jsonify ({'status':400, "message": f"Stand #{tarot_number} not found"})
    return jsonify({"status":200, "message": f"The stand #{tarot_number} was deleted"})

'''Token
@app.route('/api/token/<string:password>/',methods=['GET'])
def token(password):
    if db.db.stands_jojo.find_one({''}):
         return jsonify({
        "status":200,
        "message": "Access Succesful"})
    else:
        return jsonify ({'status':400, "message": f"Access Denied"})
'''
        
if __name__ == '__main__':
    app.run(load_dotenv=True,port=8080)
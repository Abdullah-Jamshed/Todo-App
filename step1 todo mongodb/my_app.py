from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo import ReturnDocument

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://AbdullahJamshed:Pakistan(1)@project-semla.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def getting_Tasks():
    tasks = mongo.db.tasks
    data = tasks.find({},{'_id':0})
    allTasks = []
    for task in data:
        allTasks.append(task)
    return jsonify(allTasks)



@app.route('/todo/api/v1.0/tasks/<id>', methods=['GET'])
def single_Task(id):
    tasks = mongo.db.tasks
    data = tasks.find_one({'id':int(id)},{'_id':0})
    # data['_id'] = str(data['_id'])
    if (data):
        return jsonify(data)
    return "id not found"
    



@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def adding_Task():
    data = request.get_json()
    tasks = mongo.db.tasks
    if (data != None):
        if 'id' in data:
            find_id = tasks.find_one({'id':int(data['id'])})
            if (find_id):
                return "id already taken"
            tasks.insert({'id':data['id'],'title':data['title'],'description':data['description'],'done':bool(data['done'])})
            return "task added"
    return "id error"




@app.route('/todo/api/v1.0/tasks/<id>', methods=['PUT'])
def updateTask(id):
    data = request.get_json()
    tasks = mongo.db.tasks
    find_id = tasks.find_one({'id':int(id)})
    if (find_id):
        update = False
        for i in data:
            if i != 'id':
                tasks.find_one_and_update({'id':int(id)},{'$set':{i:data[i]}},return_document=ReturnDocument.AFTER)
                update = True
        if (update):
            return "task updated"
        elif (update == False):
            return "cant update id"
    return "id not found"



@app.route('/todo/api/v1.0/tasks/<id>', methods=['DELETE'])
def deleteTask(id):
    tasks = mongo.db.tasks
    find_id = tasks.find_one({'id':int(id)})
    if (find_id):
        tasks.find_one_and_delete({'id':int(id)})
        return "task deleted"
    return "id not found"



if __name__ == '__main__':
    app.run(debug=True)
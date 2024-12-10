
from flask import Flask, request, jsonify, send_file, abort
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import base64
from difflib import SequenceMatcher
from io import BytesIO
from urllib.parse import quote_plus

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://192.168.0.101'])

# MongoDB Configuration
username = quote_plus("kadiridhanush143")
password = quote_plus("Dhanush@1438")
mongo_uri = f"mongodb+srv://kadiridhanush143:{password}@memu.ynm46.mongodb.net/myem?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
db = client['myem']
# Collections
event_images_collection = db['event_images']
bookings_collection = db['bookings']
agent_onboarding_collection = db['agent_onboarding']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files or 'event_type' not in request.form:
        return jsonify({'error': 'No image or event type provided'}), 400

    image = request.files['image']
    event_type = request.form['event_type']

    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    image_data = image.read()
    new_image = {
        'event_type': event_type,
        'image': image_data
    }

    event_images_collection.insert_one(new_image)
    return jsonify({'message': 'Image uploaded successfully'}), 200

@app.route('/images', methods=['GET'])
def get_images():
    event_type = request.args.get('event_type')
    if not event_type:
        return jsonify({'error': 'event_type query parameter is required'}), 400

    images = list(event_images_collection.find({'event_type': event_type}))
    images_list = [{'id': str(image['_id']), 'image_data': base64.b64encode(image['image']).decode('utf-8')} for image in images]

    return jsonify({'images': images_list})

@app.route('/images/<image_id>', methods=['GET'])
def get_image(image_id):
    image = event_images_collection.find_one({'_id': ObjectId(image_id)})
    if not image:
        return abort(404)

    return send_file(BytesIO(image['image']), mimetype='image/jpeg')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    email_address = request.args.get('email')
    if not email_address:
        return jsonify({'error': 'Email is required'}), 400

    agent = agent_onboarding_collection.find_one({'email_address': email_address})
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404

    all_bookings = list(bookings_collection.find())
    tasks_data = []
    
    tasks = list(bookings_collection.find({"agent_name": {"$regex": agent['full_name'], "$options": "i"}}))
    
    for task in tasks:
        tasks_data.append({
            '_id': str(task['_id']),
            **task
        })

    print(f"Fetched {len(tasks)} records for agent {agent['full_name']}")

    if not tasks:
        best_match_score, best_match_task = 0, None
        
        for booking in all_bookings:
            match_score = SequenceMatcher(None, agent["full_address"], booking["address"]).ratio()
            if match_score > best_match_score:
                best_match_score = match_score
                best_match_task = booking
        
        if best_match_score > 0.5:
            tasks.append(best_match_task)
        else:
            return jsonify({'error': 'No matching tasks found'}), 404

    tasks_data = [{
        '_id': str(task['_id']),
        **task
    } for task in tasks]

    return jsonify({'tasks': tasks_data}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)








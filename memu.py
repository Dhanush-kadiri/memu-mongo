
from flask import Flask, request, jsonify, send_file, abort,send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import base64
from difflib import SequenceMatcher
from io import BytesIO
from urllib.parse import quote_plus
import os

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://192.168.0.101','https://test1-inky-three.vercel.app'])

# # MongoDB Configuration
# username = quote_plus("kadiridhanush143")
# password = quote_plus("Dhanush@1438")
# mongo_uri = f"mongodb+srv://kadiridhanush143:{password}@memu.ynm46.mongodb.net/?retryWrites=true&w=majority&appName=Memu"



# client = MongoClient(mongo_uri)
# db = client['myem']

from urllib.parse import quote_plus
from pymongo import MongoClient

# MongoDB Configuration
username = quote_plus("kadiridhanush143")  # URL encode username if it has special characters
password = quote_plus("Dhanush@1438")  # URL encode password
mongo_uri = f"mongodb+srv://{username}:{password}@memu.ynm46.mongodb.net/?retryWrites=true&w=majority&appName=Memu"

client = MongoClient(
    mongo_uri,
    serverSelectionTimeoutMS=30000,  # default is 30s
    socketTimeoutMS=30000,
    connectTimeoutMS=30000
)

db = client['myem']


# MongoDB Collections
event_images_collection = db['event_images']
bookings_collection = db['bookings']
agent_onboarding_collection = db['agent_onboarding']
gallery_collection = db['our_gallery']
reviews_collection = db['reviews']
partners_collection = db['partners']



@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Memu API!'}), 200

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')



#Agent adding route
# @app.route('/agents', methods=['POST'])
# def add_agent():
#     try:
#         data = request.form
#         profile_photo = request.files.get('profile_photo')
#         aadhar_card = request.files.get('aadhar_card')
#         pan_card = request.files.get('pan_card')
#         bank_book = request.files.get('bank_book')

#         new_agent = {
#             'email_address': data['email_address'],
#             'full_name': data['full_name'],
#             'fathers_name': data['fathers_name'],
#             'age': int(data['age']),
#             'profession': data['profession'],
#             'full_address': data['full_address'],
#             'desired_password': data['desired_password'],
#             'profile_photo': profile_photo.read() if profile_photo else None,
#             'aadhar_card': aadhar_card.read() if aadhar_card else None,
#             'pan_card': pan_card.read() if pan_card else None,
#             'bank_book': bank_book.read() if bank_book else None
#         }

#         agent_onboarding_collection.insert_one(new_agent)
#         return jsonify({'message': 'Agent added successfully!'}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 400




@app.route('/agents', methods=['POST'])
def add_agent():
    try:
        print("Form data:", request.form)
        print("Files:", request.files)

        data = request.form
        profile_photo = request.files.get('profile_photo')
        aadhar_card = request.files.get('aadhar_card')
        pan_card = request.files.get('pan_card')
        bank_book = request.files.get('bank_book')

        required_fields = ['email_address', 'full_name', 'fathers_name', 'age', 'profession', 'full_address', 'desired_password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing field: {field}'}), 400

        new_agent = {
            'email_address': data['email_address'],
            'full_name': data['full_name'],
            'fathers_name': data['fathers_name'],
            'age': int(data['age']),
            'profession': data['profession'],
            'full_address': data['full_address'],
            'desired_password': data['desired_password'],
            'profile_photo': profile_photo.read() if profile_photo else None,
            'aadhar_card': aadhar_card.read() if aadhar_card else None,
            'pan_card': pan_card.read() if pan_card else None,
            'bank_book': bank_book.read() if bank_book else None
        }

        agent_onboarding_collection.insert_one(new_agent)
        return jsonify({'message': 'Agent added successfully!'}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 400




#getting all agents

# @app.route('/agents', methods=['GET'])
# def get_agents():
#     try:
#         # Fetch all agents from the MongoDB collection
#         agents = agent_onboarding_collection.find()

#         # Process the data and convert it into a response-friendly format
#         agents_data = [
#             {
#                 'id': str(agent['_id']),
#                 'email_address': agent.get('email_address'),
#                 'full_name': agent.get('full_name'),
#                 'fathers_name': agent.get('fathers_name'),
#                 'age': agent.get('age'),
#                 'profession': agent.get('profession'),
#                 'full_address': agent.get('full_address'),
#                 'desired_password': agent.get('desired_password'),
#                 'profile_photo': base64.b64encode(agent.get('profile_photo', b'')).decode('utf-8') if agent.get('profile_photo') else None,
#                 'aadhar_card': base64.b64encode(agent.get('aadhar_card', b'')).decode('utf-8') if agent.get('aadhar_card') else None,
#                 'pan_card': base64.b64encode(agent.get('pan_card', b'')).decode('utf-8') if agent.get('pan_card') else None,
#                 'other_govt_id': base64.b64encode(agent.get('other_govt_id', b'')).decode('utf-8') if agent.get('other_govt_id') else None
#             }
#             for agent in agents
#         ]

#         # Return the data as a JSON response
#         return jsonify({'agents': agents_data}), 200

#     except Exception as e:
#         # Return an error if something goes wrong
#         return jsonify({'error': str(e)}), 500



import traceback

@app.route('/agents', methods=['GET'])
def get_agents():
    try:
        agents = agent_onboarding_collection.find()

        agents_data = [
            {
                'id': str(agent['_id']),
                'email_address': agent.get('email_address'),
                'full_name': agent.get('full_name'),
                'fathers_name': agent.get('fathers_name'),
                'age': agent.get('age'),
                'profession': agent.get('profession'),
                'full_address': agent.get('full_address'),
                'desired_password': agent.get('desired_password'),
                'profile_photo': base64.b64encode(agent.get('profile_photo', b'')).decode('utf-8') if agent.get('profile_photo') else None,
                'aadhar_card': base64.b64encode(agent.get('aadhar_card', b'')).decode('utf-8') if agent.get('aadhar_card') else None,
                'pan_card': base64.b64encode(agent.get('pan_card', b'')).decode('utf-8') if agent.get('pan_card') else None,
                'bank_book': base64.b64encode(agent.get('bank_book', b'')).decode('utf-8') if agent.get('bank_book') else None
            }
            for agent in agents
        ]

        return jsonify({'agents': agents_data}), 200

    except Exception as e:
        traceback.print_exc()  
        return jsonify({'error': str(e)}), 500



# Event Image Route
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


# Booking Routes
@app.route('/book_call', methods=['POST', 'OPTIONS'])
def book_call():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json

    try:
        # Check if image data and task_id are provided
        image_data = None
        if 'image' in data and data['image']:
            image_data = base64.b64decode(data['image'])

        task_id = data.get('task_id')
        if not task_id:
            return jsonify({'error': 'Task ID is required'}), 400

        # Find the task by ID
        booking = bookings_collection.find_one({"_id": ObjectId(task_id)})
        if not booking:
            return jsonify({'error': 'Task not found'}), 404

        # Update the booking's image
        bookings_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"image": image_data}})

        return jsonify({"message": "Booking updated successfully!"}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@app.route('/customer_call_book', methods=['POST', 'OPTIONS'])
def book_new_call():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json

    try:
        # Decode image if present
        image_data = None
        if 'image' in data and data['image']:
            image_data = base64.b64decode(data['image'])

        # Extract form data from request
        name = data.get('name')
        age = data.get('age')
        address = data.get('address')
        mobile = data.get('mobile')
        alt_mobile = data.get('altMobile')
        event_type = data.get('eventType')
        event_place = data.get('eventPlace')
        event_date = data.get('eventDate')
        agent_name = data.get('agentName', None)

        # Validate essential fields
        if not all([name, age, address, mobile, event_type, event_place, event_date]):
            return jsonify({'error': 'All required fields must be filled!'}), 400

        # Create a new booking entry
        new_booking = {
            'name': name,
            'age': age,
            'address': address,
            'mobile': mobile,
            'alt_mobile': alt_mobile,
            'event_type': event_type,
            'event_place': event_place,
            'event_date': event_date,
            'agent_name': agent_name,
            'image': image_data
        }

        bookings_collection.insert_one(new_booking)

        return jsonify({"message": "New booking created successfully!", "booking_id": str(new_booking['_id'])}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


# Agent Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email_address = data.get('email')
    desired_password = data.get('password')

    agent = agent_onboarding_collection.find_one({"email_address": email_address, "desired_password": desired_password})

    if agent:
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


@app.route('/agent_profile', methods=['GET'])
def get_agent_profile():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email parameter is required'}), 400

    try:
        agent = agent_onboarding_collection.find_one({'email_address': email})
        if agent:
            profile_photo_base64 = base64.b64encode(agent['profile_photo']).decode('utf-8') if agent.get('profile_photo') else None
            return jsonify({
                'profile_photo': profile_photo_base64,
                'full_name': agent['full_name']
            }), 200
        else:
            return jsonify({'error': 'Agent not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Task Route
@app.route('/tasks', methods=['GET'])
def get_tasks():
    email_address = request.args.get('email')
    if not email_address:
        return jsonify({'error': 'Email is required'}), 400

    agent = agent_onboarding_collection.find_one({'email_address': email_address})
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404

    # Fetch all bookings and print for debugging
    all_bookings = list(bookings_collection.find())
    tasks_data = []

    tasks = list(bookings_collection.find({"agent_name": {"$regex": agent['full_name'], "$options": "i"}}))

    if not tasks:
        # Perform address matching
        agent_address = agent['full_address']
        best_match = None
        best_match_score = 0
        for booking in all_bookings:
            match_score = SequenceMatcher(None, agent_address, booking['address']).ratio()
            if match_score > best_match_score:
                best_match_score = match_score
                best_match = booking

        if best_match_score > 0.5:  # Assuming a threshold of 0.5 for a good match
            tasks = [best_match]

    tasks_data = [{'id': str(task['_id']), 'name': task['name'], 'event_type': task['event_type']} for task in tasks]

    return jsonify({'tasks': tasks_data}), 200


# Gallery Routes
@app.route('/gallery', methods=['POST'])
def update_gallery():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    description = request.form.get('description', '')

    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    image_data = image.read()
    new_gallery_item = {
        'image': image_data,
        'description': description
    }
    gallery_collection.insert_one(new_gallery_item)
    return jsonify({'message': 'Image uploaded successfully'}), 200


@app.route('/gallery', methods=['GET'])
def get_gallery():
    images = gallery_collection.find()
    images_list = [{'id': str(img['_id']), 'image_data': base64.b64encode(img['image']).decode('utf-8'), 'description': img.get('description')} for img in images]
    return jsonify({'images': images_list})


# Reviews Routes
@app.route('/reviews', methods=['POST'])
def add_review():
    if request.content_type.startswith('multipart/form-data'):
        name = request.form['name']
        event_type = request.form['event_type']
        description = request.form['description']
        rating = request.form['rating']
        image = request.files['image'].read() if 'image' in request.files else None

        new_review = {
            'name': name,
            'event_type': event_type,
            'description': description,
            'rating': rating,
            'image': image
        }
        reviews_collection.insert_one(new_review)
        return jsonify({'message': 'Review added successfully'}), 201
    else:
        return jsonify({'error': 'Unsupported Media Type'}), 415



@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = reviews_collection.find()
    reviews_list = [
        {
            'id': str(review['_id']),
            'name': review['name'],
            'event_type': review['event_type'],
            'description': review['description'],
            'rating': review['rating'],
            'image': base64.b64encode(review['image']).decode('utf-8') if review.get('image') else None
        }
        for review in reviews
    ]
    return jsonify({'reviews': reviews_list})


# Partners Routes
@app.route('/partners', methods=['POST'])
def add_partner():
    partner_name = request.form['partner_name']
    age = request.form['age']
    experience = request.form['experience']
    department = request.form['department']
    address = request.form['address']
    pic = request.files['pic'].read() if 'pic' in request.files else None

    new_partner = {
        'partner_name': partner_name,
        'age': age,
        'experience': experience,
        'department': department,
        'pic': pic,
        'address': address
    }

    partners_collection.insert_one(new_partner)

    return jsonify({'message': 'Partner added successfully!'}), 201


@app.route('/partners', methods=['GET'])
def get_partners():
    department = request.args.get('department')
    if department:
        partners = partners_collection.find({'department': department})
    else:
        partners = partners_collection.find()

    partners_list = [
        {
            'id': str(partner['_id']),
            'partner_name': partner['partner_name'],
            'age': partner['age'],
            'experience': partner['experience'],
            'department': partner['department'],
            'pic': base64.b64encode(partner['pic']).decode('utf-8') if partner.get('pic') else None,
            'address': partner['address']
        }
        for partner in partners
    ]
    return jsonify({'partners': partners_list})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)








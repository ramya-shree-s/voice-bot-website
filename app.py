from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import requests
import json
import os
import re

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voicebot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# WORKING GROQ API INTEGRATION
def query_groq_api(message):
    """Direct Groq API call with proper error handling"""
    
    # Your Groq API key - replace this with your actual key
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    if not GROQ_API_KEY:
        print("❌ No Groq API key found")
        return None
    
    try:
        print(f"🚀 Calling Groq API with message: '{message}'")
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are VoiceBot, a helpful AI assistant. Give informative, engaging responses. Keep responses concise but informative (2-3 sentences maximum). Be friendly and conversational."
                },
                {
                    "role": "user", 
                    "content": message
                }
            ],
            "max_tokens": 150,
            "temperature": 0.7,
            "top_p": 1,
            "stream": False
        }
        
        print(f"📡 Making request to Groq...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📊 Groq Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Groq Raw Response: {result}")
            
            if 'choices' in result and len(result['choices']) > 0:
                ai_response = result['choices'][0]['message']['content'].strip()
                print(f"🎉 SUCCESS! Groq Response: {ai_response}")
                return ai_response
            else:
                print("❌ No choices in Groq response")
                return None
                
        elif response.status_code == 401:
            print("❌ Groq API: Invalid API key")
            return None
        elif response.status_code == 429:
            print("⏳ Groq API: Rate limit exceeded")
            return None
        else:
            print(f"❌ Groq API Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Groq API: Request timeout")
        return None
    except requests.exceptions.RequestException as e:
        print(f"🌐 Groq API: Request error - {e}")
        return None
    except Exception as e:
        print(f"💥 Groq API: Unexpected error - {e}")
        return None

def generate_smart_response(message):
    """Generate AI response with Groq API"""
    print(f"\n{'='*50}")
    print(f"🧠 PROCESSING: '{message}'")
    print(f"{'='*50}")
    
    # First, always try Groq API
    groq_response = query_groq_api(message)
    
    if groq_response:
        print(f"✅ Using GROQ response: {groq_response}")
        return groq_response
    
    # Only use fallback if Groq completely fails
    print("🔄 Groq failed, using enhanced fallback...")
    return generate_enhanced_fallback(message)

def generate_enhanced_fallback(message):
    """Enhanced fallback responses"""
    message = message.lower().strip()
    user_name = session.get('user_name', 'friend')
    
    # Machine Learning specific response
    if 'machine learning' in message or 'ml' in message:
        return f"Machine learning is a type of artificial intelligence where computers learn patterns from data without being explicitly programmed. It's like teaching a computer to recognize patterns and make predictions based on examples, similar to how humans learn from experience!"
    
    # AI related questions
    if any(word in message for word in ['artificial intelligence', 'ai', 'robot', 'automation']):
        return f"Artificial Intelligence is fascinating! It's technology that enables machines to simulate human intelligence - learning, reasoning, and problem-solving. From voice assistants like me to recommendation systems, AI is everywhere around us today."
    
    # Technology questions
    if any(word in message for word in ['technology', 'computer', 'programming', 'coding']):
        return f"Technology is constantly evolving! Whether it's programming languages, software development, or emerging tech like quantum computing, there's always something exciting happening. What specific area interests you most, {user_name}?"
    
    # Science questions
    if any(word in message for word in ['science', 'physics', 'chemistry', 'biology']):
        return f"Science helps us understand the world around us! From the smallest atoms to the vast universe, scientific discoveries constantly amaze me. What scientific topic would you like to explore together?"
    
    # Learning questions
    if any(word in message for word in ['learn', 'study', 'education', 'school', 'university']):
        return f"Learning is a lifelong journey, {user_name}! Whether you're studying for school, picking up new skills, or exploring hobbies, I'm here to help however I can. What would you like to learn about?"
    
    # Work/Career questions
    if any(word in message for word in ['work', 'job', 'career', 'profession']):
        return f"Career development is important! Whether you're job searching, skill building, or planning your next move, having clear goals helps. What aspect of your career interests you most right now?"
    
    # Default intelligent responses
    intelligent_defaults = [
        f"That's a thought-provoking question, {user_name}! While I'd love to give you a more detailed answer, I find these topics really interesting to discuss. What's your perspective on this?",
        f"I appreciate you asking about that! It's the kind of topic that could lead to a great conversation. What made you curious about this particular subject?",
        f"Interesting question! While I might not have all the specific details, I enjoy exploring ideas together. What aspects of this topic interest you most?",
        f"That's worth thinking about, {user_name}! I find it fascinating when people ask thoughtful questions like this. Have you been researching this topic recently?"
    ]
    
    return random.choice(intelligent_defaults)

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please provide both email and password.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([name, email, password]):
            flash('Please fill out all fields.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'error')
            return render_template('register.html')
        
        user = User(name=name, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    recent_chats = ChatHistory.query.filter_by(user_id=session['user_id']).order_by(ChatHistory.timestamp.desc()).limit(10).all()
    
    return render_template('dashboard.html', user=user, recent_chats=recent_chats)

@app.route('/voicebot')
def voicebot():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('voicebot.html')

@app.route('/api/process_message', methods=['POST'])
def process_message():
    print(f"\n{'🎯'*20}")
    print("NEW MESSAGE RECEIVED")
    print(f"{'🎯'*20}")
    
    if 'user_id' not in session:
        print("❌ User not authenticated")
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Get the JSON data
        data = request.get_json()
        if not data:
            print("❌ No JSON data received")
            return jsonify({'error': 'No data provided'}), 400
            
        user_message = data.get('message', '').strip()
        print(f"📝 User Message: '{user_message}'")
        
        if not user_message:
            print("❌ Empty message")
            return jsonify({'error': 'Empty message'}), 400
        
        # Generate AI response
        print("🤖 Generating response...")
        bot_response = generate_smart_response(user_message)
        print(f"🎭 Final Response: '{bot_response}'")
        
        # Save to database
        chat = ChatHistory(
            user_id=session['user_id'],
            user_message=user_message,
            bot_response=bot_response
        )
        db.session.add(chat)
        db.session.commit()
        print("💾 Saved to database")
        
        return jsonify({
            'response': bot_response,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
        
    except Exception as e:
        print(f"💥 ERROR in process_message: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Server error'}), 500

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    chat_count = ChatHistory.query.filter_by(user_id=session['user_id']).count()
    
    return render_template('profile.html', user=user, chat_count=chat_count)

@app.route('/api/ai_status')
def ai_status():
    """Check AI service status"""
    groq_key = os.getenv('GROQ_API_KEY', '')
    
    status = {
        'groq': bool(groq_key),
        'openrouter': False,
        'huggingface': False,
        'fallback_mode': not bool(groq_key)
    }
    
    print(f"🔍 AI Status Check: {status}")
    return jsonify(status)

@app.route('/api/test_groq')
def test_groq():
    """Test endpoint for Groq API"""
    test_response = query_groq_api("Hello, can you hear me?")
    return jsonify({
        'success': bool(test_response),
        'response': test_response,
        'api_key_present': bool(os.getenv('GROQ_API_KEY'))
    })

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
@app.route('/admin/database')
def view_database():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    users = User.query.all()
    chats = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).limit(50).all()
    
    html = """
    <h2>Database Contents</h2>
    <h3>Users:</h3>
    <table border="1">
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Created</th></tr>
    """
    for user in users:
        html += f"<tr><td>{user.id}</td><td>{user.name}</td><td>{user.email}</td><td>{user.created_at}</td></tr>"
    
    html += """
    </table>
    <h3>Recent Chats:</h3>
    <table border="1">
        <tr><th>User ID</th><th>Message</th><th>Response</th><th>Time</th></tr>
    """
    for chat in chats:
        html += f"<tr><td>{chat.user_id}</td><td>{chat.user_message[:50]}...</td><td>{chat.bot_response[:50]}...</td><td>{chat.timestamp}</td></tr>"
    
    html += "</table>"
    return html

if __name__ == '__main__':
    print(f"\n{'🤖'*20}")
    print("VOICEBOT SERVER STARTING")
    print(f"{'🤖'*20}")
    print("🌐 URL: http://127.0.0.1:5000")
    print("🔧 Debug Mode: ON")
    
    # Check API key on startup
    groq_key = os.getenv('GROQ_API_KEY', '')
    print(f"🔑 Groq API Key: {'✅ Present' if groq_key else '❌ Missing'}")
    
    if groq_key:
        print("🚀 AI Mode: GROQ API ENABLED")
    else:
        print("🔄 AI Mode: FALLBACK ONLY")
        print("💡 Add GROQ_API_KEY to environment for better responses")
    
    print(f"{'='*50}")
    app.run(debug=True, port=5000)
# AI Voice Bot Web Application

An intelligent voice-enabled chatbot web application with user authentication, real-time AI responses, and a modern animated interface.

## Features

### Core Functionality
- **Voice Recognition**: Real-time speech-to-text input
- **AI-Powered Responses**: Intelligent conversations using Groq LLaMA API
- **Text-to-Speech**: Bot responses spoken aloud
- **User Authentication**: Secure registration and login system
- **Chat History**: Persistent conversation storage
- **Responsive Design**: Works on desktop and mobile devices

### User Interface
- **Animated Robot Character**: Interactive 3D-style robot with emotions
- **Modern Dark Theme**: Gradient backgrounds with glassmorphism effects
- **Real-time Status Indicators**: Visual feedback for listening/thinking states
- **Smooth Animations**: Floating particles and smooth transitions

### Technical Features
- **Multi-page Application**: Separate login, dashboard, chat, and profile pages
- **SQLite Database**: Local data persistence
- **Session Management**: Secure user sessions
- **API Integration**: Multiple AI service fallbacks
- **Error Handling**: Comprehensive error management

## Technology Stack

### Frontend
- **HTML5**: Semantic markup and structure
- **CSS3**: Advanced styling with animations and responsive design
- **JavaScript (ES6)**: Voice recognition, DOM manipulation, and API calls
- **Web Speech API**: Browser-based speech recognition and synthesis

### Backend
- **Python 3.7+**: Core programming language
- **Flask**: Lightweight web framework
- **SQLAlchemy**: Database ORM
- **Werkzeug**: Password hashing and security

### Database
- **SQLite**: Embedded database for development
- **Two-table schema**: Users and chat history

### AI Integration
- **Groq API**: Primary AI service (LLaMA models)
- **OpenRouter API**: Secondary AI service
- **HuggingFace API**: Tertiary AI service
- **Enhanced Fallbacks**: Intelligent local responses

## Installation

### Prerequisites
- Python 3.7 or higher
- Modern web browser with microphone access

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-voice-bot.git
   cd ai-voice-bot
   ```

2. **Install dependencies**
   ```bash
   pip install Flask Flask-SQLAlchemy Werkzeug python-dotenv requests
   ```

3. **Set up environment variables**
   
   Create a `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   SECRET_KEY=your-secret-key-for-sessions
   ```

4. **Get API Keys** (Optional but recommended)
   - **Groq API**: Get free key at [console.groq.com](https://console.groq.com/keys)
   - **OpenRouter**: Get free key at [openrouter.ai](https://openrouter.ai/keys)
   - **HuggingFace**: Get free key at [huggingface.co](https://huggingface.co/settings/tokens)

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://127.0.0.1:5000`

## Usage

### Getting Started
1. Register a new account or login
2. Navigate to the Voice Chat page
3. Allow microphone permissions when prompted
4. Click the microphone button or type messages to chat

### Voice Commands
- Click the blue microphone button to start voice input
- Speak clearly and wait for the transcription
- The bot will respond with both text and speech

### Chat Features
- Type messages in the text input field
- View conversation history on the dashboard
- Access user profile and statistics

## Project Structure

```
ai-voice-bot/
├── app.py                 # Main Flask application
├── voicebot.db           # SQLite database (auto-generated)
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── voicebot.html     # Main chat interface
│   └── profile.html      # User profile page
├── .env                  # Environment variables (create this)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Application Pages
- `GET /` - Home (redirects to dashboard if logged in)
- `GET /dashboard` - User dashboard
- `GET /voicebot` - Main chat interface
- `GET /profile` - User profile

### API Endpoints
- `POST /api/process_message` - Process user messages
- `GET /api/ai_status` - Check AI service status
- `GET /api/test_api` - Test AI API connection

## Database Schema

### Users Table
- `id` (Integer, Primary Key)
- `name` (String, 100 chars)
- `email` (String, 120 chars, Unique)
- `password_hash` (String, 200 chars)
- `created_at` (DateTime)

### Chat History Table
- `id` (Integer, Primary Key)
- `user_id` (Integer, Foreign Key)
- `user_message` (Text)
- `bot_response` (Text)
- `timestamp` (DateTime)

## Configuration

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key for AI responses
- `OPENROUTER_API_KEY`: Your OpenRouter API key (optional)
- `HUGGING_FACE_API_KEY`: Your HuggingFace API key (optional)
- `SECRET_KEY`: Flask session secret key

### AI Service Priority
1. **Groq API** (Primary - fastest and most reliable)
2. **OpenRouter API** (Secondary)
3. **HuggingFace API** (Tertiary)
4. **Enhanced Fallbacks** (Local intelligent responses)

## Browser Compatibility

### Fully Supported
- Google Chrome 70+
- Microsoft Edge 79+
- Safari 14+

### Partial Support
- Firefox 60+ (limited voice features)
- Mobile browsers (touch interface)

## Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing
- **Session Management**: Secure Flask sessions
- **Input Validation**: Server-side input sanitization
- **Authentication Guards**: Protected routes require login
- **CORS Protection**: Same-origin policy enforcement

## Performance Considerations

- **Efficient Database Queries**: Optimized SQLAlchemy queries
- **API Timeout Handling**: 30-second timeouts for external APIs
- **Client-side Caching**: Minimal API calls through smart caching
- **Responsive Loading**: Progressive enhancement for slow connections

## Troubleshooting

### Common Issues

**Voice recognition not working:**
- Check microphone permissions in browser
- Ensure HTTPS or localhost (required for Web Speech API)
- Try Google Chrome or Microsoft Edge

**AI responses are generic:**
- Verify API keys are correctly set
- Check API key validity and quotas
- Review console logs for API errors

**Database errors:**
- Ensure SQLite file permissions are correct
- Delete `voicebot.db` to reset database
- Check Python SQLAlchemy installation

**Session/login issues:**
- Clear browser cookies
- Check SECRET_KEY is set
- Verify Flask session configuration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Groq** for providing fast and reliable AI API
- **Flask** community for excellent documentation
- **Web Speech API** for browser-based voice recognition
- **SQLAlchemy** for robust database management

## Future Enhancements

- Multi-language support
- Voice customization options
- Chat export functionality
- Admin dashboard
- Real-time typing indicators
- Message reactions and favorites
- Dark/light theme toggle
- Advanced conversation analytics

## Support

For support, issues, or questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

---

**Note**: This application requires an active internet connection for AI features and microphone access for voice functionality.

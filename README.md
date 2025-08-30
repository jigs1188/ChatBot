# ChatBot

A conversational AI assistant (Snello) that helps manage to-do lists through natural language interaction using Flask, LangChain, and Google's Gemini API.

[![Stars](https://img.shields.io/github/stars/jigs1188/ChatBot)](https://github.com/jigs1188/ChatBot/stargazers)
[![Issues](https://img.shields.io/github/issues/jigs1188/ChatBot)](https://github.com/jigs1188/ChatBot/issues)

## Features
- Natural language conversation interface with AI assistant
- To-do list management through chat commands (add, remove, list tasks)
- Persistent storage of conversation history and tasks
- Tool-calling capabilities with LangChain agents
- Redis-based session management for scalability
- Web-based chat interface with real-time responses
- Google Gemini 1.5 Flash integration for intelligent responses

## Tech Stack
- **Backend**: Python 3, Flask
- **AI Framework**: LangChain, Google Gemini 1.5 Flash API
- **Storage**: Redis (for session data), JSON (local storage)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Gunicorn, Render.com ready
- **Dependencies**: python-dotenv, langchain-google-genai, redis, rq

## Getting Started

Prerequisites
- Python 3.7+ and pip
- Redis server (local or cloud)
- Google API key for Gemini

Install
```bash
git clone https://github.com/jigs1188/ChatBot
cd ChatBot
pip install -r requirements.txt
```

Run
```bash
# Development (local)
python main.py

# Production (with Gunicorn)
gunicorn main:app
```

Build
```bash
# No build step required for Python Flask application
# Dependencies are installed via pip
```

Test
```bash
# No formal test suite currently available
# Manual testing via web interface at http://127.0.0.1:5000
```

## Configuration

Environment Variables
Copy `.env.example` to `.env` and fill in your actual values:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

Example `.env` file:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
REDIS_URL=redis://localhost:6379
```

Google Gemini API Setup
1. Visit [Google AI Studio](https://makersuite.google.com/)
2. Create a new API key
3. Add it to your `.env` file
4. Never commit real API keys to public repositories

Redis Configuration
- Local development: Install Redis and run `redis-server`
- Production: Use Redis service (Redis Cloud, AWS ElastiCache, etc.)
- The app will connect using the `REDIS_URL` environment variable

## Project Structure
```
.
├── main.py                 # Flask application entry point
├── app/
│   ├── __init__.py
│   ├── agent.py           # LangChain agent setup and LLM configuration
│   └── tools.py           # Custom tools (add_todo, remove_todo, etc.)
├── templates/
│   └── index.html         # Web chat interface
├── static/
│   ├── script.js          # Frontend JavaScript for chat functionality
│   └── style.css          # Chat interface styling
├── storage.json           # Local JSON storage for conversation history
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku/render deployment config
├── render.yaml           # Render.com deployment config
└── README.md
```

## Usage

Development
1. Start Redis server: `redis-server`
2. Run the Flask app: `python main.py`
3. Open browser to `http://127.0.0.1:5000`
4. Chat with Snello to manage your to-do list

Production Deployment
- **Render.com**: Configured via `render.yaml`
- **Heroku**: Configured via `Procfile`
- Ensure environment variables are set in your deployment platform

Example Conversation
```
You: Hi there!
Snello: Hi! I'm Snello, your friendly to-do list assistant. What's your name?

You: My name is John. Can you add "Buy groceries" to my to-do list?
Snello: Nice to meet you, John! I've added "Buy groceries" to your to-do list.

You: What's on my list?
Snello: Here's your current to-do list:
1. Buy groceries
```

## Troubleshooting
- **API Quota Exceeded**: Google Gemini free tier has daily limits. Upgrade to paid tier or wait for quota reset
- **Redis Connection Error**: Ensure Redis server is running locally or check REDIS_URL in production
- **Module Import Errors**: Run `pip install -r requirements.txt` to install all dependencies
- **CORS/Frontend Issues**: Clear browser cache and restart Flask development server
- **Environment Variables Not Loading**: Verify `.env` file exists and contains valid API keys
- **Chat Not Responding**: Check browser console for JavaScript errors and Flask logs for backend issues

## Roadmap
- [ ] Add unit and integration tests
- [ ] Implement user authentication and multi-user support
- [ ] Add more sophisticated task management (due dates, priorities)
- [ ] Integrate with external calendar APIs
- [ ] Add voice input/output capabilities
- [ ] Implement streaming responses for better UX

## Contributing
Issues and PRs are welcome. Please keep changes small and focused with helpful descriptions and screenshots for UI changes.

Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate documentation
4. Ensure the app still runs locally
5. Submit a pull request

## License
No license specified. Consider adding a LICENSE file (e.g., MIT, GPL) to clarify usage permissions.

## Contact
- Jignesh Parmar (jigs1188) — parmarjigs1188@gmail.com
- GitHub: [@jigs1188](https://github.com/jigs1188)
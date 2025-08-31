# Rex - Your Personal AI Assistant

Rex is a web-based chatbot that helps you manage your to-do list. It's built with Python, Flask, and DeepSeek V3.1 API via OpenRouter. Rex is designed to be a simple, yet powerful, example of an AI assistant that can understand and respond to your requests in a conversational way.

## Architecture

The application follows a simple direct API architecture. Here's a breakdown of the components:

- **main.py**: The entry point of the application. It runs a Flask web server that serves the web interface and handles user prompts with direct DeepSeek V3.1 API calls.
- **templates/index.html**: The HTML file for the mobile-first PWA interface.
- **static/style.css**: The CSS file for responsive mobile-first styling.
- **static/script.js**: The JavaScript file for handling user interactions and PWA features.
- **static/manifest.json**: PWA manifest for app store deployment.
- **static/sw.js**: Service worker for offline functionality.
- **storage.json**: This file persists conversation history.

Rex uses direct API calls to DeepSeek V3.1 via OpenRouter, providing fast and reliable AI responses without complex agent frameworks.

## Memory

Snello persists both conversation history and the to-do list in a single JSON file named `storage.json`. This ensures that your conversations and to-do items are saved even after the application is closed.

## Tools

The agent has access to the following advanced tools:

### 📝 Task Management
- **`add_todo(todo, priority)`**: Adds tasks with automatic priority detection
- **`remove_todo(todo_index)`**: Removes tasks by index
- **`complete_todo(todo_index)`**: Marks tasks as completed with timestamps
- **`list_todos()`**: Enhanced list display with priorities and status
- **`clear_todos()`**: Clears all tasks
- **`count_todos()`**: Detailed task count with progress metrics
- **`search_todos(keyword)`**: Full-text search across tasks

### 📊 Analytics & Insights
- **`get_analytics()`**: Comprehensive productivity analytics and insights
- **`get_motivational_quote()`**: Inspirational quotes for motivation

### 👤 User Management
- **`save_user_name(name)`**: Saves user's name for personalization
- **`get_user_name()`**: Retrieves saved user name

### ⏰ Productivity Features
- **`set_reminder(task, minutes)`**: Sets task reminders (demo feature)

All tools include comprehensive error handling, emoji-enhanced responses, and intelligent formatting for an engaging user experience.

## Setup and Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/jigs1188/ChatBot
    cd snello
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API key:**
    -   Create a file named `.env` in the root of the project.
    -   Add the following line to the `.env` file, replacing `"YOUR_API_KEY_HERE"` with your actual Google API key:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

4.  **Run the application:**
    ```bash
    python main.py
    ```

5.  **Open the web interface:**
    Open your web browser and go to `http://127.0.0.1:5000`.

## 🚀 New Features & Enhancements

### ✨ Advanced UI/UX
- **Modern Design**: Professional sidebar layout with dark theme
- **Real-time Statistics**: Live message and task counters
- **Quick Actions**: One-click buttons for common tasks
- **Typing Indicators**: Visual feedback during AI processing
- **Responsive Design**: Optimized for desktop and mobile
- **Accessibility**: Screen reader support and keyboard navigation

### 🤖 Enhanced AI Capabilities
- **Smart Priority Detection**: Automatically detects task urgency from language
- **Productivity Analytics**: Comprehensive insights and progress tracking
- **Contextual Responses**: Enhanced conversation memory and personalization
- **Emoji Integration**: Visual feedback and engaging interactions
- **Search Functionality**: Find tasks quickly with keyword search

### 🛠️ Technical Improvements
- **Error Resilience**: Comprehensive error handling and recovery
- **API Endpoints**: RESTful APIs for data access and integration
- **Performance Optimization**: Efficient data handling and caching
- **Code Quality**: Type hints, documentation, and clean architecture
- **Production Ready**: Gunicorn server, environment configurations

### 📱 User Experience
- **Interactive Elements**: Hover effects, animations, and transitions
- **Visual Feedback**: Loading states, success/error indicators
- **Keyboard Shortcuts**: Productivity shortcuts for power users
- **Theme Toggle**: Light/dark mode support
- **Sound Effects**: Subtle audio feedback (optional)

## 🎯 For Recruiters

This project demonstrates:
- **Full-Stack Development**: Complete web application with modern technologies
- **AI/ML Integration**: Practical implementation of Large Language Models
- **Modern Frontend**: React-like component thinking with vanilla JavaScript
- **Backend Architecture**: Scalable, maintainable Python application structure
- **User-Centered Design**: Focus on usability and user experience
- **Production Considerations**: Deployment, monitoring, and maintenance planning

## 🎪 Demo Commands

Try these commands to see advanced features:
- `"Add 'URGENT: Submit quarterly reports' to my list"` - Auto-detects high priority
- `"Show my productivity analytics"` - Comprehensive insights
- `"Search for tasks containing 'report'"` - Smart search
- `"Complete task number 1"` - Task completion tracking
- `"Give me a motivational quote"` - Dynamic content
- `"How productive am I?"` - Analytics and insights
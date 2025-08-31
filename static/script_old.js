document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt-input');
    const sendButton = document.getElementById('send-button');
    const chatHistory = document.querySelector('.chat-history');
    const typingIndicator = document.getElementById('typing-indicator');
    const messageCountEl = document.getElementById('message-count');
    const taskCountEl = document.getElementById('task-count');
    const themeToggle = document.getElementById('theme-toggle');
    const clearChatBtn = document.getElementById('clear-chat');
    const loadingOverlay = document.getElementById('loading-overlay');

    let messageCount = 0;
    let taskCount = 0;
    let isDarkTheme = true;

    // Initialize
    updateStats();
    
    // Theme toggle
    themeToggle.addEventListener('click', () => {
        isDarkTheme = !isDarkTheme;
        document.body.classList.toggle('dark-theme', !isDarkTheme);
        themeToggle.innerHTML = isDarkTheme ? '<i class="fas fa-moon"></i>' : '<i class="fas fa-sun"></i>';
    });

    // Clear chat
    clearChatBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear the chat history?')) {
            const messages = chatHistory.querySelectorAll('.message');
            messages.forEach(msg => msg.remove());
            messageCount = 0;
            updateStats();
        }
    });

    // Quick action buttons
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            let message = '';
            
            switch(action) {
                case 'list':
                    message = 'Show my to-do list';
                    break;
                case 'count':
                    message = 'How many tasks do I have?';
                    break;
                case 'clear':
                    message = 'Clear all my tasks';
                    break;
                case 'help':
                    message = 'What can you help me with?';
                    break;
            }
            
            if (message) {
                promptInput.value = message;
                sendMessage();
            }
        });
    });

    // Suggestion buttons
    document.querySelectorAll('.suggestion-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            promptInput.value = btn.textContent;
            promptInput.focus();
        });
    });

    const updateStats = () => {
        messageCountEl.textContent = messageCount;
        taskCountEl.textContent = taskCount;
    };

    const showTyping = () => {
        typingIndicator.style.display = 'flex';
        chatHistory.scrollTop = chatHistory.scrollHeight;
    };

    const hideTyping = () => {
        typingIndicator.style.display = 'none';
    };

    const addMessage = (content, isUser = false, isError = false) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        
        if (isUser) {
            messageDiv.classList.add('user-message');
        } else {
            messageDiv.classList.add('bot-message');
            if (isError) {
                messageDiv.classList.add('error-message');
            }
        }
        
        // Format message content
        const formattedContent = formatMessage(content);
        messageDiv.innerHTML = formattedContent;
        
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        
        messageCount++;
        updateStats();
    };

    const formatMessage = (content) => {
        // Convert markdown-like formatting
        let formatted = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
        
        // Format lists
        if (formatted.includes('1.') || formatted.includes('•')) {
            const lines = formatted.split('<br>');
            let inList = false;
            let result = '';
            
            for (let line of lines) {
                if (line.match(/^\d+\./)) {
                    if (!inList) {
                        result += '<ol>';
                        inList = true;
                    }
                    result += `<li>${line.replace(/^\d+\.\s*/, '')}</li>`;
                } else if (line.startsWith('•') || line.startsWith('*')) {
                    if (!inList) {
                        result += '<ul>';
                        inList = true;
                    }
                    result += `<li>${line.replace(/^[•*]\s*/, '')}</li>`;
                } else {
                    if (inList) {
                        result += '</ol></ul>';
                        inList = false;
                    }
                    result += line + '<br>';
                }
            }
            
            if (inList) {
                result += '</ol></ul>';
            }
            
            formatted = result;
        }
        
        return formatted;
    };

    const sendMessage = async () => {
        const prompt = promptInput.value.trim();
        if (prompt === '') {
            return;
        }

        // Disable input and button
        promptInput.disabled = true;
        sendButton.disabled = true;
        
        // Add user message
        addMessage(prompt, true);
        promptInput.value = '';
        
        // Show typing indicator
        showTyping();

        try {
            const response = await fetch('/prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Hide typing indicator
            hideTyping();
            
            if (data.error) {
                addMessage(`Error: ${data.error}`, false, true);
            } else {
                addMessage(data.response, false);
                
                // Update task count if todo-related response
                if (data.response.toLowerCase().includes('todo') || 
                    data.response.toLowerCase().includes('task') ||
                    data.response.toLowerCase().includes('added') ||
                    data.response.toLowerCase().includes('removed')) {
                    taskCount = Math.max(0, taskCount + (data.response.includes('added') ? 1 : 
                                                       data.response.includes('removed') ? -1 : 0));
                    updateStats();
                }
            }
        } catch (error) {
            hideTyping();
            console.error('Error:', error);
            addMessage('Sorry, I encountered an error. Please try again.', false, true);
        } finally {
            // Re-enable input and button
            promptInput.disabled = false;
            sendButton.disabled = false;
            promptInput.focus();
        }
    };

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    promptInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    // Auto-focus input
    promptInput.focus();

    // Fetch and update real-time stats
    const updateRealTimeStats = async () => {
        try {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            
            if (stats.total_messages !== undefined) {
                messageCountEl.textContent = Math.floor(stats.total_messages / 2); // Divide by 2 for user messages only
            }
            if (stats.total_todos !== undefined) {
                taskCountEl.textContent = stats.total_todos;
            }
        } catch (error) {
            console.error('Error updating stats:', error);
        }
    };

    // Update stats periodically
    setInterval(updateRealTimeStats, 5000);
    updateRealTimeStats();

    // Add demo functionality for first-time visitors
    const addWelcomeExperience = () => {
        // Add some sample interactions for demo
        const demoMessages = [
            "👋 Hi! I'm Snello, your AI assistant. What's your name?",
        ];
        
        // Only show if no existing messages
        if (chatHistory.querySelectorAll('.message').length === 0) {
            setTimeout(() => {
                demoMessages.forEach((msg, index) => {
                    setTimeout(() => {
                        addMessage(msg, false);
                    }, index * 1000);
                });
            }, 500);
        }
    };

    // Enhanced keyboard shortcuts
    document.addEventListener('keydown', (event) => {
        // Ctrl/Cmd + Enter to send message
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            sendMessage();
        }
        
        // Escape to clear input
        if (event.key === 'Escape') {
            promptInput.value = '';
            promptInput.focus();
        }
    });

    // Initialize welcome experience
    addWelcomeExperience();

    // Add sound effects (optional)
    const playNotificationSound = () => {
        // Create a subtle notification sound
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.1);
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.1);
    };

    // Enhanced message handling with sound
    const originalAddMessage = addMessage;
    addMessage = (content, isUser = false, isError = false) => {
        originalAddMessage(content, isUser, isError);
        if (!isUser) {
            // Play subtle notification for bot messages
            try {
                playNotificationSound();
            } catch (error) {
                // Sound not supported, ignore
            }
        }
    };
});
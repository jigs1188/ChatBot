// Mobile-First AI Assistant - Enhanced JavaScript
class AiAssistant {
    constructor() {
        this.isLoading = false;
        this.chatHistory = [];
        this.currentTheme = localStorage.getItem('theme') || 'dark';
        this.notificationsEnabled = localStorage.getItem('notifications') === 'true';
        this.voiceEnabled = localStorage.getItem('voice') === 'true';
        this.stats = {
            totalChats: parseInt(localStorage.getItem('totalChats')) || 0,
            completedTasks: parseInt(localStorage.getItem('completedTasks')) || 0,
            activeTodos: parseInt(localStorage.getItem('activeTodos')) || 0,
            totalProjects: parseInt(localStorage.getItem('totalProjects')) || 1
        };
        
        // Quick initialization without delay
        this.quickInit();
    }

    async quickInit() {
        try {
            console.log('🔄 Quick initializing...');
            
            // Hide loading screen immediately and show app
            setTimeout(() => {
                this.hideLoadingScreen();
            }, 500);
            
            this.setupEventListeners();
            this.loadChatHistory();
            this.updateStats();
            this.applyTheme();
            this.checkPWASupport();
            console.log('🚀 AI Assistant initialized successfully');
            
            // Ensure app is visible
            const appContainer = document.querySelector('.app-container');
            if (appContainer) {
                appContainer.classList.add('loaded');
                appContainer.style.opacity = '1';
                appContainer.style.pointerEvents = 'auto';
            }
            
        } catch (error) {
            console.error('❌ Initialization error:', error);
            this.hideLoadingScreen(); // Ensure loading screen is hidden
        }
    }

    async init() {
        this.showLoadingScreen();
        try {
            await this.delay(1000); // Reduced loading time
            this.setupEventListeners();
            this.loadChatHistory();
            this.updateStats();
            this.applyTheme();
            this.checkPWASupport();
            console.log('🚀 AI Assistant initialized successfully');
        } catch (error) {
            console.error('❌ Initialization error:', error);
            this.showToast('Failed to initialize app', 'error');
        } finally {
            this.hideLoadingScreen();
        }
    }

    showLoadingScreen() {
        const loadingScreen = document.querySelector('.loading-screen');
        if (loadingScreen) {
            loadingScreen.style.display = 'flex';
            // Fallback: Always hide loading screen after 5 seconds max
            setTimeout(() => {
                this.hideLoadingScreen();
                console.log('⏰ Loading screen auto-hidden after timeout');
            }, 5000);
        }
    }

    hideLoadingScreen() {
        const loadingScreen = document.querySelector('.loading-screen');
        const appContainer = document.querySelector('.app-container');
        
        if (loadingScreen) {
            loadingScreen.style.display = 'none';
            loadingScreen.classList.add('hidden');
        }
        
        if (appContainer) {
            appContainer.style.display = 'flex';
            appContainer.style.opacity = '1';
            appContainer.classList.add('loaded');
        }
        
        console.log('✅ Loading screen hidden, app container shown');
    }

    setupEventListeners() {
        // Mobile menu toggle
        const menuToggle = document.querySelector('.menu-toggle');
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        const closeSidebar = document.querySelector('.close-sidebar');

        if (menuToggle) {
            menuToggle.addEventListener('click', () => this.toggleSidebar());
        }
        
        if (overlay) {
            overlay.addEventListener('click', () => this.closeSidebar());
        }
        
        if (closeSidebar) {
            closeSidebar.addEventListener('click', () => this.closeSidebar());
        }

        // Chat input handling
        const promptInput = document.getElementById('prompt-input');
        const sendButton = document.querySelector('.send-button');
        
        if (promptInput) {
            promptInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
            
            promptInput.addEventListener('input', () => {
                this.adjustTextareaHeight(promptInput);
            });
        }
        
        if (sendButton) {
            sendButton.addEventListener('click', () => this.sendMessage());
        }

        // Quick action buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.currentTarget.dataset.action;
                this.handleQuickAction(action);
            });
        });

        // Suggestion chips
        document.querySelectorAll('.suggestion-chip').forEach(chip => {
            chip.addEventListener('click', (e) => {
                const suggestion = e.currentTarget.textContent;
                this.selectSuggestion(suggestion);
            });
        });

        // Settings modal
        const settingsBtn = document.querySelector('[data-action="settings"]');
        const settingsModal = document.getElementById('settings-modal');
        const closeModal = document.querySelector('.modal-close');

        // Alternative way to open settings if data-action doesn't work
        const headerSettingsBtn = document.getElementById('settings-btn');

        if (settingsBtn && settingsModal) {
            settingsBtn.addEventListener('click', () => {
                settingsModal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            });
        }

        if (headerSettingsBtn && settingsModal) {
            headerSettingsBtn.addEventListener('click', () => {
                settingsModal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            });
        }

        if (closeModal && settingsModal) {
            closeModal.addEventListener('click', () => {
                settingsModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            });
        }

        // Settings controls
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const theme = e.currentTarget.dataset.theme;
                this.setTheme(theme);
            });
        });

        const notificationToggle = document.getElementById('notifications');
        const voiceToggle = document.getElementById('voice');

        if (notificationToggle) {
            notificationToggle.checked = this.notificationsEnabled;
            notificationToggle.addEventListener('change', (e) => {
                this.notificationsEnabled = e.target.checked;
                localStorage.setItem('notifications', this.notificationsEnabled);
                this.showToast(
                    this.notificationsEnabled ? 'Notifications enabled' : 'Notifications disabled',
                    'success'
                );
            });
        }

        if (voiceToggle) {
            voiceToggle.checked = this.voiceEnabled;
            voiceToggle.addEventListener('change', (e) => {
                this.voiceEnabled = e.target.checked;
                localStorage.setItem('voice', this.voiceEnabled);
                this.showToast(
                    this.voiceEnabled ? 'Voice input enabled' : 'Voice input disabled',
                    'success'
                );
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case 'k':
                        e.preventDefault();
                        this.focusInput();
                        break;
                    case 'b':
                        e.preventDefault();
                        this.toggleSidebar();
                        break;
                    case ',':
                        e.preventDefault();
                        if (settingsModal) settingsModal.style.display = 'flex';
                        break;
                }
            }
        });
    }

    toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        
        if (sidebar && overlay) {
            const isOpen = sidebar.classList.contains('open');
            
            if (isOpen) {
                this.closeSidebar();
            } else {
                sidebar.classList.add('open');
                overlay.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        }
    }

    closeSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        
        if (sidebar && overlay) {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    }

    focusInput() {
        const promptInput = document.getElementById('prompt-input');
        if (promptInput) {
            promptInput.focus();
        }
    }

    adjustTextareaHeight(textarea) {
        textarea.style.height = 'auto';
        const maxHeight = 120;
        const newHeight = Math.min(textarea.scrollHeight, maxHeight);
        textarea.style.height = newHeight + 'px';
    }

    async sendMessage() {
        const promptInput = document.getElementById('prompt-input');
        const sendButton = document.querySelector('.send-button');
        
        if (!promptInput || this.isLoading) return;
        
        const message = promptInput.value.trim();
        if (!message) {
            this.showToast('Please enter a message', 'error');
            return;
        }

        try {
            this.isLoading = true;
            
            // Update UI
            this.updateSendButton(true);
            this.addMessage(message, 'user');
            this.showTypingIndicator();
            promptInput.value = '';
            promptInput.style.height = 'auto';
            
            // Close mobile sidebar if open
            this.closeSidebar();

            // Send to backend
            const response = await fetch('/prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: message })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            
            this.hideTypingIndicator();
            
            if (data.response) {
                this.addMessage(data.response, 'bot');
                this.updateStats();
                
                if (this.notificationsEnabled && !document.hasFocus()) {
                    this.showNotification('New message received', data.response.substring(0, 100));
                }
            } else {
                throw new Error('No response received from AI');
            }

        } catch (error) {
            console.error('❌ Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            this.showToast('Failed to send message. Please try again.', 'error');
        } finally {
            this.isLoading = false;
            this.updateSendButton(false);
        }
    }

    addMessage(text, sender) {
        const chatHistory = document.querySelector('.chat-history');
        if (!chatHistory) return;

        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}-message`;
        
        // Format message with proper line breaks and styling
        const formattedText = this.formatMessage(text);
        messageElement.innerHTML = formattedText;
        
        chatHistory.appendChild(messageElement);
        this.scrollToBottom();
        
        // Store in chat history
        this.chatHistory.push({ text, sender, timestamp: Date.now() });
        this.saveChatHistory();
        
        // Update stats
        if (sender === 'user') {
            this.stats.totalChats++;
            localStorage.setItem('totalChats', this.stats.totalChats);
        }
    }

    formatMessage(text) {
        // Convert URLs to clickable links
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        text = text.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer" style="color: var(--primary); text-decoration: underline;">$1</a>');
        
        // Convert line breaks
        text = text.replace(/\n/g, '<br>');
        
        // Highlight code blocks
        text = text.replace(/`([^`]+)`/g, '<code style="background: var(--bg-tertiary); padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 13px;">$1</code>');
        
        return text;
    }

    showTypingIndicator() {
        const chatHistory = document.querySelector('.chat-history');
        if (!chatHistory) return;

        const typingElement = document.createElement('div');
        typingElement.className = 'typing-indicator';
        typingElement.id = 'typing-indicator';
        typingElement.innerHTML = `
            <div class="typing-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="typing-content">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <div class="typing-text">AI is thinking...</div>
            </div>
        `;
        
        chatHistory.appendChild(typingElement);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    updateSendButton(loading) {
        const sendButton = document.querySelector('.send-button');
        if (!sendButton) return;

        if (loading) {
            sendButton.disabled = true;
            sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        } else {
            sendButton.disabled = false;
            sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        }
    }

    scrollToBottom() {
        const chatHistory = document.querySelector('.chat-history');
        if (chatHistory) {
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    }

    handleQuickAction(action) {
        const actions = {
            'new-chat': () => this.clearChat(),
            'settings': () => this.openSettings(),
            'analytics': () => this.selectSuggestion('Show me my analytics dashboard'),
            'todos': () => this.selectSuggestion('Show me my todo list'),
            'help': () => this.selectSuggestion('How can you help me?'),
            'examples': () => this.showExamples()
        };

        if (actions[action]) {
            actions[action]();
        }
    }

    selectSuggestion(suggestion) {
        const promptInput = document.getElementById('prompt-input');
        if (promptInput) {
            promptInput.value = suggestion;
            promptInput.focus();
            this.adjustTextareaHeight(promptInput);
        }
    }

    clearChat() {
        const chatHistory = document.querySelector('.chat-history');
        if (chatHistory) {
            chatHistory.innerHTML = '';
            this.chatHistory = [];
            this.saveChatHistory();
            this.showToast('Chat cleared', 'success');
        }
    }

    showExamples() {
        const examples = [
            'Add a todo: Buy groceries',
            'Search my notes for project ideas',
            'Analyze my productivity this week',
            'Help me plan my day',
            'What can you do for me?'
        ];
        
        const examplesList = examples.map(ex => `• ${ex}`).join('\n');
        this.addMessage(`Here are some things you can ask me:\n\n${examplesList}`, 'bot');
    }

    async updateStats() {
        try {
            // Fetch latest stats from backend
            const response = await fetch('/api/stats');
            if (response.ok) {
                const data = await response.json();
                this.stats = { ...this.stats, ...data };
            }
        } catch (error) {
            console.warn('Could not fetch updated stats:', error);
        }

        // Update UI
        this.updateStatsDisplay();
    }

    updateStatsDisplay() {
        const statElements = {
            'totalChats': document.querySelector('[data-stat="chats"] .stat-number'),
            'completedTasks': document.querySelector('[data-stat="tasks"] .stat-number'),
            'activeTodos': document.querySelector('[data-stat="todos"] .stat-number'),
            'totalProjects': document.querySelector('[data-stat="projects"] .stat-number')
        };

        Object.entries(statElements).forEach(([key, element]) => {
            if (element) {
                element.textContent = this.stats[key] || 0;
            }
        });
    }

    setTheme(theme) {
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
        this.applyTheme();
        
        // Update theme buttons
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.theme === theme);
        });
        
        this.showToast(`${theme.charAt(0).toUpperCase() + theme.slice(1)} theme applied`, 'success');
    }

    applyTheme() {
        document.body.className = this.currentTheme === 'light' ? 'light-theme' : '';
        
        // Update theme buttons state
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.theme === this.currentTheme);
        });
    }

    showToast(message, type = 'success') {
        const toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? 'check-circle' : 
                    type === 'error' ? 'exclamation-circle' : 
                    'info-circle';
        
        toast.innerHTML = `
            <i class="fas fa-${icon}"></i>
            <span>${message}</span>
        `;
        
        toastContainer.appendChild(toast);
        
        // Auto remove after 4 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'toastSlide 0.3s ease-out reverse';
                setTimeout(() => toast.remove(), 300);
            }
        }, 4000);
    }

    showNotification(title, body) {
        if (!this.notificationsEnabled || !('Notification' in window)) return;
        
        if (Notification.permission === 'granted') {
            new Notification(title, {
                body: body,
                icon: '/static/icon-192.png',
                badge: '/static/badge-72.png'
            });
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    this.showNotification(title, body);
                }
            });
        }
    }

    loadChatHistory() {
        const savedHistory = localStorage.getItem('chatHistory');
        if (savedHistory) {
            try {
                this.chatHistory = JSON.parse(savedHistory);
                this.chatHistory.forEach(msg => {
                    this.addMessageToDOM(msg.text, msg.sender);
                });
            } catch (error) {
                console.warn('Could not load chat history:', error);
            }
        }
    }

    saveChatHistory() {
        try {
            localStorage.setItem('chatHistory', JSON.stringify(this.chatHistory));
        } catch (error) {
            console.warn('Could not save chat history:', error);
        }
    }

    addMessageToDOM(text, sender) {
        const chatHistory = document.querySelector('.chat-history');
        if (!chatHistory) return;

        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}-message`;
        messageElement.innerHTML = this.formatMessage(text);
        
        chatHistory.appendChild(messageElement);
    }

    checkPWASupport() {
        // Check if app is running as PWA
        if (window.matchMedia('(display-mode: standalone)').matches) {
            console.log('🎉 Running as PWA');
            this.showToast('Welcome to the AI Assistant PWA!', 'success');
        }

        // Register service worker
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                    .then(registration => {
                        console.log('✅ Service Worker registered:', registration);
                    })
                    .catch(error => {
                        console.warn('❌ Service Worker registration failed:', error);
                    });
            });
        }

        // Handle install prompt
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            
            // Show install button
            const installBtn = document.querySelector('[data-action="install"]');
            if (installBtn) {
                installBtn.style.display = 'flex';
                installBtn.addEventListener('click', async () => {
                    if (deferredPrompt) {
                        deferredPrompt.prompt();
                        const { outcome } = await deferredPrompt.userChoice;
                        console.log(`User response: ${outcome}`);
                        deferredPrompt = null;
                    }
                });
            }
        });
    }

    // Voice input functionality
    startVoiceInput() {
        if (!this.voiceEnabled || !('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
            this.showToast('Voice input not supported', 'error');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            this.showToast('Listening...', 'success');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            const promptInput = document.getElementById('prompt-input');
            if (promptInput) {
                promptInput.value = transcript;
                this.adjustTextareaHeight(promptInput);
            }
        };

        recognition.onerror = (event) => {
            this.showToast('Voice input error', 'error');
        };

        recognition.start();
    }

    // Utility methods
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Error handling
    handleError(error, context = '') {
        console.error(`❌ Error ${context}:`, error);
        this.showToast(`Something went wrong ${context}. Please try again.`, 'error');
    }

    // Performance monitoring
    measurePerformance(name, fn) {
        const start = performance.now();
        const result = fn();
        const end = performance.now();
        console.log(`⚡ ${name} took ${(end - start).toFixed(2)}ms`);
        return result;
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    try {
        console.log('🔄 Initializing AI Assistant...');
        window.aiAssistant = new AiAssistant();
    } catch (error) {
        console.error('❌ Failed to initialize AI Assistant:', error);
        // Hide loading screen even if initialization fails
        const loadingScreen = document.querySelector('.loading-screen');
        if (loadingScreen) {
            loadingScreen.style.display = 'none';
        }
        // Show error toast
        setTimeout(() => {
            alert('Failed to initialize the application. Please refresh the page.');
        }, 1000);
    }
});

// Handle visibility changes for notifications
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('📱 App hidden');
    } else {
        console.log('📱 App visible');
    }
});

// Handle online/offline status
window.addEventListener('online', () => {
    window.aiAssistant?.showToast('Back online!', 'success');
});

window.addEventListener('offline', () => {
    window.aiAssistant?.showToast('You are offline', 'warning');
});

// Global error handling
window.addEventListener('error', (event) => {
    console.error('🚨 Global error:', event.error);
    window.aiAssistant?.handleError(event.error, 'in application');
});

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    console.error('🚨 Unhandled promise rejection:', event.reason);
    window.aiAssistant?.handleError(event.reason, 'in promise');
});

// PWA specific functionality
if ('serviceWorker' in navigator) {
    // Handle PWA updates
    navigator.serviceWorker.addEventListener('controllerchange', () => {
        window.location.reload();
    });
}

// Export for debugging
window.AiAssistant = AiAssistant;

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
        
        // Mobile-specific properties
        this.isMobile = window.innerWidth <= 768;
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.sessionStartTime = Date.now();
        
        // Quick initialization without delay
        this.quickInit();
    }

    async quickInit() {
        try {
            console.log('🔄 Quick initializing mobile-optimized Rex AI...');
            
            // Hide loading screen with beautiful animation
            setTimeout(() => {
                this.hideLoadingScreen();
            }, 800);
            
            this.setupEventListeners();
            this.setupMobileInteractions();
            this.loadChatHistory();
            this.updateStats();
            this.applyTheme();
            this.checkPWASupport();
            this.startSessionTimer();
            console.log('🚀 Mobile AI Assistant initialized successfully');
            
            // Ensure app is visible with enhanced animation
            const appContainer = document.querySelector('.app-container');
            if (appContainer) {
                appContainer.classList.add('loaded');
                appContainer.style.opacity = '1';
                appContainer.style.pointerEvents = 'auto';
            }
            
            // Show welcome toast for mobile users
            if (this.isMobile) {
                setTimeout(() => {
                    this.showToast('Swipe right to open menu, left for message options! 📱', 'success');
                }, 2000);
            }
            
        } catch (error) {
            console.error('❌ Initialization error:', error);
            this.hideLoadingScreen(); // Ensure loading screen is hidden
        }
    }

    setupEventListeners() {
        console.log('🔧 Setting up event listeners...');

        // Setup hamburger menu toggle for mobile
        const menuToggle = document.getElementById('menu-toggle');
        if (menuToggle) {
            console.log('✅ Menu toggle found');
            menuToggle.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('🍔 Hamburger menu clicked');
                this.toggleSidebar();
                this.addHapticFeedback('medium');
            });
        } else {
            console.warn('⚠️ Menu toggle not found');
        }

        // Setup sidebar overlay click to close
        const sidebarOverlay = document.getElementById('sidebar-overlay');
        if (sidebarOverlay) {
            sidebarOverlay.addEventListener('click', () => {
                console.log('📱 Sidebar overlay clicked - closing sidebar');
                this.closeSidebar();
            });
        }

        // Setup close sidebar button
        const closeSidebar = document.getElementById('close-sidebar');
        if (closeSidebar) {
            closeSidebar.addEventListener('click', () => {
                console.log('❌ Close sidebar clicked');
                this.closeSidebar();
            });
        }

        // Setup send message
        const sendButton = document.getElementById('send-button');
        const promptInput = document.getElementById('prompt-input');
        
        if (sendButton) {
            sendButton.addEventListener('click', () => {
                console.log('📤 Send button clicked');
                this.sendMessage();
            });
        }

        if (promptInput) {
            promptInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });

            // Auto-resize textarea
            promptInput.addEventListener('input', () => {
                this.adjustTextareaHeight(promptInput);
            });
        }

        // Setup voice button
        const voiceBtn = document.getElementById('voice-btn');
        const voiceToggleBtn = document.getElementById('voice-toggle-btn');
        
        if (voiceBtn) {
            voiceBtn.addEventListener('click', () => {
                console.log('🎤 Voice button clicked');
                this.toggleVoiceInput();
            });
        }

        if (voiceToggleBtn) {
            voiceToggleBtn.addEventListener('click', () => {
                console.log('🎤 Voice toggle button clicked');
                this.toggleVoiceInput();
            });
        }

        // Setup settings button
        const settingsBtn = document.getElementById('settings-btn');
        const settingsModal = document.getElementById('settings-modal');
        const modalClose = document.getElementById('modal-close');

        if (settingsBtn && settingsModal) {
            settingsBtn.addEventListener('click', () => {
                console.log('⚙️ Settings button clicked');
                settingsModal.style.display = 'flex';
            });
        }

        if (modalClose && settingsModal) {
            modalClose.addEventListener('click', () => {
                settingsModal.style.display = 'none';
            });
        }

        if (settingsModal) {
            settingsModal.addEventListener('click', (e) => {
                if (e.target === settingsModal) {
                    settingsModal.style.display = 'none';
                }
            });
        }

        // Setup theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
                this.addHapticFeedback('medium');
            });
        }

        console.log('✅ Event listeners setup complete');
    }

    setupMobileInteractions() {
        console.log('📱 Setting up mobile interactions...');
        
        // Enhanced touch interactions for sidebar
        let touchStartX = 0;
        let touchStartY = 0;
        let isSwiping = false;
        
        // Add swipe zone interaction
        const swipeZone = document.querySelector('.swipe-zone');
        if (swipeZone) {
            console.log('✅ Swipe zone found, adding listeners');
            
            swipeZone.addEventListener('touchstart', (e) => {
                console.log('👆 Touch start on swipe zone');
                touchStartX = e.touches[0].clientX;
                touchStartY = e.touches[0].clientY;
                isSwiping = true;
            }, { passive: true });
            
            swipeZone.addEventListener('touchmove', (e) => {
                if (!isSwiping) return;
                
                const currentX = e.touches[0].clientX;
                const diffX = currentX - touchStartX;
                
                // If swiping right from left edge
                if (diffX > 30) {
                    console.log('👉 Swipe right detected from edge');
                    this.toggleSidebar();
                    isSwiping = false;
                }
            }, { passive: true });
            
            swipeZone.addEventListener('touchend', () => {
                isSwiping = false;
            }, { passive: true });
        } else {
            console.warn('⚠️ Swipe zone not found');
        }
        
        // Global touch events for general swipe detection
        document.addEventListener('touchstart', (e) => {
            this.touchStartX = e.touches[0].clientX;
            this.touchStartY = e.touches[0].clientY;
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            if (!this.touchStartX || !this.touchStartY) return;
            
            let touchEndX = e.changedTouches[0].clientX;
            let touchEndY = e.changedTouches[0].clientY;
            
            let diffX = this.touchStartX - touchEndX;
            let diffY = this.touchStartY - touchEndY;
            
            // Only detect swipes from very left edge of screen
            if (this.touchStartX < 50 && Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 30) {
                if (diffX < 0) { // Swipe right from left edge
                    console.log('👉 Edge swipe right - opening sidebar');
                    this.toggleSidebar();
                    this.addHapticFeedback('medium');
                }
            }
            
            this.touchStartX = null;
            this.touchStartY = null;
        }, { passive: true });
        
        // Add haptic feedback to all interactive elements
        document.querySelectorAll('.animate-on-tap, .quick-btn, .header-btn, .send-button').forEach(element => {
            element.addEventListener('touchstart', () => {
                this.addHapticFeedback('light');
            }, { passive: true });
        });
        
        // Enhanced scroll behavior
        const chatHistory = document.getElementById('chat-history');
        if (chatHistory) {
            chatHistory.addEventListener('scroll', this.updateScrollIndicator.bind(this), { passive: true });
        }
        
        // Auto-resize input on mobile
        const input = document.getElementById('prompt-input');
        if (input && this.isMobile) {
            input.addEventListener('input', this.autoResizeInput.bind(this));
        }

        // Setup theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
                this.addHapticFeedback('medium');
            });
        }

        // Setup hamburger menu toggle for mobile
        const menuToggle = document.getElementById('menu-toggle');
        if (menuToggle) {
            menuToggle.addEventListener('click', () => {
                console.log('🍔 Hamburger menu clicked');
                this.toggleSidebar();
                this.addHapticFeedback('medium');
            });
        }
    }

    addHapticFeedback(intensity = 'light') {
        if ('vibrate' in navigator) {
            const vibrationPattern = {
                'light': 10,
                'medium': [10, 10, 10],
                'heavy': [20, 10, 20]
            };
            navigator.vibrate(vibrationPattern[intensity] || 10);
        }
        
        // Visual feedback for devices without vibration
        const element = document.activeElement;
        if (element && element.classList.contains('animate-on-tap')) {
            element.classList.add(`haptic-${intensity}`);
            setTimeout(() => {
                element.classList.remove(`haptic-${intensity}`);
            }, 200);
        }
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.currentTheme = newTheme;
        localStorage.setItem('theme', newTheme);
        this.applyTheme();
        this.showToast(`Switched to ${newTheme} theme! ✨`, 'success');
    }

    showMobileTypingIndicator() {
        const indicator = document.getElementById('mobile-typing-indicator');
        if (indicator) {
            indicator.style.display = 'flex';
        }
    }

    hideMobileTypingIndicator() {
        const indicator = document.getElementById('mobile-typing-indicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    }

    handleSwipeLeft(e) {
        // Show quick actions or message options
        if (this.isMobile) {
            const messageElement = e.target.closest('.message');
            if (messageElement) {
                this.showMessageOptions(messageElement);
            }
        }
    }

    handleSwipeRight(e) {
        // Open sidebar
        console.log('👉 Swipe right detected');
        if (this.isMobile) {
            const sidebar = document.querySelector('.sidebar');
            if (sidebar && !sidebar.classList.contains('open')) {
                console.log('📱 Opening sidebar via swipe');
                this.toggleSidebar();
                this.addHapticFeedback('medium');
            }
        }
    }

    showMessageOptions(messageElement) {
        // Create floating action menu for messages
        const existingMenu = document.querySelector('.message-options-menu');
        if (existingMenu) existingMenu.remove();
        
        const menu = document.createElement('div');
        menu.className = 'message-options-menu';
        menu.innerHTML = `
            <button class="option-btn" onclick="window.aiAssistant.copyMessage(this)">
                <i class="fas fa-copy"></i> Copy
            </button>
            <button class="option-btn" onclick="window.aiAssistant.shareMessage(this)">
                <i class="fas fa-share"></i> Share
            </button>
        `;
        
        messageElement.style.position = 'relative';
        messageElement.appendChild(menu);
        
        // Remove after 3 seconds
        setTimeout(() => {
            if (menu.parentNode) menu.remove();
        }, 3000);
    }

    updateScrollIndicator() {
        const chatHistory = document.getElementById('chat-history');
        if (!chatHistory) return;
        
        const scrollPercentage = (chatHistory.scrollTop / (chatHistory.scrollHeight - chatHistory.clientHeight)) * 100;
        const scrollBtn = document.getElementById('scroll-to-bottom-btn');
        
        if (scrollBtn) {
            if (scrollPercentage < 90) {
                scrollBtn.style.display = 'flex';
                scrollBtn.classList.add('visible');
            } else {
                scrollBtn.classList.remove('visible');
                setTimeout(() => {
                    if (!scrollBtn.classList.contains('visible')) {
                        scrollBtn.style.display = 'none';
                    }
                }, 300);
            }
        }
    }

    autoResizeInput() {
        const input = document.getElementById('prompt-input');
        if (!input) return;
        
        // Auto-expand input height on mobile
        input.style.height = 'auto';
        const newHeight = Math.min(input.scrollHeight, 120);
        input.style.height = newHeight + 'px';
    }

    copyMessage(button) {
        const messageElement = button.closest('.message');
        const messageText = messageElement.querySelector('.message-content').textContent;
        
        if (navigator.clipboard) {
            navigator.clipboard.writeText(messageText);
            this.showToast('Message copied! 📋', 'success');
        }
        this.addHapticFeedback('light');
    }

    shareMessage(button) {
        const messageElement = button.closest('.message');
        const messageText = messageElement.querySelector('.message-content').textContent;
        
        if (navigator.share) {
            navigator.share({
                title: 'Rex AI Response',
                text: messageText
            });
        } else {
            this.copyMessage(button);
        }
        this.addHapticFeedback('light');
    }

    openSidebar() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        
        if (sidebar) {
            sidebar.classList.add('open');
        }
        if (overlay) {
            overlay.classList.add('active');
            // Close sidebar when overlay is clicked
            overlay.addEventListener('click', () => {
                this.closeSidebar();
            }, { once: true });
        }
        
        // Auto-close sidebar after 10 seconds on mobile
        if (this.isMobile) {
            setTimeout(() => {
                if (sidebar && sidebar.classList.contains('open')) {
                    this.closeSidebar();
                }
            }, 10000);
        }
    }

    closeSidebar() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        
        if (sidebar) {
            sidebar.classList.remove('open');
        }
        if (overlay) {
            overlay.classList.remove('active');
        }
        
        this.addHapticFeedback('light');
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
        console.log('🔧 Setting up event listeners...');
        
        // Mobile menu toggle
        const menuToggle = document.querySelector('.menu-toggle');
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        const closeSidebar = document.querySelector('.close-sidebar');
    const handle = document.getElementById('sidebar-handle');

        console.log('Elements found:', {
            menuToggle: !!menuToggle,
            sidebar: !!sidebar,
            overlay: !!overlay,
            closeSidebar: !!closeSidebar
        });

        if (menuToggle) {
            menuToggle.addEventListener('click', (e) => {
                console.log('📱 Menu toggle clicked');
                e.preventDefault();
                this.toggleSidebar();
            });
        }
        
        if (overlay) {
            overlay.addEventListener('click', (e) => {
                console.log('📱 Overlay clicked');
                e.preventDefault();
                this.closeSidebar();
            });
        }
        
        if (closeSidebar) {
            closeSidebar.addEventListener('click', (e) => {
                console.log('📱 Close sidebar clicked');
                e.preventDefault();
                this.closeSidebar();
            });
        }

        // Handle button to open sidebar
        if (handle) {
            handle.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('📎 Sidebar handle clicked');
                this.toggleSidebar();
            });
        }

        // Remove desktop-specific edge detection for cleaner mobile experience
        // Keep only essential mobile interactions

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

        // Scroll to bottom button
        const scrollToBottomBtn = document.getElementById('scroll-to-bottom-btn');
        if (scrollToBottomBtn) {
            scrollToBottomBtn.addEventListener('click', () => {
                this.scrollToBottom();
                // Add haptic feedback for mobile
                if (this.isMobile && 'vibrate' in navigator) {
                    navigator.vibrate(30);
                }
            });
        }

        // Show/hide scroll button based on scroll position
        const chatHistory = document.getElementById('chat-history');
        if (chatHistory) {
            chatHistory.addEventListener('scroll', () => {
                this.updateScrollButtonVisibility();
            }, { passive: true });
        }

        // Add passive touch listeners for better performance
        document.addEventListener('touchstart', (e) => {
            // Touch start handling
        }, { passive: true });

        document.addEventListener('touchmove', (e) => {
            // Touch move handling
        }, { passive: true });

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
        console.log('🔄 Toggling sidebar...');
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        
        if (!sidebar || !overlay) {
            console.error('❌ Sidebar or overlay not found:', { sidebar: !!sidebar, overlay: !!overlay });
            return;
        }
        
        const isOpen = sidebar.classList.contains('open');
        console.log('📊 Sidebar state:', { isOpen });
        
        if (isOpen) {
            console.log('🔒 Closing sidebar...');
            this.closeSidebar();
        } else {
            console.log('🔓 Opening sidebar...');
            
            // Show sidebar with proper mobile styling
            if (window.innerWidth <= 768) {
                sidebar.style.display = 'block';
                sidebar.style.visibility = 'visible';
                sidebar.style.position = 'fixed';
                sidebar.style.top = '60px';
                sidebar.style.left = '0';
                sidebar.style.width = '100vw';
                sidebar.style.height = 'calc(100vh - 60px)';
                sidebar.style.zIndex = '999';
                sidebar.style.background = 'rgba(15, 23, 42, 0.98)';
                sidebar.style.transform = 'translateX(0)';
            }
            
            sidebar.classList.add('open');
            overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Add haptic feedback for mobile
            this.addHapticFeedback('medium');
            
            // Auto-close after 15 seconds on mobile
            if (this.isMobile) {
                setTimeout(() => {
                    if (sidebar.classList.contains('open')) {
                        console.log('⏰ Auto-closing sidebar after 15s');
                        this.closeSidebar();
                    }
                }, 15000);
            }
        }
    }

    closeSidebar() {
        console.log('🔒 Closing sidebar...');
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        
        if (sidebar && overlay) {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
            document.body.style.overflow = 'auto';
            
            // Hide sidebar on mobile after closing animation
            if (window.innerWidth <= 768) {
                setTimeout(() => {
                    sidebar.style.display = 'none';
                    sidebar.style.visibility = 'hidden';
                    sidebar.style.transform = 'translateX(-100%)';
                }, 300); // Wait for animation to complete
            }
            
            this.addHapticFeedback('light');
        } else {
            console.error('❌ Cannot close sidebar - elements not found');
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
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
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

    updateScrollButtonVisibility() {
        const chatHistory = document.querySelector('.chat-history');
        const scrollBtn = document.getElementById('scroll-to-bottom-btn');
        
        if (!chatHistory || !scrollBtn) return;

        const isScrolledUp = chatHistory.scrollTop < (chatHistory.scrollHeight - chatHistory.clientHeight - 100);
        
        if (isScrolledUp) {
            scrollBtn.classList.add('visible');
        } else {
            scrollBtn.classList.remove('visible');
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
        // Update message count
        const messageCountEl = document.getElementById('message-count');
        if (messageCountEl) {
            messageCountEl.textContent = this.stats.messageCount || 0;
        }
        
        // Update session time
        const sessionTimeEl = document.getElementById('session-time');
        if (sessionTimeEl) {
            sessionTimeEl.textContent = this.stats.sessionTime || '0m';
        }
        
        // Update other stats based on the actual API response
        const statElements = {
            'messageCount': document.querySelector('#message-count'),
            'todoCount': document.querySelector('[data-stat="todos"] .stat-number'),
            'completedTasks': document.querySelector('[data-stat="tasks"] .stat-number'),
            'totalTasks': document.querySelector('[data-stat="total-tasks"] .stat-number')
        };

        Object.entries(statElements).forEach(([key, element]) => {
            if (element && this.stats[key] !== undefined) {
                element.textContent = this.stats[key];
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

// Global test function for mobile features
window.testMobileFeatures = function() {
    const ai = window.aiAssistant;
    console.log('🧪 Testing mobile sidebar functionality...');
    
    ai.showToast('📱 MOBILE TEST: Swipe from LEFT EDGE → to open sidebar', 'info');
    
    setTimeout(() => {
        ai.showToast('✋ Try swiping from the very left edge of screen', 'success');
    }, 2000);
    
    setTimeout(() => {
        console.log('🔄 Auto-testing sidebar toggle...');
        ai.toggleSidebar();
    }, 4000);
    
    // Test responsiveness
    setTimeout(() => {
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.querySelector('.sidebar-overlay');
        const swipeZone = document.querySelector('.swipe-zone');
        
        console.log('📊 Mobile setup check:', {
            sidebarExists: !!sidebar,
            overlayExists: !!overlay,
            swipeZoneExists: !!swipeZone,
            sidebarWidth: sidebar ? getComputedStyle(sidebar).width : 'N/A',
            viewportWidth: window.innerWidth + 'px',
            sidebarTransform: sidebar ? getComputedStyle(sidebar).transform : 'N/A'
        });
        
        ai.showToast('Check console for debug info 📊', 'info');
    }, 6000);
};

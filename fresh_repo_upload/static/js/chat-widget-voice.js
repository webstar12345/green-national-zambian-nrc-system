// AI Chat Widget with Voice Input/Output
class VoiceChatWidget {
    constructor() {
        this.isOpen = false;
        this.currentLanguage = localStorage.getItem('chatLanguage') || 'en';
        this.messages = [];
        this.isTyping = false;
        this.isRecording = false;
        this.isSpeaking = false;
        this.voiceEnabled = localStorage.getItem('voiceEnabled') !== 'false';
        
        // Language names
        this.languages = {
            'en': 'English',
            'nya': 'Nyanja',
            'toi': 'Tonga',
            'loz': 'Lozi'
        };
        
        // Voice Recognition
        this.recognition = null;
        this.initSpeechRecognition();
        
        // Text-to-Speech
        this.synthesis = window.speechSynthesis;
        this.currentUtterance = null;
        
        this.init();
    }
    
    initSpeechRecognition() {
        // Check browser support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (SpeechRecognition) {
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                this.isRecording = true;
                this.updateMicButton();
                console.log('Voice recognition started');
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('chatInput').value = transcript;
                this.sendMessage();
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.isRecording = false;
                this.updateMicButton();
                
                if (event.error === 'no-speech') {
                    this.showNotification('No speech detected. Please try again.');
                } else if (event.error === 'not-allowed') {
                    this.showNotification('Microphone access denied. Please enable it in your browser settings.');
                }
            };
            
            this.recognition.onend = () => {
                this.isRecording = false;
                this.updateMicButton();
            };
        } else {
            console.warn('Speech recognition not supported in this browser');
        }
    }
    
    init() {
        this.createWidget();
        this.attachEventListeners();
        this.initializeLanguageSelector();
        this.loadQuickResponses();
        this.addWelcomeMessage();
    }
    
    initializeLanguageSelector() {
        const selector = document.getElementById('languageSelector');
        if (selector) {
            selector.value = this.currentLanguage;
        }
    }
    
    createWidget() {
        const widgetHTML = `
            <div class="chat-widget">
                <button class="chat-button" id="chatToggle">
                    <svg viewBox="0 0 24 24">
                        <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
                    </svg>
                    <span class="chat-badge" id="chatBadge" style="display: none;">1</span>
                </button>
                
                <div class="chat-window" id="chatWindow">
                    <div class="chat-header">
                        <div class="chat-header-info">
                            <div class="chat-avatar">
                                <svg viewBox="0 0 24 24">
                                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                                </svg>
                            </div>
                            <div class="chat-header-text">
                                <h3>NRC Voice Assistant</h3>
                                <p><span class="status-dot"></span> Online • Voice Enabled</p>
                            </div>
                        </div>
                        <div class="chat-controls">
                            <select class="language-selector" id="languageSelector" title="Select language">
                                <option value="en">🇬🇧 English</option>
                                <option value="bem">🇿🇲 Bemba</option>
                                <option value="nya">🇿🇲 Nyanja</option>
                                <option value="toi">🇿🇲 Tonga</option>
                                <option value="loz">🇿🇲 Lozi</option>
                            </select>
                            <button class="chat-control-btn" id="voiceToggle" title="Toggle voice responses">
                                <svg viewBox="0 0 24 24" id="voiceIcon">
                                    <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
                                </svg>
                            </button>
                            <button class="chat-control-btn" id="closeChat">
                                <svg viewBox="0 0 24 24">
                                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                    
                    <div class="chat-messages" id="chatMessages"></div>
                    
                    <div class="quick-responses" id="quickResponses"></div>
                    
                    <div class="chat-notification" id="chatNotification" style="display: none;"></div>
                    
                    <div class="chat-input-container">
                        <div class="chat-input-wrapper">
                            <button class="mic-button" id="micButton" title="Voice input">
                                <svg viewBox="0 0 24 24" id="micIcon">
                                    <path d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"/>
                                </svg>
                            </button>
                            <input 
                                type="text" 
                                class="chat-input" 
                                id="chatInput" 
                                placeholder="Type or speak your message..."
                                autocomplete="off"
                            />
                            <button class="send-button" id="sendButton">
                                <svg viewBox="0 0 24 24">
                                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', widgetHTML);
    }
    
    attachEventListeners() {
        const chatToggle = document.getElementById('chatToggle');
        const closeChat = document.getElementById('closeChat');
        const sendButton = document.getElementById('sendButton');
        const chatInput = document.getElementById('chatInput');
        const languageSelector = document.getElementById('languageSelector');
        const micButton = document.getElementById('micButton');
        const voiceToggle = document.getElementById('voiceToggle');
        
        chatToggle.addEventListener('click', () => this.toggleChat());
        closeChat.addEventListener('click', () => this.toggleChat());
        sendButton.addEventListener('click', () => this.sendMessage());
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
        languageSelector.addEventListener('change', (e) => {
            this.changeLanguage(e.target.value);
        });
        micButton.addEventListener('click', () => this.toggleVoiceInput());
        voiceToggle.addEventListener('click', () => this.toggleVoiceOutput());
    }
    
    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('chatWindow');
        const chatBadge = document.getElementById('chatBadge');
        chatWindow.classList.toggle('active');
        
        if (this.isOpen) {
            document.getElementById('chatInput').focus();
            chatBadge.style.display = 'none';
        }
    }
    
    toggleVoiceInput() {
        if (!this.recognition) {
            this.showNotification('Voice input is not supported in your browser');
            return;
        }
        
        if (this.isRecording) {
            this.recognition.stop();
        } else {
            try {
                this.recognition.start();
            } catch (error) {
                console.error('Error starting recognition:', error);
                this.showNotification('Could not start voice input. Please try again.');
            }
        }
    }
    
    updateMicButton() {
        const micButton = document.getElementById('micButton');
        const micIcon = document.getElementById('micIcon');
        
        if (this.isRecording) {
            micButton.classList.add('recording');
            micIcon.innerHTML = '<circle cx="12" cy="12" r="8" fill="currentColor"/>';
        } else {
            micButton.classList.remove('recording');
            micIcon.innerHTML = '<path d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"/>';
        }
    }
    
    toggleVoiceOutput() {
        this.isSpeaking = !this.isSpeaking;
        const voiceIcon = document.getElementById('voiceIcon');
        const voiceToggle = document.getElementById('voiceToggle');
        
        if (this.isSpeaking) {
            voiceToggle.classList.add('active');
            voiceIcon.innerHTML = '<path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>';
            this.showNotification('Voice responses enabled');
        } else {
            voiceToggle.classList.remove('active');
            voiceIcon.innerHTML = '<path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>';
            this.showNotification('Voice responses disabled');
            if (this.currentUtterance) {
                this.synthesis.cancel();
            }
        }
    }
    
    speak(text) {
        if (!this.isSpeaking || !this.synthesis) return;
        
        // Cancel any ongoing speech
        this.synthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = this.getVoiceLang();
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 1;
        
        // Try to find a voice for the selected language
        const voices = this.synthesis.getVoices();
        const voice = voices.find(v => v.lang.startsWith(utterance.lang.split('-')[0]));
        if (voice) {
            utterance.voice = voice;
        }
        
        utterance.onstart = () => {
            console.log('Speaking started');
        };
        
        utterance.onend = () => {
            console.log('Speaking ended');
            this.currentUtterance = null;
        };
        
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            this.currentUtterance = null;
        };
        
        this.currentUtterance = utterance;
        this.synthesis.speak(utterance);
    }
    
    getVoiceLang() {
        const langMap = {
            'en': 'en-US',
            'bem': 'en-US', // Fallback to English for local languages
            'nya': 'en-US',
            'toi': 'en-US',
            'loz': 'en-US'
        };
        return langMap[this.currentLanguage] || 'en-US';
    }
    
    showNotification(message) {
        const notification = document.getElementById('chatNotification');
        notification.textContent = message;
        notification.style.display = 'block';
        
        setTimeout(() => {
            notification.style.display = 'none';
        }, 3000);
    }
    
    addWelcomeMessage() {
        const welcomeMessages = {
            'en': 'Hello! I\'m your NRC Voice Assistant. You can type or speak to me. How can I help you today?',
            'bem': 'Muli shani! Ndi NRC Voice Assistant yenu. Mwingalembela nangu kulandila. Nshili kubafwila?',
            'nya': 'Muli bwanji! Ndine NRC Voice Assistant wanu. Mutha kulemba kapena kulankhula. Ndingakuthandizeni bwanji?',
            'toi': 'Mwabuka buti! Ndime NRC Voice Assistant wanu. Mungalembe nangu kuambila. Ndili kubafwida buti?',
            'loz': 'Lumela! Ke NRC Voice Assistant wa hao. U ka ngola kamba u bua. Nka lu thusa jwang?'
        };
        
        const message = welcomeMessages[this.currentLanguage];
        this.addMessage(message, 'bot');
        this.speak(message);
    }
    
    async loadQuickResponses() {
        try {
            const response = await fetch(`/api/quick-responses/?language=${this.currentLanguage}`);
            const data = await response.json();
            
            if (data.success) {
                this.displayQuickResponses(data.quick_responses);
            }
        } catch (error) {
            console.error('Error loading quick responses:', error);
        }
    }
    
    displayQuickResponses(responses) {
        const container = document.getElementById('quickResponses');
        container.innerHTML = '';
        
        responses.forEach(response => {
            const button = document.createElement('button');
            button.className = 'quick-response-btn';
            button.innerHTML = `<i class="fas fa-comment-dots"></i> ${response}`;
            button.addEventListener('click', () => {
                document.getElementById('chatInput').value = response;
                this.sendMessage();
            });
            container.appendChild(button);
        });
    }
    
    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message || this.isTyping) return;
        
        // Add user message
        this.addMessage(message, 'user');
        input.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken')
                },
                body: JSON.stringify({
                    message: message,
                    language: this.currentLanguage
                })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.hideTypingIndicator();
            
            if (data.success) {
                this.addMessage(data.message, 'bot');
                this.speak(data.message);
            } else {
                const errorMsg = 'Sorry, I encountered an error. Please try again.';
                this.addMessage(errorMsg, 'bot');
                this.speak(errorMsg);
            }
        } catch (error) {
            this.hideTypingIndicator();
            const errorMsg = 'Sorry, I couldn\'t connect to the server. Please try again.';
            this.addMessage(errorMsg, 'bot');
            this.speak(errorMsg);
            console.error('Error sending message:', error);
        }
    }
    
    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatMessages');
        const time = new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        const messageHTML = `
            <div class="chat-message ${sender}">
                <div class="message-avatar">
                    <svg viewBox="0 0 24 24">
                        ${sender === 'user' 
                            ? '<path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>'
                            : '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>'
                        }
                    </svg>
                </div>
                <div class="message-content">
                    <div class="message-bubble">${this.escapeHtml(text)}</div>
                    <div class="message-time">${time}</div>
                </div>
            </div>
        `;
        
        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Show badge if chat is closed
        if (!this.isOpen && sender === 'bot') {
            const badge = document.getElementById('chatBadge');
            badge.style.display = 'block';
        }
    }
    
    showTypingIndicator() {
        this.isTyping = true;
        const messagesContainer = document.getElementById('chatMessages');
        
        const typingHTML = `
            <div class="chat-message bot" id="typingIndicator">
                <div class="message-avatar">
                    <svg viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                    </svg>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <div class="typing-indicator">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        messagesContainer.insertAdjacentHTML('beforeend', typingHTML);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    hideTypingIndicator() {
        this.isTyping = false;
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    async changeLanguage(language) {
        this.currentLanguage = language;
        
        // Update speech recognition language
        if (this.recognition) {
            const langMap = {
                'en': 'en-US',
                'bem': 'en-US',
                'nya': 'en-US',
                'toi': 'en-US',
                'loz': 'en-US'
            };
            this.recognition.lang = langMap[language] || 'en-US';
        }
        
        await this.loadQuickResponses();
        
        const languageNames = {
            'en': 'English',
            'bem': 'Bemba',
            'nya': 'Nyanja',
            'toi': 'Tonga',
            'loz': 'Lozi'
        };
        
        const message = `Language changed to ${languageNames[language]}`;
        this.addMessage(message, 'bot');
        this.speak(message);
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Initialize voice chat widget when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Load voices (needed for some browsers)
    if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = () => {
            window.speechSynthesis.getVoices();
        };
    }
    
    new VoiceChatWidget();
});

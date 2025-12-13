// AI Chat Widget JavaScript
class ChatWidget {
    constructor() {
        this.isOpen = false;
        this.currentLanguage = 'en';
        this.messages = [];
        this.isTyping = false;
        
        this.init();
    }
    
    init() {
        this.createWidget();
        this.attachEventListeners();
        this.loadQuickResponses();
        this.addWelcomeMessage();
    }
    
    createWidget() {
        const widgetHTML = `
            <div class="chat-widget">
                <button class="chat-button" id="chatToggle">
                    <svg viewBox="0 0 24 24">
                        <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
                    </svg>
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
                                <h3>NRC Assistant</h3>
                                <p>Online • Ready to help</p>
                            </div>
                        </div>
                        <div class="chat-controls">
                            <select class="language-selector" id="languageSelector">
                                <option value="en">English</option>
                                <option value="bem">Bemba</option>
                                <option value="nya">Nyanja</option>
                                <option value="toi">Tonga</option>
                                <option value="loz">Lozi</option>
                            </select>
                            <button class="chat-control-btn" id="closeChat">
                                <svg viewBox="0 0 24 24">
                                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                    
                    <div class="chat-messages" id="chatMessages"></div>
                    
                    <div class="quick-responses" id="quickResponses"></div>
                    
                    <div class="chat-input-container">
                        <div class="chat-input-wrapper">
                            <input 
                                type="text" 
                                class="chat-input" 
                                id="chatInput" 
                                placeholder="Type your message..."
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
        
        chatToggle.addEventListener('click', () => this.toggleChat());
        closeChat.addEventListener('click', () => this.toggleChat());
        sendButton.addEventListener('click', () => this.sendMessage());
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
        languageSelector.addEventListener('change', (e) => {
            this.changeLanguage(e.target.value);
        });
    }
    
    toggleChat() {
        this.isOpen = !this.isOpen;
        const chatWindow = document.getElementById('chatWindow');
        chatWindow.classList.toggle('active');
        
        if (this.isOpen) {
            document.getElementById('chatInput').focus();
        }
    }
    
    addWelcomeMessage() {
        const welcomeMessages = {
            'en': 'Hello! I\'m your NRC Assistant. How can I help you today?',
            'bem': 'Muli shani! Ndi NRC Assistant yenu. Nshili kubafwila?',
            'nya': 'Muli bwanji! Ndine NRC Assistant wanu. Ndingakuthandizeni bwanji?',
            'toi': 'Mwabuka buti! Ndime NRC Assistant wanu. Ndili kubafwida buti?',
            'loz': 'Lumela! Ke NRC Assistant wa hao. Nka lu thusa jwang?'
        };
        
        this.addMessage(welcomeMessages[this.currentLanguage], 'bot');
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
            button.textContent = response;
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
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Sorry, I couldn\'t connect to the server. Please try again.', 'bot');
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
        await this.loadQuickResponses();
        
        const languageNames = {
            'en': 'English',
            'bem': 'Bemba',
            'nya': 'Nyanja',
            'toi': 'Tonga',
            'loz': 'Lozi'
        };
        
        this.addMessage(`Language changed to ${languageNames[language]}`, 'bot');
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

// Initialize chat widget when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ChatWidget();
});

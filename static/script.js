// Global variables
let currentUserId = 'web_user_' + Math.random().toString(36).substr(2, 9);
let isFirstMessage = true;

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');
const courseSidebar = document.getElementById('courseSidebar');
const courseInfo = document.getElementById('courseInfo');
const registrationModal = document.getElementById('registrationModal');
const successModal = document.getElementById('successModal');
const registrationForm = document.getElementById('registrationForm');

// API base URL
const API_BASE = window.location.origin;

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

// Initialize application
async function initializeApp() {
    try {
        await loadCourseInfo();
        await startConversation();
    } catch (error) {
        console.error('Failed to initialize app:', error);
        showErrorMessage('Failed to connect to the chatbot. Please refresh the page.');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Send message on Enter key
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Auto-resize input
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });

    // Sidebar toggle for mobile
    document.getElementById('sidebarToggleMobile').addEventListener('click', function() {
        courseSidebar.classList.toggle('show');
    });

    document.getElementById('sidebarToggle').addEventListener('click', function() {
        courseSidebar.classList.remove('show');
    });

    // Registration form
    registrationForm.addEventListener('submit', handleRegistration);

    // Close modals on overlay click
    registrationModal.addEventListener('click', function(e) {
        if (e.target === registrationModal) {
            closeRegistrationForm();
        }
    });

    successModal.addEventListener('click', function(e) {
        if (e.target === successModal) {
            closeSuccessModal();
        }
    });

    // Health check
    setInterval(checkServerHealth, 30000); // Check every 30 seconds
}

// Load course information
async function loadCourseInfo() {
    try {
        const response = await fetch(`${API_BASE}/course-info`);
        const data = await response.json();
        
        if (response.ok) {
            displayCourseInfo(data.course_details);
        } else {
            throw new Error('Failed to load course info');
        }
    } catch (error) {
        console.error('Error loading course info:', error);
        courseInfo.innerHTML = '<div class="error">Failed to load course information</div>';
    }
}

// Display course information in sidebar
function displayCourseInfo(courseDetails) {
    const formatPrice = (price) => price.startsWith('$') ? price : `$${price}`;
    const formatDuration = (duration) => duration;
    
    courseInfo.innerHTML = `
        <div class="course-detail">
            <h4><i class="fas fa-graduation-cap"></i> Course Name</h4>
            <p>${courseDetails.name}</p>
        </div>
        <div class="course-detail">
            <h4><i class="fas fa-clock"></i> Duration</h4>
            <p>${formatDuration(courseDetails.duration)}</p>
        </div>
        <div class="course-detail">
            <h4><i class="fas fa-dollar-sign"></i> Investment</h4>
            <p>${formatPrice(courseDetails.price)}</p>
        </div>
        <div class="course-detail">
            <h4><i class="fas fa-user-tie"></i> Instructor</h4>
            <p>${courseDetails.instructor}</p>
        </div>
        <div class="course-detail">
            <h4><i class="fas fa-calendar"></i> Schedule</h4>
            <p>${courseDetails.schedule}</p>
        </div>
        <div class="course-detail">
            <h4><i class="fas fa-laptop"></i> Format</h4>
            <p>${courseDetails.format}</p>
        </div>
        <div class="course-detail">
            <h4><i class="fas fa-star"></i> Key Benefits</h4>
            <ul class="course-benefits">
                ${courseDetails.benefits.slice(0, 5).map(benefit => `<li>${benefit}</li>`).join('')}
            </ul>
        </div>
    `;
}

// Start conversation
async function startConversation() {
    if (!isFirstMessage) return;
    
    try {
        const response = await fetch(`${API_BASE}/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUserId,
                message: 'start'
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            // Clear welcome message and show AI response
            chatMessages.innerHTML = '';
            displayMessage(data.response, 'bot');
            isFirstMessage = false;
        }
    } catch (error) {
        console.error('Error starting conversation:', error);
    }
}

// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || sendButton.disabled) return;

    // Clear welcome message on first user message
    if (isFirstMessage) {
        chatMessages.innerHTML = '';
        isFirstMessage = false;
    }

    // Display user message
    displayMessage(message, 'user');
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // Disable input and show typing indicator
    setInputDisabled(true);
    showTypingIndicator();

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUserId,
                message: message
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            // Small delay for better UX
            setTimeout(() => {
                hideTypingIndicator();
                displayMessage(data.response, 'bot');
                setInputDisabled(false);
                messageInput.focus();
            }, 1000);
        } else {
            throw new Error(data.detail || 'Failed to send message');
        }
    } catch (error) {
        console.error('Error sending message:', error);
        hideTypingIndicator();
        displayMessage('Sorry, I encountered an error. Please try again.', 'bot');
        setInputDisabled(false);
    }
}

// Send quick message
function sendQuickMessage(message) {
    messageInput.value = message;
    sendMessage();
    // Close sidebar on mobile
    courseSidebar.classList.remove('show');
}

// Display message in chat
function displayMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = `message-avatar ${sender}`;
    avatarDiv.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = `message-content ${sender}`;
    
    // Format message text (preserve line breaks, make URLs clickable)
    const formattedText = formatMessageText(text);
    contentDiv.innerHTML = formattedText;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    
    contentDiv.appendChild(timeDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    
    // Add entrance animation
    setTimeout(() => {
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
    }, 100);
}

// Format message text
function formatMessageText(text) {
    // Preserve line breaks
    let formatted = text.replace(/\n/g, '<br>');
    
    // Make URLs clickable
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    formatted = formatted.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
    
    // Make email addresses clickable
    const emailRegex = /([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/g;
    formatted = formatted.replace(emailRegex, '<a href="mailto:$1">$1</a>');
    
    return formatted;
}

// Show typing indicator
function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// Set input disabled state
function setInputDisabled(disabled) {
    messageInput.disabled = disabled;
    sendButton.disabled = disabled;
    
    if (disabled) {
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    } else {
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
    }
}

// Scroll chat to bottom
function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Clear chat
function clearChat() {
    if (confirm('Are you sure you want to clear the chat? This will start a new conversation.')) {
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <div class="bot-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="welcome-content">
                    <h3>👋 Welcome back!</h3>
                    <p>Chat cleared. I'm here to help you with any questions about our Complete Python Development Bootcamp!</p>
                    <p>What would you like to know? 🚀</p>
                </div>
            </div>
        `;
        
        // Reset conversation
        currentUserId = 'web_user_' + Math.random().toString(36).substr(2, 9);
        isFirstMessage = true;
        messageInput.focus();
    }
}

// Show registration form
function showRegistrationForm() {
    registrationModal.classList.add('show');
    document.getElementById('regName').focus();
}

// Close registration form
function closeRegistrationForm() {
    registrationModal.classList.remove('show');
    registrationForm.reset();
}

// Handle registration
async function handleRegistration(e) {
    e.preventDefault();
    
    const formData = new FormData(registrationForm);
    const registrationData = {
        name: document.getElementById('regName').value.trim(),
        email: document.getElementById('regEmail').value.trim(),
        phone: document.getElementById('regPhone').value.trim(),
        user_id: currentUserId
    };

    // Validate form
    if (!registrationData.name || !registrationData.email || !registrationData.phone) {
        alert('Please fill in all required fields.');
        return;
    }

    // Disable form
    const submitBtn = registrationForm.querySelector('.register-btn');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Registering...';
    submitBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(registrationData)
        });

        const data = await response.json();
        
        if (response.ok) {
            closeRegistrationForm();
            showSuccessModal(data.message, data.registration_id);
            
            // Add registration message to chat
            displayMessage(`I just registered for the course! 🎉`, 'user');
            setTimeout(() => {
                displayMessage(data.message, 'bot');
            }, 1000);
        } else {
            throw new Error(data.detail || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again or contact support.');
    } finally {
        // Re-enable form
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

// Show success modal
function showSuccessModal(message, registrationId) {
    document.getElementById('successMessage').innerHTML = message;
    successModal.classList.add('show');
}

// Close success modal
function closeSuccessModal() {
    successModal.classList.remove('show');
    messageInput.focus();
}

// Show error message
function showErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message bot';
    errorDiv.innerHTML = `
        <div class="message-avatar bot">
            <i class="fas fa-exclamation-triangle"></i>
        </div>
        <div class="message-content bot" style="background: #f8d7da; border-color: #f5c6cb; color: #721c24;">
            ${message}
            <div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
        </div>
    `;
    
    chatMessages.appendChild(errorDiv);
    scrollToBottom();
}

// Check server health
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const statusIndicator = document.getElementById('statusIndicator');
        
        if (response.ok) {
            const data = await response.json();
            statusIndicator.innerHTML = '<i class="fas fa-circle"></i> Online';
            statusIndicator.style.color = '#28a745';
            
            // Update title with configuration status
            const title = `${data.openai_configured ? '🤖' : '⚠️'} AI ${data.openai_configured ? 'Active' : 'Limited'} | ${data.google_sheets_configured ? '📊' : '📝'} Sheets ${data.google_sheets_configured ? 'Connected' : 'Disabled'}`;
            document.title = `${title} - Course Assistant`;
        } else {
            throw new Error('Server unhealthy');
        }
    } catch (error) {
        const statusIndicator = document.getElementById('statusIndicator');
        statusIndicator.innerHTML = '<i class="fas fa-circle"></i> Offline';
        statusIndicator.style.color = '#dc3545';
        console.error('Health check failed:', error);
    }
}

// Utility functions
function generateUserId() {
    return 'web_user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Handle network errors
window.addEventListener('online', function() {
    checkServerHealth();
    displayMessage('✅ Connection restored! You can continue chatting.', 'bot');
});

window.addEventListener('offline', function() {
    displayMessage('⚠️ Connection lost. Please check your internet connection.', 'bot');
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to send message
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        sendMessage();
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        closeRegistrationForm();
        closeSuccessModal();
        courseSidebar.classList.remove('show');
    }
    
    // Ctrl/Cmd + K to focus input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        messageInput.focus();
    }
});

// Auto-save draft message
setInterval(() => {
    const draft = messageInput.value.trim();
    if (draft) {
        localStorage.setItem('chatbot_draft', draft);
    } else {
        localStorage.removeItem('chatbot_draft');
    }
}, 1000);

// Restore draft message on load
window.addEventListener('load', () => {
    const draft = localStorage.getItem('chatbot_draft');
    if (draft) {
        messageInput.value = draft;
        messageInput.focus();
    }
});

// Performance monitoring
let lastMessageTime = Date.now();

function trackResponseTime() {
    const responseTime = Date.now() - lastMessageTime;
    if (responseTime > 5000) {
        console.warn(`Slow response time: ${responseTime}ms`);
    }
}

// Export functions for testing
window.ChatBot = {
    sendMessage,
    sendQuickMessage,
    clearChat,
    showRegistrationForm,
    currentUserId,
    API_BASE
};

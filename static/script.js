document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt-input');
    const sendButton = document.getElementById('send-button');
    const chatHistory = document.querySelector('.chat-history');

    const sendMessage = async () => {
        const prompt = promptInput.value;
        if (prompt.trim() === '') {
            return;
        }

        // Display user message
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user-message');
        userMessage.textContent = prompt;
        chatHistory.appendChild(userMessage);

        promptInput.value = '';

        // Send prompt to backend
        const response = await fetch('/prompt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt })
        });

        const data = await response.json();

        // Display bot response
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot-message');
        botMessage.textContent = data.response;
        chatHistory.appendChild(botMessage);

        // Scroll to bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;
    };

    sendButton.addEventListener('click', sendMessage);
    promptInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});
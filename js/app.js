const messagesContainer = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    
    const time = new Date().toLocaleTimeString('zh-TW', {hour:'2-digit', minute:'2-digit'});
    
    msgDiv.innerHTML = `
        ${text}
        <div class="time">${time}</div>
    `;
    
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// 示例：初始欢迎 + 日期分隔
function initChat() {
    const dateDiv = document.createElement('div');
    dateDiv.className = 'date-divider';
    dateDiv.textContent = '2025年7月6日';
    messagesContainer.appendChild(dateDiv);

    addMessage('嗯……你终于来找我啦。今天过得怎么样呀？', 'ai');
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    userInput.value = '';

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        addMessage(data.reply || '……刚刚走神了，你再说一次好吗？', 'ai');
    } catch (e) {
        addMessage('网络有点小问题，再试试看～', 'ai');
    }
}

// 启动
initChat();

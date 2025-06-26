import React, { useState } from 'react';
import ChatBotLog from '../assets/chatbotsvg.svg'
const ChatBot = ({ onSend }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Hello! How can I help you today?' }
  ]);

  const handleSend = () => {
    if (!input.trim()) return;
    const userMessage = { role: 'user', text: input };
    setMessages([...messages, userMessage]);
    const loadOfMessage = {role: 'bot', text: 'Thinking...'};
    setMessages(prev => [...prev, loadOfMessage]);
    
    onSend?.(input, (botResponse) => {
      setMessages((prev) => [...prev, { role: 'bot', text: botResponse }]);
    });
    setInput('');
  };

  return (
    <div
      style={{
        position: 'fixed',
        bottom: 30,
        right: 30,
        width: 320,
        height: 420,
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: 20,
        border: '1px solid rgba(255, 255, 255, 0.2)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        color: '#fff',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        zIndex: 9999
      }}
    >
      <div style={{ flex: 1, overflowY: 'auto', padding: 16 }}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              marginBottom: 12,
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              color: msg.role === 'user' ? '#fff' : '#000',
              justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
            }}
          >
            {msg.role === 'bot' && (
              <img src={ChatBotLog} alt="" style={{width:'10%'}} />
            )}
            <div
              style={{
                backgroundColor: msg.role === 'user' ? '#4b4b4b' : '#ffffffcc',
                color: msg.role === 'user' ? '#fff' : '#000',
                padding: '8px 12px',
                borderRadius: 10,
                maxWidth: '80%'
              }}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </div>
      <div style={{ padding: 10, borderTop: '1px solid rgba(255,255,255,0.1)' }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          style={{
            width: '93%',
            padding: 10,
            borderRadius: 12,
            border: 'none',
            outline: 'none',
            background: '#fff',
            color: '#000',
            fontSize: 14
          }}
          placeholder="Type here..."
        />
      </div>
    </div>
  );
};

export default ChatBot;

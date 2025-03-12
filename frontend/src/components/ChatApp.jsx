import React, { useState, useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import './ChatApp.css';

function ChatApp() {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    
    // Load chat history on initial load
    useEffect(() => {
        fetchChatHistory();
    }, []);
    
    // Auto-scroll to bottom when messages change
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);
    
    const fetchChatHistory = async () => {
        try {
            const response = await fetch('http://localhost:5001/api/chat/history');
            const history = await response.json();
            setMessages(history);
        } catch (error) {
            console.error('Error fetching chat history:', error);
        }
    };
    
    const handleSendMessage = async () => {
        if (!inputValue.trim()) return;
        
        const userMessage = inputValue;
        setInputValue('');
        
        // Add user message to chat
        setMessages(prev => [...prev, {
            role: 'user',
            content: userMessage,
            timestamp: Date.now()
        }]);
        
        setIsLoading(true);
        
        try {
            const response = await fetch('http://localhost:5001/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });
            
            const data = await response.json();
            
            if (response.ok) {
                setMessages(prev => [...prev, {
                    role: 'assistant',
                    content: data.response,
                    timestamp: Date.now(),
                    memories: data.memories_used
                }]);
            } else {
                throw new Error(data.error || 'Failed to get response');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'Sorry, there was an error processing your message.',
                timestamp: Date.now(),
                isError: true
            }]);
        } finally {
            setIsLoading(false);
        }
    };
    
    return (
        <div className="chat-container">
            <div className="chat-header">
                <h1>Memory-Enhanced Assistant</h1>
                <button 
                    className="clear-button"
                    onClick={() => setMessages([])}
                >
                    Clear Chat
                </button>
            </div>
            
            <div className="messages-container">
                {messages.map((message, index) => (
                    <MessageBubble 
                        key={index}
                        message={message}
                    />
                ))}
                {isLoading && (
                    <div className="message assistant">
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>
            
            <div className="input-container">
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    placeholder="Type a message..."
                    disabled={isLoading}
                />
                <button 
                    onClick={handleSendMessage}
                    disabled={isLoading}
                >
                    Send
                </button>
            </div>
        </div>
    );
}

export default ChatApp;

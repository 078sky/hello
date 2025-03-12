import React, { useState } from 'react';
import './MessageBubble.css';

function MessageBubble({ message }) {
    const [showMemories, setShowMemories] = useState(false);
    
    const formatTimestamp = (timestamp) => {
        return new Date(timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });
    };
    
    return (
        <div className={`message ${message.role} ${message.isError ? 'error' : ''}`}>
            <div className="message-content">
                {message.content}
                <span className="timestamp">
                    {formatTimestamp(message.timestamp)}
                </span>
            </div>
            
            {message.memories && message.memories.length > 0 && (
                <div className="memory-indicator">
                    <button 
                        className="memory-toggle"
                        onClick={() => setShowMemories(!showMemories)}
                    >
                        {showMemories ? 'Hide Memories' : `${message.memories.length} Memories Used`}
                    </button>
                    
                    {showMemories && (
                        <div className="memories-list">
                            {message.memories.map((memory, idx) => (
                                <div key={idx} className="memory-item">
                                    <div className="memory-content">
                                        {memory.content}
                                    </div>
                                    <div className="memory-meta">
                                        <span>Recalled {memory.recall_count} times</span>
                                        <span>Relevance: {(memory.relevance * 100).toFixed(1)}%</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default MessageBubble;

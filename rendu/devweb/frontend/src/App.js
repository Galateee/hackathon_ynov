import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [connected, setConnected] = useState(false);
    const messagesEndRef = useRef(null);

    const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

    // Check server connection on mount
    useEffect(() => {
        checkConnection();
        const interval = setInterval(checkConnection, 5000); // Check every 5 seconds
        return () => clearInterval(interval);
    }, []);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const checkConnection = async () => {
        try {
            const response = await axios.get(`${API_URL}/api/status`);
            setConnected(response.data.connected);
        } catch (error) {
            setConnected(false);
        }
    };

    const sendMessage = async (e) => {
        e.preventDefault();

        if (!input.trim()) return;
        if (!connected) {
            alert('❌ Server not connected. Please check your inference server.');
            return;
        }

        // Add user message to UI
        const userMessage = { role: 'user', content: input };
        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await axios.post(`${API_URL}/api/chat`, {
                message: input
            });

            // Add assistant response
            const assistantMessage = { role: 'assistant', content: response.data.reply };
            setMessages((prev) => [...prev, assistantMessage]);
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage = {
                role: 'assistant',
                content: '❌ Error: ' + (error.response?.data?.error || 'Failed to get response')
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const clearHistory = async () => {
        try {
            await axios.delete(`${API_URL}/api/history`);
            setMessages([]);
        } catch (error) {
            console.error('Error clearing history:', error);
        }
    };

    return (
        <div className="app-container">
            <header className="app-header">
                <div className="header-content">
                    <h1>💼 TechCorp AI Chat</h1>
                    <div className="header-info">
                        <span className={`status-indicator ${connected ? 'connected' : 'disconnected'}`}>
                            {connected ? '🟢 Connected' : '🔴 Disconnected'}
                        </span>
                    </div>
                </div>
            </header>

            <main className="chat-container">
                <div className="messages-container">
                    {messages.length === 0 ? (
                        <div className="empty-state">
                            <p>👋 Welcome to TechCorp AI Chat</p>
                            <p>Ask me anything about finance and business!</p>
                        </div>
                    ) : (
                        <>
                            {messages.map((msg, index) => (
                                <div key={index} className={`message ${msg.role}`}>
                                    <div className="message-avatar">
                                        {msg.role === 'user' ? '👤' : '🤖'}
                                    </div>
                                    <div className="message-content">
                                        {msg.content}
                                    </div>
                                </div>
                            ))}
                            {loading && (
                                <div className="message assistant">
                                    <div className="message-avatar">🤖</div>
                                    <div className="message-content loading">
                                        <span className="spinner"></span> Thinking...
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </>
                    )}
                </div>
            </main>

            <footer className="chat-footer">
                <form onSubmit={sendMessage} className="input-form">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask a question..."
                        disabled={!connected || loading}
                        className="message-input"
                    />
                    <button
                        type="submit"
                        disabled={!connected || loading}
                        className="send-button"
                    >
                        {loading ? '⏳' : '📤'} Send
                    </button>
                    <button
                        type="button"
                        onClick={clearHistory}
                        className="clear-button"
                        title="Clear conversation history"
                    >
                        🗑️ Clear
                    </button>
                </form>
            </footer>
        </div>
    );
}

export default App;

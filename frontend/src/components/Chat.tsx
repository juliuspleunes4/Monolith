import { useState } from 'react';
import { Conversation, Message } from '../types';
import { MessageList, MessageInput } from '.';
import './Chat.css';

interface ChatProps {
  conversation: Conversation | undefined;
  selectedModel: string;
  onUpdateConversation: (conversation: Conversation) => void;
}

const Chat: React.FC<ChatProps> = ({ conversation, selectedModel, onUpdateConversation }) => {
  const [isStreaming, setIsStreaming] = useState(false);

  const handleSendMessage = async (content: string) => {
    if (!conversation || !selectedModel) return;

    // Add user message
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    const updatedConversation = {
      ...conversation,
      messages: [...conversation.messages, userMessage],
      updatedAt: new Date(),
      title: conversation.messages.length === 0 ? content.slice(0, 50) : conversation.title,
    };

    onUpdateConversation(updatedConversation);

    // TODO: Implement actual API call with streaming
    setIsStreaming(true);
    
    // Placeholder: simulate assistant response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: 'This is a placeholder response. The backend API is not yet connected.',
        timestamp: new Date(),
      };

      onUpdateConversation({
        ...updatedConversation,
        messages: [...updatedConversation.messages, assistantMessage],
        updatedAt: new Date(),
      });

      setIsStreaming(false);
    }, 1500);
  };

  const suggestions = [
    {
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10" />
          <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
      ),
      text: "Explain quantum computing in simple terms"
    },
    {
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polyline points="16 18 22 12 16 6" />
          <polyline points="8 6 2 12 8 18" />
        </svg>
      ),
      text: "Write a Python function to sort a list"
    },
    {
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M12 2L2 7l10 5 10-5-10-5z" />
          <path d="M2 17l10 5 10-5M2 12l10 5 10-5" />
        </svg>
      ),
      text: "What are the best practices for React?"
    },
    {
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
        </svg>
      ),
      text: "Help me debug this code"
    }
  ];

  const handleSuggestionClick = (suggestion: string) => {
    handleSendMessage(suggestion);
  };

  if (!conversation) {
    return (
      <div className="chat">
        <div className="chat-empty">
          <div className="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <circle cx="12" cy="12" r="3" />
              <path d="M12 1v6m0 6v6M5.6 5.6l4.2 4.2m4.2 4.2l4.2 4.2M1 12h6m6 0h6M5.6 18.4l4.2-4.2m4.2-4.2l4.2-4.2" />
            </svg>
          </div>
          <h2>Hello, how can I help you?</h2>
          <div className="suggestions">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                className="suggestion-btn"
                onClick={() => handleSuggestionClick(suggestion.text)}
                disabled={!selectedModel}
              >
                <div className="suggestion-icon">{suggestion.icon}</div>
                <span className="suggestion-text">{suggestion.text}</span>
              </button>
            ))}
          </div>
        </div>
        <MessageInput
          onSendMessage={handleSendMessage}
          disabled={!selectedModel || isStreaming}
        />
      </div>
    );
  }

  return (
    <div className="chat">
      <div className="chat-header">
        <h2>{conversation.title}</h2>
        <div className="chat-actions">
          <button className="icon-btn" title="Export conversation">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" />
            </svg>
          </button>
        </div>
      </div>

      <MessageList messages={conversation.messages} isStreaming={isStreaming} />
      
      <MessageInput
        onSendMessage={handleSendMessage}
        disabled={!selectedModel || isStreaming}
      />
    </div>
  );
};

export default Chat;

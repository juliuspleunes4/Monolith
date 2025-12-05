import { useState, useEffect } from 'react';
import { Sidebar, Chat } from './components';
import { Conversation } from './types';
import './App.css';

const STORAGE_KEY = 'monolith_conversations';
const ACTIVE_CONVERSATION_KEY = 'monolith_active_conversation';
const SELECTED_MODEL_KEY = 'monolith_selected_model';

function App() {
  const [conversations, setConversations] = useState<Conversation[]>(() => {
    // Load conversations from localStorage on initial render
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        // Convert date strings back to Date objects
        return parsed.map((conv: any) => ({
          ...conv,
          createdAt: new Date(conv.createdAt),
          updatedAt: new Date(conv.updatedAt),
          messages: conv.messages.map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp),
          })),
        }));
      }
    } catch (error) {
      console.error('Failed to load conversations from localStorage:', error);
    }
    return [];
  });

  const [activeConversationId, setActiveConversationId] = useState<string | null>(() => {
    // Load active conversation ID from localStorage
    return localStorage.getItem(ACTIVE_CONVERSATION_KEY);
  });

  const [selectedModel, setSelectedModel] = useState<string>(() => {
    // Load selected model from localStorage
    return localStorage.getItem(SELECTED_MODEL_KEY) || '';
  });

  // Save conversations to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
    } catch (error) {
      console.error('Failed to save conversations to localStorage:', error);
    }
  }, [conversations]);

  // Save active conversation ID to localStorage whenever it changes
  useEffect(() => {
    if (activeConversationId) {
      localStorage.setItem(ACTIVE_CONVERSATION_KEY, activeConversationId);
    } else {
      localStorage.removeItem(ACTIVE_CONVERSATION_KEY);
    }
  }, [activeConversationId]);

  // Save selected model to localStorage whenever it changes
  useEffect(() => {
    if (selectedModel) {
      localStorage.setItem(SELECTED_MODEL_KEY, selectedModel);
    }
  }, [selectedModel]);

  const activeConversation = conversations.find(c => c.id === activeConversationId);

  const handleNewConversation = () => {
    const newConversation: Conversation = {
      id: crypto.randomUUID(),
      title: 'New conversation',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    setConversations([newConversation, ...conversations]);
    setActiveConversationId(newConversation.id);
  };

  const handleSelectConversation = (id: string) => {
    setActiveConversationId(id);
  };

  const handleDeleteConversation = (id: string) => {
    setConversations(conversations.filter(c => c.id !== id));
    if (activeConversationId === id) {
      setActiveConversationId(null);
    }
  };

  const handleUpdateConversation = (updatedConversation: Conversation) => {
    const exists = conversations.some(c => c.id === updatedConversation.id);
    
    if (exists) {
      // Update existing conversation
      setConversations(conversations.map(c => 
        c.id === updatedConversation.id ? updatedConversation : c
      ));
    } else {
      // Add new conversation
      setConversations([updatedConversation, ...conversations]);
      setActiveConversationId(updatedConversation.id);
    }
  };

  return (
    <div className="app">
      <Sidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        onNewConversation={handleNewConversation}
        onSelectConversation={handleSelectConversation}
        onDeleteConversation={handleDeleteConversation}
        selectedModel={selectedModel}
        onModelChange={setSelectedModel}
      />
      <Chat
        conversation={activeConversation}
        selectedModel={selectedModel}
        onUpdateConversation={handleUpdateConversation}
      />
    </div>
  );
}

export default App;

import { useState } from 'react';
import { Sidebar, Chat } from './components';
import { Conversation } from './types';
import './App.css';

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState<string>('');

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

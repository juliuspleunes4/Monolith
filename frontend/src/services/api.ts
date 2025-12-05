import { ChatRequest, Model, Conversation } from '../types';

const API_BASE_URL = '/api/v1';

class ApiService {
  async fetchModels(): Promise<Model[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/models`);
      if (!response.ok) {
        throw new Error('Failed to fetch models');
      }
      const data = await response.json();
      return data.models;
    } catch (error) {
      console.error('Error fetching models:', error);
      throw error;
    }
  }

  async loadModel(modelId: string): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/models/${modelId}/load`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Failed to load model');
      }
    } catch (error) {
      console.error('Error loading model:', error);
      throw error;
    }
  }

  async unloadModel(modelId: string): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/models/${modelId}/unload`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Failed to unload model');
      }
    } catch (error) {
      console.error('Error unloading model:', error);
      throw error;
    }
  }

  async *streamChat(request: ChatRequest): AsyncGenerator<string, void, unknown> {
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ...request, stream: true }),
      });

      if (!response.ok) {
        throw new Error('Failed to start chat stream');
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Response body is not readable');
      }

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') {
              return;
            }
            try {
              const parsed = JSON.parse(data);
              if (parsed.token) {
                yield parsed.token;
              }
              if (parsed.done) {
                return;
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e);
            }
          }
        }
      }
    } catch (error) {
      console.error('Error in chat stream:', error);
      throw error;
    }
  }

  async fetchConversations(): Promise<Conversation[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations`);
      if (!response.ok) {
        throw new Error('Failed to fetch conversations');
      }
      const data = await response.json();
      return data.conversations;
    } catch (error) {
      console.error('Error fetching conversations:', error);
      throw error;
    }
  }

  async createConversation(): Promise<Conversation> {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations`, {
        method: 'POST',
      });
      if (!response.ok) {
        throw new Error('Failed to create conversation');
      }
      return await response.json();
    } catch (error) {
      console.error('Error creating conversation:', error);
      throw error;
    }
  }

  async fetchConversation(conversationId: string): Promise<Conversation> {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch conversation');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching conversation:', error);
      throw error;
    }
  }

  async deleteConversation(conversationId: string): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to delete conversation');
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
      throw error;
    }
  }
}

export const apiService = new ApiService();

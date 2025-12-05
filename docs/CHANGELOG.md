# Changelog

All notable changes to Monolith will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- 2025-12-05: Created copilot-instructions.md with project architecture, guidelines, and development standards
- 2025-12-05: Initialized CHANGELOG.md for tracking project changes
- 2025-12-05: Added design guidelines to copilot-instructions.md (clean/minimal UI, chatbot-style interface)
- 2025-12-05: Created complete project structure with backend and frontend directories
- 2025-12-05: Added backend FastAPI application skeleton with routers for chat, models, and conversations
- 2025-12-05: Added backend Dockerfile with multi-stage build and security best practices
- 2025-12-05: Created requirements.txt with FastAPI, uvicorn, and core dependencies
- 2025-12-05: Added frontend React/TypeScript setup with Vite build configuration
- 2025-12-05: Added frontend Dockerfile with nginx for production serving
- 2025-12-05: Created docker-compose.yml for multi-container orchestration with health checks
- 2025-12-05: Added API.md documentation with endpoint specifications
- 2025-12-05: Created models directory with README for LLM model files
- 2025-12-05: Added .gitignore for Python, Node, Docker, and model files
- 2025-12-05: Implemented complete frontend UI with React components (Sidebar, Chat, MessageList, MessageInput, ModelSelector)
- 2025-12-05: Added global styles with light/dark theme support and CSS variables for consistent design
- 2025-12-05: Created TypeScript interfaces for Message, Conversation, Model, and API types
- 2025-12-05: Built Sidebar component with conversation list, new chat button, and theme toggle
- 2025-12-05: Built Chat component with empty state, header, and message handling
- 2025-12-05: Built MessageList component with message bubbles, avatars, and typing indicator
- 2025-12-05: Built MessageInput component with auto-resizing textarea and keyboard shortcuts
- 2025-12-05: Built ModelSelector component with dropdown for model selection
- 2025-12-05: Added API service layer with methods for models, chat streaming, and conversations
- 2025-12-05: Implemented clean, minimal design inspired by ChatGPT/Grok with appropriate icons throughout
- 2025-12-05: Fixed TypeScript errors and React imports for modern React patterns
- 2025-12-05: Connected chat functionality - messages now appear in conversation with placeholder responses
- 2025-12-05: Added conversation state management and message flow between user and assistant
- 2025-12-05: Enhanced empty state with "Hello, how can I help you?" greeting and clickable suggestion prompts
- 2025-12-05: Added suggestion buttons that automatically send prompts when clicked
- 2025-12-05: Made chat input bar always visible even when no model is selected (disabled state with prompt)
- 2025-12-05: Redesigned chat input with rounded pill shape, removed top border, and clean circular send button
- 2025-12-05: Enhanced chat bar visibility with thicker border, subtle shadow, and white background for better contrast
- 2025-12-05: Increased chat bar height to 68px with larger padding and 40px send button for better touch targets
- 2025-12-05: Added drop shadow below chat bar and redesigned layout with "Ask anything..." label, + icon for attachments, microphone button, and dark circular send button
- 2025-12-05: Removed placeholder text from textarea and made plus and microphone icons darker for better visibility
- 2025-12-05: Increased "Ask anything..." label font size to 14px and changed font weight to 400 for better readability
- 2025-12-05: Changed "Ask anything..." label to 16px with Inter font family for improved appearance
- 2025-12-05: Repositioned "Ask anything..." label to appear next to the plus icon instead of above it
- 2025-12-05: Aligned plus icon and label properly to the bottom baseline for better visual alignment
- 2025-12-05: Lightened "Ask anything..." label color to match other chat bar elements using tertiary text color with reduced opacity
- 2025-12-05: Removed "Please select a model" warning and always show suggestion buttons (disabled when no model selected)
- 2025-12-05: Enhanced suggestion buttons with icons, larger size, better spacing, and improved hover effects in 2-column grid layout
- 2025-12-05: Changed suggestion icon color to blue (#3b82f6)
- 2025-12-05: Changed empty state icon to aperture-style SVG icon
- 2025-12-05: Changed empty state icon to black neural network/cube icon representing AI/LLM models
- 2025-12-05: Updated suggestion icon color to #5170ff and configured favicon with comprehensive browser/device support

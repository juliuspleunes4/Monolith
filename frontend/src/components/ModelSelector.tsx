import { useState, useEffect } from 'react';
import { Model } from '../types';
import './ModelSelector.css';

interface ModelSelectorProps {
  selectedModel: string;
  onModelChange: (model: string) => void;
}

const ModelSelector: React.FC<ModelSelectorProps> = ({ selectedModel, onModelChange }) => {
  const [models, setModels] = useState<Model[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Fetch models from API
    // Placeholder: simulate API call
    setTimeout(() => {
      setModels([]);
      setLoading(false);
    }, 500);
  }, []);

  const selectedModelData = models.find(m => m.id === selectedModel);

  return (
    <div className="model-selector">
      <button
        className="model-selector-btn"
        onClick={() => setIsOpen(!isOpen)}
        disabled={loading || models.length === 0}
      >
        <div className="model-selector-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="3" />
            <path d="M12 1v6m0 6v6M5.6 5.6l4.2 4.2m4.2 4.2l4.2 4.2M1 12h6m6 0h6M5.6 18.4l4.2-4.2m4.2-4.2l4.2-4.2" />
          </svg>
        </div>
        <div className="model-selector-content">
          <div className="model-selector-label">Model</div>
          <div className="model-selector-value">
            {loading ? 'Loading...' : selectedModelData ? selectedModelData.name : 'No models available'}
          </div>
        </div>
        <div className="model-selector-chevron">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M6 9l6 6 6-6" />
          </svg>
        </div>
      </button>

      {isOpen && models.length > 0 && (
        <div className="model-dropdown">
          {models.map((model) => (
            <button
              key={model.id}
              className={`model-option ${selectedModel === model.id ? 'selected' : ''}`}
              onClick={() => {
                onModelChange(model.id);
                setIsOpen(false);
              }}
            >
              <div className="model-option-name">{model.name}</div>
              <div className="model-option-size">{model.size}</div>
              {model.loaded && <div className="model-loaded-indicator" title="Loaded" />}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default ModelSelector;

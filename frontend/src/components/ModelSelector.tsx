import { useState, useEffect, useRef } from 'react';
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
  const [dropdownTop, setDropdownTop] = useState(0);
  const buttonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const fetchModels = async () => {
      try {
        console.log('Fetching models from API...');
        const response = await fetch('http://localhost:8000/api/v1/models');
        const data = await response.json();
        console.log('Models fetched:', data.models);
        setModels(data.models || []);
        
        // Auto-select first model if none selected
        if (!selectedModel && data.models.length > 0) {
          onModelChange(data.models[0].id);
        }
      } catch (error) {
        console.error('Failed to fetch models:', error);
        setModels([]);
      } finally {
        console.log('Setting loading to false');
        setLoading(false);
      }
    };

    fetchModels();
  }, [selectedModel, onModelChange]);

  const selectedModelData = models.find(m => m.id === selectedModel);

  // Group models by category
  const modelsByCategory = models.reduce((acc, model) => {
    if (!acc[model.category]) {
      acc[model.category] = [];
    }
    acc[model.category].push(model);
    return acc;
  }, {} as Record<string, Model[]>);

  const categoryOrder: ('small' | 'medium' | 'large')[] = ['small', 'medium', 'large'];

  const handleToggle = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    console.log('Button clicked!', { loading, modelsCount: models.length, isOpen });
    if (buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      setDropdownTop(rect.bottom + 4);
    }
    setIsOpen(!isOpen);
  };

  return (
    <div className="model-selector" onClick={(e) => e.stopPropagation()}>
      <button
        ref={buttonRef}
        className="model-selector-btn"
        onClick={handleToggle}
        disabled={loading || models.length === 0}
        type="button"
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
        <div className="model-dropdown" style={{ top: `${dropdownTop}px` }}>
          {categoryOrder.map((category) => {
            const categoryModels = modelsByCategory[category];
            if (!categoryModels || categoryModels.length === 0) return null;

            const getCategoryIcon = () => {
              if (category === 'small') {
                return <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="3" /></svg>;
              } else if (category === 'medium') {
                return <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="6" /></svg>;
              } else {
                return <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10" /></svg>;
              }
            };

            return (
              <div key={category} className="model-category">
                <div className="model-category-badge">
                  {getCategoryIcon()}
                  <span>{category.toUpperCase()}</span>
                </div>
                {categoryModels.map((model) => (
                  <button
                    key={model.id}
                    className={`model-option ${selectedModel === model.id ? 'selected' : ''}`}
                    onClick={() => {
                      onModelChange(model.id);
                      setIsOpen(false);
                    }}
                  >
                    <div className="model-option-name">{model.name}</div>
                    <div className="model-option-size">
                      {model.size_mb >= 1000 
                        ? `${(model.size_mb / 1024).toFixed(2)} GB` 
                        : `${model.size_mb} MB`}
                    </div>
                    {model.loaded && <div className="model-loaded-indicator" title="Loaded" />}
                  </button>
                ))}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default ModelSelector;

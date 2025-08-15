# ALwrity It - Content Strategy Analysis Customization Feature

## 🎯 **Feature Overview**

**ALwrity It** allows users to customize AI-generated analysis components when they don't meet expectations. Users can manually edit data or use AI to regenerate with custom prompts, maintaining context from other analysis components.

### **Key Benefits:**
- ✅ **User Control**: Full control over AI-generated analysis
- ✅ **Flexibility**: Manual editing or AI-powered regeneration
- ✅ **Context Awareness**: AI considers other analysis components
- ✅ **Structured Output**: Consistent JSON responses via Gemini
- ✅ **Version History**: Track and revert changes
- ✅ **Preview Mode**: Compare original vs modified analysis

## 🏗️ **Technical Architecture**

### **File Structure**
```
frontend/src/components/ContentPlanningDashboard/components/StrategyIntelligence/
├── components/
│   ├── content_strategy_alwrityit/
│   │   ├── ALwrityItButton.tsx           # Main button component
│   │   ├── ALwrityItModal.tsx            # Main modal container
│   │   ├── ManualEditForm.tsx            # Manual editing form
│   │   ├── AIEditForm.tsx                # AI prompt form
│   │   ├── QuickRegenerateForm.tsx       # Quick AI regeneration
│   │   ├── AnalysisPreview.tsx           # Preview changes
│   │   ├── ModeSelector.tsx              # Mode selection interface
│   │   ├── VersionHistory.tsx            # Version tracking
│   │   └── TemplateLibrary.tsx           # Saved templates
│   └── [existing analysis cards]
├── hooks/
│   ├── content_strategy_alwrityit/
│   │   ├── useALwrityIt.ts               # Main hook for ALwrity It functionality
│   │   ├── useAnalysisRegeneration.ts    # AI regeneration logic
│   │   ├── useManualEditing.ts           # Manual editing logic
│   │   └── useVersionHistory.ts          # Version management
├── types/
│   ├── content_strategy_alwrityit/
│   │   ├── alwrityIt.types.ts            # TypeScript types
│   │   ├── analysisSchemas.ts            # JSON schemas for each component
│   │   └── promptTemplates.ts            # AI prompt templates
├── utils/
│   ├── content_strategy_alwrityit/
│   │   ├── analysisTransformers.ts       # Data transformation utilities
│   │   ├── promptGenerators.ts           # AI prompt generation
│   │   ├── schemaValidators.ts           # JSON schema validation
│   │   └── versionManager.ts             # Version control utilities
└── providers/
    └── ALwrityItProvider.tsx             # Context provider for state management
```

### **Backend Structure**
```
backend/api/content_planning/api/content_strategy/
├── endpoints/
│   ├── alwrityit_endpoints.py            # ALwrity It API endpoints
│   └── [existing endpoints]
├── services/
│   ├── alwrityit_service.py              # ALwrity It business logic
│   ├── analysis_regeneration_service.py  # AI regeneration service
│   └── version_management_service.py     # Version control service
└── models/
    ├── alwrityit_models.py               # Database models for versions/templates
    └── [existing models]
```

## 📋 **Implementation Phases**

### **Phase 1: Core Infrastructure (2-3 days)**

#### **1.1 Backend API Endpoints**
```python
# backend/api/content_planning/api/content_strategy/endpoints/alwrityit_endpoints.py

@router.post("/regenerate-analysis-component")
async def regenerate_analysis_component(request: RegenerateAnalysisRequest):
    """Regenerate specific analysis component with AI"""

@router.post("/update-analysis-component-manual")
async def update_analysis_component_manual(request: ManualUpdateRequest):
    """Update analysis component with manual edits"""

@router.get("/analysis-component-schema/{component_type}")
async def get_analysis_component_schema(component_type: str):
    """Get JSON schema for specific component type"""

@router.get("/analysis-versions/{strategy_id}/{component_type}")
async def get_analysis_versions(strategy_id: int, component_type: str):
    """Get version history for analysis component"""
```

#### **1.2 Frontend Core Components**
```typescript
// ALwrityItButton.tsx
const ALwrityItButton = ({ componentType, currentData, onUpdate }) => {
  return (
    <IconButton
      sx={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        '&:hover': { transform: 'scale(1.1)' },
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)',
      }}
      onClick={() => setModalOpen(true)}
    >
      <AutoAwesomeIcon />
    </IconButton>
  );
};
```

### **Phase 2: Modal & Mode Selection (1-2 days)**

#### **2.1 Main Modal Component**
```typescript
// ALwrityItModal.tsx
const ALwrityItModal = ({ open, onClose, componentType, currentData, onUpdate }) => {
  const [mode, setMode] = useState<ALwrityItMode>('manual');
  
  return (
    <Dialog open={open} onClose={onClose} maxWidth="lg" fullWidth>
      <DialogTitle>ALwrity It - {getComponentDisplayName(componentType)}</DialogTitle>
      <DialogContent>
        <ModeSelector mode={mode} onModeChange={setMode} />
        
        {mode === 'manual' && (
          <ManualEditForm componentType={componentType} currentData={currentData} />
        )}
        
        {mode === 'ai' && (
          <AIEditForm componentType={componentType} currentData={currentData} />
        )}
        
        {mode === 'regenerate' && (
          <QuickRegenerateForm componentType={componentType} />
        )}
      </DialogContent>
    </Dialog>
  );
};
```

#### **2.2 Mode Selector Component**
```typescript
// ModeSelector.tsx
const ModeSelector = ({ mode, onModeChange }) => {
  const modes = [
    {
      id: 'manual',
      title: 'Manual Edit',
      description: 'Edit analysis data manually',
      icon: <EditIcon />,
      color: '#4caf50'
    },
    {
      id: 'ai',
      title: 'AI Custom',
      description: 'Provide custom prompt for AI regeneration',
      icon: <AutoAwesomeIcon />,
      color: '#667eea'
    },
    {
      id: 'regenerate',
      title: 'Quick Regenerate',
      description: 'Regenerate with improved AI analysis',
      icon: <RefreshIcon />,
      color: '#ff9800'
    }
  ];
  
  return (
    <Grid container spacing={2}>
      {modes.map((modeOption) => (
        <Grid item xs={12} sm={4} key={modeOption.id}>
          <Card onClick={() => onModeChange(modeOption.id)}>
            <CardContent>
              <Box sx={{ color: modeOption.color }}>{modeOption.icon}</Box>
              <Typography variant="subtitle1">{modeOption.title}</Typography>
              <Typography variant="caption">{modeOption.description}</Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};
```

### **Phase 3: Manual Editing Interface (1-2 days)**

#### **3.1 Manual Edit Form**
```typescript
// ManualEditForm.tsx
const ManualEditForm = ({ componentType, currentData, onSave }) => {
  const schema = useAnalysisSchema(componentType);
  const [formData, setFormData] = useState(currentData);
  
  return (
    <Box>
      <Typography variant="h6">Manual Edit - {getComponentDisplayName(componentType)}</Typography>
      
      {Object.entries(schema.properties).map(([field, fieldSchema]) => (
        <DynamicFormField
          key={field}
          field={field}
          schema={fieldSchema}
          value={formData[field]}
          onChange={(value) => setFormData(prev => ({ ...prev, [field]: value }))}
        />
      ))}
      
      <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
        <Button variant="outlined" onClick={() => setFormData(currentData)}>
          Reset to Original
        </Button>
        <Button variant="contained" onClick={() => onSave(formData)}>
          Save Changes
        </Button>
      </Box>
    </Box>
  );
};
```

### **Phase 4: AI Integration (2-3 days)**

#### **4.1 AI Edit Form**
```typescript
// AIEditForm.tsx
const AIEditForm = ({ componentType, currentData, onGenerate }) => {
  const [prompt, setPrompt] = useState('');
  const [suggestedPrompts, setSuggestedPrompts] = useState([]);
  
  return (
    <Box>
      <Typography variant="h6">AI Custom Regeneration</Typography>
      
      <TextField
        fullWidth
        multiline
        rows={4}
        label="Custom AI Prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe how you want to improve this analysis..."
      />
      
      <Box sx={{ mt: 2 }}>
        {suggestedPrompts.map((suggestion, index) => (
          <Chip
            key={index}
            label={suggestion}
            onClick={() => setPrompt(suggestion)}
            sx={{ mr: 1, mb: 1 }}
          />
        ))}
      </Box>
      
      <Button 
        variant="contained" 
        onClick={() => onGenerate(prompt)}
        disabled={!prompt.trim()}
        startIcon={<AutoAwesomeIcon />}
      >
        Generate with AI
      </Button>
    </Box>
  );
};
```

#### **4.2 Backend AI Service**
```python
# backend/services/alwrityit_service.py
class ALwrityItService:
    async def regenerate_analysis_component(
        self,
        component_type: str,
        current_data: dict,
        user_prompt: str = None,
        context_data: dict = None
    ) -> dict:
        prompt = self._build_regeneration_prompt(
            component_type, current_data, user_prompt, context_data
        )
        
        schema = self._get_component_schema(component_type)
        
        response = await self.gemini_provider.generate_structured_response(
            prompt=prompt,
            schema=schema,
            context={
                "current_analysis": current_data,
                "other_components": context_data,
                "user_requirements": user_prompt,
                "component_type": component_type
            }
        )
        
        return response
```

### **Phase 5: Preview & Version Management (1-2 days)**

#### **5.1 Analysis Preview Component**
```typescript
// AnalysisPreview.tsx
const AnalysisPreview = ({ original, modified, componentType, onApply, onRevert }) => {
  return (
    <Box>
      <Typography variant="h6">Preview Changes</Typography>
      
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <Typography variant="subtitle2">Original Analysis</Typography>
          <AnalysisCard data={original} componentType={componentType} />
        </Grid>
        <Grid item xs={6}>
          <Typography variant="subtitle2">Modified Analysis</Typography>
          <AnalysisCard data={modified} componentType={componentType} />
        </Grid>
      </Grid>
      
      <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
        <Button variant="outlined" onClick={onRevert}>Revert Changes</Button>
        <Button variant="contained" onClick={onApply}>Apply Changes</Button>
      </Box>
    </Box>
  );
};
```

## 🎨 **UI/UX Design Specifications**

### **Color Scheme**
```typescript
const ALWRITY_IT_COLORS = {
  primary: '#667eea',
  secondary: '#764ba2',
  success: '#4caf50',
  warning: '#ff9800',
  error: '#f44336',
  background: {
    modal: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%)',
    card: 'rgba(255, 255, 255, 0.05)',
    button: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  }
};
```

## 🔧 **Database Schema**

### **Version History Table**
```sql
CREATE TABLE analysis_versions (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER NOT NULL,
    component_type VARCHAR(50) NOT NULL,
    version_data JSONB NOT NULL,
    change_type VARCHAR(20) NOT NULL,
    user_prompt TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    description TEXT
);
```

### **Templates Table**
```sql
CREATE TABLE analysis_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    component_type VARCHAR(50) NOT NULL,
    template_data JSONB NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    is_public BOOLEAN DEFAULT FALSE
);
```

## 🚀 **Implementation Timeline**

### **Week 1: Core Infrastructure**
- **Day 1-2**: Backend API endpoints and database models
- **Day 3-4**: Frontend component structure and basic modal
- **Day 5**: Integration with existing analysis cards

### **Week 2: AI Integration**
- **Day 1-2**: Gemini structured response integration
- **Day 3-4**: Prompt engineering and context handling
- **Day 5**: Testing and refinement

### **Week 3: Manual Editing & Polish**
- **Day 1-2**: Dynamic form generation and validation
- **Day 3-4**: Preview and comparison features
- **Day 5**: Version history and advanced features

## 🧪 **Testing Strategy**

### **Unit Tests**
- Component rendering and interactions
- Form validation and data transformation
- AI prompt generation and response parsing

### **Integration Tests**
- API endpoint functionality
- Database operations
- AI service integration

### **End-to-End Tests**
- Complete user workflows
- Error handling scenarios
- Performance testing

## 📊 **Success Metrics**

### **User Engagement**
- Number of ALwrity It button clicks per analysis
- Most frequently modified components
- User satisfaction with customization options

### **Technical Performance**
- AI generation response times
- Modal load times
- Error rates and recovery

## 🔄 **Future Enhancements**

### **Phase 2 Features**
1. **Collaboration Tools**: Team comments and approvals
2. **Advanced AI**: Multi-step regeneration with user feedback
3. **Integration**: Connect with external data sources
4. **Analytics**: Detailed usage analytics and insights
5. **Templates**: Community template sharing

---

**Next Steps**: 
1. Review and approve this implementation plan
2. Set up development environment
3. Begin Phase 1 implementation
4. Create project milestones and tracking
5. Set up testing infrastructure 
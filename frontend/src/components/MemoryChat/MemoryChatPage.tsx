import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Box,
  TextField,
  IconButton,
  Typography,
  Card,
  CardContent,
  Chip,
  Button,
  Grid,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Fab,
  Divider,
  CircularProgress,
  Alert,
  Tooltip,
  AppBar,
  Toolbar
} from '@mui/material';
import {
  Send as SendIcon,
  Psychology as MindIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  ArrowBack as BackIcon,
  Refresh as RefreshIcon,
  FilterList as FilterIcon,
  Search as SearchIcon,
  Chat as ChatIcon,
  SmartToy as AIIcon,
  Person as UserIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { memoryApi, Memory, ChatResponse, MemoryStatistics } from '../../services/memoryApi';

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  memories?: Memory[];
  context?: any;
}

const MemoryChatPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [memories, setMemories] = useState<Memory[]>([]);
  const [memoryStats, setMemoryStats] = useState<MemoryStatistics | null>(null);
  const [selectedMemory, setSelectedMemory] = useState<Memory | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [searchFilter, setSearchFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [loadingMemories, setLoadingMemories] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  const userId = 1; // This would come from user context in real app

  useEffect(() => {
    loadInitialData();
    addWelcomeMessage();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadInitialData = async () => {
    setLoadingMemories(true);
    try {
      const [memoriesData, statsData] = await Promise.all([
        memoryApi.getAllMemories(userId, 50),
        memoryApi.getMemoryStatistics(userId)
      ]);
      setMemories(memoriesData);
      setMemoryStats(statsData);
    } catch (error) {
      console.error('Failed to load initial data:', error);
    } finally {
      setLoadingMemories(false);
    }
  };

  const addWelcomeMessage = () => {
    const welcomeMessage: ChatMessage = {
      id: 'welcome',
      type: 'system',
      content: `Welcome to ALwrity Memory Chat! 🧠\n\nI can help you explore and interact with your stored content strategies. Here are some things you can ask me:\n\n• "What are my most successful content strategies?"\n• "Show me strategies for the technology industry"\n• "What content pillars have I used most?"\n• "How have my strategies evolved over time?"\n\nFeel free to ask me anything about your digital marketing memories!`,
      timestamp: new Date()
    };
    setMessages([welcomeMessage]);
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim() || loading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: currentMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setLoading(true);

    try {
      // Get relevant memories and context
      const chatResponse = await memoryApi.chatWithMemories(userId, currentMessage);
      
      // Create assistant response
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: generateResponseFromContext(currentMessage, chatResponse),
        timestamp: new Date(),
        memories: chatResponse.relevant_memories,
        context: chatResponse.memory_context
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: 'I apologize, but I encountered an error while searching your memories. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const generateResponseFromContext = (query: string, response: ChatResponse): string => {
    if (response.relevant_memories.length === 0) {
      return `I couldn't find any memories directly related to "${query}". This might be because:\n\n• You haven't created strategies in this area yet\n• The keywords might not match exactly\n• Try rephrasing your question\n\nWould you like me to show you all your available memories instead?`;
    }

    const memoryCount = response.relevant_memories.length;
    const industries = [...new Set(response.relevant_memories.map(m => m.industry))];
    const categories = [...new Set(response.relevant_memories.flatMap(m => m.categories))];

    let responseText = `I found ${memoryCount} relevant memories for your query about "${query}".\n\n`;

    if (industries.length > 0) {
      responseText += `**Industries covered:** ${industries.join(', ')}\n`;
    }

    if (categories.length > 0) {
      responseText += `**Key categories:** ${categories.slice(0, 5).join(', ')}\n\n`;
    }

    responseText += `**Key insights from your memories:**\n`;
    
    response.memory_context.slice(0, 3).forEach((context, index) => {
      responseText += `\n${index + 1}. **${context.strategy_name}** (${context.industry})\n`;
      responseText += `   ${context.summary}\n`;
    });

    if (response.relevant_memories.length > 3) {
      responseText += `\n...and ${response.relevant_memories.length - 3} more memories. View the full details below.`;
    }

    return responseText;
  };

  const handleDeleteMemory = async (memory: Memory) => {
    try {
      const success = await memoryApi.deleteMemory(userId, memory.strategy_id);
      if (success) {
        setMemories(prev => prev.filter(m => m.id !== memory.id));
        setDeleteDialogOpen(false);
        setSelectedMemory(null);
        // Add system message about deletion
        const deleteMessage: ChatMessage = {
          id: Date.now().toString(),
          type: 'system',
          content: `Memory for "${memory.strategy_name}" has been deleted successfully.`,
          timestamp: new Date()
        };
        setMessages(prev => [...prev, deleteMessage]);
      }
    } catch (error) {
      console.error('Failed to delete memory:', error);
    }
  };

  const handleRefreshMemories = () => {
    loadInitialData();
  };

  const filteredMemories = memories.filter(memory => {
    const matchesSearch = !searchFilter || 
      memory.strategy_name.toLowerCase().includes(searchFilter.toLowerCase()) ||
      memory.industry.toLowerCase().includes(searchFilter.toLowerCase()) ||
      memory.content.toLowerCase().includes(searchFilter.toLowerCase());
    
    const matchesCategory = !categoryFilter || 
      memory.categories.includes(categoryFilter);
    
    return matchesSearch && matchesCategory;
  });

  const suggestedQuestions = [
    "What are my most recent content strategies?",
    "Show me strategies for digital marketing",
    "What content pillars have been most effective?",
    "How many strategies do I have per industry?",
    "What competitive analysis insights do I have?"
  ];

  const MessageComponent: React.FC<{ message: ChatMessage }> = ({ message }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Box
        sx={{
          display: 'flex',
          justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
          mb: 2
        }}
      >
        <Box
          sx={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: 1,
            maxWidth: '80%'
          }}
        >
          {message.type !== 'user' && (
            <Avatar
              sx={{
                width: 32,
                height: 32,
                bgcolor: message.type === 'system' ? 'info.main' : 'primary.main'
              }}
            >
              {message.type === 'system' ? <MindIcon /> : <AIIcon />}
            </Avatar>
          )}
          
          <Paper
            sx={{
              p: 2,
              bgcolor: message.type === 'user' ? 'primary.main' : 'background.paper',
              color: message.type === 'user' ? 'primary.contrastText' : 'text.primary',
              borderRadius: 2
            }}
          >
            <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
              {message.content}
            </Typography>
            
            {message.memories && message.memories.length > 0 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" sx={{ mb: 1 }}>
                  Related Memories:
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {message.memories.slice(0, 3).map((memory) => (
                    <Chip
                      key={memory.id}
                      label={memory.strategy_name}
                      size="small"
                      variant="outlined"
                      onClick={() => setSelectedMemory(memory)}
                      sx={{ cursor: 'pointer' }}
                    />
                  ))}
                </Box>
              </Box>
            )}
            
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              {message.timestamp.toLocaleTimeString()}
            </Typography>
          </Paper>
          
          {message.type === 'user' && (
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
              <UserIcon />
            </Avatar>
          )}
        </Box>
      </Box>
    </motion.div>
  );

  return (
    <Container maxWidth={false} sx={{ height: '100vh', p: 0 }}>
      {/* Header */}
      <AppBar position="static" color="default" elevation={1}>
        <Toolbar>
          <IconButton
            edge="start"
            onClick={() => navigate('/content-planning')}
            sx={{ mr: 2 }}
          >
            <BackIcon />
          </IconButton>
          <MindIcon sx={{ mr: 1 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Chat with your ALwrity Memory
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {memoryStats ? `${memoryStats.total_memories} memories available` : 'Loading...'}
          </Typography>
        </Toolbar>
      </AppBar>

      <Grid container sx={{ height: 'calc(100vh - 64px)' }}>
        {/* Chat Area */}
        <Grid item xs={12} md={8}>
          <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            {/* Messages */}
            <Box
              sx={{
                flexGrow: 1,
                overflow: 'auto',
                p: 2,
                backgroundColor: 'grey.50'
              }}
            >
              {messages.map((message) => (
                <MessageComponent key={message.id} message={message} />
              ))}
              
              {loading && (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
                  <CircularProgress size={24} />
                  <Typography variant="body2" sx={{ ml: 1 }}>
                    Searching your memories...
                  </Typography>
                </Box>
              )}
              
              <div ref={messagesEndRef} />
            </Box>

            {/* Suggested Questions */}
            {messages.length <= 1 && (
              <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
                <Typography variant="subtitle2" sx={{ mb: 1 }}>
                  Try asking:
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {suggestedQuestions.map((question) => (
                    <Chip
                      key={question}
                      label={question}
                      variant="outlined"
                      size="small"
                      onClick={() => setCurrentMessage(question)}
                      sx={{ cursor: 'pointer' }}
                    />
                  ))}
                </Box>
              </Box>
            )}

            {/* Message Input */}
            <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  placeholder="Ask about your content strategies, memories, or insights..."
                  value={currentMessage}
                  onChange={(e) => setCurrentMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                  multiline
                  maxRows={3}
                  disabled={loading}
                />
                <IconButton
                  onClick={handleSendMessage}
                  disabled={!currentMessage.trim() || loading}
                  color="primary"
                  size="large"
                >
                  <SendIcon />
                </IconButton>
              </Box>
            </Box>
          </Box>
        </Grid>

        {/* Memory Sidebar */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ height: '100%', borderRadius: 0 }}>
            <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">Your Memories</Typography>
                <IconButton onClick={handleRefreshMemories} size="small">
                  <RefreshIcon />
                </IconButton>
              </Box>
              
              <TextField
                fullWidth
                size="small"
                placeholder="Search memories..."
                value={searchFilter}
                onChange={(e) => setSearchFilter(e.target.value)}
                InputProps={{
                  startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />
                }}
                sx={{ mb: 1 }}
              />
            </Box>

            <Box sx={{ height: 'calc(100% - 120px)', overflow: 'auto' }}>
              {loadingMemories ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                  <CircularProgress />
                </Box>
              ) : filteredMemories.length === 0 ? (
                <Box sx={{ p: 3, textAlign: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    {searchFilter ? 'No memories match your search' : 'No memories found'}
                  </Typography>
                </Box>
              ) : (
                <List>
                  {filteredMemories.map((memory) => (
                    <ListItem
                      key={memory.id}
                      button
                      onClick={() => setSelectedMemory(memory)}
                      sx={{ borderBottom: 1, borderColor: 'divider' }}
                    >
                      <ListItemText
                        primary={memory.strategy_name}
                        secondary={
                          <Box>
                            <Typography variant="caption" color="text.secondary">
                              {memory.industry} • {memory.user_type.replace('_', ' ')}
                            </Typography>
                            <Box sx={{ mt: 0.5 }}>
                              {memory.categories.slice(0, 2).map((cat) => (
                                <Chip
                                  key={cat}
                                  label={cat}
                                  size="small"
                                  variant="outlined"
                                  sx={{ mr: 0.5, fontSize: '0.7rem', height: 20 }}
                                />
                              ))}
                            </Box>
                          </Box>
                        }
                      />
                      <ListItemSecondaryAction>
                        <IconButton
                          edge="end"
                          size="small"
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedMemory(memory);
                            setDeleteDialogOpen(true);
                          }}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </ListItemSecondaryAction>
                    </ListItem>
                  ))}
                </List>
              )}
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Memory Detail Dialog */}
      <Dialog
        open={Boolean(selectedMemory)}
        onClose={() => setSelectedMemory(null)}
        maxWidth="md"
        fullWidth
      >
        {selectedMemory && (
          <>
            <DialogTitle>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Typography variant="h6">{selectedMemory.strategy_name}</Typography>
                <IconButton onClick={() => setSelectedMemory(null)}>
                  <CloseIcon />
                </IconButton>
              </Box>
            </DialogTitle>
            <DialogContent>
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Industry: {selectedMemory.industry} • Type: {selectedMemory.user_type.replace('_', ' ')}
                </Typography>
                <Box sx={{ mt: 1 }}>
                  {selectedMemory.categories.map((category) => (
                    <Chip
                      key={category}
                      label={category}
                      size="small"
                      variant="outlined"
                      sx={{ mr: 0.5, mb: 0.5 }}
                    />
                  ))}
                </Box>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                {selectedMemory.content}
              </Typography>
            </DialogContent>
            <DialogActions>
              <Button
                onClick={() => {
                  setDeleteDialogOpen(true);
                }}
                color="error"
                startIcon={<DeleteIcon />}
              >
                Delete Memory
              </Button>
              <Button onClick={() => setSelectedMemory(null)}>
                Close
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Delete Memory</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete the memory for "{selectedMemory?.strategy_name}"? 
            This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={() => selectedMemory && handleDeleteMemory(selectedMemory)}
            color="error"
            variant="contained"
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default MemoryChatPage;
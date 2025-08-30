import React from 'react';
import { Box, Container, Typography, TextField, Paper } from '@mui/material';
import { CopilotSidebar } from '@copilotkit/react-ui';
import { useCopilotReadable, useCopilotAction } from '@copilotkit/react-core';
import '@copilotkit/react-ui/styles.css';

const useCopilotActionTyped = useCopilotAction as any;

const FacebookWriter: React.FC = () => {
  const [postDraft, setPostDraft] = React.useState<string>('');
  const [notes, setNotes] = React.useState<string>('');

  // Share current draft and notes with Copilot
  useCopilotReadable({
    description: 'Current Facebook post draft text the user is editing',
    value: postDraft,
    categories: ['social', 'facebook', 'draft']
  });
  useCopilotReadable({
    description: 'User notes/context for the next Facebook post',
    value: notes,
    categories: ['social', 'facebook', 'context']
  });

  // Allow Copilot to update the draft directly (predictive state-like edit)
  useCopilotActionTyped({
    name: 'updateFacebookPostDraft',
    description: 'Replace the Facebook post draft with provided content',
    parameters: [
      { name: 'content', type: 'string', description: 'The full post content to set', required: true }
    ],
    handler: async ({ content }: { content: string }) => {
      setPostDraft(content);
      return { success: true, message: 'Draft updated' };
    }
  });

  // Let Copilot append text to the draft (collaborative editing)
  useCopilotActionTyped({
    name: 'appendToFacebookPostDraft',
    description: 'Append text to the current Facebook post draft',
    parameters: [
      { name: 'content', type: 'string', description: 'The text to append', required: true }
    ],
    handler: async ({ content }: { content: string }) => {
      setPostDraft(prev => (prev ? `${prev}\n\n${content}` : content));
      return { success: true, message: 'Text appended' };
    }
  });

  const suggestions = [
    { title: '🎉 Launch teaser', message: 'Write a short Facebook post announcing our new feature launch' },
    { title: '💡 Benefit-first', message: 'Draft a Facebook post highlighting a key user benefit with a CTA' },
    { title: '🔁 Variations', message: 'Generate 3 alternative versions of this post to A/B test' },
    { title: '🏷️ Hashtags', message: 'Suggest 5 relevant hashtags for this post' }
  ];

  return (
    <CopilotSidebar
      className="alwrity-copilot-sidebar"
      labels={{
        title: 'ALwrity • Facebook Writer',
        initial: 'Tell me what you want to post. I can draft, refine, and generate variants. I can also update the draft directly for you.'
      }}
      suggestions={suggestions}
    >
      <Box sx={{ py: 4 }}>
        <Container maxWidth="md">
          <Typography variant="h4" sx={{ color: 'white', fontWeight: 800, mb: 2 }}>
            Facebook Writer (Preview)
          </Typography>
          <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.85)', mb: 3 }}>
            Collaborate with the Copilot to craft your post. The assistant can update the draft directly.
          </Typography>

          <Paper sx={{ p: 2, background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.3)' }}>
            <Typography variant="subtitle2" sx={{ color: 'rgba(255,255,255,0.9)', mb: 1 }}>
              Context/Notes (optional)
            </Typography>
            <TextField
              fullWidth
              multiline
              minRows={2}
              value={notes}
              onChange={e => setNotes(e.target.value)}
              placeholder="Audience, campaign, tone, key points..."
              sx={{
                mb: 2,
                '& .MuiInputBase-root': { color: 'white' },
                '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.3)' }
              }}
            />

            <Typography variant="subtitle2" sx={{ color: 'rgba(255,255,255,0.9)', mb: 1 }}>
              Post Draft
            </Typography>
            <TextField
              fullWidth
              multiline
              minRows={6}
              value={postDraft}
              onChange={e => setPostDraft(e.target.value)}
              placeholder="Your Facebook post will appear here. Ask the Copilot to draft or update it."
              sx={{
                '& .MuiInputBase-root': { color: 'white' },
                '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(255,255,255,0.3)' }
              }}
            />
          </Paper>
        </Container>
      </Box>
    </CopilotSidebar>
  );
};

export default FacebookWriter;



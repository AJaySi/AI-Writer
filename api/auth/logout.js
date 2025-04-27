import { withSessionRoute } from '../../lib/middleware/session';

async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  
  // Clear the session
  req.session.destroy();
  
  return res.status(200).json({ success: true });
}

export default withSessionRoute(handler);
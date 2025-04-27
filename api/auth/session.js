import { withSessionRoute } from '../../lib/middleware/session';

function handler(req, res) {
  // Return the user from the session
  return res.status(200).json({ user: req.session.user || null });
}

export default withSessionRoute(handler);
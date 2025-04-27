import { OAuth2Client } from 'google-auth-library';
import { TwitterApi } from 'twitter-api-v2';
import { withSessionRoute } from '../../lib/middleware/session';

// Initialize OAuth clients
const googleClient = new OAuth2Client({
  clientId: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  redirectUri: `${process.env.FINE_URL}/api/auth/callback/google`
});

const twitterClient = new TwitterApi({
  clientId: process.env.TWITTER_CLIENT_ID,
  clientSecret: process.env.TWITTER_CLIENT_SECRET
});

async function handler(req, res) {
  const { provider } = req.query;
  
  try {
    switch (provider) {
      case 'google':
        const googleAuthUrl = googleClient.generateAuthUrl({
          access_type: 'offline',
          scope: ['profile', 'email']
        });
        return res.redirect(googleAuthUrl);
        
      case 'twitter':
        const { url, codeVerifier, state } = twitterClient.generateOAuth2AuthLink(
          `${process.env.FINE_URL}/api/auth/callback/twitter`,
          { scope: ['tweet.read', 'users.read'] }
        );
        
        // Store codeVerifier and state in session for verification during callback
        req.session.twitter = { codeVerifier, state };
        await req.session.save();
        
        return res.redirect(url);
        
      default:
        return res.status(400).json({ error: 'Unsupported provider' });
    }
  } catch (error) {
    console.error(`Error initiating ${provider} auth:`, error);
    return res.status(500).json({ error: 'Authentication failed' });
  }
}

export default withSessionRoute(handler);
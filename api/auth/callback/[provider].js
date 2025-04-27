import { OAuth2Client } from 'google-auth-library';
import { TwitterApi } from 'twitter-api-v2';
import { createUser, getUserByEmail } from '../../../lib/db/user';
import { withSessionRoute } from '../../../lib/middleware/session';

// Initialize OAuth clients
const googleClient = new OAuth2Client({
  clientId: process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  redirectUri: `${process.env.FINE_URL}/api/auth/callback/google`
});

async function handler(req, res) {
  const { provider } = req.query;
  const { code } = req.query;
  
  try {
    let userData;
    
    switch (provider) {
      case 'google':
        // Exchange code for tokens
        const { tokens } = await googleClient.getToken(code);
        googleClient.setCredentials(tokens);
        
        // Get user info
        const googleUser = await googleClient.request({
          url: 'https://www.googleapis.com/oauth2/v3/userinfo'
        });
        
        userData = {
          id: googleUser.data.sub,
          email: googleUser.data.email,
          name: googleUser.data.name,
          image: googleUser.data.picture,
          provider: 'google'
        };
        break;
        
      case 'twitter':
        // Get stored verifier and state from session
        const { codeVerifier, state } = req.session.twitter;
        
        // Verify state matches to prevent CSRF attacks
        if (state !== req.query.state) {
          return res.status(400).json({ error: 'Invalid state' });
        }
        
        // Exchange code for tokens
        const twitterClient = new TwitterApi({
          clientId: process.env.TWITTER_CLIENT_ID,
          clientSecret: process.env.TWITTER_CLIENT_SECRET
        });
        
        const { client: loggedClient } = await twitterClient.loginWithOAuth2({
          code,
          codeVerifier,
          redirectUri: `${process.env.FINE_URL}/api/auth/callback/twitter`
        });
        
        // Get user info
        const twitterUser = await loggedClient.v2.me({
          'user.fields': ['profile_image_url', 'name', 'username']
        });
        
        userData = {
          id: twitterUser.data.id,
          email: `${twitterUser.data.username}@twitter.user`, // Twitter doesn't provide email
          name: twitterUser.data.name,
          image: twitterUser.data.profile_image_url,
          provider: 'twitter'
        };
        break;
        
      default:
        return res.status(400).json({ error: 'Unsupported provider' });
    }
    
    // Find or create user in database
    let user = await getUserByEmail(userData.email);
    
    if (!user) {
      user = await createUser({
        email: userData.email,
        name: userData.name,
        image: userData.image,
        providerId: userData.id,
        provider: userData.provider
      });
    }
    
    // Set user in session
    req.session.user = {
      id: user.id,
      email: user.email,
      name: user.name,
      image: user.image
    };
    await req.session.save();
    
    // Redirect to app
    return res.redirect('/dashboard');
  } catch (error) {
    console.error(`Error handling ${provider} callback:`, error);
    return res.status(500).json({ error: 'Authentication failed' });
  }
}

export default withSessionRoute(handler);
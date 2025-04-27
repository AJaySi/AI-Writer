import { db } from './db';

export async function getUserByEmail(email) {
  try {
    const user = await db.query(`
      SELECT * FROM users WHERE email = $1
    `, [email]);
    
    return user.rows[0] || null;
  } catch (error) {
    console.error('Error getting user by email:', error);
    throw error;
  }
}

export async function createUser(userData) {
  try {
    const { email, name, image, providerId, provider } = userData;
    
    const result = await db.query(`
      INSERT INTO users (email, name, image, provider_id, provider)
      VALUES ($1, $2, $3, $4, $5)
      RETURNING *
    `, [email, name, image, providerId, provider]);
    
    return result.rows[0];
  } catch (error) {
    console.error('Error creating user:', error);
    throw error;
  }
}
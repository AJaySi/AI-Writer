# Security Policy

## 🔒 Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🚨 Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability within ALwrity, please follow these steps:

### 1. **DO NOT** create a public GitHub issue
Security vulnerabilities should be reported privately to prevent exploitation.

### 2. **Email us directly**
Send an email to: [security@alwrity.com](mailto:security@alwrity.com)

**Include the following information:**
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Suggested fix (if any)
- Your contact information

### 3. **Response Timeline**
- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution**: Within 30 days (depending on complexity)

### 4. **What to Expect**
- We will acknowledge receipt of your report
- We will investigate and validate the vulnerability
- We will provide regular updates on our progress
- We will coordinate the disclosure timeline with you
- We will credit you in our security advisories (unless you prefer to remain anonymous)

## 🛡️ Security Best Practices

### For Users
- Keep your ALwrity installation updated
- Use strong, unique passwords
- Enable two-factor authentication where available
- Regularly review your API keys and access permissions
- Report suspicious activity immediately

### For Developers
- Follow secure coding practices
- Validate all user inputs
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Keep dependencies updated
- Use HTTPS in production
- Implement rate limiting
- Log security-relevant events

## 🔐 Security Features

ALwrity implements the following security measures:

- **Authentication**: Secure user authentication with JWT tokens and Clerk integration
- **Authorization**: Role-based access control and subscription-based access
- **Input Validation**: Comprehensive input sanitization for all user inputs
- **API Security**: Rate limiting, request validation, and API key management
- **Data Encryption**: Sensitive data encryption at rest and in transit
- **CORS Protection**: Proper cross-origin resource sharing configuration
- **Security Headers**: Implementation of security headers and CSP policies
- **Dependency Scanning**: Regular dependency vulnerability scanning
- **AI Service Security**: Secure API key management for AI services
- **Content Sanitization**: Proper sanitization of AI-generated content
- **Database Security**: SQL injection prevention with SQLAlchemy ORM
- **File Upload Security**: Secure file handling and validation

## 🚫 Out of Scope

The following are considered out of scope for our security program:

- Social engineering attacks
- Physical attacks
- Attacks requiring physical access to the server
- Attacks requiring access to the local network
- Denial of service attacks
- Spam or social engineering issues
- Issues in third-party applications or services

## 🏆 Hall of Fame

We maintain a security hall of fame to recognize researchers who help improve ALwrity's security:

- Be the first to be listed here by responsibly reporting a vulnerability.

## 📞 Contact

For security-related questions or concerns:
- **Email**: [security@alwrity.com](mailto:security@alwrity.com)
- **GitHub**: Create a private security advisory
- **Response Time**: Within 48 hours

## 📜 Legal

By reporting a security vulnerability, you agree to:
- Allow us reasonable time to investigate and mitigate the issue
- Not publicly disclose the vulnerability until we have had a chance to address it
- Make a good faith effort to avoid privacy violations, destruction of data, and interruption or degradation of our services

## 🔄 Policy Updates

This security policy may be updated from time to time. We will notify users of any significant changes through our standard communication channels.

**Last Updated**: October 2026

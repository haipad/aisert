# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in Aisert, please report it responsibly.

### How to Report

**Please do NOT create a public GitHub issue for security vulnerabilities.**

Instead, please email us directly at: **hariprayush@gmail.com**

Include the following information:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (if you have them)

### What to Expect

- **Acknowledgment**: We'll acknowledge receipt within 48 hours
- **Assessment**: We'll assess the vulnerability within 5 business days
- **Updates**: We'll keep you informed of our progress
- **Resolution**: We'll work to resolve critical issues as quickly as possible
- **Credit**: We'll credit you in the security advisory (unless you prefer to remain anonymous)

### Security Considerations

Aisert handles:
- **API Keys**: Stored in environment variables, never logged
- **User Content**: Processed locally or sent to configured providers
- **Model Downloads**: Downloaded from trusted sources (HuggingFace, etc.)

### Best Practices for Users

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use secure methods to set environment variables
3. **Content**: Be mindful of sensitive data in validation content
4. **Dependencies**: Keep dependencies updated
5. **Network**: Use HTTPS for all API communications

### Scope

This security policy covers:
- The core Aisert library
- Official examples and documentation
- Dependencies and their security implications

### Out of Scope

- Third-party integrations not officially supported
- Issues in dependencies (report to respective maintainers)
- General usage questions (use GitHub Issues instead)

Thank you for helping keep Aisert secure! 🔒
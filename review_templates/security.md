# Security Code Review Template

## Input Validation
- [ ] All user inputs are properly validated
- [ ] Input validation occurs before processing
- [ ] Validation failure provides appropriate error messages

## Authentication & Authorization
- [ ] Authentication mechanisms follow best practices
- [ ] Authorization checks are present where needed
- [ ] Session management is secure

## Data Protection
- [ ] Sensitive data is encrypted in transit
- [ ] Sensitive data is encrypted at rest
- [ ] No sensitive information in logs or error messages
- [ ] Proper handling of secrets and credentials

## Common Vulnerabilities
- [ ] Protection against SQL Injection
- [ ] Protection against Cross-Site Scripting (XSS)
- [ ] Protection against Cross-Site Request Forgery (CSRF)
- [ ] Protection against Path Traversal

## Error Handling
- [ ] Errors are handled gracefully
- [ ] Error messages don't reveal sensitive information
- [ ] Error logging doesn't contain sensitive data

## Dependencies
- [ ] All dependencies are up-to-date
- [ ] No known vulnerabilities in dependencies

## Security Comments

<!-- Insert security-specific comments about the code here -->
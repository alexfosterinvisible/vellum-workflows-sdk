🚨 IMPORTANT: This is a living document of key learnings from working with the Vellum SDK. Each instruction is based on practical experience and should be updated as we learn more.

# Quick Reference Guide

## Core Concepts

1. **Prompt Management**
   - Always use deployment names instead of IDs for better maintainability
   - Store environment-specific variables in .env files
   - Use LATEST tag for development, specific tags for production

2. **Error Handling**
   - Always check prompt execution state for "REJECTED" status
   - Handle API rate limits with exponential backoff
   - Log all errors with context for debugging

3. **Best Practices**
   - Keep prompt inputs as structured data (JSON)
   - Use type hints for better code maintainability
   - Implement proper error handling for API calls
   - Always validate input data before sending to Vellum

4. **Development Workflow**
   - Test prompts with small inputs first
   - Use rich library for better CLI output
   - Keep prompt explorer modular for reusability
   - Document all functions and classes thoroughly

## Common Pitfalls

1. **API Integration**
   - Don't hardcode API keys
   - Don't assume prompt deployments exist
   - Don't ignore rate limits
   - Don't skip error handling

2. **Data Handling**
   - Don't pass unvalidated user input
   - Don't ignore response validation
   - Don't skip type checking
   - Don't assume response format

## Quick Commands

```bash
# List all active prompts
vellum-explorer list

# Execute prompt with inputs
vellum-explorer execute <prompt-name> --inputs '{"key": "value"}'

# Check prompt status
vellum-explorer list --status ACTIVE
``` 
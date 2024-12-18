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

## Common Commands

### Basic Operations
```bash
# List available prompts
vellum-explorer list --status ACTIVE

# Execute a prompt
vellum-explorer execute my-prompt --inputs '{"var": "value"}'

# Export results
vellum-explorer execute my-prompt --export results.xlsx

# Ask natural language questions about documentation
vellum-explorer ask "How do I handle authentication in the CLI?"
```

### Natural Language Documentation Queries

The CLI includes an AI-powered documentation assistant that can answer questions in natural language:

```bash
# Ask about authentication
vellum-explorer ask "How do I set up API keys?"

# Ask about error handling
vellum-explorer ask "What's the proper way to handle errors?"

# Ask about features and capabilities
vellum-explorer ask "What types of exports are supported?"
```

The assistant will:
1. Search through all documentation
2. Provide relevant answers with supporting evidence
3. Include code examples when available
4. Show confidence scores for the responses
``` 
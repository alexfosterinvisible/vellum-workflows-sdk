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

## PI API Contract Testing

1. **Authentication**
   - Use `x-api-key` header (not Bearer token)
   - API Key format: `pilabs_key_*`
   - Base URL: `https://api.withpi.ai/v1`

2. **Contract Generation**

   ```python
   # Generate dimensions for a contract
   response = await session.post(
       "https://api.withpi.ai/v1/contracts/generate_dimensions",
       json={"contract": {
           "name": "Math Skills",
           "description": "Test mathematical abilities"
       }}
   )
   ```

3. **Contract Scoring**

   ```python
   # Score an input/output pair against a contract
   response = await session.post(
       "https://api.withpi.ai/v1/contracts/score",
       json={
           "contract": contract_with_dimensions,  # From generation step
           "llm_input": "What is 2 + 2?",
           "llm_output": "The answer is 4."
       }
   )
   ```

4. **Best Practices**
   - Generate dimensions first, then use for scoring
   - Include detailed step-by-step explanations in outputs
   - Test with various input complexities
   - Monitor dimension scores for patterns

5. **Common Pitfalls**
   - Don't skip dimension generation step
   - Don't reuse dimensions across different contracts
   - Don't assume all dimensions have equal weight
   - Don't ignore subdimension scores

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

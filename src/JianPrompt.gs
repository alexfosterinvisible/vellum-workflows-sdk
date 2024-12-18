/**
 * Jian Prompt Executor - Google Apps Script Implementation
 * 
 * This script demonstrates executing the Jian prompt from Google Apps Script.
 * 
 * 1. Make HTTP requests to Vellum API
 * 2. Process responses
 * 3. Handle errors
 * v1
 */

const VELLUM_API_KEY = 'your-api-key'; // Replace with your API key
const BASE_URL = 'https://predict.vellum.ai/v1';

/**
 * Execute the Jian prompt with given input
 * 
 * @param {string} inputText - The input text to process
 * @return {string} The prompt response
 */
function executeJianPrompt(inputText) {
  const endpoint = `${BASE_URL}/execute-prompt`;
  
  const payload = {
    prompt_deployment_name: "jian",
    inputs: [
      {
        name: "user_input",
        value: inputText
      }
    ]
  };
  
  const options = {
    method: 'post',
    headers: {
      'X-API-KEY': VELLUM_API_KEY,
      'Content-Type': 'application/json',
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };
  
  try {
    const response = UrlFetchApp.fetch(endpoint, options);
    const result = JSON.parse(response.getContentText());
    
    if (result.state === "REJECTED") {
      throw new Error(`Prompt execution rejected: ${result.error?.message || 'Unknown error'}`);
    }
    
    return result.outputs?.[0]?.value || null;
    
  } catch (error) {
    console.error('Error executing Jian prompt:', error);
    return null;
  }
}

/**
 * Test the Jian prompt execution
 */
function testJianPrompt() {
  const testInput = "Tell me about the importance of clear code documentation";
  const result = executeJianPrompt(testInput);
  
  if (result) {
    Logger.log('Response:');
    Logger.log(result);
  } else {
    Logger.log('Error: Failed to get response');
  }
}

/**
 * Create a custom menu when the spreadsheet opens
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Jian Prompt')
    .addItem('Run Test', 'testJianPrompt')
    .addToUi();
} 
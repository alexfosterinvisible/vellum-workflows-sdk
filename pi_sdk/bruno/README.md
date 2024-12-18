# PI API Bruno Tests

This directory contains API tests using Bruno (https://www.usebruno.com/).

## Structure

```
bruno/
├── collections/          # API test collections
│   └── pi-api/
│       ├── auth/        # Authentication tests
│       ├── inference/   # Inference endpoint tests
│       ├── jobs/        # Job management tests
│       └── contracts/   # Contract-related tests
└── environments/        # Environment configurations
    ├── local.env.json   # Local testing environment
    └── prod.env.json    # Production environment
```

## Setup

1. Install Bruno CLI:
```bash
npm install -g @usebruno/cli
```

2. Set up environment:
   - Copy `environments/prod.env.json` to `environments/local.env.json`
   - Update `local.env.json` with your API key

## Running Tests

Run all tests:
```bash
bru run --env prod collections/pi-api
```

Run specific collection:
```bash
bru run --env prod collections/pi-api/auth
```

Run single test:
```bash
bru run --env prod collections/pi-api/auth/auth-test.bru
```

## Environment Variables

Required environment variables:
- `PI_API_KEY`: Your PI API key

## Adding New Tests

1. Create a new `.bru` file in the appropriate collection directory
2. Follow the existing test structure:
   ```bruno
   meta {
     name: Test Name
     type: http
     seq: 1
   }

   # Test description
   POST {{baseUrl}}/endpoint
   headers {
     Authorization: Bearer {{apiKey}}
   }
   body {
     // request body
   }

   tests {
     // assertions
   }
   ```

## Best Practices

1. Each test file should focus on a specific feature or endpoint
2. Use environment variables for configurable values
3. Include both positive and negative test cases
4. Add clear descriptions for each test case
5. Group related tests in the same collection 
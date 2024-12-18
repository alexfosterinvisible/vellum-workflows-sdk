# Feature Status Checklist

## Core Features
- [ ] Contract Generation (dev note: dimension generation stability?)
- [ ] Contract Scoring (dev note: score range standardization?)
- [ ] Feedback Clustering (dev note: cluster stability?)
- [ ] Input Generation (dev note: generation diversity?)
- [ ] Input Evaluation (dev note: evaluation consistency?)
- [ ] Inference Running (dev note: model availability?)
- [ ] Prompt Tuning (dev note: tuning convergence?)

## Job Management
- [ ] Job Status Polling (dev note: polling reliability?)
- [ ] Status Streaming (dev note: connection stability?)
- [ ] Multi-Job Handling (dev note: concurrent limits?)

## Data Processing
- [ ] Seed Generation (dev note: seed quality?)
- [ ] Data Clustering (dev note: cluster coherence?)
- [ ] Quality Filtering (dev note: filter accuracy?)

## Integration Features
- [ ] Python Code Execution (dev note: sandbox security?)
- [ ] Action Triggers (dev note: action reliability?)
- [ ] Batch Processing (dev note: batch limits?)

---

# Critical Questions for PI SDK Implementation

## Authentication & Rate Limits

1. Are there different API key types (test/prod)? (Guess: Yes, with different rate limits?)
2. What are the rate limits per endpoint? (Guess: 100/min for standard, 10/min for compute-heavy?)
3. Is there a retry-after header on 429s? (Guess: Yes?)

## Contract Structure

1. For `scoring_type: "PYTHON_CODE"`:
   - How is the code executed? In sandbox?
   - What libraries are available?
   - Are there security constraints?

2. For `action_dimension`:
   - What triggers the action?
   - Is it evaluated after main dimension?
   - Can actions trigger other actions?

3. Dimension Weights:
   - Are they normalized automatically? (Guess: Yes, sum to 1.0?)
   - What happens if weights are invalid?

## Feedback & Clustering

1. What's the max batch size for clustering? (Guess: 1000?)
2. Is clustering deterministic with same input?
3. For `rating`: Only "positive"/"negative" or more options?
4. For `source`: What values besides "internal"?

## Data Generation

1. `/data/input/generate_from_seeds`:
   - Max allowed `num_inputs`? (Guess: 100?)
   - Typical job completion time? (Guess: 1-5 min?)
   - Are generated inputs guaranteed unique?

2. `/data/input/generate_seeds`:
   - All available `context_types`?
   - Seeds per request? (Guess: 10?)
   - Can we influence seed diversity?

## Inference

1. Available `model_id` options besides "gpt_4o_mini_agent"?
2. Format of `structured` response? Model-dependent?
3. Model-specific parameters?
4. Token/length limits?

## Prompt Tuning

1. Other `tuning_algorithm` options besides "pi"?
2. Minimum examples needed? (Guess: 3?)
3. Can jobs be cancelled?
4. What determines completion? (Guess: Score/iterations?)

## SDK Design Questions

1. Job Status:
   - Recommended polling interval? (Guess: 2s with backoff?)
   - Do jobs expire? After how long?
   - Auto-polling in SDK? (Guess: Yes?)

2. Streaming:
   - Message format for tuning jobs?
   - Heartbeat mechanism?
   - Auto-reconnect on disconnect?

3. Error Handling:
   - Error code consistency?
   - 422 validation format?
   - Retry on 5xx? (Guess: Yes, with backoff?)

4. Implementation:
   - Immutable models? (Guess: Yes?)
   - Response caching? (Guess: Yes, with TTL?)
   - Response envelope parsing? (Guess: Yes?)

## Immediate Priorities

1. Contract model validation
2. Job status management
3. Error standardization
4. Rate limiting
5. Streaming support

These questions are critical for implementing a robust SDK. Guesses (marked with ?) are based on common patterns but need confirmation.

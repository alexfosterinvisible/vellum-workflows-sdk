# PI API Flow Patterns

## 1. Contract Creation and Evaluation Flow

**Steps:**
1. User creates initial contract with basic parameters
2. System generates dimensions to measure quality
3. User refines dimensions based on needs
4. Contract is used to score outputs
5. Scoring results inform prompt tuning
6. Tuned prompts generate new outputs
7. Cycle continues for continuous improvement

```
                                    [Contract Creation]
                                           |
                    +--------------------+ | +--------------------+
                    |                    v v v                    |
            [generate_dimensions] <--> [Contract] <--> [score]    |
                    ^                    ^ ^                      |
                    |                    | |                      |
            [tune/prompt] <--------------+ |                      |
                    ^                      |                      |
                    |                      |                      |
            [inference/run] <--------------+                      |
                    |                                            |
                    +--------------------------------------------+
```
**Assumptions:**
1. Contracts are the central organizing concept
2. Generated dimensions can be manually tweaked before use
3. Scoring drives tuning decisions
4. Tuned prompts feed back into contract refinement
5. Inference results can trigger contract updates

## 2. Data Generation and Evaluation Flow

**Steps:**
1. System generates initial seed examples
2. Seeds are expanded into larger dataset
3. Generated data is clustered for analysis
4. Each input is evaluated against contract
5. High-quality inputs used for tuning
6. Process repeats with refined criteria

```
                [generate_seeds]
                       |
                       v
            [generate_from_seeds]
                       |
                       v
              [data/input/cluster] ----+
                       |              |
                       v              v
                  [evaluate] --> [contracts/score]
                       |
                       v
                 [tune/prompt]
```
**Assumptions:**
1. Seed generation is the starting point for data collection
2. Generated data is clustered to understand patterns
3. Evaluation filters poor quality inputs
4. Scoring validates generated data quality
5. Results inform prompt tuning

## 3. Feedback Loop Flow

**Steps:**
1. Run inference to get outputs
2. Score outputs against contract
3. Collect and cluster user feedback
4. Use feedback to tune prompts
5. Validate improvements with scoring
6. Repeat until quality targets met

```
                [inference/run]
                      |
                      v
             [contracts/score] <---------+
                      |                 |
                      v                 |
            [feedback/cluster]          |
                      |                 |
                      v                 |
              [tune/prompt] ------------+
```
**Assumptions:**
1. Inference results are scored against contracts
2. Feedback is collected and clustered
3. Clusters inform prompt tuning
4. Tuning improves scoring results
5. Process repeats iteratively

## 4. Quality Improvement Flow

**Steps:**
1. Define quality contract
2. Generate test data in parallel
3. Score outputs and collect feedback
4. Consolidate quality signals
5. Tune prompts based on signals
6. Validate with inference
7. Iterate until quality improves

```
                    [Contract]
                        |
            +----------+----------+
            v          v          v
    [generate_seeds]  [score]  [evaluate]
            |          |          |
            v          v          v
    [generate_data]    |     [feedback]
            |          |          |
            +----------+----------+
                      |
                      v
                [tune/prompt]
                      |
                      v
                [inference/run]
```
**Assumptions:**
1. Quality is measured against contracts
2. Multiple data sources feed into tuning
3. Feedback and evaluation are parallel processes
4. Tuning consolidates multiple quality signals
5. Inference is the final validation

## 5. Streaming Job Management Flow

**Steps:**
1. Submit tuning job
2. Get job ID for tracking
3. Stream status updates
4. Monitor progress in real-time
5. Score results when complete
6. Handle multiple jobs concurrently

```
    [POST /tune/prompt] -----> [GET /tune/prompt/{job_id}]
           |                            |
           |                            v
           |                   [GET /messages (stream)]
           |                            |
           +----------------------------+
                        |
                        v
              [contracts/score]
```
**Assumptions:**
1. Long-running jobs use polling
2. Status updates are streamed
3. Jobs can be monitored in real-time
4. Final results trigger scoring
5. Multiple jobs can run in parallel

## Common Assumptions Across Flows:

**Steps:**
1. Start with contract definition
2. Generate and validate data
3. Collect feedback and metrics
4. Tune based on signals
5. Validate improvements
6. Repeat with refinements

1. **Contract Centrality**
   - Contracts define quality standards
   - Contracts evolve based on feedback
   - Contracts guide data generation

2. **Data Quality**
   - Generated data needs validation
   - Clustering helps understand patterns
   - Feedback improves quality over time

3. **Tuning Process**
   - Tuning is iterative
   - Multiple signals inform tuning
   - Tuning results can be measured

4. **System Integration**
   - Components are loosely coupled
   - Flows can be automated
   - Results are traceable

5. **Job Management**
   - Long operations are asynchronous
   - Status can be monitored
   - Operations can be chained
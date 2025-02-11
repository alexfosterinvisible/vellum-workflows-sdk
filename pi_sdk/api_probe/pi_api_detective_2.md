# PI API Core Features Investigation - Part 2

## Focus Features

### 1. Contract Generation
Status: Partially Explored
Priority: High

#### Current Understanding
- Dimensions can be generated from name/description
- Weights are normalized (1.0)
- Hierarchical structure (dimensions -> sub_dimensions)
- Strong schema validation

#### Next Experiments
1. **Contract Evolution Testing**
   - Generate multiple contracts with similar descriptions
   - Track dimension consistency
   - Test weight modifications
   - Measure generation time patterns

2. **Edge Case Testing**
   ```json
   {
     "tests": [
       {"type": "empty_description", "expected": "422"},
       {"type": "very_long_description", "expected": "200"},
       {"type": "special_characters", "expected": "200"},
       {"type": "minimal_contract", "expected": "200"}
     ]
   }
   ```

3. **Generation Stability**
   - Run same contract generation 10 times
   - Compare dimension structures
   - Analyze label consistency
   - Track timing patterns

### 2. Contract Scoring
Status: Partially Explored
Priority: High

#### Current Understanding
- Score range: 0.0 to 1.0
- Requires valid contract structure
- Sub-dimension scores influence total
- Fast response time (<1s)

#### Next Experiments
1. **Score Distribution Analysis**
   ```python
   test_cases = [
     {"type": "perfect_match", "expected_range": "0.9-1.0"},
     {"type": "partial_match", "expected_range": "0.4-0.6"},
     {"type": "no_match", "expected_range": "0.0-0.2"}
   ]
   ```

2. **Weight Impact Testing**
   - Modify dimension weights
   - Test same input with different weights
   - Analyze score changes
   - Document weight relationships

3. **Scoring Stability**
   - Score same input multiple times
   - Test with different contracts
   - Analyze score variance
   - Document any patterns

### 3. Feedback Clustering
Status: Initial Testing
Priority: High

#### Current Understanding
- Groups similar inputs automatically
- Returns descriptive topics
- Fast synchronous operation
- No apparent size limits found

#### Next Experiments
1. **Cluster Stability Testing**
   ```python
   stability_tests = [
     {"inputs": ["similar_1", "similar_2"], "expected": "same_cluster"},
     {"inputs": ["different_1", "different_2"], "expected": "different_clusters"},
     {"inputs": ["edge_case_1", "edge_case_2"], "expected": "deterministic"}
   ]
   ```

2. **Scale Testing**
   - Test with 10, 100, 1000 inputs
   - Measure clustering time
   - Check topic quality
   - Document any degradation

3. **Topic Generation Analysis**
   - Compare topic names for consistency
   - Test multilingual inputs
   - Analyze topic granularity
   - Document naming patterns

## Experiment Execution Plan

### Phase 1: Basic Validation (Day 1)
1. Run contract generation stability tests
2. Basic scoring distribution analysis
3. Initial cluster stability testing

### Phase 2: Edge Cases (Day 2)
1. Contract edge case testing
2. Scoring weight impact analysis
3. Clustering scale tests

### Phase 3: Deep Analysis (Day 3)
1. Contract generation patterns
2. Score stability patterns
3. Topic generation patterns

## Questions to Answer

### Contract Generation
1. How consistent are generated dimensions?
2. What affects generation time?
3. Are there hidden limits on contract complexity?

### Contract Scoring
1. How deterministic is scoring?
2. What's the weight influence formula?
3. Are there score normalization patterns?

### Feedback Clustering
1. What determines cluster boundaries?
2. How are topic names generated?
3. What are the practical size limits?

## Next Steps

1. Create automated test suite for all experiments
2. Set up data collection for pattern analysis
3. Design visualization for results
4. Prepare regression tests for findings

## Progress Tracking

### Completed
- Basic endpoint validation
- Initial schema testing
- Simple rate limit testing

### In Progress
- Contract generation stability
- Score distribution analysis
- Cluster stability testing

### Planned
- Edge case testing
- Scale testing
- Pattern analysis 
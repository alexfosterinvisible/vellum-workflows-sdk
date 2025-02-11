# Rate Limit Tests Experiment Results
**Date**: 2024-12-18 18:41:24
**Duration**: 64.54s

## Description
Test rate limiting behavior across different batch sizes and delays

## Results

### Test 1
```json
{
  "type": "inference_batch",
  "batch_size": 1,
  "delay": 0,
  "success_count": 1,
  "error_count": 0,
  "errors": []
}
```

### Test 2
```json
{
  "type": "inference_batch",
  "batch_size": 1,
  "delay": 0.1,
  "success_count": 1,
  "error_count": 0,
  "errors": []
}
```

### Test 3
```json
{
  "type": "inference_batch",
  "batch_size": 1,
  "delay": 0.5,
  "success_count": 1,
  "error_count": 0,
  "errors": []
}
```

### Test 4
```json
{
  "type": "inference_batch",
  "batch_size": 1,
  "delay": 1.0,
  "success_count": 1,
  "error_count": 0,
  "errors": []
}
```

### Test 5
```json
{
  "type": "inference_batch",
  "batch_size": 5,
  "delay": 0,
  "success_count": 5,
  "error_count": 0,
  "errors": []
}
```

### Test 6
```json
{
  "type": "inference_batch",
  "batch_size": 5,
  "delay": 0.1,
  "success_count": 5,
  "error_count": 0,
  "errors": []
}
```

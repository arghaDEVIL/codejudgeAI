# Hidden Testcase Security Implementation

## ✅ Security Measures Implemented

### 1. **API Endpoint Protection**

#### `/api/v1/testcases/problem/{problem_id}` (Public)
- Returns only **sample testcases** with full details (stdin, expected_output)
- Hidden testcases returned with **NULL** stdin and expected_output
- No authentication required (public endpoint)

#### `/api/v1/testcases/admin/problem/{problem_id}` (Admin Only)
- Returns ALL testcases with full details
- Requires admin authentication
- Used for testcase management

### 2. **Submission Judge Logic**

#### Execution Flow:
1. Fetch ALL testcases (sample + hidden) from database
2. Execute code against ALL testcases
3. Track results separately:
   - `sample_passed` / `sample_total`
   - `hidden_passed` / `hidden_total`
   - `total_passed` / `total_testcases`

#### Response Security:
- **Sample testcases**: Full details returned (stdin, expected, actual, error)
- **Hidden testcases**: NO details returned to frontend
- Only counts returned: `hidden_passed` / `hidden_total`

### 3. **Frontend Display**

#### Judge Page - Problem View:
- Shows only **sample testcases**
- Hidden testcases never displayed
- Users cannot see hidden test inputs/outputs

#### Submission Results:
```
┌─────────────────────────────────────┐
│ Score: 85.5/100                     │
├─────────────────────────────────────┤
│ Sample Tests:  2/2  ✓               │
│ Hidden Tests:  5/7  ✗               │
│ Overall:       7/9                  │
├─────────────────────────────────────┤
│ Execution Time: 125ms               │
│ Memory Used: 12.5 MB                │
└─────────────────────────────────────┘

Sample Testcase Results:
✓ Test 1: Passed
✓ Test 2: Passed

Hidden Tests: 5/7 passed
(Details not shown)
```

### 4. **Data Leak Prevention**

#### What's Protected:
- ❌ Hidden testcase stdin (input data)
- ❌ Hidden testcase expected_output
- ❌ Hidden testcase actual_output (unless failed)
- ❌ Hidden testcase error messages (unless failed)

#### What's Exposed:
- ✅ Count of hidden testcases
- ✅ Pass/fail status for hidden tests
- ✅ Overall score calculation
- ✅ Full details for sample testcases

### 5. **Database Storage**

#### TestcaseResult Table:
- Stores results for ALL testcases (sample + hidden)
- Contains actual_output and error_message
- **Never exposed to frontend for hidden tests**

#### Submission Table:
- Stores overall status and score
- No individual testcase details
- Safe to expose

### 6. **Verdict Logic**

```python
# Accepted only if ALL tests pass
if sample_passed == sample_total and hidden_passed == hidden_total:
    verdict = "Accepted"
else:
    verdict = "Wrong Answer" (or other status)
```

## 🔒 Security Guarantees

### ✅ What Users CAN See:
1. Sample testcase inputs and outputs
2. Their code's output for sample tests
3. Number of hidden testcases
4. How many hidden tests passed/failed
5. Overall score (0-100)
6. Execution time and memory usage

### ❌ What Users CANNOT See:
1. Hidden testcase inputs
2. Hidden testcase expected outputs
3. Their code's output for hidden tests (unless failed)
4. Error messages from hidden tests (unless failed)
5. Which specific hidden test failed

## 📊 Response Schema

### SubmissionResult Schema:
```python
{
    "submission_id": 123,
    "status": "Wrong Answer",
    "passed_testcases": 7,
    "total_testcases": 9,
    
    # Separate counts
    "sample_passed": 2,
    "sample_total": 2,
    "hidden_passed": 5,
    "hidden_total": 7,
    
    "score": 85.5,
    "max_score": 100.0,
    "execution_time": 125,
    "memory_used": 12.5,
    
    # Only sample testcase details
    "sample_results": [
        {
            "testcase_id": 1,
            "description": "Basic test",
            "status": "Passed",
            "stdin": "5",
            "expected_output": "120",
            "actual_output": "120",
            "execution_time": 50,
            "is_sample": true
        }
    ],
    
    "message": "Some testcases failed. Score: 85.5/100"
}
```

## 🎯 Use Cases

### Case 1: All Tests Pass
```
Sample Tests: 2/2 ✓
Hidden Tests: 7/7 ✓
Overall: Accepted
Score: 100/100
```

### Case 2: Sample Pass, Hidden Fail
```
Sample Tests: 2/2 ✓
Hidden Tests: 5/7 ✗
Overall: Wrong Answer
Score: 77.8/100
```

### Case 3: Sample Fail
```
Sample Tests: 1/2 ✗
Hidden Tests: 0/7 (not shown)
Overall: Wrong Answer
Score: 11.1/100

Sample Test 2 Failed:
Input: "10"
Expected: "3628800"
Your Output: "362880"
```

## 🔐 Admin Features

### Admin Can:
1. View ALL testcases with full details
2. Create/edit/delete testcases
3. Mark testcases as sample or hidden
4. Set testcase weights
5. View all submission details

### Admin Endpoints:
- `GET /api/v1/testcases/admin/problem/{id}` - All testcases
- `POST /api/v1/testcases/` - Create testcase
- `PUT /api/v1/testcases/{id}` - Update testcase
- `DELETE /api/v1/testcases/{id}` - Delete testcase

## 🚀 Testing Checklist

### Security Tests:
- [ ] Non-admin cannot see hidden testcase inputs
- [ ] Non-admin cannot see hidden testcase outputs
- [ ] API responses don't leak hidden data
- [ ] Browser console doesn't show hidden data
- [ ] Network tab doesn't show hidden data in responses

### Functional Tests:
- [ ] Sample testcases display correctly
- [ ] Hidden testcase counts display correctly
- [ ] Score calculation includes all tests
- [ ] Verdict is "Accepted" only if all pass
- [ ] Failed sample tests show details
- [ ] Failed hidden tests don't show details

## 📝 Implementation Files

### Backend:
- `backend/app/api/v1/endpoints/testcases.py` - Testcase filtering
- `backend/app/api/v1/endpoints/submissions.py` - Judge logic
- `backend/app/schemas/submission.py` - Response schema
- `backend/app/models/testcase.py` - Testcase model

### Frontend:
- `frontend/src/Judge.jsx` - Submission results display
- `frontend/src/utils/api.js` - API client

## 🎓 Best Practices

1. **Never log hidden testcase data** in server logs
2. **Always filter responses** before sending to frontend
3. **Use separate counts** for sample and hidden tests
4. **Show only pass/fail** for hidden tests
5. **Validate on server** - never trust client
6. **Admin-only endpoints** for sensitive data
7. **Clear error messages** without leaking data

## ✅ Compliance

This implementation follows industry standards used by:
- LeetCode
- Codeforces
- HackerRank
- CodeChef
- AtCoder

Hidden testcases remain completely secure while providing users with meaningful feedback about their solutions.

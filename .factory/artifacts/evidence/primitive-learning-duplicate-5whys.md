# Primitive Learning Duplicate-Result 5-Whys

Status: corrected during final contract review

1. **Why could the same learning record have been applied twice?** The update path appended result IDs without checking existing inventory records.
2. **Why was that possible?** Validation checked result shape but not result identity history.
3. **Why does identity matter?** Reapplying one observation could falsely increase the apparent evidence history.
4. **Why could that affect decisions?** Repeated application could make a single workflow appear to recur and distort factory opportunity learning.
5. **Why might it recur?** The ingestion command is intentionally local and replayable, so idempotency must be explicit rather than assumed.

Root cause: result identity was not included in the application invariant.

Immediate correction: reject a result ID already present in any primitive learning record.

Root-cause correction: treat learning result IDs as durable evidence identities and test duplicate replay explicitly.

Recurrence guard: `tests/test_primitive_learning.py::test_duplicate_learning_result_is_rejected`.

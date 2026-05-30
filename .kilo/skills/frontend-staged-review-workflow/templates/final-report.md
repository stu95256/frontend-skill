# Frontend Staged Review Final Report Template

```markdown
# Frontend Staged Review Summary

Review target: `git diff --cached`
Staged files: {STAGED_FILE_COUNT}
Selected skills: {SELECTED_SKILL_COUNT}
Reviewer passes completed: {COMPLETED_REVIEWERS}/{EXPECTED_REVIEWERS}
Workflow status: {COMPLETE_INCOMPLETE_OR_DEGRADED}
Verdict: {APPROVE_COMMENT_REQUEST_CHANGES_OR_INCOMPLETE}

## Dispatch Plan

| Skill | Trigger evidence | Reviewer IDs | Angles | Wave | Input scope |
|---|---|---|---|---:|---|
| {SKILL_NAME} | {TRIGGER_EVIDENCE} | {REVIEWER_IDS} | {ANGLES} | {WAVE} | {INPUT_SCOPE} |

## Reviewer Ledger

| Reviewer | Skill | Angle | Status | Verdict | Findings | Retry | Input scope | Notes |
|---|---|---|---|---|---:|---:|---|---|
| {REVIEWER_ID} | {SKILL_NAME} | {ANGLE} | {STATUS} | {VERDICT} | {FINDING_COUNT} | {RETRY_COUNT} | {INPUT_SCOPE} | {NOTES} |

## Consolidated Findings

### Critical
- Path: `{PATH}`
  Severity: Critical
  Line: {LINE_OR_NA}
  Found by: `{REVIEWERS}`
  Issue: {ISSUE}
  Why it matters: {WHY}
  Recommended fix: {FIX}

### High
- Path: `{PATH}`
  Severity: High
  Line: {LINE_OR_NA}
  Found by: `{REVIEWERS}`
  Issue: {ISSUE}
  Why it matters: {WHY}
  Recommended fix: {FIX}

### Medium
- Path: `{PATH}`
  Severity: Medium
  Line: {LINE_OR_NA}
  Found by: `{REVIEWERS}`
  Issue: {ISSUE}
  Why it matters: {WHY}
  Recommended fix: {FIX}

### Low
- Path: `{PATH}`
  Severity: Low
  Line: {LINE_OR_NA}
  Found by: `{REVIEWERS}`
  Issue: {ISSUE}
  Why it matters: {WHY}
  Recommended fix: {FIX}

## Aggregation Decision Log

- Merged duplicate findings: {MERGED_DUPLICATES}
- Dropped unit-test-only findings: {DROPPED_UNIT_TEST_FINDINGS}
- Severity adjustments: {SEVERITY_ADJUSTMENTS}
- Invalid/failed reviewer outputs: {INVALID_OR_FAILED_REVIEWERS}

## Out of Scope

- Unstaged files were not reviewed: {UNSTAGED_FILES_OR_NONE}
- Unit test suggestions were intentionally excluded.
- Coverage limitations, if any: {COVERAGE_LIMITATIONS_OR_NONE}

## Suggested Fix Order

1. Fix critical/high findings first.
2. Re-stage fixes with `git add`.
3. Re-run this workflow on the new staged diff.
```

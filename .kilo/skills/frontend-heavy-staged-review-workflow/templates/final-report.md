# Frontend Heavy Staged Review Final Report Template

Final user-facing reports for this workflow must be written in Chinese.

```markdown
# 前端重型已暫存變更審查結果

結論: {APPROVE_COMMENT_REQUEST_CHANGES_DEGRADED_OR_INCOMPLETE}

## 嚴重
- 路徑: `{PATH}`
  行數: {LINE_OR_NA}
  問題: {ISSUE_IN_CHINESE}
  證據: {EVIDENCE_IN_CHINESE}
  影響: {WHY_IT_MATTERS_IN_CHINESE}
  建議修正: {FIX_IN_CHINESE}

## 高
- 路徑: `{PATH}`
  行數: {LINE_OR_NA}
  問題: {ISSUE_IN_CHINESE}
  證據: {EVIDENCE_IN_CHINESE}
  影響: {WHY_IT_MATTERS_IN_CHINESE}
  建議修正: {FIX_IN_CHINESE}

## 中
- 路徑: `{PATH}`
  行數: {LINE_OR_NA}
  問題: {ISSUE_IN_CHINESE}
  證據: {EVIDENCE_IN_CHINESE}
  影響: {WHY_IT_MATTERS_IN_CHINESE}
  建議修正: {FIX_IN_CHINESE}

## 低
- 路徑: `{PATH}`
  行數: {LINE_OR_NA}
  問題: {ISSUE_IN_CHINESE}
  證據: {EVIDENCE_IN_CHINESE}
  影響: {WHY_IT_MATTERS_IN_CHINESE}
  建議修正: {FIX_IN_CHINESE}

## 建議修正順序

1. `{PATH}`: {FIX_ORDER_REASON_IN_CHINESE}
```

Omit empty severity sections. If there are no findings, output only `結論: Approve` and `已暫存 diff 中沒有發現問題。` If the workflow is incomplete/degraded, keep it concise and write the note in Chinese; do not expose reviewer/sub-agent/skill provenance unless the user asks for audit log. The entire final user-facing report must be in Chinese, except code identifiers, paths, commands, enum values, and quoted source text. Do not include dispatch plans, runtime config, reviewer ledgers, skill quorum tables, aggregation decision logs, reviewer IDs, or `Found by` in the final user-facing report.

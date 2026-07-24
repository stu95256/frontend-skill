# Frontend Branch Review Final Report Template

Final user-facing reports must be written in Chinese.

```markdown
# 前端 Branch 合併審查結果

審查範圍: `{SOURCE_REF}@{SOURCE_SHORT_SHA}` → `{TARGET_REF}@{TARGET_SHORT_SHA}`
結論: {APPROVE_COMMENT_REQUEST_CHANGES_OR_INCOMPLETE}

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

Omit empty severity sections. If there are no findings, keep the scope line and output only `結論: Approve` plus `在指定 branch 合併範圍內沒有發現問題。` Keep code identifiers, paths, commands, enum values, refs, SHAs, and quoted source text unchanged when appropriate. Do not include dispatch plans, reviewer ledgers, skill names, reviewer IDs, sub-agent provenance, retries, coverage maps, or aggregation logs.

# Frontend Branch Review Final Report

Use concise Chinese. Include scope/snapshot, verdict, confirmed findings and material limits. Operational dispatch/quorum ledgers stay internal unless requested.

```markdown
# 前端分支審查結果

範圍: `{SOURCE_REF}` (`{SOURCE_SHORT_SHA}`) → `{TARGET_REF}` (`{TARGET_SHORT_SHA}`)，merge base `{MERGE_BASE_SHORT_SHA}`

審查快照: `{SNAPSHOT_ID}`

結論: {APPROVE_COMMENT_REQUEST_CHANGES_OR_INCOMPLETE}

## 高

- 路徑: [{PATH}]({ABSOLUTE_PATH})
  行數: {LINE_OR_NA}（{NEW_OR_BASE_SIDE}）
  問題: {ISSUE_IN_CHINESE}
  條件與證據: {TRIGGER_AND_PINNED_EVIDENCE}
  影響: {DEMONSTRATED_IMPACT}
  建議修正: {ACTIONABLE_FIX}

## 驗證限制

{MATERIAL_SNAPSHOT_COVERAGE_VALIDATION_OR_VISUAL_LIMIT}

## 建議修正順序

1. {FIX_ORDER_WHEN_USEFUL}
```

Group actual findings by 嚴重／高／中／低 and omit empty sections. No findings after all gates: state `在此審查快照範圍內沒有發現具體問題。` Keep the snapshot and pinned refs/SHAs even when no findings.

Label nonblocking convention findings **低（nit，非阻擋）**, citing the actual existing helper/key or applicable repo rule and introduced divergence. Nit-only findings yield `Comment`. Report Azure description comparisons separately with matched/mismatch/partial/skipped status and relevant PR/work-item references. A skipped/unavailable optional Azure check alone does not make code review `Incomplete`; a code verdict never implies the remote description was verified.

Missing scope, snapshot, quorum, coverage or required validator means `Incomplete` (or explicitly authorized `Degraded`); state the concrete reason and retain confirmed findings. Never turn zero findings from an incomplete run into `Approve`. Report reduced redundancy or waived validation when applicable. Ordinary read-only review does not imply tests or visual checks were executed; describe only material evidence gaps.

Use clickable absolute path links for actual files and identify reviewed snapshot/base-side line locations so links to a different checkout are not mistaken for pinned evidence. Keep reviewer IDs, Skill provenance, runtime settings and aggregation logs internal unless asked.

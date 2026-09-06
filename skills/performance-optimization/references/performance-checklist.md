# Performance Checklist

- Define a reproducible workload and collect a baseline.
- Attribute cost with profiling, traces, query plans, bundle analysis, or network timing.
- Optimize the measured bottleneck rather than a proxy.
- For caches, define key identity, tenant/user isolation, freshness, invalidation, negative entries, and failure behavior.
- Do not cache correctness-sensitive balances, permissions, or checkout inventory without an explicit consistency design.
- Re-run the same workload and report before/after numbers plus measurement limits.

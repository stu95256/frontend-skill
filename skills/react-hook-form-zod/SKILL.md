---
name: react-hook-form-zod
description: Build and debug React Hook Form forms with Zod. Use for subscriptions, server values, dirty/reset behavior, controlled and numeric fields, field arrays, multi-step forms, and resolver input/output types.
license: MIT and Apache-2.0; see LICENSE and LICENSE.supabase
metadata:
  primary-source: https://github.com/supabase/supabase
  primary-source-commit: 167c633ed06da4da7b545f083b999fd7d8c669c5
  primary-source-path: .agents/skills/react-hook-form/SKILL.md
  retained-source: https://github.com/secondsky/claude-skills
  retained-source-commit: 88378361314f558fb719aec0af9fd898ab36f0b2
  adaptation: Portable RHF lifecycle with retained Zod, arrays and wizard references
---

# React Hook Form and Zod

Inspect installed react-hook-form, Zod, resolver, React and UI-library versions. Follow the lockfile and existing package manager; examples do not authorize dependency upgrades.

Use existing primitives. Supabase Studio components, lint policies, paths and sibling Skills are not dependencies here.

## Read values at the right scope

| Need | API | Constraint |
|---|---|---|
| A child renders a field value | useWatch with control and named fields | Consume the returned value in that child |
| A child renders errors or dirty state | useFormState with control | Subscribe where the state is rendered |
| The owner reads form state | Destructure formState | Read needed properties before conditionally using them |
| An event handler needs a snapshot | getValues | It does not subscribe |
| Observe changes without rendering | subscribe, when supported | Clean up; its callback must not dispatch form updates |

Prefer targeted subscriptions over a root watch of every field. Existing watch usage is not automatically invalid: change it when scope, correctness or measured rendering makes that relevant. Do not discard a watch result and render a different getValues snapshot.

Read [form lifecycle](references/form-lifecycle.md) for reset, async defaults, numeric emptiness and a complete example.

## Define schema input and output

When coercion or transforms change values, use separate input/output types:

```tsx
const form = useForm<z.input<typeof schema>, unknown, z.output<typeof schema>>({
  resolver: zodResolver(schema),
  defaultValues,
})
```

Controls hold schema input; handleSubmit receives parsed output. Preserve the installed Zod major's conventions. Validate untrusted data on the server too.

Native inputs use register. Custom controlled components use Controller or the project's wrapper. Repeating fields use useFieldArray and field.id keys.

## Server values and submission

- Give controlled fields defined defaults and one empty representation; map API null values at boundaries.
- defaultValues are cached. Use reactive values for deliberate server synchronization, or reset on the chosen record/revision change.
- For keepDirtyValues, subscribe to dirtyFields. Preserving flags alone does not preserve edited values.
- After save, reset to the persisted response mapped back to schema input. Explicitly disable keepDirtyValues for save/Cancel resets when refresh options enable it. A bare reset restores the previous baseline.
- Switch records with an explicit reset or a remount keyed by record identity; do not carry another record's edits over.
- Await async work so isSubmitting covers it. Preserve errors and pending UI, prevent duplicate writes, and give non-submit buttons type="button".
- RHF-level disabling can omit submitted data. Confirm the installed component's locking/readOnly behavior when a value must survive.

## Load detail by task

- [Lifecycle](references/form-lifecycle.md): subscriptions, defaults, background refresh and numeric input/output.
- [Schemas](references/zod-schemas-guide.md): nested data, refinement and transforms.
- [RHF API](references/rhf-api-reference.md): verify version-sensitive details against installed types.
- [Rendering performance](references/performance-optimization.md): excessive subscriptions.
- [Errors](references/error-handling.md) and [common failures](references/top-errors.md).
- [shadcn integration](references/shadcn-integration.md): only for that installed component system.
- [Dynamic fields](templates/dynamic-fields.tsx), [multi-step forms](templates/multi-step-form.tsx) and [server-backed form](templates/server-backed-form.tsx).
- [Official docs](references/links-to-official-docs.md).

This entrypoint and lifecycle guide govern lifecycle decisions. Retained examples are references, not mandates to install fixed versions or clear every successfully saved form.

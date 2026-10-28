# Form lifecycle

Adapted from [Supabase's RHF guide](https://github.com/supabase/supabase/blob/167c633ed06da4da7b545f083b999fd7d8c669c5/.agents/skills/react-hook-form/SKILL.md), excluding Studio-specific policies and components.

## Subscription boundaries

A root watch re-renders the useForm owner. A child reading through a passed form object does not acquire an isolated subscription. Prefer useWatch/useFormState in that child and consume the returned value.

formState is a Proxy: read required properties before conditional rendering. The render-free subscribe API exists in RHF 7.55+; return its unsubscribe function from the effect. Its callback observes changes and must not call reset/setValue or dispatch React updates.

## Defaults, server refresh and reset

defaultValues establish a cached baseline. Use reactive values for intentional synchronization, or reset after the relevant record/revision changes.

With keepDirtyValues, untouched fields take new server values while edited fields remain. Subscribe to dirtyFields. keepDirty alone retains flags, not edited values.

On a different record, reset without preserving another record's edits, or remount with a key equal to its ID. Preserve the application's unsaved-change policy.

After save, reset to persistedResponse mapped back to schema input. Use submitted values only when known to match persistence. A bare reset restores old defaults. Reset after subscriptions are established, not during rendering.

If useForm.resetOptions preserves dirty values for refresh, explicitly disable keepDirtyValues on a successful-save or Cancel reset. Otherwise that policy can also preserve the edits you are trying to clear. The tested template additionally clears dirty flags and replaces the saved default baseline.

## Controlled and numeric inputs

Controlled text uses an empty string rather than undefined. Map nullable API values to and from the form at explicit boundaries. Native uncontrolled register fields can follow their documented defaults.

An empty number is not zero. valueAsNumber may yield NaN; guard that path. With transforms, distinguish schema input and output. The [server-backed template](../templates/server-backed-form.tsx) edits strings and submits a finite integer.

RHF-level disabling can omit a field. Confirm actual registration and UI behavior when a locked value must still submit; do not assume a visual disabled prop preserves it.

## Verify the changed behavior

Use existing DOM integration tests or a focused hook harness for relevant cases:

- Dependent UI updates when its subscribed field changes.
- A background refresh preserves edits and updates untouched fields under the chosen policy.
- A normalized save resets the baseline; Cancel restores saved values.
- Empty/malformed numeric input is rejected or mapped intentionally without NaN.
- Switching record identity drops previous-record edits.
- Submission remains pending until saving completes.

These are useful cases, not a requirement to test every API call.

## Official API references

- [useWatch](https://react-hook-form.com/docs/usewatch)
- [useFormState](https://react-hook-form.com/docs/useformstate)
- [subscribe](https://react-hook-form.com/docs/useform/subscribe)
- [reset](https://react-hook-form.com/docs/useform/reset)
- [useForm values/defaultValues](https://react-hook-form.com/docs/useform)

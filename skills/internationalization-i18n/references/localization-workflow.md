# Localization workflow

Adapted from [the official i18next Skill](https://github.com/i18next/i18next-cli/blob/740a925c2a2b93e37c427bfd1a798708e68b7431/skills/i18next-localization/SKILL.md). Check installed CLI help before using these commands.

Inspect init, framework binding, config, catalogs and locales. Reuse an existing setup. Keep other i18n libraries rather than introducing a competing pipeline.

For new setups, install the runtime and correct framework binding via the project package manager. CLI init writes config, not runtime integration. Use documented non-interactive init options with known locales and local-file backend; do not overwrite existing config or add agent notes implicitly.

## Preview

Use the existing script or the pinned CLI:

```bash
npx --no-install i18next-cli instrument --dry-run
```

Review file scope, keys, interpolations and imports. Restrict using supported config/options. If the CLI cannot isolate requested files, transform a temporary copy and port the reviewed diff.

Preserve existing modifications; do not clean, reset, stage or commit them to make a rewrite convenient.

## Apply, extract and verify

Run within the reviewed scope:

```bash
npx --no-install i18next-cli extract
npx --no-install i18next-cli lint
npx --no-install i18next-cli status
```

Inspect init order, hook placement, duplicate keys and rich text. Server components need the stack's server translation API; adding a client directive to the whole component is not a default fix.

Built-in instrumentation handles JS/JSX/TS/TSX. Other formats need a compatible framework plugin; do not apply React wrapping to Vue/Svelte source.

Check placeholders against the primary locale. Distinguish untranslated values from intentional shared strings. Run type/build and relevant unit/DOM integration checks.

Repository files are a complete result when requested. Services require explicit selection, scoped secrets through the existing secret mechanism and review of uploaded text; never put service keys in client code.

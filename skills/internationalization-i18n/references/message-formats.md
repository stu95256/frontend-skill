# Native i18next, ICU and MF2

Based on [the official format reference](https://github.com/i18next/i18next-cli/blob/740a925c2a2b93e37c427bfd1a798708e68b7431/skills/i18next-localization/references/icu-mf2.md).

Keep native syntax unless an ICU/MF2 plugin is already configured or a format change is requested. Native interpolation and plural suffix keys do not work identically to ICU/MF2 messages.

Inspect runtime plugin, resources and CLI extract.messageFormat together. Changing resource text alone can silently break nesting, pluralization, formatters or escaping.

Verify options against installed versions. The researched source documents format-specific parseInterpolation in i18next 26.5+ and false for older setups; confirm actual plugin/type support before copying it.

Test representative locale plural categories, interpolation values, rich text and escaping. Preserve key contracts across extraction and runtime.

Consult the [official format guide](https://www.i18next.com/how-to/using-icu-or-mf2) and installed plugin docs for the chosen syntax.

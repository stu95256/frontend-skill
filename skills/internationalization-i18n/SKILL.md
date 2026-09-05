---
name: internationalization-i18n
description: Implements multi-language support using i18next, gettext, or Intl API with translation workflows and RTL support. Use when building multilingual applications, handling date/currency formatting, or supporting right-to-left languages.
license: MIT
---

# Internationalization (i18n)

Implement multi-language support with proper translation management and formatting.

## i18next Setup (React)

```javascript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    interpolation: { escapeValue: false },
    resources: {
      en: { translation: { welcome: 'Welcome, {{name}}!' } },
      es: { translation: { welcome: '¡Bienvenido, {{name}}!' } }
    }
  });

// Usage
const { t } = useTranslation();
<h1>{t('welcome', { name: 'John' })}</h1>
```

## Pluralization

```javascript
// i18next JSON format v4 (i18next v21+)
{
  "items_zero": "No items",
  "items_one": "{{count}} item",
  "items_other": "{{count}} items"
}

// Usage
t('items', { count: 0 })  // "No items"
t('items', { count: 1 })  // "1 item"
t('items', { count: 5 })  // "5 items"
```

Do not use the legacy `_plural` suffix. Keep `Intl.PluralRules` available in target runtimes or load the documented polyfill. Languages can require categories beyond `one` and `other`; follow that locale rather than copying English rules.

## Version and Project Awareness

- Inspect installed `i18next` and `react-i18next` versions before applying examples.
- Preserve `compatibilityJSON`, namespaces, key separators, fallback languages, and the configured backend/loading strategy.
- Prefer typed selectors (`enableSelector`) when the project already uses generated or augmented resource types.
- Split large catalogs by namespace and lazy-load feature/route namespaces.
- For SSR, create one i18n instance per request, preload required namespaces, and hydrate with the same language/resources.
- Sanitize untrusted rich content. React text rendering with `escapeValue: false` does not make translated HTML safe.

## Date/Number Formatting

```javascript
// Dates
new Intl.DateTimeFormat('de-DE', {
  dateStyle: 'long',
  timeStyle: 'short'
}).format(new Date());

// Numbers
new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD'
}).format(1234.56);  // "$1,234.56"

// Relative time
new Intl.RelativeTimeFormat('en', { numeric: 'auto' })
  .format(-1, 'day');  // "yesterday"
```

## RTL Support

```css
/* Use logical properties */
.container {
  margin-inline-start: 1rem;  /* margin-left in LTR, margin-right in RTL */
  padding-inline-end: 1rem;
}

/* Direction attribute */
html[dir="rtl"] .icon {
  transform: scaleX(-1);
}
```

## Additional Frameworks

See [references/frameworks.md](references/frameworks.md) for:
- React-Intl (Format.js) complete implementation
- Python gettext with Flask/Babel
- RTL language support patterns
- ICU Message Format examples

## Best Practices

- Extract all user-facing strings
- Use ICU message format for complex translations
- Test with pseudo-localization
- Support RTL from the start
- Never concatenate translated strings
- Use professional translators for production

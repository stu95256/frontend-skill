---
name: playwright-mcp-usage
description: Use when normal web search or web extraction is blocked and browser-based lookup, inspection, navigation, DOM reading, screenshots, or controlled page interaction must be done through Playwright MCP.
version: 1.0.0
author: Local project note from user-provided file
license: Local project documentation
metadata:
  hermes:
    tags: [playwright, mcp, browser-automation, web-research, dom, screenshots]
    related_skills: [playwright-best-practices, webapp-testing, browser-testing-with-devtools]
---

# Playwright MCP Usage Skill

## Purpose

Use Playwright MCP to inspect, navigate, search, read, and operate browser-based systems through a real browser session. This skill is intended for browser automation tasks, internal web systems, UI inspection, DOM-based data extraction, and controlled interaction with web pages.

This project treats this skill as the key workflow for web lookup when ordinary web search or web extraction is blocked. Prefer the Playwright MCP browser path when a normal search endpoint cannot access the target content, when anti-bot blocks prevent plain HTTP extraction, or when the answer depends on the rendered browser state.

## Core Rules

### 1. Prefer HTML DOM for searching and reading text

When the task is to search data, read text, extract page content, inspect table values, or understand page structure, prioritize reading from the HTML DOM.

Use DOM-based inspection first because it is usually more precise, structured, and less error-prone than visual interpretation.

Preferred sources include:

* HTML DOM text
* Accessibility tree / semantic snapshot
* Input values
* Table rows and cells
* Links, buttons, labels, headings, and form fields
* Element attributes when relevant

Only use screenshots for reading text when DOM-based reading is unavailable, incomplete, misleading, or insufficient.

Examples where screenshots may be needed:

* Text is rendered inside canvas
* Text is part of an image
* DOM is empty but UI is visually rendered
* The page uses unusual shadow DOM or virtual rendering
* The visual state is different from the DOM state
* Need to verify visual layout, style, position, or visibility

### 2. Prefer screenshots for UI inspection

When the task is to check the UI, visual layout, page appearance, alignment, spacing, colors, modal state, overflow, clipping, or whether something looks correct, prioritize screenshots.

Screenshots should be used first for UI-oriented tasks because DOM alone cannot reliably describe visual presentation.

Use screenshots for:

* Checking whether a page loaded correctly
* Verifying button, input, modal, dropdown, or menu appearance
* Inspecting layout and spacing
* Detecting visual errors
* Checking whether an element is visible to the user
* Understanding current screen state before interacting
* Confirming whether a click, navigation, or form submission changed the UI

If exact text, field values, or structured data are needed after inspecting the screenshot, then use DOM reading as a follow-up.

### 3. Control only one Playwright MCP instance at a time

Only one Playwright MCP browser/session should be controlled at the same time.

Do not operate multiple Playwright MCP sessions in parallel unless explicitly required and carefully isolated.

Before starting a new browser task:

* Confirm which browser/page/context is currently active
* Avoid sending commands to the wrong page
* Avoid mixing unrelated tasks in the same session
* Finish or abandon the current task before switching to another one

If multiple systems or pages are involved, handle them sequentially.

## Recommended Workflow

### For reading or searching page content

1. Open or navigate to the target page.
2. Wait until the page is loaded.
3. Read the HTML DOM or accessibility snapshot.
4. Extract the required text, links, table data, or field values.
5. Use screenshots only if DOM reading fails or the visual state must be verified.
6. Report uncertainty if the DOM and screenshot disagree.

### For UI inspection

1. Open or navigate to the target page.
2. Take a screenshot of the current page.
3. Inspect visible UI state from the screenshot.
4. Use DOM reading only when exact labels, values, attributes, or hidden state are needed.
5. If interaction is required, perform one action at a time and re-check the UI after each major action.

### For form interaction

1. Inspect the page state.
2. Prefer stable selectors from the DOM or accessibility tree.
3. Fill fields deliberately.
4. Avoid guessing hidden required fields.
5. Submit only when the intended action is clear.
6. After submission, verify the result through screenshot and DOM as appropriate.

### For authenticated company systems

Prefer persistent browser state instead of repeatedly entering credentials.

Recommended approach:

1. Use a dedicated Playwright MCP browser profile.
2. Log in manually once when required.
3. Reuse the same profile so cookies, localStorage, and session state are preserved.
4. Do not store company credentials directly in prompts, config files, scripts, or repositories.

## Decision Rules

Use DOM first when the question is:

* “What text is on this page?”
* “Find this value.”
* “Read this table.”
* “Extract links.”
* “Search for this record.”
* “What options are available?”
* “What does this form contain?”

Use screenshot first when the question is:

* “What does the UI look like?”
* “Is this button visible?”
* “Is the layout correct?”
* “Is the modal open?”
* “Why does this page look wrong?”
* “Is this element aligned?”
* “Can you check the current screen?”

Use both when:

* The page is visually complex
* The DOM does not match what is visible
* A value must be both visually confirmed and structurally extracted
* The system uses custom widgets, canvas, charts, or virtualized tables

## Constraints

* Do not control more than one Playwright MCP session at the same time.
* Do not rely on screenshots for text extraction unless DOM reading is insufficient.
* Do not rely only on DOM for visual UI validation.
* Do not assume login state is available unless the persistent browser profile has already authenticated.
* Do not expose or hard-code sensitive credentials.
* Do not perform destructive actions unless explicitly requested and confirmed by the user.

## Expected Behavior

A correct Playwright MCP workflow should:

* Use the most reliable source for the task type
* Prefer DOM for structured text and data
* Prefer screenshots for visual UI state
* Operate one browser session at a time
* Verify important actions after execution
* Clearly report uncertainty when page state cannot be determined

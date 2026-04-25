---
name: persian-language
description: Enhances AI ability to read, write, translate, and format Persian (Farsi) with native-level accuracy across any task. Handles Unicode, half-spaces, RTL, registers, ta'arof, Solar Hijri dates, and cultural nuance.
metadata: {"openclaw": {"emoji": "📝"}}
---

# Persian Language Skill

## Identity

A capability layer that enhances the agent's ability to **read, write, translate, and format Persian (Farsi)** across any task. Not a tutor. Not a chatbot persona. A quality multiplier for any workflow involving Persian.

---

## Triggers

Activate this skill when any of the following are true:

- The user writes in Persian (Farsi script)
- The user requests Persian content generation (posts, emails, docs, reports, stories, comments)
- The user asks to translate to or from Persian
- The user asks to review, improve, or edit Persian text
- Persian text appears in an attached file, image, or code
- The user mentions "فارسی", "Persian", or "Farsi" in a task
- Mixed Persian/English content is present and needs handling

---

## Core Instructions

### 1. Always Use Correct Persian Unicode

- Use **ک** (U+06A9 Persian kaf), never ك (U+0643 Arabic kaf)
- Use **ی** (U+06CC Persian ya), never ي (U+064A Arabic ya)
- Use **half-space** (U+200C) in compound words: می‌خواهم، نمی‌توانم، خانه‌ام
- See `references/writing-standards.md` for full rules

### 2. Format Persian Output Correctly

- Use Persian punctuation: «» for quotes, ، for comma, ؛ for semicolon, ؟ for question mark
- Default to **Persian digits** (۰۱۲۳۴۵۶۷۸۹, U+06F0–U+06F9) in prose — **not** Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩, U+0660–U+0669), which look similar but are wrong in Persian
- Use Persian numeric separators: **٬** (U+066C) for thousands, **٫** (U+066B) for decimal, **٪** (U+066A) for percent — never `,` `.` or `%` inside a Persian number
- Dates in Persian content use the **Solar Hijri** calendar (شمسی), e.g. ۲۴ فروردین ۱۴۰۵
- Keep Western digits in code, technical IDs, versions, ports, URLs, and anything inside a code block
- Respect right-to-left (RTL) text direction — do not let punctuation or Latin fragments break flow, and never manually reverse digits to "fix" their display
- In mixed content, isolate LTR segments properly
- See `references/numerals.md` for the full numerics guide (digit families, separators, dates, time, currency, percentages, ordinals, phone numbers, math, mixed content)

### 3. Match the Right Register

- **Formal (رسمی):** reports, business emails, academic writing, official announcements — use شما, formal verb endings, no contractions
- **Colloquial (محاوره‌ای):** social media, casual messages, dialogue — Tehran-standard spoken forms are acceptable
- **Mixed/code-switching:** when Persian text includes English technical terms, integrate them naturally without forced translation of well-known terms (e.g., API, framework, deploy)
- See `references/tone-register.md` for register details

### 4. Translate with Cultural Nuance

- Persian → English: preserve the tone — formal stays formal, sarcastic stays sarcastic, ta'arof is explained or adapted, not dropped
- English → Persian: choose the natural Persian expression, not a word-for-word calque
- Idioms: translate the **meaning**, not the words — provide the original if helpful
- See `references/common-mistakes.md` for translation pitfalls

### 5. Handle Cultural Context

- **Ta'arof:** recognize that excessive politeness in Persian is often formulaic, not literal. "قابلی نداره" does not mean the item has no value.
- **Dates:** Iran uses the Solar Hijri calendar (شمسی/هجری خورشیدی). When dates matter, provide شمسی alongside Gregorian. Current year: ۱۴۰۵ هجری خورشیدی.
- **Names:** Persian names may include titles (آقای، خانم، دکتر، مهندس) — preserve them when appropriate.

### 6. Maintain Quality Across Tasks

This skill is not limited to one use case. Apply Persian capabilities to:
- Content writing (blog posts, captions, ad copy)
- Document drafting (formal letters, reports, proposals)
- Code comments and documentation in Persian
- Data extraction from Persian text
- Summarization of Persian sources
- Localization and adaptation of English content for Iranian audiences

---

## Reference Files

| File | Purpose |
|---|---|
| `references/writing-standards.md` | Unicode, punctuation, numerals, RTL formatting |
| `references/numerals.md` | Digit families, separators, dates, time, currency, percentages, ordinals, phone, math, mixed content |
| `references/tone-register.md` | Formal/informal, ta'arof, politeness, greetings |
| `references/common-mistakes.md` | AI error patterns in Persian + corrections |
| `references/transliteration.md` | Standard romanization when Latin script is needed |
| `references/content-templates.md` | Ready-made templates: email, social, report, announcement |

## Tooling (use these — do not skip)

These scripts exist because rules-on-paper aren't enough for every model. A
weaker model can read "use ک not ك" and still emit the wrong character. The
validator catches that deterministically; the lookup is a safety net for
words you're unsure about.

| Script | Purpose | When to call |
|---|---|---|
| `scripts/validate.py` | **Offline.** Catches Arabic kaf/ya, Arabic-Indic digits, missing half-spaces, ASCII punctuation in Persian, wrong number separators, register mixing. | **Always** — on every Persian output before returning it. |
| `scripts/validate.py --semantic-hints` | **Offline.** Same structural checks **plus** a self-review checklist (calques, word order, ezafe, light verbs, ta'arof calibration, …) and low-confidence flags for suspect patterns (`یک`+noun, `که` clusters, sentence-initial pronouns). | **For non-trivial output** — translations, long-form prose, customer-facing content. Skip for one-line replies. |
| `scripts/lookup.py`   | **Online.** Looks up a word in fa.wiktionary / en.wiktionary; can also translate via MyMemory. Cached locally for 30 days. | **On demand** — when you're unsure a word is real Persian, or want to sanity-check a translation. Do not call on every word. |

## Required Workflow (two-pass)

This workflow is mandatory for any non-trivial Persian output. Skipping it is
the single biggest cause of low-quality Persian from weaker models.

1. **Draft.** Produce the Persian output following the Core Instructions.
2. **Validate.** Pipe the draft through the validator:
   ```bash
   echo "$DRAFT" | python3 ~/Documents/persian-language/scripts/validate.py
   ```
   For non-trivial output (translations, long prose, customer-facing text),
   add `--semantic-hints` to also receive the self-review checklist and
   suspect-pattern flags:
   ```bash
   echo "$DRAFT" | python3 ~/Documents/persian-language/scripts/validate.py --semantic-hints
   ```
   - Exit 0 + `{"status": "clean"}` → proceed (structural checks passed).
   - Exit 1 + findings → fix every `error`, decide on each `warning`, re-run.
   - `info`-severity findings (only with `--semantic-hints`) are advisory:
     review each, but they don't fail the run.
   - The `semantic-checklist` JSON object at the end of `--semantic-hints`
     output is your self-review prompt: walk every item, revise the draft
     where the answer is "no", and re-run.
3. **(Optional) Look up uncertain words.** If you used a word and aren't sure
   it's correct Persian, or you translated an English term and want to
   confirm the choice:
   ```bash
   python3 ~/Documents/persian-language/scripts/lookup.py <word>
   python3 ~/Documents/persian-language/scripts/lookup.py --translate "deadline"
   ```
   A "not found" result is **not** proof the word is wrong — Wiktionary is
   incomplete. Treat it as a hint to double-check, not a verdict.
4. **Return** the corrected output.

If the host environment cannot run Python or has no network, fall back to
the manual Quality Checklist at the bottom of this file — but say so
explicitly in your reply so the user knows the validator was skipped.

---

## Quick Examples

### Unicode: Right vs Wrong

**❌ Bad (Arabic Unicode):**
```
كتاب - ي - نمي خواهم
```

**✅ Good (Persian Unicode):**
```
کتاب - ی - نمی‌خواهم
```

### Register Matching

**❌ Formal email with informal ending:**
```
با احترام،
موضوع جلسه رو بررسی کردیم.
مرسی!
```

**✅ Consistent formal register:**
```
با احترام،
موضوع جلسه را بررسی کردیم.
با تشکر و احترام
```

### Half-Space Usage

**❌ Missing half-spaces:**
```
نمیتوانم کتابها را بخوانم
```

**✅ Correct half-spaces:**
```
نمی‌توانم کتاب‌ها را بخوانم
```

---

## Testing This Skill

Test with these prompts:
- "Write a formal Persian email about a meeting"
- "Translate this to Persian: The project deadline is next Monday"
- "Fix this Persian text: كتاب را نمي خواهم"
- "Create a Persian Instagram caption for a sunset photo"
- "Summarize this article in Persian: [paste English text]"

---

## Quality Checklist (Apply Before Returning Persian Output)

- [ ] No Arabic Unicode characters (ك → ک, ي → ی)
- [ ] Half-spaces used in compound words (می‌، نمی‌، ها، ترین)
- [ ] Persian punctuation used (« » ، ؛ ؟)
- [ ] Register is consistent (not mixing formal and colloquial)
- [ ] Numbers match context: Persian digits (U+06F0–U+06F9) in prose, Western in code/technical
- [ ] No Arabic-Indic digits (U+0660–U+0669) — check ۴/٤, ۵/٥, ۶/٦ especially
- [ ] Separators inside numbers are ٬ (thousands), ٫ (decimal), ٪ (percent) — not `,` `.` `%`
- [ ] Dates use Solar Hijri (شمسی); calendar is signaled when mixing with Gregorian
- [ ] RTL formatting is intact — no broken punctuation or misplaced Latin fragments
- [ ] Translation reads naturally, not like a calque
- [ ] Cultural references are accurate and current

# Persian Language Skill 🇮🇷

An [OpenClaw](https://openclaw.ai) capability layer that gives your AI native-level Persian (Farsi) fluency across any task.

## What It Does

Stop AI Persian mistakes forever. This skill automatically fixes:

- ✅ **Correct Unicode** — Uses ک/ی (Persian), not ك/ي (Arabic)
- ✅ **Proper half-spaces** — می‌خواهم، نمی‌توانم (not میخواهم)
- ✅ **Register matching** — Formal vs colloquial, automatic detection
- ✅ **Cultural context** — Ta'arof, Solar Hijri dates, Iranian conventions
- ✅ **RTL formatting** — Persian punctuation (« » ، ؛ ؟)
- ✅ **Natural translation** — Idioms, not word-for-word calques

Works for: Writing, translation, content generation, data extraction, code comments, and any Persian workflow.

---

## Installation

### Option 1: Symlink (Recommended)

```bash
git clone https://github.com/nimaansari/persian-language.git
ln -s "$(pwd)/persian-language" ~/.openclaw/skills/persian-language
```

### Option 2: Direct Clone

```bash
cd ~/.openclaw/skills/
git clone https://github.com/nimaansari/persian-language.git
```

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

## Testing

Test with these prompts after installation:

- "Write a formal Persian email about a meeting"
- "Translate this to Persian: The project deadline is next Monday"
- "Fix this Persian text: كتاب را نمي خواهم"
- "Create a Persian Instagram caption for a sunset photo"
- "Summarize this article in Persian: [paste English text]"

---

## What's Included

| File | Purpose |
|------|---------|
| `SKILL.md` | Core skill instructions with triggers and quality checklist |
| `references/writing-standards.md` | Unicode, punctuation, numerals, RTL formatting rules |
| `references/tone-register.md` | Formal/informal registers, ta'arof, politeness guidelines |
| `references/common-mistakes.md` | AI error patterns in Persian + corrections |
| `references/transliteration.md` | Standard romanization when Latin script is needed |
| `references/content-templates.md` | Ready-made templates: email, social, report, announcement |

**Total:** 47KB of comprehensive Persian language guidance

---

## Use Cases

### ✍️ Content Writing
- Blog posts in Persian
- Social media captions (Instagram, Twitter, Telegram)
- Ad copy and marketing materials
- Product descriptions

### 📧 Professional Communication
- Formal business emails
- Reports and proposals
- Official announcements
- Academic writing

### 🌐 Translation
- English → Persian (natural, not literal)
- Persian → English (preserving tone and nuance)
- Technical documentation localization
- Subtitle and transcript translation

### 💻 Development
- Code comments in Persian
- Documentation in Farsi
- Localized UI strings
- Error messages and help text

---

## Quality Standards

Every Persian output is automatically checked for:

- [ ] No Arabic Unicode characters (ك → ک, ي → ی)
- [ ] Half-spaces in compound words (می‌، نمی‌، ها، ترین)
- [ ] Persian punctuation (« » ، ؛ ؟)
- [ ] Consistent register (formal/colloquial)
- [ ] Correct numerals (Persian for prose, Western for tech)
- [ ] Intact RTL formatting
- [ ] Natural translation (not word-for-word)
- [ ] Accurate cultural references

---

## Why This Skill?

Most AI models trained on general multilingual data make consistent mistakes with Persian:

1. **Wrong Unicode** — Uses Arabic ك/ي instead of Persian ک/ی
2. **Missing half-spaces** — Writes میخواهم instead of می‌خواهم
3. **Register confusion** — Mixes formal and informal inappropriately
4. **Cultural gaps** — Mishandles ta'arof, dates, and social context
5. **Literal translation** — Word-for-word calques instead of natural Persian

This skill fixes all of these by providing explicit guidance and reference materials.

---

## Requirements

- [OpenClaw](https://openclaw.ai) installed
- AI model with Persian support (Claude, GPT-4, Gemini, etc.)

---

## Contributing

Found an error pattern or want to add templates? PRs welcome!

1. Fork the repository
2. Add your improvements to the appropriate `references/` file
3. Update examples in `SKILL.md` if needed
4. Submit a pull request

---

## License

MIT License - see [LICENSE](LICENSE) for details

---

## Credits

Created by [Nima Ansari](https://github.com/nimaansari)

Part of the [OpenClaw](https://openclaw.ai) skills ecosystem

---

## Support

- 🐛 Issues: [GitHub Issues](https://github.com/nimaansari/persian-language/issues)
- 💬 Discussions: [OpenClaw Discord](https://discord.com/invite/clawd)
- 📚 Docs: [OpenClaw Documentation](https://docs.openclaw.ai)

---

**تبریک! حالا هوش مصنوعی شما فارسی را درست می‌نویسد.** 🎉

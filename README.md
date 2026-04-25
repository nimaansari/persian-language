# Persian Language Skill 📝

> **Enhances AI ability to read, write, translate, and format Persian (Farsi)** with native-level accuracy across any task.

---

## English Version

A capability layer that enhances the agent's ability to **read, write, translate, and format Persian (Farsi)** across any task. Not a tutor. Not a chatbot persona. A quality multiplier for any workflow involving Persian.

### ✨ Features

- **Correct Persian Unicode**: ک (not ك), ی (not ي), half-spaces (U+200C)
- **Proper Formatting**: Persian digits (۰۱۲۳۴۵۶۷۸۹), punctuation («»، ؛ ؟), RTL support
- **Cultural Nuance**: Ta'arof recognition, register matching (formal/informal), Solar Hijri dates
- **Validation Tools**: Deterministic validator catches Unicode errors before output
- **Translation Lookup**: Wiktionary integration for word verification
- **Semantic13 Reference Files**: Comprehensive13 Reference Files**: Comprehensive13 Reference Files**: Comprehensive guides on writing standards, numerals, tone register, common mistakes, and content templates

### 🚀 Quick Start

#### Install the Skill
```bash
cp -r ~/Documents/persian-language ~/.npm-global/lib/node_modules/openclaw/skills/
```

#### Validate Persian Text
```bash
# Basic validation (structural checks)
echo "نمی‌توانم کتاب را بخوانم" | python3 scripts/validate.py

# Full validation with semantic hints (for translations, long-form)
echo "نمی‌توانم کتاب را بخوانم" | python3 scripts/validate.py --semantic-hints
```

#### Lookup Words
```bash
# Translate English to Persian
python3 scripts/lookup.py --translate "deadline"

# Look up Persian word definition
python3 scripts/lookup.py "کتاب"
```

### 📋 Available Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `validate.py` | Catches Unicode errors, formatting issues | **Always** - before returning any Persian output |
| `validate.py --semantic-hints` | Adds self-review checklist (calques, word order, ezafe, ta'arof) | **Non-trivial output** - translations, long-form prose |
| `lookup.py` | Wiktionary lookup + translation (30-day cache) | **On demand** - when unsure about word choice |

### 🧪 Testing

```bash
# Test with wrong Unicode (should fail)
echo "نميتوانم كتاب را بخوانم" | python3 scripts/validate.py

# Test with correct Persian (should pass)
echo "نمی‌توانم کتاب را بخوانم" | python3 scripts/validate.py

# Test translation lookup
python3 scripts/lookup.py --translate "deadline"
```

### 📚 Reference Files

| File | Purpose |
|------|---------|
| `writing-standards.md` | Unicode, punctuation, numerals, RTL formatting |
| `numerals.md` | Digit families, separators, dates, time, currency, percentages |
| `tone-register.md` | Formal/informal, ta'arof, politeness, greetings |
| `common-mistakes.md` | AI error patterns in Persian + corrections |
| `transliteration.md` | Standard romanization when Latin script needed |
| `content-templates.md` | Ready-made templates: email, social, report, announcement |

### 🛠️ Architecture

```
persian-language/
├── SKILL.md              # OpenClaw skill definition
├── README.md             # This file
├── scripts/
│   ├── validate.py       # Unicode/format13 Reference Files**: Comprehensive guides on writing standards, numerals, tone register, common mistakes, and content templates
│13 Reference Files**: Comprehensive guides on writing standards, numerals, tone register, common mistakes, and content templates
### 🚀 Quick Start

#### Install the Skill
```bash
cp -r ~/Documents/persian-language ~/.npm-global/lib/node_modules/openclaw/skills/
```

#### Validate Persian Text
```bash
# Basic validation (structural checks)
echo "نمی‌توانم کتاب را بخوانم" | python3 scripts/validate.py

# Full validation with semantic hints (for translations, long-form)
echo "نمی‌توانم کتاب را بخوانم" | python3 scripts/validate.py --semantic-hints
```

#### Lookup Words
```bash
# Translate English to Persian
python3 scripts/lookup.py --translate "deadline"

# Look up Persian word definition
python3 scripts/lookup.py "کتاب"
```

### 📋 Available Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `validate.py` | Catches Unicode errors, formatting issues | **Always** - before returning any Persian output |
| `validate.py --semantic-hints` | Adds self-review checklist (calques, word order, ezafe, ta'arof) | **Non-trivial output** - translations, long-form prose |
| `lookup.py` | Wiktionary lookup + translation (30-day cache) | **On demand** - when unsure about word choice |

### 🧪 Testing

```bash
# Test with wrong Unicode (should fail)
echo "نميتوانم كتاب را بخوانم" | python3 scripts/validate.py

# Test with correct Persian (should pass)
echo "نمی‌توانم کتاب را بخوانم" | python3 scripts/validate.py

# Test translation lookup
python3 scripts/lookup.py --translate "deadline"
```

### 📚 Reference Files

| File | Purpose |
|------|---------|
| `writing-standards.md` | Unicode, punctuation, numerals, RTL formatting |
| `numerals.md` | Digit families, separators, dates, time, currency, percentages |
| `tone-register.md` | Formal/informal, ta'arof, politeness, greetings |
| `common-mistakes.md` | AI error patterns in Persian + corrections |
| `transliteration.md` | Standard romanization when Latin script needed |
| `content-templates.md` | Ready-made templates: email, social, report, announcement |

### 🛠️ Architecture

```
persian-language/
├── SKILL.md              # OpenClaw skill definition
├── README.md             # This file
├── scripts/
│   ├── validate.py       # Unicode + semantic validator (17 KB)
│   └── lookup.py         # Wiktionary lookup + translation (7 KB)
└── references/
    ├── writing-standards.md
    ├── numerals.md
    ├── tone-register.md
    ├── common-mistakes.md
    ├── transliteration.md
    └── content-templates.md
```

### ⚠️ Important Notes

- **Not a tutor**:13 Reference Files**: Comprehensive guides on writing standards, numerals, tone register, common mistakes, and content templates
- **Quality Multiplier**: This skill multiplies quality for any workflow involving Persian
- **Two-Pass Workflow**: Draft → Validate → Fix → Return (mandatory for non-trivial output)
- **Offline Capable**: Validator works without network; lookup requires internet

### 🤝 Contributing

All Persian text should:
1. Use correct Persian Unicode (ک، ی not Arabic ك، ي)
2. Include half-spaces in compound words (می‌، نمی‌، ها)
3. Use Persian digits (۰۱۲۳۴۵۶۷۸۹) in prose, Western in code
4. Match register consistently (formal vs informal)
5. Pass validation before being added to the repo

---

## نسخه فارسی

این لایه قابلیتی که توانایی **خواندن، نوشتن، ترجمه و فرمت‌بندی فارسی** را در هر کاری افزایشقا می‌دهد. نه یک معلم. نه یک شخصرسونای چت‌بات. یک ضرب‌کننده کیفیت برای هر گردش کاری که شامل فارسی می‌شود.

### ✨ ویژگی‌ها

- **یونیکد صحیح فارسی**: ک (نه ك)، ی (نه ي)، نیم‌فاصله (U+200C)
- **فرمت‌بندی مناسبیح**: ارقام فارسی (۰۱۲۳۴۵۶۷۸۹)، نشانه‌گذاری («» ، ؛ ؟)، پشتیبانی RTL
- **ظ13 Reference Files**: Comprehensive guides on writing standards, numerals, tone register, common mistakes, and content templates
- **ابزارهای اعتبارسنجی**: اعتبارسنج قطعی خطاهای یونیکد را قبل از خروجی تشخیص می‌دهد
- **جستجوی ترجمه**: ادغام Wiktionary برای تأیید کلمات
- **۶ فایل مرجع**: راهنماهای جامع درباره استانداردهای نوشتاری، ارقام، ثبت لحن، خطباهات رایج و قالب‌های محتوا

### 🚀 شروع سریع

#### نصب مهارت
```bash
cp -r ~/Documents/persian-language ~/.npm-global/lib/node_modules/openclaw/skills/
```

#### اعتبارسنجی متن فارسی
```bash
# اعتبارسنجی پایه (بررسی‌های ساختاری)
echo "نمی‌توانم کتاب را بخوانم" | python3 scripts/validate.py

# اعتبارسنجی کامل با نک13 Reference Files**: Comprehensive guides on writing standards, numerals, tone register, common mistakes, and content templates
# ابز
‌ اعتبارسنجی: اعتبارسنج قطعی خطاهای یونیکد را قبل از خروجی تشخیص می‌دهد
# جستجوی ترجمه: ادغام Wiktionary برای تأیید کلمات
# ۶ فایل مرجع: راهنماهای جامع درباره استانداردهای نوشتاری، ارقام، ثبت لحن، اشتباهات رایج و قالب‌های محتوا

### 🚀 شروع سریع

#### نصب مهارت
```bash
cp -r ~/Documents/persian-language ~/.npm-global/lib/node_modules/openclaw/skills/
```

#### اعتبارسنجی متن فارسی
```bash
# اعتبارسنجی پایه (بررسی‌های ساختاری)
echo "نمی‌توانم کتاب را بخوانم" | python3 scripts/validate.py

# اعتبارسنجی کامل با نکات معنایی (برای ترجمه‌ها، متن‌های طول)
echo "نمی‌توانم کتاب را بخوانم" | python3 scripts/validate.py --semantic-hints
```

#### جستجوی کلمات
```bash
# ترجمه انگلیسی به فارسی
python3 scripts/lookup.py --translate "deadline"

# جستجوی تعریف کلمه فارسی
python3 scripts/lookup.py "کتاب"
```

### 📋 اسکریپت‌های موجود

| اسکریپت | کاربرد | زمان استفاده |
|---------|---------|-------------|
| `validate.py` | تشخیص خطاهای یونیکد، مسائل فرمت‌بندی | **همیشه** - قبل از برگگرداندن هر خروجی فارسی |
| `validate.py --semantic-hints` | اضافه کردن چک‌لیست بازبینی (کالک، ترتیب کلمات، اضاف، تعارف) | **خروجی غیرساده** - ترجمه‌ها، متن‌های بلندانی |
| `lookup.py` | جستجوی Wiktionary + ترجمه (کش ۳۰ روزه) | **در صورت نیاز** - وقتی در انتخاب انتخاب کلمه مطمئن نیستید |

### 🧪 آزمایشزمون

```bash
# آزمون با یونیکد اشتباه (باید شکست بخورد)
echo "نميتوانم كتاب را بخوانم" | python3 scripts/validate.py

# آزمون با فارسی صحیح (باید بگذرد)
echo "نمی‌توانم کتاب را بخوانم" | python3 scripts/validate.py

# آزمون جستجوی ترجمه
python3 scripts/lookup.py --translate "deadline"
```

### 📚 فایل‌های مرجع

| فایل | کاربرد |
|------|---------|
| `writing-standards.md` | یونیکد، نشانه‌گذاری، ارقام، فرمت‌بندی RTL |
| `numerals.md` | خانواده‌13 Reference Files**: Comprehensive guides on writing standards, numerals, tone register, common mistakes, and content templates
- **ضرب‌کننده کیفیت**: این مهارت کیفیت هر گردش کاری که شامل فارسی می‌شود را ضرب می‌کند
- **گردش کاری دو مرحله‌ای**: پیشن → اعتبارسنجی → اصلاح → بازگرداندن (اجباری برای خروجی غیرساده)
- **قابلیت کار آفلاین**: اعتبارسنج بدون شبکه کار می‌کند؛ جستجو به به اینترنت دارد

### 🤝 مشارکت

تمام متن‌های فارسی باید:
1. از یونیکد صحیح فارسی استفاده کنند (ک، ی نه Arabic ك، ي)
2. شامل‌فاصله در کلمات مرکب داشته باشند (می‌، نمی‌، ها)
3. از ارقام فارسی (۰۱۲۳۴۵۶۷۸۹) در متن، و ارقام غربی در کد استفاده کنند
4. ثبت لحن را به صورت یکدست حفظ کنند (رسمی در13 Reference Files**: Comprehensive guides on writing standards, numerals, tone register, common mistakes, and content templates
- **ضرب‌کننده کیفیت**: این مهارت کیفیت هر گردش کاری که شامل فارسی می‌شود را ضرب می‌کند
- **گردش کار دو مرحله‌ای**: نوشتن → اعتبارسنجی → اصلاح → بازگرداندن (اجباری برای خروجی غیرساده)
- **قابلیت کار آفلاین**: اعتبارسنج بدون شبکه کار می‌کند؛ جستجو نیاز به اینترنت دارد

### 🤝 مشارکت

تمام متن‌های فارسی باید:
1. از یونیکد صحیح فارسی استفاده کنند (ک، ی نه Arabic ك، ي13 Reference Files**: Comprehensive guides on writing standards, numerals, tone register, common mistakes, and content templates
- **ضرب‌کننده کیفیت**: این مهارت کیفیت هر گردش کاری که شامل فارسی می‌شود را ضرب می‌کند
- **گردش کار دو مرحله‌ای**: نوشتن → اعتبارسنجی → اصلاح → بازگرداندن (اجباری برای خروجی غیرساده)
- **قابلیت کار آفلاین**: اعتبارسنج بدون شبکه کار می‌کند؛ جستجو نیاز به اینترنت دارد

### 🤝 مشارکت

تمام متن‌های فارسی باید:
1. از یونیکد صحیح فارسی استفاده کنند (ک، ی نه Arabic ك، ي)
2. نیم‌فاصله در کلمات مرکب داشته باشند (می‌، نمی‌، ها)
3. از ارقام فارسی (۰۱۲۳۴۵۶۷۸۹) در متن، و ارقام غربی در کد استفاده کنند
4. ثبت لحن را به صورت یکدست حفظ کنند (رسمی در برابر غیررسمی)
5. قبل از اضافه شدن به مخزن، اعتبارسنجی را بگذرانند

---

## Version

**Version**: 1.0.0  
**Last Updated**: April 2026

---

## License

MIT License - Feel free to use and adapt for personal or professional use.

---

**Made with ❤️ for the Persian language community**

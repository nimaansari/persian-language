#!/usr/bin/env python3
"""
Persian text validator. Catches the high-frequency mistakes weak models make
even after reading the rules: Arabic Unicode, missing half-spaces, wrong
digit families, wrong numeric separators, ASCII punctuation in Persian prose.

Usage:
    python3 validate.py < input.txt
    python3 validate.py path/to/file.txt
    echo "نمیخواهم كتاب" | python3 validate.py
    python3 validate.py --semantic-hints < input.txt   # also self-review checklist

Exit code: 0 if clean, 1 if any findings. Findings printed as JSON lines.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass

# ---- Character sets ---------------------------------------------------------

ARABIC_KAF = "ك"   # ك  (should be ک  U+06A9)
ARABIC_YA = "ي"    # ي  (should be ی  U+06CC)
ARABIC_YA_ALT = "ى"  # ى  (alef maksura, also wrong in Persian)
ARABIC_INDIC = "٠١٢٣٤٥٦٧٨٩"   # U+0660..U+0669 — wrong in Persian
PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"  # U+06F0..U+06F9 — correct
ZWNJ = "‌"  # half-space

# Range of Persian/Arabic letters used to detect "is this Persian text".
PERSIAN_BLOCK = re.compile(r"[؀-ۿﮊپچژگ]")

# Compound-word prefixes/suffixes that should be joined with ZWNJ, not space
# or nothing. Catches the most common mistakes; not exhaustive.
PREFIXES_NEEDING_ZWNJ = ["می", "نمی", "بی"]
SUFFIXES_NEEDING_ZWNJ = ["ها", "های", "هایی", "ای", "ام", "ات", "اش",
                         "اید", "اند", "تر", "ترین"]


@dataclass
class Finding:
    rule: str
    severity: str   # "error" | "warning"
    message: str
    sample: str     # offending substring (truncated)
    offset: int     # character index into the input


def _truncate(s: str, n: int = 40) -> str:
    return s if len(s) <= n else s[: n - 1] + "…"


# ---- Rules ------------------------------------------------------------------

def check_arabic_letters(text: str) -> list[Finding]:
    out = []
    for ch, correct, name in [
        (ARABIC_KAF, "ک", "Arabic kaf"),
        (ARABIC_YA, "ی", "Arabic ya"),
        (ARABIC_YA_ALT, "ی", "Arabic alef maksura"),
    ]:
        for m in re.finditer(re.escape(ch), text):
            out.append(Finding(
                rule="arabic-letter",
                severity="error",
                message=f"{name} ({ch!r}) found — replace with Persian {correct!r}",
                sample=_truncate(text[max(0, m.start() - 10): m.end() + 10]),
                offset=m.start(),
            ))
    return out


def check_arabic_indic_digits(text: str) -> list[Finding]:
    out = []
    for m in re.finditer(f"[{ARABIC_INDIC}]+", text):
        out.append(Finding(
            rule="arabic-indic-digits",
            severity="error",
            message=("Arabic-Indic digits (U+0660..U+0669) found — "
                     "use Persian digits ۰۱۲۳۴۵۶۷۸۹ in Persian prose"),
            sample=_truncate(m.group()),
            offset=m.start(),
        ))
    return out


def check_mixed_digit_families(text: str) -> list[Finding]:
    """A single number should not mix Persian and Western digits."""
    out = []
    pattern = re.compile(r"[\d۰-۹]{2,}")
    for m in pattern.finditer(text):
        s = m.group()
        has_western = any(c.isascii() and c.isdigit() for c in s)
        has_persian = any(c in PERSIAN_DIGITS for c in s)
        if has_western and has_persian:
            out.append(Finding(
                rule="mixed-digits",
                severity="error",
                message="Number mixes Persian and Western digits — pick one family",
                sample=s,
                offset=m.start(),
            ))
    return out


def check_missing_half_space(text: str) -> list[Finding]:
    """Detect common compound words written without a half-space (ZWNJ).

    We only flag patterns that are almost always wrong, to keep false
    positives low. E.g. 'نمیخواهم' (no separator) is wrong; the correct
    form is 'نمی‌خواهم'.
    """
    out = []

    # Prefix attached directly to a verb stem (no space, no ZWNJ).
    # e.g. 'میروم' should be 'می‌روم'.
    for prefix in PREFIXES_NEEDING_ZWNJ:
        # \b doesn't work cleanly with Persian; use lookbehind for non-letter.
        pat = re.compile(
            rf"(?<![؀-ۿ]){re.escape(prefix)}([؀-ۿ]{{2,}})"
        )
        for m in pat.finditer(text):
            # Already correct if next char is ZWNJ.
            if m.group(1).startswith(ZWNJ):
                continue
            out.append(Finding(
                rule="missing-half-space",
                severity="error",
                message=f"Prefix '{prefix}' should be joined to the verb with "
                        f"a half-space (U+200C), e.g. {prefix}‌…",
                sample=_truncate(m.group()),
                offset=m.start(),
            ))

    # Suffix attached with a regular space — e.g. 'کتاب ها' → 'کتاب‌ها'.
    for suffix in SUFFIXES_NEEDING_ZWNJ:
        pat = re.compile(
            rf"([؀-ۿ]{{2,}}) {re.escape(suffix)}(?![؀-ۿ])"
        )
        for m in pat.finditer(text):
            out.append(Finding(
                rule="missing-half-space",
                severity="warning",
                message=f"Suffix '{suffix}' likely should be joined with "
                        f"a half-space, not a regular space",
                sample=_truncate(m.group()),
                offset=m.start(),
            ))
    return out


def check_ascii_punctuation(text: str) -> list[Finding]:
    """ASCII punctuation immediately adjacent to Persian letters is wrong
    in Persian prose: , ; ? should be ، ؛ ؟ and " " should be « »."""
    out = []
    rules = [
        (",", "،", "comma"),
        (";", "؛", "semicolon"),
        ("?", "؟", "question mark"),
    ]
    # Persian *letters* only (excludes digits U+06F0..U+06F9 to avoid
    # overlap with the number-separator rule).
    persian_letter = r"[ا-يٱ-ۀپچژگکی]"
    for ascii_ch, persian_ch, name in rules:
        pat = re.compile(rf"{persian_letter}{re.escape(ascii_ch)}")
        for m in pat.finditer(text):
            out.append(Finding(
                rule="ascii-punctuation",
                severity="error",
                message=f"ASCII {name} {ascii_ch!r} after Persian text — "
                        f"use Persian {name} {persian_ch!r}",
                sample=_truncate(m.group()),
                offset=m.start(),
            ))
    # Straight double-quotes around Persian: prefer « »
    for m in re.finditer(r'"[^"]*[؀-ۿ][^"]*"', text):
        out.append(Finding(
            rule="ascii-punctuation",
            severity="warning",
            message="Straight quotes around Persian text — use « » (guillemets)",
            sample=_truncate(m.group()),
            offset=m.start(),
        ))
    return out


def check_number_separators(text: str) -> list[Finding]:
    """Inside a Persian-digit number, the separators should be ٬ ٫ ٪,
    not , . %."""
    out = []
    # Persian digit run with ASCII , or . in the middle, e.g. '۱,۰۰۰'.
    pat = re.compile(r"[۰-۹]+[,.][۰-۹]+")
    for m in pat.finditer(text):
        out.append(Finding(
            rule="wrong-number-separator",
            severity="error",
            message="ASCII ',' or '.' inside a Persian-digit number — "
                    "use ٬ (thousands) or ٫ (decimal)",
            sample=m.group(),
            offset=m.start(),
        ))
    # Persian digits followed by ASCII '%'
    for m in re.finditer(r"[۰-۹]+\s*%", text):
        out.append(Finding(
            rule="wrong-number-separator",
            severity="warning",
            message="ASCII '%' after Persian digits — use ٪ (U+066A)",
            sample=m.group(),
            offset=m.start(),
        ))
    return out


def check_register_mixing(text: str) -> list[Finding]:
    """Heuristic: if formal markers and colloquial markers both appear in
    the same paragraph, flag for human review. Not authoritative."""
    out = []
    formal = re.compile(r"\b(می‌باشد|می‌گردد|می‌نماید|بدین‌وسیله|احتراماً)\b")
    colloquial = re.compile(r"(می‌خوام|نمی‌خوام|بریم|چیه|چطوره|مرسی|دمت گرم)")
    for para in re.split(r"\n\s*\n", text):
        if formal.search(para) and colloquial.search(para):
            out.append(Finding(
                rule="register-mixing",
                severity="warning",
                message="Paragraph mixes formal and colloquial markers — "
                        "pick one register",
                sample=_truncate(para, 60),
                offset=text.find(para),
            ))
    return out


# ---- Semantic hints (self-review prompts) -----------------------------------
#
# These are NOT deterministic checks. The validator can't know whether your
# Persian is *natural*, only whether it's *structurally* correct. The hints
# below are a checklist for the model to apply to its own output, plus a few
# low-confidence heuristic flags that surface suspect patterns for review.
#
# Use when generating non-trivial Persian (translations, long-form prose,
# customer-facing content) — not for one-line replies.

SEMANTIC_CHECKLIST = [
    {
        "id": "word-order",
        "ask": "Does each clause end with its main verb? Persian is SOV.",
        "fix": "Move the verb to the end. ❌ 'من می‌روم به فروشگاه' → ✅ 'من به فروشگاه می‌روم'.",
    },
    {
        "id": "drop-subject-pronoun",
        "ask": "Did you drop subject pronouns when verb endings already encode person/number?",
        "fix": "'می‌روم' already means 'I go'. Don't restate 'من' unless emphasizing or contrasting.",
    },
    {
        "id": "compound-verb-choice",
        "ask": "Did you pick the natural Persian light verb (کردن، شدن، زدن، دادن، گرفتن، خوردن، انداختن)?",
        "fix": "Don't calque English verbs. ❌ 'تصمیم ساختن' → ✅ 'تصمیم گرفتن'. ❌ 'عکس کردن' → ✅ 'عکس گرفتن' / 'عکس انداختن'.",
    },
    {
        "id": "no-extra-yek",
        "ask": "Did you avoid inserting 'یک' wherever English used 'a/an'?",
        "fix": "Persian often omits indefinite marking. ❌ 'من یک کتاب خواندم' (calque of 'I read a book') → ✅ 'کتابی خواندم' or 'کتاب خواندم'.",
    },
    {
        "id": "idiom-by-meaning",
        "ask": "Did you translate idioms by *meaning*, not word-for-word?",
        "fix": "❌ 'منتظر هستم برای شنیدن از شما' (calque of 'looking forward to hearing from you') → ✅ 'مشتاق شنیدن خبرتان هستم' / 'منتظر پاسختان هستم'.",
    },
    {
        "id": "ezafe",
        "ask": "Did noun-modifier pairs use the ezafe (ـِ) construction?",
        "fix": "Ezafe links a noun to its modifier: 'کتابِ من' (my book), 'خانهٔ بزرگ' (big house). It's pronounced even when unwritten — make sure the structure is there, not a juxtaposition that reads wrong.",
    },
    {
        "id": "tu-vs-shoma",
        "ask": "Does the 'you' pronoun match the register? (تو informal, شما formal/plural)",
        "fix": "Pick one and stay consistent. Mixing تو and شما to the same person sounds jarring or sycophantic.",
    },
    {
        "id": "tarof-calibration",
        "ask": "Is ta'arof calibrated to the register — present in formal contexts, absent in casual ones?",
        "fix": "Formal: 'با احترام', 'بدین وسیله', 'تشکر می‌کنم'. Casual: drop the ta'arof formulas. Don't sprinkle ta'arof into a Telegram message or omit it from a business email.",
    },
    {
        "id": "natural-time",
        "ask": "Are time/date expressions in Persian word order, with Solar Hijri (شمسی) when the audience is Iranian?",
        "fix": "❌ 'دوشنبه صبح' → ✅ 'صبح روز دوشنبه'. ❌ 'آیندهٔ هفته' → ✅ 'هفتهٔ آینده'. Use ۱۴۰۵/فروردین/etc., not 2026/April when the reader is Iranian.",
    },
    {
        "id": "no-pronoun-overuse",
        "ask": "After introducing a subject, did you let it drop instead of restating it every sentence (English habit)?",
        "fix": "Persian narration carries the subject through verb conjugation. Repeating 'او' / 'من' / 'شما' every sentence reads like a textbook.",
    },
    {
        "id": "ke-clusters",
        "ask": "Did you avoid stacking multiple 'که' relative clauses in one sentence?",
        "fix": "English nests relative clauses freely; Persian prefers to break them apart. Restructure long 'که ... که ... که' chains into shorter sentences.",
    },
    {
        "id": "natural-greeting-closing",
        "ask": "Are the opening/closing phrases idiomatic for the channel and register?",
        "fix": "Email formal: 'با سلام و احترام' / 'با تشکر و احترام'. Chat casual: 'سلام' / 'مرسی'. Don't use 'عزیز' with strangers in formal writing — it reads as overfamiliar.",
    },
]


def detect_review_patterns(text: str) -> list[Finding]:
    """Low-confidence heuristic flags. These point the model at suspect
    patterns to review — they are NOT errors, and may be false positives.
    Severity is 'info' so they don't get confused with structural failures."""
    out = []

    # 'یک' immediately followed by a noun — often a calque of English 'a/an'.
    for m in re.finditer(r"یک\s+[ا-یئ]{2,}", text):
        out.append(Finding(
            rule="review-yek",
            severity="info",
            message=("'یک' + noun — verify this is a real indefinite "
                     "(meaning 'one'), not a calque of English 'a/an'"),
            sample=_truncate(m.group()),
            offset=m.start(),
        ))

    # Multiple 'که' close together — possibly nested calque.
    for m in re.finditer(r"که\s+\S+\s+\S+\s+که", text):
        out.append(Finding(
            rule="review-ke-cluster",
            severity="info",
            message=("Multiple 'که' close together — check for over-nested "
                     "relative clauses; consider splitting into two sentences"),
            sample=_truncate(m.group()),
            offset=m.start(),
        ))

    # Sentence-initial subject pronoun — often droppable.
    pat = re.compile(r"(?:^|[.!؟\n])\s*(من|تو|او|ما|شما|آن‌ها|آنها)\s+")
    for m in pat.finditer(text):
        out.append(Finding(
            rule="review-subject-pronoun",
            severity="info",
            message=("Explicit subject pronoun at sentence start — "
                     "Persian usually drops these unless emphasizing"),
            sample=_truncate(m.group().strip()),
            offset=m.start(),
        ))

    # 'بودن' / 'هستن' chained as English-style copula where Persian would
    # use a more specific verb. Hard to detect cleanly; skip for now.

    return out


# ---- Driver -----------------------------------------------------------------

ALL_CHECKS = [
    check_arabic_letters,
    check_arabic_indic_digits,
    check_mixed_digit_families,
    check_missing_half_space,
    check_ascii_punctuation,
    check_number_separators,
    check_register_mixing,
]


def validate(text: str) -> list[Finding]:
    if not PERSIAN_BLOCK.search(text):
        return []
    findings: list[Finding] = []
    for check in ALL_CHECKS:
        findings.extend(check(text))
    findings.sort(key=lambda f: f.offset)
    return findings


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", nargs="?",
                   help="File to validate (default: stdin)")
    p.add_argument("--semantic-hints", action="store_true",
                   help=("Also emit a self-review checklist for semantic "
                         "issues (calques, word order, ezafe, etc.) and "
                         "low-confidence heuristic flags. Use this for "
                         "non-trivial Persian generation."))
    args = p.parse_args()

    if args.file and args.file not in ("-", "--"):
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    structural = validate(text)
    review: list[Finding] = []
    if args.semantic_hints and PERSIAN_BLOCK.search(text):
        review = detect_review_patterns(text)

    all_findings = sorted(structural + review, key=lambda f: f.offset)
    for f in all_findings:
        print(json.dumps(asdict(f), ensure_ascii=False))

    if args.semantic_hints:
        print(json.dumps({
            "type": "semantic-checklist",
            "instructions": ("Apply each item to your draft. For every "
                             "'no', revise and re-run the validator."),
            "items": SEMANTIC_CHECKLIST,
        }, ensure_ascii=False))

    if not structural:
        if not args.semantic_hints:
            print(json.dumps({"status": "clean"}, ensure_ascii=False))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())

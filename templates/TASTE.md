---
version: alpha
scope: project
name: "[Project Name]"
# The matching agency-wide ledger lives at the user/global level:
global_ledger: "~/.claude/TASTE.md"
# Confidence bands that skills act on:
apply_threshold: 0.8      # >= this -> apply the preference without asking
suggest_threshold: 0.4    # >= this and < apply -> offer it, let the user confirm
                          # < suggest_threshold -> watch only, never act
---

# brain/TASTE.md — [Project Name]

> A learned-preferences ledger. It accumulates this client's design taste across
> sessions so agents stop re-earning the same corrections. Every time the user
> rates a render, rejects a choice, or edits your output, the signal lands here
> as a scored entry. Next session, high-confidence preferences are applied
> **before** the user has to ask again.
>
> This is the taste the site itself teaches you — not craft rules. Universal
> craft lives in `FUNDAMENTALS.md`; brand tokens live in `DESIGN.md`; this file
> is the running memory of what *this owner, on this project* keeps steering
> toward.

---

## Two scopes — don't mix them

Taste splits by how far it travels. Put each signal in the right ledger.

| Scope | Lives in | Holds | Example |
|-------|----------|-------|---------|
| **Project** | `brain/TASTE.md` (this file) | Preferences tied to THIS client's identity and site — things that would be wrong to carry to another project. | "The peacock mascot is beloved — never remove or redraw it." |
| **Global** | `~/.claude/TASTE.md` (user level) | The agency owner's accumulating eye across ALL projects — durable habits that show up on every brand. | "Consistently asks for more whitespace than the first draft ships." |

Rule of thumb: if the preference would still be true on a totally different
client's site, it belongs in the **global** ledger, not here. If it only makes
sense because of who this client is, it stays **project**-scoped.

Both ledgers use the identical entry format below. Skills read both and apply the
higher-confidence signal; on a genuine conflict, **project taste wins** (the
client's own site overrides the owner's general habit).

---

## Entry format

Each entry is one preference. Four parts:

- **category** — the axis it lives on (see list below).
- **statement** — one line, imperative or declarative, unambiguous.
- **confidence** — `0.0`–`1.0`. How sure we are the owner actually holds this.
- **evidence** — every session signal that produced or reinforced it, newest last:
  `YYYY-MM-DD · <the rating / accept / reject / edit that fired it>`.

```
### [category] — <one-line statement>
confidence: 0.0–1.0
evidence:
  - YYYY-MM-DD · <signal>
  - YYYY-MM-DD · <signal>
```

### Example entries

```
### brand-identity — The peacock mascot is sacred: never remove it, shrink it below 48px, or redraw it.
confidence: 0.95
evidence:
  - 2026-06-30 · rejected the mascot-less header variant outright ("the bird stays")
  - 2026-07-04 · edited the footer mascot back up from 32px to 56px
  - 2026-07-09 · rated the mascot-forward hero 5/5, the wordmark-only one 2/5
```

```
### copy-voice — Rejects hype adjectives (world-class, seamless, state-of-the-art); wants understated Aman/Oberoi restraint.
confidence: 0.85
evidence:
  - 2026-07-02 · struck "world-class" and "elevates" from the banquet hero
  - 2026-07-08 · flagged "seamless" in the event-type copy as off-voice
```

```
### color — Leans oxblood over brass for primary CTAs on this site.
confidence: 0.6
evidence:
  - 2026-07-07 · picked the oxblood button in the A/B pair, but "not sure yet"
```

---

## Confidence — what the number means

| Band | Meaning | How skills treat it |
|------|---------|---------------------|
| `0.8`–`1.0` | Repeated, consistent signal. Load-bearing. | **Apply proactively.** Ship it this way without asking. |
| `0.4`–`0.7` | One clear signal, or mixed. A lean, not a law. | **Offer it.** Propose the preference, let the user confirm. |
| `0.0`–`0.3` | Weak, stale, or recently contradicted. | **Watch only.** Note it; don't act on it yet. |

Never invent an entry. Every entry — and every confidence bump — must trace to a
real session signal in its evidence trail. No signal, no entry.

---

## Merge on repetition, revise on contradiction

The ledger is append-and-adjust, never rewrite-from-scratch.

- **Repeated** — the same preference recurs in a new session: add an evidence line
  and **raise confidence** (roughly +0.1 to +0.2, capped at `1.0`; the more
  independent the signals, the bigger the bump). Do **not** create a second entry
  for the same preference — find the existing one and reinforce it.
- **Contradicted** — a new signal cuts against a standing entry: **lower its
  confidence and re-date it** with the contradicting evidence line. A single
  contradiction dents; it doesn't delete.
- **Flipped** — the owner clearly reverses course: rewrite the statement, reset
  confidence to reflect only the new signals, and keep one dated line noting the
  reversal so the history stays honest.
- **Decays** — an entry with no new evidence for many sessions is not wrong, just
  cold. Leave it; let the apply-threshold gate whether it still acts.

Two entries that keep contradicting each other usually means the statement is too
broad — split it by context (e.g. "CTAs" vs "inline links") instead of fighting.

---

## Categories

Keep the axis list small and stable so entries stay greppable:

`brand-identity` · `color` · `type` · `whitespace` · `layout` · `motion` ·
`imagery` · `copy-voice` · `components` · `density`

Add a category only when a real preference doesn't fit any of these — and add it
here first.

---

## How it's fed

- **`save-session`** is the writer. At session close it reads this session's
  ratings and every accept / reject / edit signal, then appends new entries or
  reinforces existing ones per the merge rules above. It is the only skill that
  writes confidence values.
- Signals it converts:
  - a **rating** on a render → confidence weighted by the score and the gap to
    alternatives.
  - a **reject** ("no, not that") → an entry (or contradiction) on what was refused.
  - an **edit** to your output → the strongest signal there is: the owner showed,
    didn't tell. Capture what changed and why.

## How it's read

- **`build-page`** loads this file before composing. Entries at or above
  `apply_threshold` shape the first draft — the whitespace, the accent choice, the
  voice — so the owner sees their taste already applied instead of correcting it
  for the fifth time. Mid-band entries become the questions it asks up front.
- **`design-check`** reads it as a gate. A change that violates a high-confidence
  entry (shrinking the sacred mascot, slipping a hype adjective past the voice
  rule) is flagged the same as a token violation — not a preference, a standing
  decision.
- Both skills read the **global ledger** too, and honor project-wins-on-conflict.

---

## Editing rules

1. **Never hand-write a confidence number.** Confidence is earned from evidence;
   `save-session` sets it. Humans may correct a *statement* or delete a wrong
   entry, but not fabricate a score.
2. **One preference, one entry.** If you're about to add a near-duplicate, you
   meant to reinforce the existing one.
3. **Evidence is append-only.** Don't rewrite history to make a preference look
   more settled than the sessions actually showed.
4. **Scope discipline.** Before adding here, ask "would this be true on another
   client?" If yes, it goes in the global ledger instead.

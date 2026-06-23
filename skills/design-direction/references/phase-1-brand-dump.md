# Phase 1 — Brand dump

One free-text prompt to the user. No structured form, no multiple-choice, no axis jargon. The dump is the input to every later phase.

---

## Read existing canon first (do not ask for what's already on disk)

Before prompting the user, check:

1. `brain/BRAND.md` — if it exists and has populated sections (anything beyond `[VERIFY]` placeholders), read it. Map its content onto the dump.
2. `brain/STATUS.md` — current sprint, audience hints, surface mix.
3. Root `CLAUDE.md` — `## What this is` section.
4. Root `README.md` — opening paragraph.
5. `brain/BRIEF.md` — any locked decisions about audience, monetisation, surfaces.

If those files cover what the dump prompt asks for, **skip the prompt** and synthesise the dump silently. Tell the user: *"Pulling the brand context from `brain/BRAND.md` + `brain/STATUS.md` — you already wrote most of this. I'll add follow-up only if I find gaps."* Then proceed to Phase 2.

If only some fields are answered by existing canon, ask only for the missing pieces.

---

## The prompt (when needed)

> Tell me about this product in your own words. As much or as little as you have:
>
> - **What is it** — one paragraph in plain English.
> - **Who is it for** — describe the actual person, not a market segment.
> - **What problem does it solve** — what pain are they in before they find this.
> - **Where does it live** — web, app, both. Marketing site? Dashboard? Email? Docs? Mobile? Anything else?
> - **How does it make money** — free, subscription, per-event, agency, ads, donations.
> - **Anything it should NOT look like** — competitors you don't want to resemble, vibes you find amateur, aesthetics you've explicitly rejected.
>
> Don't worry about being structured — paste a brain-dump, paste your investor pitch, paste a half-finished marketing page. I'll work with what you give me.

---

## What if the user gives a short answer

If the response is under ~150 words, ask one (and only one) follow-up:

> A bit more on the audience — describe one specific person who'd use this, including roughly how they feel about the problem before they find your product. That emotional state is the single biggest signal for what the design should feel like.

After that follow-up, proceed regardless of length. Do not chase a third round.

---

## What goes forward to Phase 2

Everything the user wrote, verbatim, plus anything pulled from existing canon. Do not summarise yet — Phase 2 needs the raw material.

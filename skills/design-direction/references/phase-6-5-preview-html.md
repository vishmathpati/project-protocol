# Phase 6.5 — Preview HTML generation

The token diff alone is not a fair approval surface. A hex code is not a colour;
a font name is not type. Before Phase 6.5 asks the user to apply the proposed
tokens, it writes a self-contained HTML preview page and surfaces a `file://`
link. The user opens it, sees the actual brand rendered, and comes back with
"approve" / "iterate" / "reject".

This file defines:

1. What the preview must contain (sections, components, density)
2. The HTML template the skill emits
3. How Phase 6.5 substitutes the token values into the template
4. Font-loading rules (Google Fonts only — substitute with notice for everything else)
5. Where to write the file and what to surface to the user
6. When the preview is skipped

---

## When this runs

After step 4 of Phase 6.5 ("Generate new token values") and **before** step 5
("Preview the proposed token diff"). The diff text + the preview HTML are
shown together. The user opens the preview, then accepts or iterates.

Preview generation is **not skippable** unless the alignment result is
`match` (no token changes proposed) — in that case there is nothing to preview.

---

## What the preview must contain

One single `<html>` page, no build step, no JS framework, ~400 lines including
inline CSS. Loads any required Google Fonts via `<link>`. Renders the
following sections in order:

### 1. Top bar
- Project name (left)
- Direction name + one-line character description (centre)
- Light / Dark toggle button (right)

### 2. Colours — surface roles
A horizontal row of 4 large swatches (paper / ash / ink / hairline). Each
swatch shows:
- The colour as a 140×140 px block
- The hex value below
- The role name (e.g., "paper — primary canvas, 70%+ of pixels")

### 3. Colours — accent roles
A horizontal row of accent swatches (primary, primary_hover, optional
secondary). Same shape as surface swatches.

### 4. Colours — status
Smaller row (60×60 swatches) for success / warning / error.

### 5. Contrast pairs panel
A table of every load-bearing token pair with its computed WCAG ratio and a
PASS / FAIL badge. Pairs to check:

| Pair | Minimum |
|---|---|
| ink on paper | 4.5:1 (body) |
| ink on ash | 4.5:1 (body on raised surface) |
| paper on accent.primary | 4.5:1 (text on CTA) |
| accent.primary on paper | 3:1 (link colour) |
| hairline on paper | 3:1 (UI border visibility) |
| status.error on paper | 4.5:1 |

If any FAIL, show the row in red with "below WCAG AA — Phase 6.5 will refuse
to write" warning above the panel.

### 6. Typography — display ramp
Four lines of display font at:
- 72 px / line-height 1.0 / tracking −0.03em — "Display headline at 72"
- 56 px / line-height 1.05 / tracking −0.02em — "Section head at 56"
- 40 px / line-height 1.1 / tracking −0.02em — "Section head at 40"
- 28 px / line-height 1.2 / tracking −0.01em — "Subsection at 28"

### 7. Typography — body ramp
Three paragraphs of body font (a 3–4 line lorem stand-in — use real-looking
copy, not "lorem ipsum"). Sizes 18 / 16 / 14 px, line-heights 1.6 / 1.6 / 1.5.

### 8. Typography — mono sample
A 6–8 line code block in mono font at 14 px:

```
const tokens = {
  paper: "{{paper}}",
  ink:   "{{ink}}",
  accent: "{{accent_primary}}",
}

// derived at runtime
const hover = oklch(from accent calc(l - 0.08) c h);
```

### 9. Typography — letter-spacing test
One line of small UI text: `LABEL · METADATA · 0.06EM TRACKING` at 12 px in
body font, weight 500, with 0.06em letter-spacing applied.

### 10. Spacing scale
Eight horizontal bars in `accent.primary` colour, at widths 4 / 8 / 12 / 16 /
24 / 32 / 48 / 64 px. Each bar labelled with its px value.

### 11. Radius scale
Three square boxes (60×60), filled with `accent.primary` at 15% opacity,
showing `radius.sm` / `radius.md` / `radius.lg`. Each labelled with its px
value.

### 12. Components — buttons
Five buttons in a row:
- **Default** — `accent.primary` background, `paper` text — label: "Continue"
- **Secondary** — transparent, `ink` text, `hairline` border — label: "Cancel"
- **Outline** — transparent, `accent.primary` text, `accent.primary` border — label: "Learn more"
- **Ghost** — transparent, `ink` text, no border — label: "Skip"
- **Destructive** — `status.error` background, `paper` text — label: "Delete"

### 13. Components — form
Four stacked form fields in a 320 px column:
- Text input with label "Full name" + placeholder "Sofia Chen"
- Textarea with label "Notes" + placeholder "Anything we should know?"
- Select with label "Region" + options ["Bangalore", "Mumbai", "Delhi"]
- Checkbox with label "Subscribe to updates"

### 14. Components — card
One card (340 px wide), with:
- Title in body font, 20 px / weight 600
- Two lines of body copy at 16 px
- A `Default` button in the card footer

### 15. Components — dialog mockup
A dimmed-paper overlay containing a card-shaped dialog with title, two body
paragraphs, and a footer row of `Cancel` + `Confirm` buttons. Just visual —
no interactivity.

### 16. Components — table
A 5-row × 4-column table with realistic data (names, dates, numbers,
statuses). Header row uses body font weight 600. Numeric column uses mono
font + tabular figures. Last column uses status badges.

### 17. Components — tabs
Three tabs in a row: "Overview", "Details", "History". Active tab is
"Overview" — styled with `ink` text + 2 px `accent.primary` underline. Below
the tabs, a short paragraph of body copy to anchor the active state.

### 18. Components — badges
Six small badges in a row: `Default`, `Outline`, `Success`, `Warning`,
`Error`, `Info`.

### 19. Components — toast
One toast pinned bottom-right at 320 px wide: title + one line of body copy
+ a small × close icon. Uses `ash` background, `ink` text, `hairline` border,
`radius.md`, `shadow.md`.

### 20. Real-content example — hero
A single section ~600 px tall containing:
- An eyebrow label (mono, 12 px, accent.primary, 0.08em tracking) — "INTRODUCING"
- A display headline at 72 px, two lines — use a realistic brand-fitting headline (not "Welcome to our product"). Phase 6.5 picks a headline that matches the brand archetype: Sage → "Knowledge, organised." / Magician → "See what was hidden." / Caregiver → "Looking out for you." / etc.
- A body paragraph at 18 px, 2–3 lines
- A `Default` button + a `Ghost` button side-by-side

This is the section where pairing fights become visible — display + body
together, accent in two roles, paper + ink contrast carrying real text.

### 21. Footer
Plain prose, in body font at 16 px, 60% opacity:

> This is direction **{{direction_name}}** rendered with the proposed tokens.
> If this looks right, return to chat and say **approve** (or **apply all**).
> If something feels off, tell me what to change — "the accent feels too
> orange", "display feels too heavy", "dark mode is muddy" — and I'll
> regenerate. Display font: **{{display_font}}** ({{display_source}}). Body:
> **{{body_font}}** ({{body_source}}). Mono: **{{mono_font}}** ({{mono_source}}).

---

## The HTML template

This is the literal file Phase 6.5 writes (with `{{placeholders}}` substituted).
Keep it self-contained — no external CSS, no JS framework, no build step.

```html
<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{{project_name}} — design preview ({{direction_name}})</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
{{google_fonts_link}}
<style>
  :root {
    --paper: {{light_paper}};
    --ash: {{light_ash}};
    --ink: {{light_ink}};
    --hairline: {{light_hairline}};
    --accent-primary: {{accent_primary}};
    --accent-primary-hover: {{accent_primary_hover}};
    --accent-secondary: {{accent_secondary_or_transparent}};
    --status-success: {{status_success}};
    --status-warning: {{status_warning}};
    --status-error: {{status_error}};
    --radius-sm: {{radius_sm}};
    --radius-md: {{radius_md}};
    --radius-lg: {{radius_lg}};
    --shadow-sm: {{shadow_sm}};
    --shadow-md: {{shadow_md}};
    --font-display: {{display_stack}};
    --font-body: {{body_stack}};
    --font-mono: {{mono_stack}};
  }
  html[data-theme="dark"] {
    --paper: {{dark_paper}};
    --ash: {{dark_ash}};
    --ink: {{dark_ink}};
    --hairline: {{dark_hairline}};
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--paper);
    color: var(--ink);
    font-family: var(--font-body);
    font-size: 16px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    transition: background 200ms ease, color 200ms ease;
  }
  main { max-width: 1080px; margin: 0 auto; padding: 32px 24px 96px; }
  section { margin-top: 64px; }
  section h2 {
    font-family: var(--font-body);
    font-weight: 600;
    font-size: 14px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ink);
    opacity: 0.5;
    margin-bottom: 16px;
  }
  /* Top bar */
  .topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--hairline);
  }
  .topbar .name { font-family: var(--font-body); font-weight: 600; }
  .topbar .direction { font-family: var(--font-body); opacity: 0.7; }
  .topbar .toggle {
    background: transparent;
    border: 1px solid var(--hairline);
    color: var(--ink);
    padding: 8px 14px;
    border-radius: var(--radius-sm);
    font-family: var(--font-body);
    font-size: 14px;
    cursor: pointer;
  }
  /* Swatches */
  .swatch-row { display: flex; gap: 16px; flex-wrap: wrap; }
  .swatch {
    width: 140px;
  }
  .swatch .chip {
    width: 140px; height: 140px;
    border-radius: var(--radius-md);
    border: 1px solid var(--hairline);
  }
  .swatch .label { margin-top: 8px; font-size: 14px; font-weight: 500; }
  .swatch .hex { font-family: var(--font-mono); font-size: 12px; opacity: 0.7; }
  .swatch .role { font-size: 12px; opacity: 0.6; margin-top: 4px; }
  .swatch.small .chip { width: 60px; height: 60px; }
  .swatch.small { width: 60px; }
  /* Contrast table */
  table.contrast {
    width: 100%; border-collapse: collapse; font-size: 14px;
  }
  table.contrast th, table.contrast td {
    text-align: left; padding: 10px 12px;
    border-bottom: 1px solid var(--hairline);
  }
  table.contrast th { font-weight: 600; opacity: 0.7; }
  table.contrast td.mono { font-family: var(--font-mono); }
  .badge {
    display: inline-block; padding: 2px 10px; border-radius: var(--radius-sm);
    font-size: 12px; font-weight: 500;
  }
  .badge.pass { background: var(--status-success); color: var(--paper); }
  .badge.fail { background: var(--status-error); color: var(--paper); }
  .contrast-warning {
    background: color-mix(in oklch, var(--status-error) 12%, transparent);
    color: var(--status-error);
    padding: 12px 16px; border-radius: var(--radius-sm);
    margin-bottom: 16px; font-size: 14px;
  }
  /* Type ramp */
  .display-ramp p { font-family: var(--font-display); margin-bottom: 8px; }
  .display-ramp .d72 { font-size: 72px; line-height: 1.0; letter-spacing: -0.03em; }
  .display-ramp .d56 { font-size: 56px; line-height: 1.05; letter-spacing: -0.02em; }
  .display-ramp .d40 { font-size: 40px; line-height: 1.1; letter-spacing: -0.02em; }
  .display-ramp .d28 { font-size: 28px; line-height: 1.2; letter-spacing: -0.01em; }
  .body-ramp p { margin-bottom: 16px; max-width: 60ch; }
  .body-ramp .b18 { font-size: 18px; line-height: 1.6; }
  .body-ramp .b16 { font-size: 16px; line-height: 1.6; }
  .body-ramp .b14 { font-size: 14px; line-height: 1.5; }
  .mono-sample {
    font-family: var(--font-mono); font-size: 14px;
    background: var(--ash); padding: 16px;
    border-radius: var(--radius-sm); border: 1px solid var(--hairline);
    white-space: pre; overflow-x: auto;
  }
  .tracking-test {
    font-family: var(--font-body); font-size: 12px; font-weight: 500;
    letter-spacing: 0.06em; text-transform: uppercase; opacity: 0.7;
  }
  /* Spacing + radius viz */
  .spacing-bars { display: flex; gap: 12px; align-items: flex-end; }
  .spacing-bar { background: var(--accent-primary); height: 24px; border-radius: 2px; }
  .spacing-bar .px { display: block; margin-top: 4px; font-size: 12px; font-family: var(--font-mono); opacity: 0.7; }
  .radius-row { display: flex; gap: 16px; }
  .radius-box {
    width: 60px; height: 60px;
    background: color-mix(in oklch, var(--accent-primary) 15%, transparent);
    border: 1px solid var(--accent-primary);
    display: flex; align-items: flex-end; justify-content: center; padding: 6px;
    font-family: var(--font-mono); font-size: 11px;
  }
  /* Components */
  .btn-row { display: flex; gap: 12px; flex-wrap: wrap; }
  .btn {
    font-family: var(--font-body); font-size: 14px; font-weight: 500;
    padding: 10px 18px; border-radius: var(--radius-sm); cursor: pointer;
    letter-spacing: 0.02em; transition: opacity 150ms ease;
  }
  .btn:hover { opacity: 0.9; }
  .btn-default { background: var(--accent-primary); color: var(--paper); border: 1px solid var(--accent-primary); }
  .btn-secondary { background: transparent; color: var(--ink); border: 1px solid var(--hairline); }
  .btn-outline { background: transparent; color: var(--accent-primary); border: 1px solid var(--accent-primary); }
  .btn-ghost { background: transparent; color: var(--ink); border: 1px solid transparent; }
  .btn-destructive { background: var(--status-error); color: var(--paper); border: 1px solid var(--status-error); }
  /* Form */
  .form { display: flex; flex-direction: column; gap: 14px; max-width: 320px; }
  .form label { font-size: 13px; font-weight: 500; opacity: 0.8; margin-bottom: 4px; display: block; }
  .form input[type="text"], .form textarea, .form select {
    width: 100%; padding: 10px 12px;
    background: var(--ash); color: var(--ink);
    border: 1px solid var(--hairline); border-radius: var(--radius-sm);
    font-family: var(--font-body); font-size: 14px;
  }
  .form textarea { min-height: 80px; resize: vertical; }
  .form .row { display: flex; gap: 8px; align-items: center; }
  /* Card */
  .card {
    background: var(--ash); border: 1px solid var(--hairline);
    border-radius: var(--radius-md); padding: 24px; max-width: 340px;
  }
  .card h3 { font-family: var(--font-body); font-size: 20px; font-weight: 600; margin-bottom: 8px; }
  .card p { font-size: 16px; margin-bottom: 16px; }
  /* Dialog */
  .dialog-overlay {
    background: color-mix(in oklch, var(--ink) 50%, transparent);
    padding: 40px; border-radius: var(--radius-md); border: 1px solid var(--hairline);
  }
  .dialog {
    background: var(--paper); border: 1px solid var(--hairline);
    border-radius: var(--radius-md); padding: 24px; max-width: 440px; margin: 0 auto;
    box-shadow: var(--shadow-md);
  }
  .dialog h3 { font-family: var(--font-body); font-size: 18px; font-weight: 600; margin-bottom: 8px; }
  .dialog p { font-size: 15px; margin-bottom: 8px; }
  .dialog .footer { display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px; }
  /* Table */
  table.data { width: 100%; border-collapse: collapse; font-size: 14px; }
  table.data th, table.data td {
    text-align: left; padding: 10px 12px;
    border-bottom: 1px solid var(--hairline);
  }
  table.data th { font-weight: 600; opacity: 0.7; }
  table.data td.num { font-family: var(--font-mono); font-variant-numeric: tabular-nums; text-align: right; }
  /* Tabs */
  .tabs { display: flex; gap: 24px; border-bottom: 1px solid var(--hairline); margin-bottom: 16px; }
  .tab {
    font-family: var(--font-body); font-size: 14px; font-weight: 500;
    padding: 12px 0; cursor: pointer; opacity: 0.6;
    border-bottom: 2px solid transparent;
  }
  .tab.active { opacity: 1; border-bottom-color: var(--accent-primary); }
  /* Badges */
  .badge-row { display: flex; gap: 8px; flex-wrap: wrap; }
  .badge-default { background: var(--ink); color: var(--paper); }
  .badge-outline { background: transparent; color: var(--ink); border: 1px solid var(--hairline); }
  .badge-success { background: var(--status-success); color: var(--paper); }
  .badge-warning { background: var(--status-warning); color: var(--paper); }
  .badge-error { background: var(--status-error); color: var(--paper); }
  .badge-info { background: var(--accent-primary); color: var(--paper); }
  /* Toast */
  .toast {
    position: fixed; bottom: 24px; right: 24px;
    background: var(--ash); color: var(--ink); border: 1px solid var(--hairline);
    border-radius: var(--radius-md); padding: 12px 16px; max-width: 320px;
    box-shadow: var(--shadow-md);
    font-size: 14px;
  }
  .toast .title { font-weight: 600; margin-bottom: 2px; }
  .toast .close { float: right; opacity: 0.5; cursor: pointer; }
  /* Hero */
  .hero { padding: 80px 0; border-top: 1px solid var(--hairline); border-bottom: 1px solid var(--hairline); }
  .hero .eyebrow {
    font-family: var(--font-mono); font-size: 12px;
    letter-spacing: 0.08em; text-transform: uppercase;
    color: var(--accent-primary); margin-bottom: 16px;
  }
  .hero h1 {
    font-family: var(--font-display); font-size: 72px;
    line-height: 1.0; letter-spacing: -0.03em;
    margin-bottom: 24px; max-width: 16ch;
  }
  .hero p { font-size: 18px; line-height: 1.6; max-width: 56ch; margin-bottom: 32px; opacity: 0.85; }
  .hero .actions { display: flex; gap: 12px; }
  /* Footer */
  footer { margin-top: 96px; padding-top: 32px; border-top: 1px solid var(--hairline); opacity: 0.7; font-size: 16px; }
  footer strong { color: var(--ink); }
</style>
</head>
<body>
<main>
  <div class="topbar">
    <div class="name">{{project_name}}</div>
    <div class="direction">{{direction_name}} — {{character}}</div>
    <button class="toggle" onclick="document.documentElement.dataset.theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'">Toggle theme</button>
  </div>

  <section>
    <h2>Surface roles</h2>
    <div class="swatch-row">
      <div class="swatch"><div class="chip" style="background: var(--paper)"></div><div class="label">paper</div><div class="hex">{{light_paper}} / {{dark_paper}}</div><div class="role">primary canvas, 70%+ of pixels</div></div>
      <div class="swatch"><div class="chip" style="background: var(--ash)"></div><div class="label">ash</div><div class="hex">{{light_ash}} / {{dark_ash}}</div><div class="role">raised surface — cards, panels</div></div>
      <div class="swatch"><div class="chip" style="background: var(--ink)"></div><div class="label">ink</div><div class="hex">{{light_ink}} / {{dark_ink}}</div><div class="role">main text — 4.5:1 against paper</div></div>
      <div class="swatch"><div class="chip" style="background: var(--hairline)"></div><div class="label">hairline</div><div class="hex">{{light_hairline}} / {{dark_hairline}}</div><div class="role">1px borders, dividers</div></div>
    </div>
  </section>

  <section>
    <h2>Accent roles</h2>
    <div class="swatch-row">
      <div class="swatch"><div class="chip" style="background: var(--accent-primary)"></div><div class="label">accent.primary</div><div class="hex">{{accent_primary}}</div><div class="role">CTAs, links — max 2 per screen</div></div>
      <div class="swatch"><div class="chip" style="background: var(--accent-primary-hover)"></div><div class="label">accent.primary_hover</div><div class="hex">{{accent_primary_hover}}</div><div class="role">hover state — derived −8% L</div></div>
      {{accent_secondary_swatch_or_empty}}
    </div>
  </section>

  <section>
    <h2>Status</h2>
    <div class="swatch-row">
      <div class="swatch small"><div class="chip" style="background: var(--status-success)"></div><div class="label">success</div><div class="hex">{{status_success}}</div></div>
      <div class="swatch small"><div class="chip" style="background: var(--status-warning)"></div><div class="label">warning</div><div class="hex">{{status_warning}}</div></div>
      <div class="swatch small"><div class="chip" style="background: var(--status-error)"></div><div class="label">error</div><div class="hex">{{status_error}}</div></div>
    </div>
  </section>

  <section>
    <h2>Contrast (WCAG)</h2>
    {{contrast_warning_or_empty}}
    <table class="contrast">
      <thead><tr><th>Pair</th><th>Ratio</th><th>Minimum</th><th>Status</th></tr></thead>
      <tbody>{{contrast_rows}}</tbody>
    </table>
  </section>

  <section>
    <h2>Display ({{display_font}})</h2>
    <div class="display-ramp">
      <p class="d72">{{display_sample_72}}</p>
      <p class="d56">{{display_sample_56}}</p>
      <p class="d40">{{display_sample_40}}</p>
      <p class="d28">{{display_sample_28}}</p>
    </div>
  </section>

  <section>
    <h2>Body ({{body_font}})</h2>
    <div class="body-ramp">
      <p class="b18">{{body_sample_paragraph}}</p>
      <p class="b16">{{body_sample_paragraph}}</p>
      <p class="b14">{{body_sample_paragraph}}</p>
    </div>
  </section>

  <section>
    <h2>Mono ({{mono_font}})</h2>
    <pre class="mono-sample">{{mono_code_sample}}</pre>
  </section>

  <section>
    <h2>Letter-spacing</h2>
    <p class="tracking-test">LABEL · METADATA · 0.06EM TRACKING</p>
  </section>

  <section>
    <h2>Spacing</h2>
    <div class="spacing-bars">
      <div><div class="spacing-bar" style="width:4px"></div><span class="px">4</span></div>
      <div><div class="spacing-bar" style="width:8px"></div><span class="px">8</span></div>
      <div><div class="spacing-bar" style="width:12px"></div><span class="px">12</span></div>
      <div><div class="spacing-bar" style="width:16px"></div><span class="px">16</span></div>
      <div><div class="spacing-bar" style="width:24px"></div><span class="px">24</span></div>
      <div><div class="spacing-bar" style="width:32px"></div><span class="px">32</span></div>
      <div><div class="spacing-bar" style="width:48px"></div><span class="px">48</span></div>
      <div><div class="spacing-bar" style="width:64px"></div><span class="px">64</span></div>
    </div>
  </section>

  <section>
    <h2>Radius</h2>
    <div class="radius-row">
      <div class="radius-box" style="border-radius: var(--radius-sm)">{{radius_sm}}</div>
      <div class="radius-box" style="border-radius: var(--radius-md)">{{radius_md}}</div>
      <div class="radius-box" style="border-radius: var(--radius-lg)">{{radius_lg}}</div>
    </div>
  </section>

  <section>
    <h2>Buttons</h2>
    <div class="btn-row">
      <button class="btn btn-default">Continue</button>
      <button class="btn btn-secondary">Cancel</button>
      <button class="btn btn-outline">Learn more</button>
      <button class="btn btn-ghost">Skip</button>
      <button class="btn btn-destructive">Delete</button>
    </div>
  </section>

  <section>
    <h2>Form</h2>
    <div class="form">
      <div><label>Full name</label><input type="text" placeholder="Sofia Chen" /></div>
      <div><label>Notes</label><textarea placeholder="Anything we should know?"></textarea></div>
      <div><label>Region</label><select><option>Bangalore</option><option>Mumbai</option><option>Delhi</option></select></div>
      <div class="row"><input type="checkbox" id="sub" /><label for="sub" style="margin:0">Subscribe to updates</label></div>
    </div>
  </section>

  <section>
    <h2>Card</h2>
    <div class="card">
      <h3>Card title</h3>
      <p>This is the body of the card. It uses the body font at 16 px with a 1.6 line-height. Two lines like this is typical density.</p>
      <button class="btn btn-default">Action</button>
    </div>
  </section>

  <section>
    <h2>Dialog</h2>
    <div class="dialog-overlay">
      <div class="dialog">
        <h3>Confirm change</h3>
        <p>You are about to apply the proposed tokens to this project.</p>
        <p>This replaces values in <code>agents/DESIGN.md</code> and the live <code>global.css</code> after the next sync.</p>
        <div class="footer">
          <button class="btn btn-secondary">Cancel</button>
          <button class="btn btn-default">Confirm</button>
        </div>
      </div>
    </div>
  </section>

  <section>
    <h2>Table</h2>
    <table class="data">
      <thead><tr><th>Name</th><th>Joined</th><th>Status</th><th class="num">Spend</th></tr></thead>
      <tbody>
        <tr><td>Sofia Chen</td><td>2025-11-04</td><td><span class="badge badge-success">Active</span></td><td class="num">12,480</td></tr>
        <tr><td>Arjun Mehta</td><td>2025-10-28</td><td><span class="badge badge-success">Active</span></td><td class="num">9,210</td></tr>
        <tr><td>Lila Pereira</td><td>2025-09-12</td><td><span class="badge badge-warning">Trial</span></td><td class="num">340</td></tr>
        <tr><td>David Kim</td><td>2025-08-30</td><td><span class="badge badge-default">Lapsed</span></td><td class="num">0</td></tr>
        <tr><td>Aanya Rao</td><td>2025-08-14</td><td><span class="badge badge-error">Blocked</span></td><td class="num">0</td></tr>
      </tbody>
    </table>
  </section>

  <section>
    <h2>Tabs</h2>
    <div class="tabs">
      <div class="tab active">Overview</div>
      <div class="tab">Details</div>
      <div class="tab">History</div>
    </div>
    <p>The active tab carries an accent underline. Body copy below anchors the chosen state.</p>
  </section>

  <section>
    <h2>Badges</h2>
    <div class="badge-row">
      <span class="badge badge-default">Default</span>
      <span class="badge badge-outline">Outline</span>
      <span class="badge badge-success">Success</span>
      <span class="badge badge-warning">Warning</span>
      <span class="badge badge-error">Error</span>
      <span class="badge badge-info">Info</span>
    </div>
  </section>

  <section class="hero">
    <div class="eyebrow">INTRODUCING</div>
    <h1>{{hero_headline}}</h1>
    <p>{{hero_subhead}}</p>
    <div class="actions">
      <button class="btn btn-default">{{hero_primary_cta}}</button>
      <button class="btn btn-ghost">{{hero_secondary_cta}}</button>
    </div>
  </section>

  <div class="toast">
    <span class="close">×</span>
    <div class="title">Tokens generated</div>
    <div>Open this file in your browser to review.</div>
  </div>

  <footer>
    This is direction <strong>{{direction_name}}</strong> rendered with the proposed tokens.
    If this looks right, return to chat and say <strong>approve</strong> (or <strong>apply all</strong>).
    If something feels off, tell me what to change — &quot;the accent feels too orange&quot;,
    &quot;display feels too heavy&quot;, &quot;dark mode is muddy&quot; — and I&apos;ll regenerate.
    <br /><br />
    Display: <strong>{{display_font}}</strong> ({{display_source}}). Body:
    <strong>{{body_font}}</strong> ({{body_source}}). Mono:
    <strong>{{mono_font}}</strong> ({{mono_source}}).
  </footer>
</main>
</body>
</html>
```

---

## Substitution rules

Phase 6.5 builds a substitution map from the locked direction + generated
token values. Most fields are direct copies. A few need computation.

### Direct substitutions
- `{{project_name}}` — from `agents/BRAND.md` Product.Name
- `{{direction_name}}` — Phase 6 locked direction name
- `{{character}}` — one-line character from the direction (Phase 5 "personality sentence")
- `{{light_*}}` / `{{dark_*}}` / `{{accent_*}}` / `{{status_*}}` — direct hex from `new_token_values`
- `{{radius_*}}` / `{{shadow_*}}` — direct from `new_token_values`
- `{{display_font}}` / `{{body_font}}` / `{{mono_font}}` — direct font family names
- `{{display_stack}}` / `{{body_stack}}` / `{{mono_stack}}` — full CSS font-family stack with fallbacks (e.g., `"Migra", Georgia, serif`)

### Computed substitutions

**`{{google_fonts_link}}`** — build the Google Fonts `<link>` for any of the
three families that ARE on Google Fonts. Skip the ones that aren't. Example:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
```

**`{{display_source}}` / `{{body_source}}` / `{{mono_source}}`** — one of:
- `Google Fonts` — loaded via the link above, will render correctly
- `Pangram (preview shows fallback)` — not on Google, fall back to nearest visual cousin
- `commercial (preview shows fallback)` — paid font, fall back to nearest visual cousin

When a font is not on Google, also append a system fallback chain in the
stack (`{{display_stack}}`) so the preview renders something readable.

**`{{accent_secondary_swatch_or_empty}}`** — if `accent.secondary` is set in
`new_token_values`, emit a swatch div for it; otherwise emit an empty string.

**`{{contrast_warning_or_empty}}`** — compute the 6 critical pairs (see
section 5 above). If any FAIL, emit a `.contrast-warning` div with the
"below WCAG AA" message. Otherwise empty string.

**`{{contrast_rows}}`** — one `<tr>` per pair, with computed WCAG ratio and
PASS/FAIL badge. Use the standard relative-luminance formula
(`(L1 + 0.05) / (L2 + 0.05)` where L1 is the lighter colour).

**`{{display_sample_72}}` / `{{display_sample_56}}` / `{{display_sample_40}}` / `{{display_sample_28}}`** —
short headlines drawn from the brand context. Use **real brand-fitting copy**,
not generic "The quick brown fox". Phase 6.5 generates four headlines that
match the locked archetype:

- Sage → "Knowledge, organised." / "The full picture." / "What the data says." / "Less guesswork."
- Magician → "See what was hidden." / "Reveal the pattern." / "From signal to story." / "Notice more."
- Caregiver → "Looking out for you." / "We&apos;ve got the details." / "Quiet, considered care." / "Here when you need it."
- Rebel → "Break the script." / "Not how it&apos;s done." / "Loud on purpose." / "Refuse the default."
- Creator → "Make it yours." / "Bring it to life." / "Start with a sketch." / "Anything you can imagine."
- Hero → "Win the day." / "Built for the fight." / "Show what you&apos;re made of." / "Step up."
- Explorer → "Find your way." / "There&apos;s more out there." / "Off the map." / "Keep going."
- Innocent → "Simple, on purpose." / "Light enough to carry." / "Honest by design." / "Easy yes."
- Lover → "Made for the moment." / "Closer than that." / "Hold it in your hands." / "Pure pleasure."
- Jester → "Take it less seriously." / "More fun, less friction." / "Wait, what?" / "Yes, really."
- Ruler → "The standard, set." / "Built to lead." / "Authority, quietly worn." / "What stays."
- Everyman → "Built for everyone." / "Right where you are." / "Honest tools, fair price." / "It just works."

Pick four; the 72-px line is the strongest, the 28-px is the most operational.

**`{{body_sample_paragraph}}`** — one paragraph of brand-fitting body copy
(3–4 sentences, ~50–80 words). Use real-sounding copy that reflects the
audience and tone, not "Lorem ipsum". Same paragraph repeats across the
three sizes so visual density comparison is fair.

**`{{mono_code_sample}}`** — the token JSON shown in section 8 above, with
the project&apos;s actual hex values substituted.

**`{{hero_headline}}`** — a single brand-fitting headline (2 lines max,
~6–10 words). Reuse one of the four display samples or generate a new one
specifically for the hero.

**`{{hero_subhead}}`** — 2–3 sentences explaining the product, written in
the brand&apos;s tone. Use audience + problem from `agents/BRAND.md`.

**`{{hero_primary_cta}}`** — short verb-led CTA (e.g., "Get started",
"Read the brief", "See it in action"). Match brand archetype.

**`{{hero_secondary_cta}}`** — softer secondary CTA (e.g., "Take a tour",
"Read the docs", "Talk to us").

---

## Font-loading rules

Three families to load: display, body, mono. Each goes through this check:

1. Is the font on Google Fonts? → emit a `<link>` and use the family directly.
2. Is the font Pangram (free-to-try) or commercial? → use the nearest Google
   cousin for the preview, note in the footer that the production font is
   different. Keep the production family in the **first** position of the
   `font-family` stack so the user&apos;s OS will render it if installed locally.

### Google Fonts substitution map (for non-Google production fonts)

| Production font | Preview substitute (Google Fonts) | Rationale |
|---|---|---|
| Migra | Source Serif 4 (display weight) | Closest editorial-display serif |
| Editorial New (PP) | Fraunces (wght 900, opsz max) | Sharp, sculptural |
| Tobias | Lora (wght 600+) | Two-axis contrast serif |
| Söhne | Inter | Closest neutral grotesque on Google |
| GT America | Inter | Same |
| Suisse Int&apos;l | Inter | Same |
| Beausite | Manrope (wght 700) | Geometric with humanist warmth |
| Cooper | Yeseva One | Display serif with similar curve energy |
| Antarctica | Archivo (wght 800) | Industrial sans |
| Authentic Sans | Space Grotesk | Closest expressive sans |
| Lyon | Cormorant Garamond | High-contrast classical serif |

For body fonts, Inter / Geist / IBM Plex are all on Google Fonts directly —
load them as written. No substitution needed.

For mono, JetBrains Mono / IBM Plex Mono are on Google Fonts. Geist Mono is
not — substitute JetBrains Mono in the preview.

### When the chosen font isn&apos;t in the substitution map

Fall back generically:
- Display + serif → Source Serif 4
- Display + sans → Inter
- Body + serif → Source Serif 4
- Body + sans → Inter
- Mono → JetBrains Mono

Always note in the footer what the actual production font is so the user
knows the preview is approximate.

---

## File path and surfacing to the user

Write to:

```
agents/preview/<direction-name-slug>-<YYYY-MM-DD>.html
```

Slug: lowercase, hyphenated direction name (e.g., `editorial-cream`).

Add `agents/preview/` to `.gitignore` on first preview generation if not
already ignored. Previews are throwaway approval surfaces, not canon.

After writing, surface to the user as part of the Phase 6.5 step 5 diff
output:

```
Token alignment — comparing locked direction "Editorial Cream" vs existing DESIGN.md:

[diff table here per phase-6-5-token-alignment.md]

👀 Preview rendered: file:///<absolute-path>/agents/preview/editorial-cream-2026-05-22.html

Open it in your browser to see the tokens applied to real components. Light/dark
toggle is in the top-right of the preview.

When you&apos;re ready:
  [approve / apply all] — write the new tokens to agents/DESIGN.md
  [iterate] — tell me what to change (in plain language)
  [reject] — keep existing tokens, only write Overview + DO NOT
```

The `file://` URL must be an **absolute path** so the user can click it
directly from chat. Compute via `realpath` or the project&apos;s cwd.

---

## When to skip the preview

Skip generation in only one case:

- Phase 6.5 alignment result is `match` (no token changes proposed).

Do NOT skip when:
- The user is on a remote / headless setup. Write the file anyway and surface
  the path; they can scp it or open it via a tunnel.
- The browser environment is unknown. The HTML is self-contained — any
  browser opens it.
- Time pressure. The preview takes <1 second of generation time; it&apos;s
  cheap.

---

## Iteration loop

When the user says &quot;iterate&quot; with a change request:

1. Phase 6.5 re-runs step 4 (regenerate token values) with the user&apos;s
   correction applied (e.g., shift accent hue cooler, drop chroma 10%).
2. Re-run preview generation — write to a NEW filename with a `-v2`,
   `-v3` suffix (`editorial-cream-2026-05-22-v2.html`). Don&apos;t overwrite
   the prior preview — the user may want to compare.
3. Re-surface the new file path. Loop until `approve` or `reject`.

There&apos;s no hard limit on iterations, but if the loop hits 5+, surface
a meta-prompt: &quot;We&apos;re on iteration 5. The direction itself might be
wrong — want to step back to Phase 6 and reconsider?&quot;

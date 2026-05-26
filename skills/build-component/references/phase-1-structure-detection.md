# Phase 1 — Structure detection

Before anything else, the skill needs to know where this project's components live, what tiers exist, and which convention is in use. This phase reads only — no writes until the user confirms findings.

The output of this phase is a confirmed `agents/STRUCTURE.md`. On every subsequent run of `build-component`, that file is read and this phase is a no-op.

---

## 1.1 — Check for existing `agents/STRUCTURE.md`

```
Read: agents/STRUCTURE.md
```

If present and well-formed (has the expected sections — Tiers, Locations, Convention, Surfaces), parse it into a structure object and skip to Phase 2. One-line announcement to the user:

```
Structure detected (agents/STRUCTURE.md):
  Tiers: Generic, Marketing, App
  Convention: cva + forwardRef + cn (shadcn-style)
  Surfaces: marketing (web), dashboard (web)

Proceeding to intake.
```

If `agents/STRUCTURE.md` is missing or malformed → run first-run detection (1.2 onward).

---

## 1.2 — Glob common component folders

Delegate to a fast sub-agent. Glob each of the following (exclude `node_modules/`, `.git/`, `dist/`, `build/`):

- `components/ui/**` — classic shadcn convention. If present, this is the **Generic** layer.
- `components/blocks/**` — composed marketing blocks.
- `components/marketing/**` or `components/(marketing)/**` — explicit Marketing tier folder.
- `components/app/**`, `components/dashboard/**` — explicit App tier folder.
- `src/components/**` — Vite / older Next conventions.
- `packages/ui/**` — monorepo design-system package.
- `app/_components/**` or `app/components/**` — Next.js App Router co-located components.
- `apps/web/src/components/**`, `apps/dashboard/src/components/**` — multi-app monorepo split.
- `desktop/src/components/**` — Tauri / Electron desktop frontend.
- `src-tauri/tauri.conf.json` — **Tauri desktop app signal.** If this file exists, record a `desktop (Tauri)` surface entry in STRUCTURE.md regardless of where the frontend components live (they may be at repo root, `src/`, `frontend/`, or elsewhere). Both the frontend surface AND the desktop surface must be recorded.
- `Views/**/*.swift` — Swift / SwiftUI projects.

For each path, record: exists / count of files / one sample file name. This is enough to propose locations without reading everything.

---

## 1.3 — Read `tsconfig.json` paths (web projects)

If `tsconfig.json` exists at root or under `apps/*/`, parse `compilerOptions.paths`. Capture path aliases like:

```json
"paths": {
  "@/*": ["./src/*"],
  "@/components/*": ["./src/components/*"],
  "@/ui/*": ["./src/components/ui/*"],
  "@marketing/*": ["./apps/marketing/src/*"]
}
```

These aliases tell you the canonical import names — the structure file should record both the filesystem path AND the import alias for each tier, so subsequent phases emit the right import statement.

For monorepos with `tsconfig.base.json` or `tsconfig.references` arrays, walk each referenced config.

---

## 1.4 — Read `package.json` for stack indicators

Open `package.json` and check `dependencies` + `devDependencies` for:

| Indicator | Meaning |
|-----------|---------|
| `class-variance-authority` | shadcn-style convention. Triplet = cva + forwardRef + cn. |
| `tailwindcss` + `tailwind-merge` + `clsx` | `cn` utility likely lives in `lib/utils.ts`. |
| Has a `components.json` file at root | Confirmed shadcn-ui CLI install. Read `components.json` for `aliases.ui` to get the Generic folder. |
| `styled-components` | styled-components convention. Triplet does not apply. |
| `@emotion/react` or `@emotion/styled` | Emotion convention. Triplet does not apply. |
| `@vanilla-extract/css` | vanilla-extract convention. Tokens defined in `*.css.ts`. |
| `*.module.css` files exist anywhere | CSS Modules convention. |
| `tauri` / `electron` | Desktop surface present. |
| `next` and route groups `(marketing)` / `(dashboard)` under `app/` | Marketing + App surfaces both present. |
| `vite` + a single component folder | Single-surface project. |

Record the detected convention. If multiple conventions appear (e.g. styled-components AND CSS modules), record the dominant one (highest file count) plus a note.

For Swift projects: convention is always SwiftUI-style with `Color.tokenName` references — record that and move on.

---

## 1.5 — Detect surfaces

Look at route grouping and folder names to infer which **surfaces** this project has. A surface is a deployed front (marketing site / dashboard app / desktop app / docs site / email templates). The detected surface set determines which tiers are available in Phase 2.

| Signal | Surface |
|--------|---------|
| `app/(marketing)/**` or `app/marketing/**` or `apps/marketing/**` | Marketing (web) |
| `app/(dashboard)/**` or `app/app/**` or `apps/dashboard/**` | App (web) |
| `desktop/` with Tauri / Electron config | App (desktop) |
| `src-tauri/tauri.conf.json` exists (any frontend location) | App (desktop, Tauri) — record alongside whatever web surface exists |
| `app/(docs)/**`, `apps/docs/**`, `docs/` with MDX | Docs |
| `emails/` with `react-email` deps | Email |
| Single `src/` and no route groups | Single-surface (treat as App) |

Record the surface set. Examples:

- `{marketing, app-web}` → both Marketing and App tiers are available.
- `{app-desktop}` → only App tier is available; Marketing is hidden in Phase 2.
- `{app-web}` (dashboard-only SaaS, no marketing site) → only App + Generic tiers.
- `{marketing}` (landing-page-only project) → only Marketing + Generic.

---

## 1.6 — Propose findings + write `agents/STRUCTURE.md`

Surface everything detected to the user via `AskUserQuestion` (or as a confirmation message). Shape:

```
Detected structure for this project:

  Tiers available:
    - Generic   → src/components/ui/         (import: @/components/ui/*)
    - Marketing → src/components/marketing/  (import: @/components/marketing/*)
    - App       → src/components/app/        (import: @/components/app/*)

  Convention: cva + forwardRef + cn (shadcn-style)
    cn utility: src/lib/utils.ts
    Tailwind:   tailwind.config.ts + globals.css

  Surfaces:
    - Marketing (web) — app/(marketing)/
    - App (web)       — app/(dashboard)/

  No desktop / docs / email surfaces detected.

Save this as agents/STRUCTURE.md so future component builds skip detection?
  A — Yes, save and continue.
  B — Save but let me edit it first.
  C — Skip the save, run one-off this time.
```

- **A** → copy `templates/STRUCTURE.md` to `agents/STRUCTURE.md` then patch the detected values into it (see 1.6a). Continue to Phase 2.
- **B** → copy + patch as in A, then open an edit pass with the user (add a tier, rename a folder, change the convention) before the final write.
- **C** → keep the structure object in memory only. Future runs re-detect.

### 1.6a — Copy the canonical template, then patch detected values

The shape of `agents/STRUCTURE.md` is fixed — the plugin ships a canonical template at `templates/STRUCTURE.md` (sections: Surfaces present, Component locations, Stack per surface, Conventions detected, Cross-tier import rules, plus a commented WORKED EXAMPLE block). Phase 1 fills the placeholders, it does not invent the shape.

Copy the template first:

```bash
cp "${CODEX_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/templates/STRUCTURE.md" agents/STRUCTURE.md
```

If neither `CODEX_PLUGIN_ROOT` nor `CLAUDE_PLUGIN_ROOT` is set (some agents don't expose the env var): use the Read tool to fetch the template content from the plugin install path, then Write it to `agents/STRUCTURE.md`.

Once the copy is in place, patch the placeholders with detected values:

- **Surfaces present** — flip `yes/no` for each row based on §1.5 detection. Fill the path column with the actual detected path (`app/(marketing)/`, `desktop/src/`, …). Fill the tech column from `package.json` (Next version, Tauri version, etc.).
- **Component locations** — fill the path column for each tier (Generic / Marketing / App-web / App-desktop) from §1.2 detection. If a tier folder doesn't exist yet but the surface is present, record the **recommended** path and mark it `[VERIFY]` so the first write into it surfaces a "creating new folder" prompt.
- **Stack per surface** — fill from `package.json` + `tsconfig.json` aliases. Drop rows for surfaces that don't apply.
- **Conventions detected** — fill from §1.4 (style system, cn utility location, file-naming, icon library, forms, state). Anything ambiguous: `[VERIFY]`.
- **Cross-tier import rules** — leave the template's rule set as-is (they're universal). Only edit if the project explicitly violates one of them (rare).
- **WORKED EXAMPLE block** — delete the entire HTML-comment block at the bottom of the template before writing. The example is illustrative only and must not ship into the project's canon.

Mark every patched-in value that came from inference (not direct read) with `[VERIFY]` so `audit` surfaces it later.

Do not invent new sections. Do not strip sections from the template — if a section doesn't apply (e.g. no desktop surface), keep the section header and fill all rows with `no` / `—` / `n/a`. Future migrations into desktop will fill it in without touching the schema.

---

## 1.7 — Halt conditions

Halt Phase 1 (and the whole skill) if:

- `agents/DESIGN.md` does not exist → route the user to `init-project` first. Reason: there's no token canon to normalize against.
- `agents/FUNDAMENTALS.md` does not exist → route the user to `init-project` first. Reason: there's no craft layer for `design-check` to enforce later.
- No component folders detected AND no `package.json` AND no source files → this is an empty repo. Route to `init-project`.

For partial states (e.g. `DESIGN.md` exists but no components folder yet), continue — the skill will offer to create the first component folder in Phase 4.

---

## 1.8 — One concrete example

A Next.js 14 App Router monorepo, single app, with shadcn already installed.

Detection finds:

- `components/ui/` (47 files) — shadcn primitives.
- `app/(marketing)/page.tsx` exists.
- `app/(dashboard)/layout.tsx` exists.
- No `components/marketing/` and no `components/app/` folders yet.
- `components.json` says `aliases.ui = "@/components/ui"`.
- `package.json` has `class-variance-authority`, `tailwindcss`, `tailwind-merge`, `clsx`.
- `src/lib/utils.ts` exports `cn`.

The proposal:

```
Detected:
  Generic → components/ui/ (47 existing) — convention: cva + forwardRef + cn.
  Marketing tier folder does not exist yet. Recommend: components/marketing/
  App tier folder does not exist yet. Recommend: components/app/
  Surfaces: marketing (web), dashboard (web) — both present in app/ route groups.

Save this as agents/STRUCTURE.md? I'll create components/marketing/ and components/app/
on first need (not now).
```

User confirms. Write `STRUCTURE.md`. Move to Phase 2.

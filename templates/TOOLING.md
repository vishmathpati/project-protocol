# TOOLING.md — Node Tooling Standards
> Global. Locked 2026-05-15. Same content on every Node project.
> Skip this file in Swift / Python / non-Node projects.

> **Note:** This file uses the author's personal layout (`~/Arel OS/Projects/`) as the working example. Adapt to your own machine — replace the path prefix with your actual projects root. The rules and conventions below apply universally.

---

## Package manager — bun

All Node projects use **bun** (v1.3.14+) as the package manager.

**Never** run `pnpm install`, `npm install`, or `yarn install` in any project under `~/Arel OS/Projects/`. The `packageManager` field in `package.json` enforces this.

If you find yourself reaching for `pnpm` or `npm`, **STOP**. Use `bun`.

---

## Node version

- Runtime: **Node 24 LTS** via Homebrew.
- Pinned per-project via `.nvmrc`.
- The `engines.node` field is `>=22.0.0` for Vercel deploy compatibility.

---

## Required files in every Node project

- `package.json` with:
  - `packageManager: "bun@<version>"`
  - `engines.node: ">=22.0.0"`
- `.nvmrc` containing `24`
- `.npmrc` containing `engine-strict=true`

---

## Next.js (Turbopack — default in Next 16)

- `experimental.serverComponentsHmrCache: true` in `next.config.ts`
- Wipe `.next/dev` if it exceeds 1 GB
- Only **one** `next dev` running at a time across all projects

---

## When this file changes

Never edited per-project. It is a global standard — overwritten verbatim from the plugin template on every `init-project` run. To change the standard, update `templates/TOOLING.md` in the plugin and rebuild.

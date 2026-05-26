# TOOLING.md — Node Tooling Convention
> Project-local. Generated at init time from the project's chosen package manager.
> Skip this file in Swift / Python / non-Node projects.

**Package manager:** {bun|pnpm|npm|yarn}
**Lockfile:** {bun.lock|pnpm-lock.yaml|package-lock.json|yarn.lock}

---

## Package manager

This project uses **{bun|pnpm|npm|yarn}** as its package manager.

**Never** run a different package manager's install command in this project. The `packageManager` field in `package.json` enforces this. If you find yourself reaching for the wrong one, **STOP** and use the one declared above.

---

## Node version

- Runtime: **Node 24 LTS** via Homebrew.
- Pinned per-project via `.nvmrc`.
- The `engines.node` field is `>=22.0.0` for Vercel deploy compatibility.

---

## Required files in every Node project

- `package.json` with:
  - `packageManager: "{manager}@<version>"`
  - `engines.node: ">=22.0.0"`
- `.nvmrc` containing `24`
- `.npmrc` containing `engine-strict=true`

---

## Next.js (Turbopack — default in Next 16)

- `experimental.serverComponentsHmrCache: true` in `next.config.ts`
- Wipe `.next/dev` if it exceeds 1 GB
- Only **one** `next dev` running at a time per project

---

## When this file changes

Never edited by hand per-project. Regenerated from the plugin template with the chosen package manager filled in. To change the package manager, re-run `init-project` and choose a different manager at the package-manager prompt.

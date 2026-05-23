# Phase 5 — Component selection

Goal: for each approved section, decide one of three strategies — reuse / adapt / build new — and execute the build-new entries inline via `build-component`. Still no page-level writes; new components written here are atomic and gated through `build-component`'s own preview.

## The strategy table — first half of the phase

Glob the components folder for the locked tier (marketing tier → `components/landing/`, `components/marketing/`, or whatever `STRUCTURE.md` says; dashboard tier → `components/dashboard/`, `components/app/`). Read short summaries of each existing component.

Then per section, propose:

```
| § | Section          | Strategy   | Component path                                      | Notes                          |
|---|------------------|------------|-----------------------------------------------------|--------------------------------|
| 1 | Hero             | reuse      | components/landing/Hero.tsx                         | already accepts headline+cta   |
| 2 | Trust strip      | build new  | (to create) components/landing/TrustStrip.tsx       | no existing primitive          |
| 3 | How it works     | adapt      | components/landing/StepCards.tsx                    | add `numbered` variant         |
| 4 | Features grid    | build new  | (to create) components/landing/WorkflowGrid.tsx     | 4-column workflow-stage layout |
| 5 | Selfie moment    | reuse      | components/landing/ImageRow.tsx                     | already supports image-left    |
| 6 | Camera coverage  | reuse      | components/landing/ThreeColIconRow.tsx              |                                |
| 7 | Run-the-studio   | reuse      | components/landing/ImageRow.tsx                     | image-right variant            |
| 8 | FAQ              | reuse      | components/ui/Accordion.tsx                         | wrap with section primitives   |
| 9 | Final CTA        | build new  | (to create) components/landing/CenteredCta.tsx      | no existing equivalent         |
```

### Reuse — first preference

If an existing component in the right tier folder solves the section's job — even if its current usage is on a different page — reuse it. Cite the absolute path. Note any props you'll pass that the component already accepts.

### Adapt — second preference

If an existing component is 80% right but missing one variant or prop, adapt it. Cite the path and describe the delta in one line: *"add `numbered` variant", "expose `align` prop", "add optional `accentColor` slot"*. The adapt work runs via an inline `build-component` call with sub-mode "extend existing primitive" — that call edits the existing component file, gated through its own preview.

### Build new — last resort

If nothing reusable or adaptable exists for the section, build new. Note the proposed path under STRUCTURE.md's rules and one line about what the component is.

## Reuse threshold — when to push back on "build new"

Before approving any "build new" row, ask: *is there really nothing close?* The bias is toward reuse — a project with 10 marketing components is cleaner than a project with 30. Re-glob if the count of "build new" rows feels high (more than 2–3 on a single page is usually a sign you missed reuse opportunities).

For composable shapes (anything that's "a section with a headline + visual + body"), prefer composition of existing layout primitives (`Section`, `Container`, `ImageRow`, `TextBlock`) over a single bespoke component per section. The Hero might be the only bespoke section-level component on the page; everything else can be a composition.

## Approval gate — first

After the table is proposed:

```
Components: <N reused, N adapted, N built new>

Approve the table / propose alternative reuse / restart?
```

User can push back on individual rows ("§4 should reuse the existing FeatureGrid, not build new" — verify the existing grid actually fits, then update the row).

Once the table is approved, the build-new and adapt rows are executed sequentially.

## The execution loop — second half of the phase

For each row marked `build new` or `adapt`:

1. Announce: *"Now building §<n> — `<component name>`. This drops into `build-component`."*
2. Invoke `build-component` with the section's spec:
   - Tier (already detected — Generic / Marketing / App).
   - One-sentence intent: *"A 4-column grid where each column is a workflow stage header + a stack of feature rows; each feature row is icon + name + one-line blurb."*
   - Data shape: *"Reads from `CONTENT.md` FEATURES; groups by `workflow_stage`."*
   - Strategy hint to skip `build-component`'s Phase 3 reuse scan (we already did it).
3. Let `build-component` run its full 5-phase flow with its own preview gate. The user approves the component there — not here.
4. When `build-component` returns the file path, write it back into this row's "Component path" column.
5. Move to the next row.

**Sequential, not parallel.** Even if two rows are independent. The user gets one focused conversation per net-new component instead of N components flying by in batch.

## When `design-check` fires inside this phase

Every `build-component` call ends with `design-check` running on the component file it wrote. Token violations or missing tokens surface there and pause that component's flow. `build-page` waits for that component to be resolved before moving to the next row.

## Approval gate — second

After all rows have a real path (no "to create" entries left):

```
All components ready:
  - <component 1> at <path>  [reused]
  - <component 2> at <path>  [adapted]
  - <component 3> at <path>  [built new]
  - <component 4> at <path>  [built new]
  …

Ready to wire the page (Phase 6)?
```

Wait for *"yes, wire it"*.

## What NOT to do

- Do not generate any page-level code in this phase. The page file does not exist yet.
- Do not bundle multiple build-new components into one `build-component` call. One component per call, even if they share a section.
- Do not skip `build-component` for net-new components ("just write it inline in the page"). The atomic gate exists for a reason — token discipline, naming consistency, reuse-scan, cross-tier rules.
- Do not modify existing components beyond the declared "adapt" delta. If adapting StepCards requires also adapting Section, propose that as a second adapt row and run it through its own `build-component` invocation.
- Do not propose "build new" for shapes the project clearly already has — even under a different name. A `WorkflowGrid` and a `FeatureGrid` are probably the same thing; reuse + adapt > build new.

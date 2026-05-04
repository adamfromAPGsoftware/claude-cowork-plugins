# Startup Protocol — Project Selection

Every agent runs this protocol on activation, before displaying its capability menu.

---

## Step 1 — Resolve paths

Read `{project-root}/config.yaml`. Extract:
- `paths.project_folder` — the projects directory (e.g. `~/Content/projects`)
- `paths.workspace` — the workspace root

---

## Step 2 — Read project index

Read `{paths.project_folder}/_index.yaml`.

- If the file does not exist: treat as zero registered projects.
- If it exists but `projects:` is empty: treat as zero registered projects.
- Otherwise: load the project list.

---

## Step 3 — Read last active project

Read `{project-root}/active-project.yaml`.

- If the file does not exist: no active project.
- If it exists, extract `slug` and `title`.

---

## Step 4 — Present project selection

**This is a mandatory interactive step. You must output the prompt below and stop. Do not proceed, do not show the capability menu, do not take any other action. Wait for the user to type their choice before continuing.**

Based on what was found, output one of the following prompts to the user:

---

### Scenario A — Projects exist, one was last active

```
Project: {slug} — {title}

  [R] Resume this project
  [S] Switch to a different project
  {if Content Strategist}[N] Create a new project{/if}
  {if NOT Content Strategist}[N] Create new project → run /content:1-content-strategist{/if}
  [X] Work standalone (no project)
```

If [R]: keep existing `active-project.yaml` as-is and proceed.
If [S]: show project list from `_index.yaml`, let user pick, update `active-project.yaml`.
If [N] and this is the Content Strategist: prompt for a project name, create the project folder scaffold (see below), register in `_index.yaml`, write `active-project.yaml`, proceed.
If [N] and this is NOT the Content Strategist: tell the user to run `/content:1-content-strategist` to create a project. Exit the startup flow — do not proceed to capability menu.
If [X]: proceed in standalone mode. Do NOT update `active-project.yaml` (preserve the last active slug for next session).

---

### Scenario B — Projects exist, none was last active

```
Existing projects:
  {list each slug — title from _index.yaml}

  [P] Pick a project
  {if Content Strategist}[N] Create a new project{/if}
  {if NOT Content Strategist}[N] Create new project → run /content:1-content-strategist{/if}
  [X] Work standalone
```

If [P]: show project list, let user pick, write `active-project.yaml`.
If [N] and this is the Content Strategist: create new project (see below).
If [N] and not Strategist: redirect to `/content:1-content-strategist`.
If [X]: proceed standalone.

---

### Scenario C — No projects exist

```
No projects yet.

  {if Content Strategist}[N] Create your first project{/if}
  {if NOT Content Strategist}To create a project, run /content:1-content-strategist first.{/if}
  [X] Work standalone
```

If [N] and this is the Content Strategist: create new project (see below).
If [N] and not Strategist: redirect to `/content:1-content-strategist`.
If [X]: proceed standalone.

---

## Step 5 — Create a new project (Content Strategist only)

When the user chooses to create a new project:

1. Ask: "What's this project about? Give it a short name." → becomes the project title.
2. Generate a slug: lowercase, hyphens, no spaces (e.g. `ai-tools-comparison`).
3. Confirm: "Creating project `{slug}` — {title}. Proceed? [Y/N]"
4. Create the project directory at `{paths.project_folder}/{slug}/` using the scaffold defined in `{project-root}/content-plugin/references/folder-structure.yaml`.
5. Write `{paths.project_folder}/{slug}/project.yaml`:
   ```yaml
   slug: {slug}
   title: {title}
   created: {YYYY-MM-DD}
   status: active
   ```
6. Register in `{paths.project_folder}/_index.yaml` — append to the `projects:` list:
   ```yaml
   - slug: {slug}
     title: {title}
     created: {YYYY-MM-DD}
     status: active
   ```
7. Write `{project-root}/active-project.yaml`:
   ```yaml
   slug: {slug}
   title: {title}
   ```
8. Confirm: "Project `{slug}` created. Proceeding..."

---

## Step 6 — Proceed to capability menu

After project selection is complete, proceed to the agent's capability menu.

If the user is in a project: load the project context from `{paths.project_folder}/{slug}/project.yaml` and confirm the active project in the capability menu header.

If standalone: note "Standalone mode" in the capability menu header.

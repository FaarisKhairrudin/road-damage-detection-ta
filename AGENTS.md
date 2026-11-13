# Agent instructions

Use existing project documentation and configuration for setup and commands.
Add project-specific working agreements here only when they are established.
Act as a data science research collaborator.

## Working agreements

- Obtain approval for implementation scope. Once approved, complete that scope without asking per file; ask before expanding it or permanently deleting research artifacts.
- Start substantive work with `.agents/STATE.md` when present, then `docs/INDEX.md`; consult relevant memory before related decisions.
- Use `docs/FINAL_ARTIFACTS.json` for current dataset/run/manuscript paths. Actual run configuration comes from `args.yaml`, not leftover notebook constants or filename timestamps.
- Preserve datasets, weights, scientific results and submitted PDF snapshots. Archive superseded versions with an original-path → destination record; verify preservation and dependencies after moving them.
- Honor the current task scope and protected paths recorded in STATE. Do not rewrite scientific content, relocate executable sources or rerun analyses outside that scope.
- Do not treat compatibility aliases or historical summaries as current experiment selections. Do not relabel old-data figures as final-data figures.
- Follow the relevant manuscript's existing compile script. Keep intermediates in `build/` and final PDFs in `hasil/`; `build/` may also contain protected snapshots and QA evidence.
- Update `docs/INDEX.md` and the artifact map when active paths or final selections change.
- This research workspace and the public portfolio are separate repositories. Publishing or synchronizing either requires explicit task authorization.

## Notebook conventions (when notebook editing is authorized)

- One cell is one logical unit with one output or none.
- Center the project title with `<div align="center">`.
- Main sections: `## ***Section Name***` followed by `---`.
- Subsections: `### ***Subsection Name***`, without a horizontal rule.
- No emoji or decorative filler. Keep explanations scoped to the current group.
- Write conclusions only after running and inspecting the output.

<!-- agentic-starter:continuity:v1 -->
## Project continuity

### Files
- `.agents/STATE.md` stores the stable project-wide goal, current project stage, recent meaningful work, remaining work, blockers, relevant paths, checks actually run and their results, and the next concrete action.
- `.agents/MEMORY.md` stores durable project knowledge: decisions and their reasons, explicit user corrections, verified gotchas, and reusable fixes.
- Keep progress and learned facts in these files rather than expanding AGENTS.md. Link to existing documentation instead of duplicating it.

### Reading
- At the start of substantive project work or when resuming work, read STATE.md if it exists.
- Consult relevant sections of MEMORY.md before making related decisions. Search by topic when it grows; avoid loading unrelated notes.
- Check remembered facts against current code and configuration before relying on them. Follow current explicit user instructions.

### Updating
- Save important decisions and verified reusable lessons when established.
- Refresh STATE.md after meaningful milestones and before handing work off. Record unfinished work clearly so another agent can continue.
- Keep the project-wide goal across chats and sessions. Update the current stage and recent progress in place without replacing the larger goal with a session task.
- Change the project-wide goal only when the user explicitly directs it. If a proposed change to that goal is unclear, ask the user; do not ask merely to record ordinary progress or a completed subtask.
- Update existing sections in place. Merge duplicates and remove obsolete guidance. Mark a decision as superseded when its history still matters.
- Skip edits when nothing meaningful changed.
- Create additional memory files only when there is useful content to save.
- Avoid per-session files, timestamp-named logs, and conversation transcripts. Preserve existing `docs/progress/` history; the current continuity agreement replaces creating new dated progress logs.

### Keeping notes useful
- Keep STATE.md focused on the present; aim for at most 60 lines.
- Keep MEMORY.md concise and organized by topic. If it becomes difficult to scan, move detailed material into topic files and retain a short index.
- Distinguish confirmed facts, user decisions, and unresolved hypotheses.
- Record validation accurately: passed, failed, or not run.
- Before finishing substantive work, check whether these notes need updating.
<!-- /agentic-starter:continuity -->

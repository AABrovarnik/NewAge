# GitHub handoff

The current workspace has no usable git repository or remote (`.git` is read-only and contains no repository metadata). After attaching the intended repository, publish with:

```bash
git add plugins/personal-ai-chief-architect Posts/personal-ai-chief-architect.md
git commit -m "Add personal AI chief architect plugin"
git push -u origin HEAD
```

Before pushing, run:

```bash
python3 plugins/personal-ai-chief-architect/scripts/preflight.py
python3 /root/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/personal-ai-chief-architect
```

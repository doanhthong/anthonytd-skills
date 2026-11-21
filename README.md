# anthonytd-skills

Agent skills I use daily. Install all of them or pick one.

## Skills

| Skill | What it does |
|-------|--------------|
| [writing-style](skills/writing-style/SKILL.md) | Write, rewrite, or review prose: conclusion first, short sentences, why → what → how → details. |
| [herdr-agent-team](skills/herdr-agent-team/SKILL.md) | Orchestrate builder + reviewer agents in Herdr panes, milestone by milestone. Streamline or multi-worktree. |
| [serve-markdown](skills/serve-markdown/SKILL.md) | Serve a markdown file or folder to your Tailscale devices. Rendered, live reload. |

## Install

**Any agent (Claude Code, Cursor, Codex, etc.)** via [skills.sh](https://skills.sh):

```bash
npx skills add doanhthong/anthonytd-skills                        # all skills
npx skills add doanhthong/anthonytd-skills --skill writing-style  # one skill
```

**Claude Code plugin** (installs all skills):

```
/plugin marketplace add doanhthong/anthonytd-skills
/plugin install anthonytd-skills@anthonytd-skills
```

**Manual:**

```bash
git clone https://github.com/doanhthong/anthonytd-skills.git
ln -s "$PWD/anthonytd-skills/skills/writing-style" ~/.claude/skills/writing-style
```

## Add a skill

1. Create `skills/<name>/SKILL.md` with `name` and `description` frontmatter.
2. Add a row to the table above.

## Make it yours

Fork it. Edit any `SKILL.md`. Install from your fork.

## License

MIT

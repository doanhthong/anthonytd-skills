---
name: writing-style
description: Write, rewrite, or review prose in a concise, scannable, top-down style — conclusion first, short sentences, strict abstraction ladder (why → what → how → details), concrete examples, one term per concept. Use whenever writing or rewriting docs, specs, PRDs, READMEs, emails, Slack messages, summaries, reports, or any prose meant for people to read. Also use to review writing — "review this doc", "give feedback on my writing", "is this clear?" — and when the user asks to "make this concise", "tighten this", "apply my writing style", or invokes /writing-style.
---

# Writing Style

Write so the reader gets the point in 5 seconds and the details only if they want them.

## The rules

| # | Rule | In one line |
|---|------|-------------|
| 1 | **Lead with what matters** | Conclusion or decision first. |
| 2 | **Progressive disclosure** | Gist at the top. Details further down. |
| 3 | **Strict abstraction ladder** | Why → what → how → details. Never mix levels. Never jump back up. |
| 4 | **Be concise** | Cut every word that adds no meaning. |
| 5 | **Short sentences** | One idea per sentence. |
| 6 | **Logical, not verbose** | State the point, then the reason. No filler, hedging, or repetition. |
| 7 | **Scannable** | Headings, bullets, and tables over long paragraphs. |
| 8 | **Concrete over abstract** | Examples, numbers, and names over vague claims. |
| 9 | **One term per concept** | Pick a word. Keep it. No synonyms. |

## How to apply

### Structure first

1. Write the conclusion as the first sentence. If the reader stops there, they still got the point.
2. Order sections down the ladder: why → what → how → details.
3. Keep each section at one level. A "how" section has no rationale. A "why" section has no steps.
4. Never return to a higher level after going lower. No "why" after "how".

### Then sentences

- One idea per sentence. Split on "and", "which", "while".
- Point first, reason second: "Use X. It cuts load time by 40%."
- Delete filler: "basically", "actually", "in order to", "it's worth noting that", "as mentioned".
- Delete hedging: "might", "perhaps", "somewhat", "arguably" — unless the uncertainty is real and matters.
- Say it once. No closing summary that repeats the opening.

### Then format

- Use a heading when a section has more than ~3 points.
- Use bullets for parallel items. Use numbered lists for sequences.
- Use a table when comparing 2+ items on 2+ attributes.
- Bold only the key term in a bullet, not whole sentences.

### Then words

- Replace vague with specific: "faster" → "2× faster", "many users" → "1,200 users", "a tool" → "dbt".
- Pick one term per concept and grep for its synonyms before finishing (e.g. "user" vs "customer" vs "client").

## Example

**Before**

> We've been thinking a lot about our onboarding process, and it seems like there might be some issues with it. Basically, a lot of new users tend to drop off fairly early, which is something we'd like to address. After looking into it, we think the main reason is that the setup step is somewhat long. So we're proposing that we could maybe split it into smaller steps, which would hopefully make things easier for customers.

**After**

> **Decision:** Split onboarding setup into 3 short steps.
>
> **Why:** 45% of new users drop off at setup. It takes ~8 minutes.
>
> **How:**
> 1. Connect data source.
> 2. Pick a template.
> 3. Invite team (optional, skippable).

What changed:

- Decision moved to line 1.
- Hedges removed ("seems like", "might", "maybe", "hopefully").
- Vague claims made concrete ("a lot" → 45%, "long" → 8 minutes).
- "users" and "customers" unified to "users".
- Why and how separated into their own sections.

## Final check

Before returning any text, verify:

- [ ] First sentence states the conclusion or decision.
- [ ] Sections go down the ladder and never back up.
- [ ] Each section stays at one abstraction level.
- [ ] No sentence carries two ideas.
- [ ] No filler, hedging, or repeated points.
- [ ] Every vague claim has a number, name, or example.
- [ ] Each concept uses one term throughout.
- [ ] A reader skimming headings and bold text gets the gist.

## When rewriting someone's text

- Keep their meaning and facts. Do not invent numbers — mark gaps as `[number?]` instead.
- Keep their voice for informal text (Slack, email). Apply structure rules lightly there.
- Return the rewrite first. List major changes after, only if asked or if meaning shifted.

## When reviewing

Point out problems. Don't rewrite the whole text.

1. **Verdict first.** One line: ready to send or needs work, plus the biggest issue.
2. **Findings table**, most severe first:

   | # | Rule | Where | Problem | Fix |
   |---|------|-------|---------|-----|
   | 1 | Lead with what matters | ¶1 | Decision buried in ¶4 | Move "We'll ship Friday" to line 1 |
   | 2 | One term per concept | §Setup, §FAQ | "workspace" and "project" mean the same thing | Use "workspace" |
   | 3 | Concrete over abstract | ¶2 | "significantly faster" | Give the number: "3× faster" |

3. Rank by severity: structure (rules 1–3), then logic (6, 9), then sentences (4–5), then format and words (7–8).
4. Quote the exact phrase so the writer can find it.
5. List at most ~10 findings. Group repeats: "Hedging ×6, e.g. 'might', 'perhaps'".

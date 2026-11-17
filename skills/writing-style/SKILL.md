---
name: writing-style
description: Write, rewrite, or review prose in a concise, scannable, top-down style — conclusion first, short sentences, strict abstraction ladder (why → what → how → details), concrete examples, one term per concept. Use whenever writing or rewriting docs, specs, PRDs, READMEs, emails, Slack messages, summaries, reports, or any prose meant for people to read. Also use to review writing — "review this doc", "give feedback on my writing", "is this clear?" — and when the user asks to "make this concise", "tighten this", "apply my writing style", or invokes /writing-style.
---

# Writing Style

## Rules

- **Be concise.** Cut every word that adds no meaning.
- **Short sentences.** One idea per sentence.
- **Scannable.** Use headings, bullets, and tables over long paragraphs.
- **Logical, not verbose.** State the point, then the reason. Skip filler, hedging, and repetition.
- **Progressive disclosure.** Reader gets the gist from the top. Details come only when they read further.
- **Strict abstraction ladder.** Go from high-level to low-level: why → what → how → details. Never mix levels in one section. Never jump back up.
- **Lead with what matters.** Put the conclusion or decision first.
- **Concrete over abstract.** Prefer examples, numbers, and names over vague claims.
- **One term per concept.** Don't switch synonyms for the same thing.

Check every output against these rules before returning it.

## Specifics

- Filler to cut: "basically", "actually", "in order to", "it's worth noting that", "as mentioned".
- Hedges to cut: "might", "perhaps", "somewhat", "arguably". Keep them only when the uncertainty is real.
- Use a table to compare 2+ items on 2+ attributes. Use numbered lists for sequences.

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
> 3. Invite team (optional).

## When rewriting

- Keep the writer's meaning and facts. Don't invent numbers. Mark gaps as `[number?]`.
- Keep the writer's voice in informal text (Slack, email).

## When reviewing

Point out problems. Don't rewrite the whole text.

1. **Verdict first.** Ready to send or needs work, plus the biggest issue.
2. **Findings table**, most severe first. Quote the exact phrase.

   | # | Rule | Where | Problem | Fix |
   |---|------|-------|---------|-----|
   | 1 | Lead with what matters | ¶1 | Decision buried in ¶4 | Move "We'll ship Friday" to line 1 |
   | 2 | One term per concept | §Setup, §FAQ | "workspace" and "project" mean the same thing | Use "workspace" |

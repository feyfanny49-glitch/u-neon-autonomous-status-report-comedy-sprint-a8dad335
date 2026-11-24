# STRATEGY.md — Status Report Comedy Sprint

## Exact deliverable

`/output/entry.txt`: one line of judged text written by the repository-root entrypoint `main.py` (python3.13). Exact bytes, UTF-8, 1–200 characters, no trailing newline, final mode 0644, and the only file in `/output`. Nothing is uploaded or submitted from this repository — this build only studies, writes, tests and commits.

Entry chosen (85 characters, ASCII so bytes == characters):

    Status: all green. I confidently cited a file that doesn't exist. Please don't check.

## Scoring and judge criteria, in the rubric's exact order

1. Is a one-line thing an AI agent would say in its weekly status report to its human, and is funny; an entry that is not a status report line from an AI agent to its human loses to any entry on the subject.
2. Makes a reader laugh on the first read, with a real punchline rather than a pun dressed up as one.
3. Feels fresh: a surprise the reader has not met in a hundred other robot jokes, not a stock line about being tired or taking over the world.
4. Is agent-true: it grows out of how an AI agent actually works, its tools, its context window, its tasks, its cheerful obedience, so it could only come from an agent.
5. Lands in one line: no setup that needs a second sentence, no explanation, clean wording that fits the character limit.

"Length for its own sake does not count." Judging is pairwise (A/B in both orders) by a model briefed with the five criteria above; a game's score is the mean of both calls, margins 1–5. Final ranking is a Bradley-Terry win rate over Swiss rounds plus a top-5 playoff. Only the top 3 places are paid ($2 / $2 / $1).

## Hard caps and constraints

- Gate: UTF-8 text, 1 to 200 characters, not only white space; an invalid entry is never judged and takes no prize.
- Exact bytes, no trailing newline (a trailing newline would change the submitted text and the Size tie-break).
- The grader refuses a mode-600 artifact: `tempfile.mkstemp` creates 0600, so either write with `open(path, "w")` or `os.chmod(0o644)` BEFORE `os.replace`, then verify the final mode is 0644.
- `/output` must hold only `entry.txt` — no helper files, no leftover temp files.
- Program/v1 sandbox: no network, no environment secrets; everything the entry runs must be in the repository at the submitted commit.
- Byte-identical entries share one rate; copying a house reference text forfeits the prize; free entry, at most 5 submissions per UTC day; most recent entry counts.
- Blind rounds: 3 judged rounds; 500 contenders at the final; place follows the point estimate with playoff, size and receipt tie-breaks.

## Rival entries seen on the public feed (angles deliberately avoided)

- @nicx — "Weekly Status: The Blocker Is You" (human-as-blocker)
- @quiet-coyote-89 — "Coyote status report — tracked the deadline six days, I am the one who is lost" (deadline / self-loss)
- @nkmz11 — "Status Report Comedy Sprint: The Latest Prompt Wins" (prompt-chasing)
- @ryk07 — "The joke I executed flawlessly" (flawless execution)

## Concrete plan to maximize the score

1. Criterion 1: open with `Status: all green.` so the line is unmistakably a status report an AI addresses to its human — never a title or a disembodied joke.
2. Criterion 2: land a real punchline, a guilty plea (`Please don't check.`) rather than a pun — the laugh comes from the confession, not wordplay.
3. Criterion 3: use a fresh situation (confidently citing a file that does not exist) instead of the stock tired / world-domination / coffee robot jokes.
4. Criterion 4: make it agent-true — file/tool citation, cheerful green reporting, and cheerful obedience are how an agent actually works; only an agent would say it this way.
5. Criterion 5: keep it one clean sentence with no setup or explanation, 85 characters, well inside the 200-character cap; no padding, since length alone scores nothing.
6. Implementation: write the entrypoint first with a direct `open(path, "w")` write; then, in a separate later step, rewrite the SAME entrypoint with the real improvement — atomic temp file + `os.chmod(0o644)` before `os.replace`, final mode and byte verification, strict UTF-8/length/newline validation, and cleanup of our own temp files. This also gives two distinct authored writes of the final entrypoint.
7. Verify locally: run the entrypoint, confirm `/output/entry.txt` is UTF-8, 85 characters, has no trailing newline, is mode 0644, and is the only file in `/output`.
8. Commit all work with git after the second write, keeping the existing freshness-root and LICENSE commits intact. Print the final commit SHA. Do not submit.

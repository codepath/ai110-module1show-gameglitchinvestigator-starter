# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case                        | Prompt Used                                                                            | AI-Suggested Test                                                                                                                                                                                                                                                                                    | Did It Pass? | Your Reasoning                                                                                                                                                                                                                                                                  |
| -------------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Out-of-range / negative inputs   | "can you walk me through tackling edge case negative number and score can go negative" | `test_parse_guess_rejects_out_of_range` — parametrized over `"0"`, `"-5"`, `"21"`, `"1000"` on Easy (1–20); asserts `ok is False`, `value is None`, and the error names the range. Paired with `test_parse_guess_accepts_in_range_including_bounds` to confirm the bounds (`1`, `20`) are inclusive. | Yes (29/29)  | `parse_guess` only checked "is this a number?", so `-5` and `1000` were accepted as valid guesses. We added `low`/`high` parameters and an out-of-range branch. The test pins both the rejection _and_ the inclusive boundaries so a future off-by-one (`<` vs `<=`) is caught. |
| Non-numeric input must not crash | (same conversation — flagged while reviewing my first attempt)                         | `test_parse_guess_still_rejects_non_numbers_without_crashing` — `parse_guess("abc", 1, 100)` must return `(False, None, "That is not a number.")`, not raise.                                                                                                                                        | Yes          | My first attempt put `int(raw) < 1` _before_ the `try/except`, which crashed on `"abc"`. The AI caught the ordering bug: range-check must run _after_ the parse succeeds. This test guards against that exact regression.                                                       |
| Score going negative             | "can you walk me through tackling edge case negative number and score can go negative" | `test_wrong_guess_does_not_push_score_below_zero` and `test_wrong_guess_clamps_low_score_to_zero` — `update_score(0, "Too Low", 3) == 0` and `update_score(3, "Too Low", 2) == 0`.                                                                                                                   | Yes          | Wins were floored at 10, but wrong guesses had no floor, so a bad run produced a negative score. We wrapped the deduction in `max(0, current_score - 5)`. The tests check both the at-zero case and a low-positive case that would otherwise go negative.                       |

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
You are a Python expert. I want you to write professional grade docstrings to every function in logic_utils.py.
Now review the code for PEP 8 style compliance
```

**Linting output before:**

```
logic_utils.py:1:0: C0114: Missing module docstring (missing-module-docstring)
logic_utils.py:67:11: W0718: Catching too general exception Exception (broad-exception-caught)
logic_utils.py:143:8: R1731: Consider using 'points = max(points, 10)' instead of unnecessary if block (consider-using-max-builtin)
```

**Changes applied:**

- **C0114** — Added a module-level docstring at the top of the file.
- **W0718** — Replaced `except Exception` with `except (ValueError, TypeError)`, the only two errors `int()` and `float()` can actually raise on bad input.
- **R1731** — Collapsed the two-line `if points < 10: points = 10` block into `max(10, ...)` inline.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

|                          | Model A                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Model B                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Model name**           | Claude                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Copilot                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Response summary**     | The first fix was storing the current difficulty in session state and detecting when it changed, so switching difficulty automatically resets the secret number and game state rather than waiting for an explicit New Game click. The second fix was ensuring the New Game button handler runs before any st.stop() call, so the reset logic isn't swallowed when the game is in a won/lost state. Together, these changes mean the game always respects the player's chosen difficulty and the New Game button reliably works from any game state. | The st.stop() call executed before the "New Game" button could work, trapping users after a win/loss. Fix: Move the game-over status check after the "New Game" button logic so users can reset the game and change difficulty. Bug #2: The hints were wrong because the code compared strings lexicographically (e.g., "9" > "10" = True) instead of numerically. Fix: Convert both guess and secret to int before comparison in check_guess(). |
| **More Pythonic?**       | No                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Yes                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **Clearer explanation?** | Yes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | No                                                                                                                                                                                                                                                                                                                                                                                                                                               |

**Which did you prefer and why?**

> I prefer Claude's response because it walk me through the bug and solution using simple explanation

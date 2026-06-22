# AI Interactions Log

---

## Agent Workflow (SF8)

**What task did you give the agent?**

I asked Claude (claude-sonnet-4-6) to: "Move the check_guess, parse_guess, update_score, and get_range_for_difficulty functions into logic_utils.py, fix the inverted hint bug and the string/int type-switch bug in the process, and update app.py to import from logic_utils."

**What did the agent do?**

1. Read both `app.py` and `logic_utils.py` to understand the existing (broken) implementations.
2. Wrote correct implementations of all four functions into `logic_utils.py`, fixing:
   - `check_guess`: inverted hint messages (returning correct "Too High"/"Too Low" labels)
   - `update_score`: removed points-on-wrong-guess logic; only Win awards points
   - `get_range_for_difficulty`: fixed Hard range from 1–50 to 1–200
3. Rewrote `app.py` to import from `logic_utils`, removed the string/int cast on even attempts, fixed attempts init to 0, and fixed the New Game button to reset all state.
4. Added 12 edge-case tests in `tests/test_game_logic.py` covering `parse_guess`, `update_score`, and difficulty ranges.

**What did you have to verify or fix manually?**

- Verified the test assertions matched the intended game semantics (e.g., score floor of 10, not 0).
- Confirmed the `HINT_MESSAGES` dict in `app.py` matched the outcome strings returned by `check_guess` exactly.
- Checked that the `test_score_win_first_attempt` expected value (90) matched the formula `max(10, 100 - 10 * 1) = 90` — the agent computed this correctly.

---

## Test Generation (SF7)

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Non-numeric string input | "Generate edge-case tests for parse_guess covering inputs a user might accidentally type" | `assert parse_guess("abc") == (False, None, "That is not a number.")` | Yes | Players might type words; the function must reject them cleanly |
| Empty string | Same prompt | `assert parse_guess("") == (False, None, "Enter a guess.")` | Yes | Clicking Submit without typing is a common mistake |
| Negative number | Same prompt | `ok, val, err = parse_guess("-5"); assert ok and val == -5` | Yes | Negative numbers are valid integers even if out of game range; parser should accept them |
| Float string "42.9" | Same prompt | `ok, val, err = parse_guess("42.9"); assert ok and val == 42` | Yes | Players might type decimals; the function truncates to int |
| None input | Same prompt | `ok, val, err = parse_guess(None); assert ok is False` | Yes | Defensive: session_state could theoretically deliver None |
| Score unchanged on wrong guess | "Generate tests verifying score behavior on non-win outcomes" | `assert update_score(0, "Too High", 1) == 0` | Yes | Core fix verification: wrong guesses must not change score |
| Score floor clamped at 10 | Same prompt | `assert update_score(0, "Win", 20) == 10` | Yes | Late wins should still award minimum points, not go negative |
| Hard harder than Normal | "Test that difficulty ranges are ordered correctly" | `assert get_range_for_difficulty("Hard")[1] > get_range_for_difficulty("Normal")[1]` | Yes | Sanity check for the difficulty bug fix |

---

## Linting & Style (SF9)

**Prompt used:**

```
Review logic_utils.py for PEP 8 compliance and add professional docstrings to all functions.
Each docstring should explain parameters, return values, and note any bug that was fixed.
```

**Linting output before:**

```
app.py:158:9: E501 line too long (the string-cast conditional was long)
logic_utils.py: all functions raised NotImplementedError — no style to lint
```

**Changes applied:**

- Added docstrings to all four functions in `logic_utils.py` documenting params, return type, and the specific bug each function fixes.
- Kept lines under 79 characters throughout both files.
- Renamed the inline `except Exception` to `except (ValueError, TypeError)` for specificity — the AI suggested this as more Pythonic and it makes the error handling intent clearer.
- Replaced scattered inline hint strings in `app.py` with a `HINT_MESSAGES` dict (AI suggestion accepted — cleaner than repeating strings).

---

## Model Comparison (SF11)

**Task given to both models:**

"Explain why `check_guess(60, 50)` returns 'Too High' but the original app.py showed the message 'Go HIGHER!' — what is the bug and how do you fix it?"

| | Model A | Model B |
|-|---------|---------|
| **Model name** | Claude Sonnet 4.6 | Claude Sonnet 4.6 (second session, cold context) |
| **Response summary** | Identified that the outcome label ("Too High") was correct but the display message string was wrong — suggested separating outcome from message into a lookup dict | Suggested the entire `check_guess` conditional was inverted and recommended swapping `>` to `<` — which would have broken the outcome labels |
| **More Pythonic?** | Yes — lookup dict is cleaner than inline strings | No — the suggested swap would have created new bugs |
| **Clearer explanation?** | Yes — correctly identified the data/display separation issue | Less accurate — confused the label with the message string |

**Which did you prefer and why?**

The first session's response was more accurate because it had the full file context attached. The second session (cold context) only saw the `check_guess` function in isolation and made an incorrect inference. This confirms that providing the AI with full file context produces significantly better suggestions — a lesson worth remembering for future projects.

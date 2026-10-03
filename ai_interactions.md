# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->
i told the ai to make the scoring logic so that there is a bit of uncertainty and risk when you guess you may gain 4 points or lose 10 or 5 points depending on the attempt number and the feedback(too low, too high)

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->
it did that but then it also added or subtracted from the final score

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->
i had to check the win and loss it added the 10 point bonus on a win and subtracted ot added 4, -5 or -10 from the loss 

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

i asked ai to add test after each refactor then i checked the test then ran it till it was 100%
| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Win condition | "add a test for a correct secret match" | `check_guess(50, 50) == "Win"` | Yes | This checks the core game comparison before scoring is applied. |
| Too high guess | "add a test for a high guess" | `check_guess(60, 50) == "Too High"` | Yes | This makes sure the hint direction matches the real relationship between guess and secret. |
| Too low guess | "add a test for a low guess" | `check_guess(40, 50) == "Too Low"` | Yes | This prevents the game from giving the wrong direction message on lower guesses. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
check the Python code for any obvious cleanup, duplicate logic, and unclear naming, but keep the game rules the same
```

**Linting output before:**

```
there were a few repeated conditions and some unclear variable names in the score and attempt logic
```

**Changes applied:**

I used the suggestion to tighten up the logic and remove some repeated checks. I kept the parts that matched the rules we wanted and ignored the ones that changed the game behaviour. Most of the clean-up was small, but it made the final logic easier to follow and easier to test.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

I asked both models to help me fix the scoring and win/loss logic and explain why the game was behaving inconsistently.

| | Model A | Model B |
|-|---------|---------|
| **Model name** | Copilot | Claude |
| **Response summary** | It was more direct and focused on the actual bug in the score logic. | It gave a broader explanation and a few extra ideas, but it was less precise on the game rules. |
| **More Pythonic?** | Yes, it suggested a cleaner fix that was easier to test. | Somewhat, but it was a bit more verbose. |
| **Clearer explanation?** | Yes, it explained the issue in a way that matched the rules we wanted. | It was clear, but not as focused on the exact problem. |

**Which did you prefer and why?**

I preferred Copilot because it was quicker and more practical. It gave a fix I could check against the game logic without having to sort through a lot of extra explanation.

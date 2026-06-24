# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to create a visualization system in which the user could see its attempts in the line of numbers (from 0 to 100). Each attempt was to be marked with a star and updated right after the submission was made.


**What did the agent do?**
1. Read app.py
2. Add the visualization bar
3. Suggest code modification
4. Modify the code (after being approved)
5. Verify the accuracy of the code added

**What did you have to verify or fix manually?**
- I reviewed whether the functionality was right, the stars were located in teh right places and were accumlated as the user kept playing. 
- When double checking values that could create issues (the endpoints of the range: 0 & 100) I realized the stars weren't working correclty and troubleshooted this issue so it worked nicely.
---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case        | Prompt Used  |         AI-Suggested Test        | Did It Pass? | Your Reasoning    |
|------------------|--------------|----------------------------------|--------------|-------------------|
| Negative Numbers |shared prompt |test_negative_decimal_rejected()  | Yes          | Out of range      | 
| No input         |shared prompt |test_empty_input_rejected()       | Yes          | There's no guess  |       
| Decimal Values   |shared prompt |test_decimal_input_rejected()     | Yes          | They aren't whole |
| numbers < 100    |shared prompt |test_number_above_100_is_invalid()| Yes          | Out of range      | 
| Text             |shared prompt |test_text_input_rejected()        | Yes          | Not a valid guess |
---------------------------------------------------------------------------------------------------------
Prompt:
```
Create a separate suite of tests for the edge cases of the guessing game, you can read the following files for the full context -> @app.py  @logic_utils.py .
The edge cases I could find are: negative numbers, no input, decimal values, text or numbers greater tha 100. Let me know if you can detect another edge case that I missed.  Again, ensure EACH edge case has THEIR OWN test
```

Further Notes:
```
    Since the prompt wasn't specific in terms of which test wanted to be conducted, the AI agent automatically decided to test EVERY function/step in teh process, from parsing to checking the values. I found that to be helpfull (and acknowledge it was a missed thought from the developer side, since we should test every function in the system works perfectly). In my opinion, it wasw a good example of why we can learn and assist our thinking with AI agents - but not rely too heavily on them as to not realize the faults we make and hence not learn from them. 
```
## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->

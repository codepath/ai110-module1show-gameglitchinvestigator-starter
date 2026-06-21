# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

I entered a guess of 50. The hint was "Go HIGHER", then I entered 100 and it kept hinting "Go HIGHER"

Then I clicked new game and my previous guess remained in the "Enter your guess" text box.

New game, started at 40 and kept hinting "Go Lower" until I hit 1. Cannot go any lower than 1. The actual value was 73.

After winning a game. The game did not respond when playing hard

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| guess of 100| hint: go higher | hint: go lower  |"None" |
| guess of 1| hint: go lower | hint: go higher | "None"|
| Click on New Game after winning| Creates a clean new game | Game does not react to input guess|"None" |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude Code in agent mode.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
AI got it right with the inverted hints. The AI suggested the following:
if guess > secret:
    return "Too High", "📉 Go LOWER!"
else:
    return "Too Low", "📈 Go HIGHER!"

This bug is pretty straight forward. I knew by looking at it that it was swaped. 


- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
The AI suggested the following:
if new_game:
    st.session_state.attempts = 0   # ← BUG: first submit increments to 1, but
                                    #   the game starts counting from attempt 1

During implementation I selected the attempts = 0 line to double check that needed to be fix. Ended up that the fix or reset had to happen elsewhere in the codebase.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

Even though I ran a few tests, I made sure I tested the app myself and attempted the inital test bugs against my documented fixes.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  I tested the app by entering a number higher than the correct guess and it return the corrrect output: Go Lower.

  Also, tested the app by enterign a number lower than the correct guess and it return the correct output: Go Higher.

  Lastly, I fixed the new game feature after winning a game. 

- Did AI help you design or understand any tests? How?
Basically AI did all the pytest work. I am unfamiliar with this at this moment so I went ahead and did it manually.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Imagine you have a magic whiteboard that erases itself every time someone touches it.
Every button click, every keypress — the whole whiteboard gets wiped clean and redrawn from scratch. That's Streamlit. Your Python script is the instructions for redrawing the whiteboard.
The problem is obvious: if you write "count = 5" on the whiteboard, then someone clicks a button, the board erases, redraws, and "count = 5" is gone. Back to zero.
session_state is basically a sticky note on the side of the whiteboard that doesn't get erased. You write important stuff there — the score, whose turn it is, what the secret number is — and it survives every erase-and-redraw cycle.
So the golden rule is simple: anything your app needs to remember goes on the sticky note. Anything you can just recalculate from scratch each time can live on the whiteboard.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

I'd like to keep up the habit of documenting my prompts and the AI response. Also, tripple checking AI's output. 

- What is one thing you would do differently next time you work with AI on a coding task?

Use a new chat for every issue/bug
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I've felt as cheating when using AI to help me code. This project helped me ease into AI generated code and treat it as a suggestion not a definitive. Reminder that I am the lead programmer when working with AI.

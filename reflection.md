# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
at first it looked fine till you entered an atttempt and it still said attempt 0 and it said go lower till i reached 0 which is the lowest it can go and then it told me the secret was 65 which i was always lower than 
- List at least two concrete bugs you noticed at the start  
1. at the end the of a win or loss the current score was not the final score because there was a lag in attempts it would only reflect it after one additional attempt after a win 2. the hints were backwards saying go lower when you were already "too low" 3. the initial code was zero based in the sense that it made you do the first attemot twice before it moved forward
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret is 65; user guesses 90 and then 100 on later submits | The secret should stay fixed at 65 while each guess is compared against it | The app alternates the secret between an integer and a string, so the comparison is inconsistent and the hint logic appears to change the answer | `if st.session_state.attempts % 2 == 0: secret = str(st.session_state.secret)` causes mixed-type comparisons before `check_guess` runs |
| User clicks “New Game” after a win or loss | The game should reset to a fresh round and allow play again | The button appears to do nothing because the game status is not reset, and the old lock state keeps the app from restarting properly | `if new_game: st.session_state.attempts = 0; st.session_state.secret = random.randint(1, 100)` does not reset `st.session_state.status` or the history/score state, so the app continues to stop on the previous game state |
| Guess 15 when the secret is 38 | A lower guess should say “Go HIGHER!” because 15 is below the secret | The app says “Go LOWER!” even though the actual value is lower than the secret, so the direction message is reversed | The message mapping in the app is reversed: `Too Low` is mapped to `"📉 Go LOWER!"` instead of `"📈 Go HIGHER!"` |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Copilot
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
the hint logic was backwards telling the user to "GO HIGHER" instread of "GO LOWER"
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
ai suggested removing the logic that if the attempt was too high and even then i add 5 points and if it was odd, too high subtract 5 points and if it was too low remove 5 points, it wanted me to make it so it just removed 5 points, but i wanted to add a gamble if its odd and too low you either gain 4 points or lose 10 and if its even and too high you either gain 4 points or lose 10 points but if its odd and too high you lose 5 points and, if its even and too low you lose 5 points this way you can choose do i lose 5 points or possibly gain 2 points or lose 10 points because you know whether your attempt is even or odd
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
i played the game and observed the behavior
- Describe at least one test you ran (manual or using pytest)
i checked whether it would help narrow down my guess with a trial guess which it didnt at first on the first guess attempt in then it did it on the second which told me there was a lag in the attempts so i fixed that
  and what it showed you about your code.
  it showed the code was lagging behind in attempts on the ui
- Did AI help you design or understand any tests? How?
it helped me understand it by showing me how the check logic works the scoring logic and the display logic
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
i would say streamlit is like a app where you create an app using its already made functions in python

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
testing my code and re-running till i get a desired output and making a program as useable and understandable as possible 
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
in order to not waste tokens ill do multiple tests like a spiral model for testing before i ask ai for a fix or an explanation
- In one or two sentences, describe how this project changed the way you think about AI generated code.
 ai can make a lot of mistakes and a lot of misunderstandings so it is best to be clear
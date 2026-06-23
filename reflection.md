# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
I started the game in normal mode. I saw that on the main page, it said that you had 7 attempts left, but on the side settings, it said I had 8 attempts. I got lucky the first time and guessed correctly. The secret number was 1.
- List at least two concrete bugs you noticed at the start  
*The "New Game" button does not work, the game gets stuck after you win. I had to restart the page to play again.
*Pressing the Enter key did not submit a guess, even though the submission box says, "Press Enter to apply." You had to click the "Submit Guess" button to enter the guess.
*You start with the value of attempts set to 1.
*You have to press the "Submit Guess" button twice to get a hint about your guess. Sometimes it would skip adding the guessed number completely if you did not press the "Submit Guess" button twice.
*The hints were wrong, sometimes telling me to go higher when the target number was way lower. (ex: target number is 35, I input 50, the hints say to go higher.)
*The "New Game" button only works when you have not lost/win the game.
It still adds an input that is not an integer when you submit your guess.
*Stores String inputs regardless.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|  70   | "Go lower"        |   "Go higher"   |   None
|  50   | "Go higher"       |   "Go lower"    |   "0":"70"
| hello | "This is not      | "This is not a  |  "1" : "50"  
|       |  a number" / Does |  number."       |
|       | not store the value|                |
|  30   |  "Go lower"       |   No message.   |   "2":"hello"
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

I started the game in normal mode. One of the suggestions was to switch the "🔽 Go LOWER!" and "🔼 Go HIGHER!" messages in check_guess. This is what the AI suggested:

      If your guess is too high, you should go LOWER, not higher. The two messages are simply reversed. The fix is to swap them:

      if guess > secret:

          return "Too High", "🔽 Go LOWER!"

      else:

          return "Too Low", "🔼 Go HIGHER!"

 What was happening was that if you guessed 50 and the target was 35, you would get a message that said "Go Higher" instead of "Go Lower". After switching the message, I input the same value again, and the message matched the behavior.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
One suggestion that was misleading had to do with the submission button sometimes doing nothing (showing no message) when you input an answer. The AI suggested this:

        if show_hint:

            st.warning(message)

        else:

            st.info("Guess submitted.")

I found this a little misleading since it did not target the actual issue; the "Guess submitted" message doesn't really give a lot of context for what the target number is.



---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I decided it was fixed when different inputs still gave the expected output.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
I ran the tests that were checked by AI for def test_hint_direction_is_correct(): and def test_parse_guess_only_accepts_integers(): and it showed that the tests were successful. I manually inputed the values as well to double check and the expected behavior was the same.
- Did AI help you design or understand any tests? How?
AI helped me understand how to run tests using pytest. Since I was not familiar with it before, it told me which commands to run when executing the file and how to check whether the logic I was using for the test was actually useful. I originally wrote a less detailed test for test_parse_guess_only_accepts_integers(), but then the AI showed me that I actually have to test for other input values, like strings.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit session state is when we run the app in our browser, and "reruns" refers to the app's script running again from top to bottom every time we interact with the app.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
I want to keep using plan mode when consulting the AI, I feel like that way I'm able to make better edits and have more control of what is being generated.
- What is one thing you would do differently next time you work with AI on a coding task?
I would like to write better prompts that are easier for the AI to execute, maybe use a different prompting format that is faster to interpret.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I used to think that a lot of the time, the generated code would not work correctly, but the quality of the prompt greatly affects the result. Even when I think I have a decent prompt, there is always a way to optimize.
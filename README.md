# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

The game was a basic guess the number game where the user had to guess a secret number in a certain number of attempts. 
Here are the bugs found  and their fixes.    
    57 -  - Fix: move the status check (and st.stop()) to before the guess U
                                                                
      -  12. Invalid guesses consume attempts but cannot trigger game over 
         -(app.py:88-124)                                                     
      61 -  - st.session_state.attempts is incremented (line 89) before parse_
         -guess is                                                            
      62 -  called. If the guess is invalid, the attempt is used up but the ga
         -me-over                                                             
      63 -  check (lines 117-124) is inside the else block and never runs.    
      64 -  - A player who submits only invalid input can exhaust all attempts
         - and the                                                            
      65 -  game will never transition to "lost".                             
       3   No newline at end of file
       4 +(none - all resolved)                                               



  Bug 11 — Guess UI shown when game is already over (app.py)
  The st.info counter, text input, and buttons all rendered before the status !=
  "playing" check. When a player lost/won, st.stop() would fire but those UI elements
   were already on screen — showing a stale "Attempts left: 1" counter alongside the
  game-over message. Fix: moved the New Game button above the status check so it's
  always accessible, then moved st.stop() before the guess UI so the input/counter
  never render when the game is over.

  Bug 12 — Invalid guesses exhaust attempts without triggering game over (app.py)
  st.session_state.attempts += 1 ran before parse_guess, but the game-over check was
  inside the else block (only reached for valid guesses). A player submitting garbage
   input could burn through all attempts and the game would never transition to
  "lost". Fix: moved the game-over check outside the else block so it runs after


## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]
Please see the screenshot in the root directory

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]

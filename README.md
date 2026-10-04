# 🛡️ Cyber Awareness Challenge

A dark-themed quiz web app that teaches everyday cyber security: phishing, scams, passwords, and safe browsing. Every attempt gives you 5 fresh questions from a bank of 35, and every answer comes with a short explanation.

## Screenshots
| Home | Quiz | Result |
|------|------|--------|
| <img width="1520" height="897" alt="image" src="https://github.com/user-attachments/assets/97e0e5c0-7fbf-4847-9ac6-563e10c581d7" />
 | <img width="1490" height="915" alt="image" src="https://github.com/user-attachments/assets/fff6c36e-b2cc-4a3b-ab8d-3e80ae6f3442" />
 | <img width="1482" height="892" alt="image" src="https://github.com/user-attachments/assets/29055827-9da6-48ed-9ce2-2bc0f448b0fe" />
 |

## Features
- **Animated front page** with a hacker-terminal intro
- **35-question bank**, 5 questions per attempt
- **No repeats until the bank is used up.** You get 7 different sets, then a new shuffled round starts
- **Instant review** after every attempt: your answer, the correct answer, and a short explanation
- **Rank system** from "Phishing Bait" to "Cyber Guardian", shown with glowing shields
- **Confetti** for a perfect score
- **Dark neon design** that works on desktop and mobile

## Topics covered
Phishing, smishing, and spear phishing, fake OTP and UPI scams, fake job offers, passwords and password managers, 2FA and MFA fatigue, safe downloads, public Wi-Fi and VPNs, ransomware and keyloggers, social engineering, and basic attacks like SQL injection, DDoS, and man-in-the-middle.

## How it works
1. The app picks 5 questions that have not been used yet in the current round.
2. It remembers which ones you have seen in a signed session cookie.
3. When you submit, the server grades your answers and shows the review.
4. When all 35 questions have been used, a new round starts.

## Security notes
- **Correct answers never leave the server.** The quiz page contains only the questions and options.
- **The server decides which questions are graded.** It uses the set stored in your session, not anything the browser sends.
- **Input is validated.** Submitted answers that are not valid option numbers are ignored.
- **Signed session cookie** with `SameSite=Lax`. The secret key is generated when the app starts, so no secret is stored in the code. You can set a fixed key with the `SECRET_KEY` environment variable.
- **Flask escapes template output automatically**, which helps prevent cross-site scripting.
- Python's `random` is used for picking questions because it is not security-sensitive. Anything that protects a secret uses `secrets`.

## Limitations
- There are no user accounts and no saved score history.
- Progress is tied to the browser session and resets when the server restarts.
- The questions are stored in `app.py`, so adding questions means editing the code.
- The rank is based on only 5 questions, so it is just for fun.
- It runs on Flask's development server and is not meant for production.

## Tech stack
Python, Flask, Jinja2, HTML, CSS, and a little JavaScript (confetti).

## Project structure
```
quizz_app/
    app.py
    requirements.txt
    README.md
    static/
        style.css
    templates/
        start.html
        index.html
        result.html
```

## How to run (Windows)
```
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```
Then open http://127.0.0.1:5002 in your browser.

## Future improvements
- Question categories and difficulty levels
- A timer for each attempt
- Load questions from a JSON file or a database
- User accounts with score history and a leaderboard
- More questions and regular updates

import os
import random
import secrets

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

# The secret key signs the session cookie so it cannot be edited.
# It is created when the app starts, so no secret is stored in the code.
# To keep one fixed key, set a SECRET_KEY environment variable.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

QUESTIONS_PER_QUIZ = 5

# "answer" is the position of the correct option, starting from 0
QUESTIONS = [
    {
        "question": "What is the biggest warning sign of a phishing email?",
        "options": [
            "It has a company logo",
            "It creates urgency, like 'Act in 24 hours or your account will be closed'",
            "It was sent in the morning",
            "It greets you by name",
        ],
        "answer": 1,
        "explanation": "Attackers create panic so you act before you think. Logos and names are easy to copy or find online.",
    },
    {
        "question": "You get an SMS from your 'bank' with a link to verify your account. What should you do?",
        "options": [
            "Click the link quickly to avoid account closure",
            "Reply with your card details",
            "Don't click it. Open the bank's official app or website yourself, or call the bank",
            "Forward it to your friends",
        ],
        "answer": 2,
        "explanation": "Links in unexpected messages can lead to fake sites. Always go to the official app or website yourself.",
    },
    {
        "question": "Which password is the best choice?",
        "options": [
            "A short password with your name",
            "Your birth date",
            "The same password for every account",
            "A long password that is unique for each account",
        ],
        "answer": 3,
        "explanation": "Length makes a password harder to guess, and using a different one per account means one leak cannot open all your accounts.",
    },
    {
        "question": "What is two-factor authentication (2FA)?",
        "options": [
            "A second proof of identity, like a code sent to your phone, in addition to your password",
            "Using two different passwords for one account",
            "Logging in twice a day",
            "Running two antivirus programs",
        ],
        "answer": 0,
        "explanation": "Even if someone steals your password, they still need the second factor to get in.",
    },
    {
        "question": "Someone calls saying they are from your bank and asks for the OTP you just received. What do you do?",
        "options": [
            "Share it, since they are from the bank",
            "Never share it. Hang up and call the bank on its official number",
            "Share only half of it",
            "Ask them to send it by SMS first",
        ],
        "answer": 1,
        "explanation": "Banks never ask for your OTP. Anyone who asks for it is trying to steal from you.",
    },
    {
        "question": "What does the padlock (HTTPS) in the browser address bar mean?",
        "options": [
            "The website is 100% safe and trustworthy",
            "The website is owned by the government",
            "The website has no advertisements",
            "The connection is encrypted, but the site itself could still be fake",
        ],
        "answer": 3,
        "explanation": "HTTPS protects the data in transit. Phishing sites can use HTTPS too, so always check the domain name.",
    },
    {
        "question": "Which link looks the most suspicious?",
        "options": [
            "https://www.amazon.in/orders",
            "https://support.google.com",
            "https://amazon.in.account-verify.xyz/login",
            "https://www.irctc.co.in",
        ],
        "answer": 2,
        "explanation": "The real domain is the part just before the first single slash. Here it is account-verify.xyz. The text amazon.in is only a subdomain, a trick to fool you.",
    },
    {
        "question": "Why is public Wi-Fi risky?",
        "options": [
            "Other people on the network may spy on your traffic, or you may connect to a fake hotspot",
            "It always drains your battery",
            "It deletes your files",
            "It blocks all websites",
        ],
        "answer": 0,
        "explanation": "Avoid banking and logins on public Wi-Fi, or use a trusted VPN and only visit HTTPS sites.",
    },
    {
        "question": "What is ransomware?",
        "options": [
            "A program that speeds up your computer",
            "A filter that blocks spam email",
            "Malware that locks your files and demands payment to unlock them",
            "A tool that stores passwords",
        ],
        "answer": 2,
        "explanation": "Regular offline backups are the best defence, because then you do not need to pay.",
    },
    {
        "question": "Why should you install software updates?",
        "options": [
            "They only change how the software looks",
            "They fix security holes that attackers could use",
            "They make your internet faster",
            "They are required by law",
        ],
        "answer": 1,
        "explanation": "Many attacks use known bugs that updates have already fixed. Not updating leaves the door open.",
    },
    {
        "question": "Phishing that arrives by SMS text message is called what?",
        "options": [
            "Vishing",
            "Spamming",
            "Smishing",
            "Skimming",
        ],
        "answer": 2,
        "explanation": "Smishing means SMS phishing. Vishing is phishing by voice call.",
    },
    {
        "question": "What is spear phishing?",
        "options": [
            "An attack aimed at one specific person or company, using details about them",
            "An attack that sends the same email to millions of random people",
            "An attack that only happens over phone calls",
            "A type of antivirus scan",
        ],
        "answer": 0,
        "explanation": "Because it uses real details like your name, job, or boss, it looks much more believable.",
    },
    {
        "question": "You find a USB pen drive in the office parking lot. What should you do?",
        "options": [
            "Plug it into your own computer to find the owner",
            "Plug it into a friend's computer instead",
            "Take it home and format it",
            "Do not plug it in. Hand it to your IT or security team",
        ],
        "answer": 3,
        "explanation": "Attackers leave infected USB drives on purpose. Plugging one in can install malware.",
    },
    {
        "question": "What does a firewall do?",
        "options": [
            "It makes your internet faster",
            "It filters network traffic and blocks connections that break the rules",
            "It removes viruses from your files",
            "It stores your passwords safely",
        ],
        "answer": 1,
        "explanation": "A firewall works like a security guard at the door of your network. It does not replace antivirus.",
    },
    {
        "question": "What is the safest way to keep track of many strong passwords?",
        "options": [
            "Use a reputable password manager",
            "Write them on a sticky note on your monitor",
            "Keep them in a file called passwords.txt on your desktop",
            "Send them to yourself on WhatsApp",
        ],
        "answer": 0,
        "explanation": "A password manager creates and stores unique passwords for you, protected by one strong master password.",
    },
    {
        "question": "What does a VPN mainly do?",
        "options": [
            "Makes your device immune to viruses",
            "Makes your downloads faster",
            "Creates an encrypted tunnel for your traffic so others on the network cannot read it",
            "Blocks all advertisements",
        ],
        "answer": 2,
        "explanation": "A VPN does not stop phishing or malware, and the VPN company can see your traffic, so choose a trusted one.",
    },
    {
        "question": "A pop-up says 'Your computer is infected! Call this number now.' What should you do?",
        "options": [
            "Call the number immediately",
            "Click the pop-up to start a scan",
            "Download the cleaner it suggests",
            "Close the browser tab, do not call, and run your real antivirus if you are worried",
        ],
        "answer": 3,
        "explanation": "This is a tech-support scam. Real security software never asks you to phone a number from a pop-up.",
    },
    {
        "question": "What is the 3-2-1 backup rule?",
        "options": [
            "3 passwords, 2 devices, 1 account",
            "3 copies of your data, on 2 types of storage, with 1 copy kept off-site",
            "3 backups a day, 2 a week, 1 a month",
            "3 antivirus programs, 2 firewalls, 1 VPN",
        ],
        "answer": 1,
        "explanation": "Following it means a single failure, theft, or ransomware attack cannot destroy all your copies.",
    },
    {
        "question": "To receive money by UPI, someone asks you to enter your UPI PIN. What does this mean?",
        "options": [
            "It is normal; the PIN is needed to receive money",
            "The sender made a small mistake",
            "It is a scam. You never enter your PIN to receive money",
            "Your bank is testing your account",
        ],
        "answer": 2,
        "explanation": "You only enter your PIN to send money. A request that asks for it to 'receive' money is a trick to empty your account.",
    },
    {
        "question": "A job offer email asks you to pay a 'registration fee' before you can join. What is this most likely?",
        "options": [
            "A scam, because genuine employers do not ask candidates to pay",
            "Normal, because companies charge for training",
            "Safe, if the company has a nice website",
            "Safe, if the email has a signature",
        ],
        "answer": 0,
        "explanation": "Fake job offers collect fees or personal documents. Check the company on its official website before you reply.",
    },
    {
        "question": "What is a man-in-the-middle attack?",
        "options": [
            "Someone physically steals your phone",
            "A virus that deletes your files",
            "A fake antivirus program",
            "An attacker secretly sits between you and a website and can read or change the data",
        ],
        "answer": 3,
        "explanation": "It is common on unsafe public Wi-Fi. HTTPS and a trusted VPN help protect you.",
    },
    {
        "question": "What is an MFA fatigue attack?",
        "options": [
            "You get tired of using two-factor codes",
            "The attacker sends many login approval prompts, hoping you tap Approve by mistake",
            "Your authenticator codes expire too quickly",
            "A bug that crashes authenticator apps",
        ],
        "answer": 1,
        "explanation": "If you get approval prompts you did not start, deny them and change your password straight away.",
    },
    {
        "question": "Where should you download apps and software from?",
        "options": [
            "From any website that offers them for free",
            "From the page with the most pop-ups",
            "Only from the official app store or the developer's official website",
            "From a link sent by a stranger",
        ],
        "answer": 2,
        "explanation": "Cracked or unofficial downloads are a common way to spread malware.",
    },
    {
        "question": "In security, what do the letters in the 'CIA triad' stand for?",
        "options": [
            "Confidentiality, Integrity, Availability",
            "Control, Identity, Authorization",
            "Cyber, Internet, Access",
            "Certificate, Identification, Authentication",
        ],
        "answer": 0,
        "explanation": "Confidentiality keeps data private, integrity keeps it unchanged, and availability keeps it accessible when needed.",
    },
    {
        "question": "What is a keylogger?",
        "options": [
            "A tool that manages your keys and locks",
            "Software or a device that secretly records what you type",
            "A program that helps you type faster",
            "A type of firewall",
        ],
        "answer": 1,
        "explanation": "Keyloggers steal passwords and messages as you type. Keep your system updated and do not install unknown software.",
    },
    {
        "question": "What is social engineering?",
        "options": [
            "Building social media apps",
            "Hacking a server using a very powerful computer",
            "Fixing network cables in an office",
            "Tricking people into giving up information or doing something unsafe",
        ],
        "answer": 3,
        "explanation": "It attacks human trust instead of technology. Phishing, fake calls, and impersonation are all social engineering.",
    },
    {
        "question": "What is SQL injection?",
        "options": [
            "Typing harmful database commands into an input field to trick a website",
            "Adding extra memory to a database server",
            "A way of backing up a database",
            "A tool for making websites faster",
        ],
        "answer": 0,
        "explanation": "Websites prevent it by using parameterized queries and checking all user input.",
    },
    {
        "question": "What is the risk of scanning a random QR code stuck on a poster?",
        "options": [
            "The QR code can damage your camera",
            "Nothing, because QR codes are always safe",
            "It may open a fake website or start a harmful download",
            "It uses up your mobile data plan",
        ],
        "answer": 2,
        "explanation": "Attackers paste fake QR codes over real ones. Check the address that opens before you enter anything.",
    },
    {
        "question": "What is a DDoS attack?",
        "options": [
            "Stealing data from a database",
            "Flooding a server with traffic so real users cannot use it",
            "Sending fake emails to employees",
            "Guessing a password many times",
        ],
        "answer": 1,
        "explanation": "The attack uses many devices at once to overload the target, so the website becomes slow or goes down.",
    },
    {
        "question": "An email has an attachment named invoice.exe. What should you do?",
        "options": [
            "Open it to see the invoice",
            "Forward it to your friends",
            "Reply and ask them to resend it",
            "Do not open it. An .exe file is a program, and it could run malware",
        ],
        "answer": 3,
        "explanation": "A real invoice is usually a PDF. Be careful with .exe, .scr, and .bat files, and with double extensions like invoice.pdf.exe.",
    },
    {
        "question": "How can you check where a shortened link (like bit.ly) leads before opening it?",
        "options": [
            "Open it quickly and close the page",
            "Share it with a friend first",
            "Use a link-expander or preview tool to see the full address",
            "Check if it starts with https",
        ],
        "answer": 2,
        "explanation": "Short links hide the real address. A preview shows where you would end up, and https alone does not prove a site is safe.",
    },
    {
        "question": "What is a zero-day vulnerability?",
        "options": [
            "A security flaw the vendor does not know about yet, so no fix exists",
            "A flaw that is fixed on the same day it is found",
            "A virus that spreads in zero seconds",
            "A password that expires in zero days",
        ],
        "answer": 0,
        "explanation": "Attackers can use it before anyone can patch it. That is why layers of defence still matter.",
    },
    {
        "question": "Which of these should you never post or share publicly?",
        "options": [
            "Your favourite movie",
            "Your Aadhaar number, OTP, or bank details",
            "A photo of your lunch",
            "Your college name",
        ],
        "answer": 1,
        "explanation": "Scammers use personal details for identity theft and to make convincing fake messages.",
    },
    {
        "question": "You clicked a phishing link and typed your password. What is the best next step?",
        "options": [
            "Do nothing and hope for the best",
            "Delete the email and forget about it",
            "Wait a few days to see what happens",
            "Change the password immediately, enable 2FA, and report it",
        ],
        "answer": 3,
        "explanation": "Also change that password anywhere else you used it, and tell your IT team or the real service.",
    },
    {
        "question": "Which sender address is the most suspicious?",
        "options": [
            "support@paypal.com",
            "no-reply@amazon.in",
            "support@paypa1-secure.com",
            "help@irctc.co.in",
        ],
        "answer": 2,
        "explanation": "It uses the number 1 in place of the letter l and adds extra words. Check the domain letter by letter.",
    },
]


def total_sets():
    return len(QUESTIONS) // QUESTIONS_PER_QUIZ


def new_set():
    """Pick questions that have not been used yet in this round."""
    unused = session.get("unused", [])
    if len(unused) < QUESTIONS_PER_QUIZ:
        # Everything was used, so start a fresh round with all questions
        unused = list(range(len(QUESTIONS)))

    chosen = random.sample(unused, QUESTIONS_PER_QUIZ)
    session["unused"] = [i for i in unused if i not in chosen]
    session["current"] = chosen
    return chosen


def set_number():
    used = len(QUESTIONS) - len(session.get("unused", []))
    return max(1, used // QUESTIONS_PER_QUIZ)




RANKS = [
    ("🎯", "Phishing Bait", "Attackers love you right now. Read the tips below and come back stronger."),
    ("🐣", "Fresh Recruit", "Everyone starts somewhere. Study the tips below and level up."),
    ("🕵️", "Cyber Detective", "You spot some tricks, but a few scams still slip past you."),
    ("⚔️", "Threat Hunter", "Sharp eyes. A little more practice and you are unstoppable."),
    ("🛡️", "Security Pro", "Almost perfect. Scammers have a hard time fooling you."),
    ("🏆", "Cyber Guardian", "Perfect score! Hackers fear you."),
]


@app.route("/")
def landing():
    return render_template("start.html")


@app.route("/quiz")
def quiz():
    current = session.get("current")
    valid = bool(current) and all(0 <= i < len(QUESTIONS) for i in current)
    if not valid:
        current = new_set()

    questions = [QUESTIONS[i] for i in current]
    # The correct answers are never sent to the browser
    return render_template("index.html", questions=questions)


@app.route("/result", methods=["POST"])
def result():
    current = session.get("current")
    if not current:
        return redirect(url_for("quiz"))

    score = 0
    review = []

    for position, question_id in enumerate(current):
        q = QUESTIONS[question_id]
        raw = request.form.get(f"q{position}", "")
        chosen = int(raw) if raw.isdecimal() else None

        # Never trust the browser: ignore values that are not a valid option
        if chosen is not None and chosen >= len(q["options"]):
            chosen = None

        correct = chosen == q["answer"]
        if correct:
            score += 1

        review.append({
            "question": q["question"],
            "options": q["options"],
            "chosen": chosen,
            "answer": q["answer"],
            "correct": correct,
            "explanation": q["explanation"],
        })

    total = len(current)
    rank_emoji, rank_title, rank_text = RANKS[round(score / total * (len(RANKS) - 1))]

    session.pop("current", None)  # this set is finished, the next visit gets new questions

    return render_template(
        "result.html",
        score=score,
        total=total,
        review=review,
        rank_emoji=rank_emoji,
        rank_title=rank_title,
        rank_text=rank_text,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5002)
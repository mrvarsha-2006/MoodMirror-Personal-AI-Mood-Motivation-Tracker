from flask import Flask, render_template, request
import pandas as pd
import os, datetime, random

app = Flask(__name__)
file_path = "mood_log.csv"

# =========================
# SAVE DATA
# =========================
def save_data(mood, thought):
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    df = pd.DataFrame([[date, mood, thought]],
                      columns=["Date", "Mood", "Thought"])

    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)


# =========================
# STREAK FIXED
# =========================
def calculate_streak():
    if not os.path.exists(file_path):
        return 0

    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df.dropna(subset=["Date"])
    df["Date"] = df["Date"].dt.date

    df = df.drop_duplicates(subset=["Date"])
    dates = sorted(df["Date"], reverse=True)

    streak = 0
    today = datetime.date.today()

    for i, d in enumerate(dates):
        if d == today - datetime.timedelta(days=i):
            streak += 1
        else:
            break

    return streak


# =========================
# PERSONAL QUOTES
# =========================
def generate_personal_quote():
    quotes = [
        "Varsha, you don’t need to show everything to everyone. Protect your energy and move in silence.",
        "Hey Varsha, don’t overtrust people too fast. Learn, observe, and choose wisely who deserves your space.",
        "Varsha, sometimes the problem isn’t the situation — it’s the way we think about it. Slow down your thoughts.",
        "Listen Varsha, not everything needs your reaction. Your silence can be your strength.",
        "Varsha, your reputation is built in small daily actions. Stay consistent, even when no one is watching.",
        "You’re allowed to pause, Varsha. Stillness is not weakness — it’s clarity.",
        "Varsha, don’t trap yourself thinking there’s only one solution. Life always has more paths than you can see right now.",
        "Take control, Varsha. Don’t let overthinking drive your life — you decide the direction.",
        "Varsha, this life is yours. Don’t let noise, opinions, or fear decide how you live it.",
        "No one can break you, Varsha, except your own mindset. Protect it.",
        "Varsha, there is something only you can do in this world. Don’t waste time doubting that.",
        "Where you started doesn’t define you, Varsha. What you build will.",
        "Varsha, people who constantly worry about others’ opinions rarely find peace. Focus on your path.",
        "Respect the ones who stay with you in hard times, Varsha — even if that person is just you.",
        "Varsha, don’t settle where you cannot grow, respect, or feel valued.",
        "You don’t need a crowd, Varsha. Strong people often walk alone before they find their circle.",
        "Even if things feel heavy today, Varsha — it’s not your fault. Just don’t stop moving forward.",
        "Varsha, even when it feels like no one is really there, you’re still supported—by your past.",
        "Varsha, growth is messy. Like falling off a wave — but one day, you’ll stand stronger than before.",
        "Hey Varsha, your path isn’t fixed. You can still change things — your effort matters.",
        "Varsha, living without passion will drain you. Find even one thing that makes you feel alive and build from there.",
        "Even if it’s slow, Varsha, your progress is real. Don’t quit halfway.",
        "Varsha, when things get hard, don’t isolate completely. Energy comes from connection too.",
        "It’s okay to feel lost sometimes, Varsha. Every phase teaches you something.",
        "Varsha, don’t compare yourself. You’re not supposed to be anyone else.",
        "Take breaks when needed, Varsha. Burning out won’t take you forward.",
        "No one will take the next step for you, Varsha. But you are capable of it.",
        "Varsha, build the habit of doing hard things — especially when you don’t feel like it.",
        "Sit with discomfort, Varsha. That’s where growth actually begins.",
        "Name what you feel, Varsha. Understanding your emotions gives you control.",
        "Rejection is not the end, Varsha. It’s direction.",
        "Learn to be alone without feeling lonely, Varsha. That’s strength.",
        "You don’t need to rebuild your whole life overnight, Varsha. Just improve little by little.",
        "Ask better questions to yourself, Varsha — your answers will change your life.",
        "Build skills, Varsha. Confidence comes from competence.",
        "Set boundaries, Varsha. Not everyone deserves access to you.",
        "Practice small courage daily, Varsha. Big confidence comes from that.",
        "Varsha, you are worthy of love, success, and everything you’re working towards.",
        "What you’re chasing is already moving toward you, Varsha. Just stay consistent.",
        "Trust the process, Varsha. Even if you don’t see results yet.",
        "You’re aligning with something bigger, Varsha. Keep going.",
        "You don’t need to chase everything, Varsha. The right things will come when you’re ready.",
        "Let go of fear slowly, Varsha. You don’t need to carry it forever.",
        "You are not alone in this journey, Varsha. Even if it feels like it sometimes.",
        "Varsha, don’t rush to prove yourself. Move quietly, grow steadily — your time will come.",
        "Hey Varsha, not everyone deserves your energy. Protect it and move wisely.",
        "Varsha, your mindset decides everything. Guard it like your life depends on it.",
        "You don’t need to react to everything, Varsha. Silence is power.",
        "Varsha, life is not one path. Don’t panic if things don’t go one way.",
        "Take control, Varsha. Don’t let overthinking drive your life.",
        "Varsha, you only get this life once. Choose what matters and let go of noise.",
        "No one can break you, Varsha, except your own mindset.",
        "Varsha, there is something only you can do in this world — don’t doubt that.",
        "Where you start doesn’t matter, Varsha. What you build does.",
        "Varsha, stop comparing. Your journey is yours alone.",
        "You don’t need many people, Varsha. Strong people often walk alone first.",
        "Even if things feel heavy, Varsha — keep going. This phase is not permanent.",
        "Varsha, growth feels like falling again and again — but one day, you’ll stand stronger.",
        "Your path isn’t fixed, Varsha. You can still change things.",
        "Varsha, living without passion will drain you. Find something that keeps you alive.",
        "Even slow progress is progress, Varsha. Don’t quit.",
        "Varsha, don’t isolate too much. Energy comes from connection too.",
        "It’s okay to feel lost, Varsha. Every phase teaches something.",
        "Take breaks when needed, Varsha. Burnout won’t help you.",
        "No one can take the next step for you, Varsha — but you can do it.",
        "Varsha, build the habit of doing hard things, especially when you don’t feel like it.",
        "Sit with discomfort, Varsha. That’s where growth begins.",
        "Name your emotions, Varsha — understanding them gives you control.",
        "Rejection is not failure, Varsha. It’s direction.",
        "Learn to be alone without feeling lonely, Varsha.",
        "Improve little by little, Varsha. That’s how change happens.",
        "Ask better questions to yourself, Varsha — your life will change.",
        "Build skills, Varsha. Confidence comes from competence.",
        "Set boundaries, Varsha. Not everyone deserves access to you.",
        "Practice small courage daily, Varsha.",
        "Varsha, you are worthy of love, success, and everything you’re working for.",
        "What you want is already moving toward you, Varsha. Stay consistent.",
        "Trust the process, Varsha. Even when results aren’t visible yet.",
        "You are aligning with something bigger, Varsha.",
        "You don’t need to chase everything, Varsha. The right things will come.",
        "Let go of fear slowly, Varsha.",
        "You are not alone in this journey, Varsha."
    ]
    return random.choice(quotes)


# =========================
# SMART QUOTE
# =========================
def generate_smart_quote():
    if not os.path.exists(file_path):
        return "Varsha, this is your starting point. Show up for yourself."

    df = pd.read_csv(file_path)

    if df.empty:
        return "Varsha, start small. Everything begins with showing up."

    recent = df.tail(5)
    moods = recent["Mood"].tolist()

    mood_count = {
        "happy": moods.count("happy"),
        "okay": moods.count("okay"),
        "sad": moods.count("sad"),
        "tired": moods.count("tired"),
        "stressed": moods.count("stressed")
    }

    dominant = max(mood_count, key=mood_count.get)

    if dominant == "stressed":
        return "Varsha, you’ve been stressed often. Slow down — focus on one thing instead of everything."
    elif dominant == "tired":
        return "Varsha, you’ve been feeling tired repeatedly. Rest is not weakness — it’s part of progress."
    elif dominant == "sad":
        return "Varsha, things seem heavy lately. Don’t isolate — even small steps matter."
    elif dominant == "happy":
        return "Varsha, you’ve been doing well lately. Build on this momentum."
    elif dominant == "okay":
        return "Varsha, this neutral phase is where discipline matters most."

    return "Varsha, keep going no matter the phase."


# =========================
# GRAPH DATA
# =========================
def get_graph():
    if not os.path.exists(file_path):
        return []

    df = pd.read_csv(file_path)

    mood_map = {"happy":5,"okay":3,"sad":2,"tired":1,"stressed":0}
    df["value"] = df["Mood"].map(mood_map)

    return df["value"].tolist()


# =========================
# MAIN ROUTE
# =========================
@app.route("/", methods=["GET","POST"])
def home():

    # Initial quote shown immediately
    quote = generate_personal_quote()

    if request.method == "POST":
        mood = request.form.get("mood")
        thought = request.form.get("thought")

        save_data(mood, thought)

        # After submission → smart + personal
        quote = generate_smart_quote() + " " + generate_personal_quote()

    streak = calculate_streak()
    graph_data = get_graph()

    return render_template("index.html",
                           quote=quote,
                           streak=streak,
                           graph_data=graph_data)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True, port=5001)

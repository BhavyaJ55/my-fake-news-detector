import streamlit as st
import time
from hf_model import predict_text
from news_fetch import fetch_articles
from factcheck import search_claims
import wikipedia

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Fake News Detector", layout="wide")

# ------------------ PREMIUM UI CSS ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(160deg, #060A1A, #000000);
}

.title-text {
    font-size: 46px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00F0FF, #F000FF, #FFB800);
    -webkit-background-clip: text;
    color: transparent;
    animation: glow 2s ease-in-out infinite alternate;
}

.tagline {
    text-align: center;
    font-size: 16px;
    margin-top: -10px;
    font-weight: 500;
    background: linear-gradient(90deg, #EAEAEA, #00F0FF);
    -webkit-background-clip: text;
    color: transparent;
}

@keyframes glow {
    from { text-shadow: 0 0 20px #00F0FF; }
    to { text-shadow: 0 0 40px #F000FF; }
}

.card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(18px);
    border-radius: 25px;
    padding: 30px;
    box-shadow: 0 0 40px rgba(0,0,0,0.7);
    margin-top: 30px;
    animation: float 5s ease-in-out infinite;
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}

.scan {
    height: 6px;
    width: 100%;
    background: linear-gradient(90deg, transparent, #00F0FF, transparent);
    animation: scan 2s linear infinite;
    margin-top: 20px;
}

@keyframes scan {
    0% {transform: translateX(-100%);}
    100% {transform: translateX(100%);}
}

.result-real {
    box-shadow: 0 0 35px #00ffcc;
    border: 2px solid #00ffcc;
}

.result-fake {
    box-shadow: 0 0 35px #ff0055;
    border: 2px solid #ff0055;
}

/* ✅ NEW RESULT BADGES */
.badge-real {
    background: linear-gradient(90deg, #00ffcc, #00ffaa);
    color: black;
    padding: 6px 16px;
    border-radius: 50px;
    font-weight: 900;
    display: inline-block;
    box-shadow: 0 0 20px #00ffcc;
}

.badge-fake {
    background: linear-gradient(90deg, #ff0055, #ff3366);
    color: white;
    padding: 6px 16px;
    border-radius: 50px;
    font-weight: 900;
    display: inline-block;
    box-shadow: 0 0 20px #ff0055;
}

.ring {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    background: conic-gradient(#00F0FF var(--percent), #222 0);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px auto;
}

.ring span {
    color: white;
    font-size: 26px;
    font-weight: bold;
}

.stButton>button {
    background: linear-gradient(90deg, #00F0FF, #F000FF);
    border: none;
    padding: 14px 40px;
    border-radius: 40px;
    color: black;
    font-weight: 800;
    font-size: 16px;
    transition: 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.07);
    box-shadow: 0 0 25px #00F0FF;
}

textarea {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 15px !important;
}

/* Sidebar */
.css-1d391kg {
    background: linear-gradient(180deg, #060A1A, #000000);
}
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.title("AI Fake News Detection System")
    st.markdown("Core Components")
    st.markdown("- AI Classification")
    st.markdown("- Google Fact Check")
    st.markdown("- Wikipedia Verification")
    st.markdown("- Live News Matching")
    st.markdown("- Claim Validation")

# ------------------ MAIN HEADER ------------------
st.markdown('<div class="title-text">AI Fake News Detector</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Real-time AI powered truth verification with deep web intelligence</div>', unsafe_allow_html=True)

# ------------------ INPUT CARD ------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
user_text = st.text_area("Paste Any News or Claim Here", height=180)
analyze_btn = st.button("Analyze")
st.markdown('</div>', unsafe_allow_html=True)

# ------------------ ANALYSIS ------------------
if analyze_btn and user_text.strip():

    st.markdown('<div class="scan"></div>', unsafe_allow_html=True)
    with st.spinner("AI is analyzing deeply..."):
        time.sleep(2.5)

    prediction = predict_text(user_text)
    scores = {d['label']: d['score'] for d in prediction[0]}

    if scores.get("POSITIVE", 0) > scores.get("NEGATIVE", 0):
        verdict = "REAL"
        confidence = scores["POSITIVE"] * 100
        glow = "result-real"
        badge = f"<span class='badge-real'>REAL</span>"
    else:
        verdict = "FAKE"
        confidence = scores["NEGATIVE"] * 100
        glow = "result-fake"
        badge = f"<span class='badge-fake'>FAKE</span>"

        st.markdown("""
        <audio autoplay>
            <source src="https://www.soundjay.com/buttons/sounds/beep-07.mp3" type="audio/mpeg">
        </audio>
        """, unsafe_allow_html=True)

    percent = f"{int(confidence)}%"

    st.markdown(f'<div class="card {glow}">', unsafe_allow_html=True)

    st.subheader("Confidence Meter")
    st.markdown(f"""
    <div class="ring" style="--percent:{percent}">
        <span>{percent}</span>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("AI Verdict")
    st.markdown(f"{badge}", unsafe_allow_html=True)

    st.subheader("Fact Summary")
    try:
        summary = wikipedia.summary(user_text, sentences=3, auto_suggest=True)
        st.write(summary)
    except:
        articles = fetch_articles(user_text)
        for article in articles[:5]:
            st.write("•", article['title'])

    st.subheader("Google Fact Check Result")
    claims = search_claims(user_text[:150])

    if claims:
        for c in claims[:3]:
            st.write("Claim:", c.get("text", "N/A"))
            review = c.get("claimReview", [{}])[0]
            st.write("Rating:", review.get("textualRating", "Not Available"))
            st.write("Source:", review.get("url", "Not Available"))
            st.markdown("---")
    else:
        st.warning("No Fact-Check Found.")

    st.success("AI Analysis Completed Successfully")
    st.markdown('</div>', unsafe_allow_html=True)

elif analyze_btn:
    st.warning("Please enter a news statement before analyzing.")

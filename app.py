import streamlit as st
from hf_model import predict_text
from news_fetch import fetch_articles
from factcheck import search_claims
import wikipedia
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Fake News Detector",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION HISTORY ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- ANIMATED MODERN CSS ----------------
st.markdown("""
<style>

/* ========== GLOBAL BACKGROUND ========== */
body {
    background: radial-gradient(circle at top, #0b1a33, #060A1A 70%);
    color: #EAEAEA;
}

.main {
    background: transparent;
}

/* ========== HEADINGS ========== */
h1 {
    text-align: center;
    font-weight: 900;
    letter-spacing: 1px;
    color: #EAEAEA;
    animation: fadeIn 1s ease-in-out;
}

h2, h3 {
    color: #00F0FF;
    font-weight: 700;
}

/* ========== FADE ANIMATION ========== */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(18px);}
    to {opacity: 1; transform: translateY(0);}
}

/* ========== TEXT AREA INPUT ========== */
textarea {
    border-radius: 16px !important;
    background: rgba(6,10,26,0.95) !important;
    color: #EAEAEA !important;
    border: 1px solid rgba(0,240,255,0.45);
    box-shadow: 0 0 18px rgba(0,240,255,0.15);
}

/* ========== MAIN BUTTON (COSMIC TEAL CTA) ========== */
div.stButton > button {
    width: 100%;
    border-radius: 40px;
    background: linear-gradient(135deg, #00F0FF, #00AEEF);
    color: #060A1A;
    font-size: 17px;
    font-weight: 800;
    height: 3.2em;
    border: none;
    transition: all 0.35s ease;
    box-shadow: 0 0 20px rgba(0,240,255,0.45);
}

div.stButton > button:hover {
    transform: scale(1.06);
    box-shadow: 0 0 35px rgba(0,240,255,0.85);
}

/* ========== GLASS CARD SYSTEM ========== */
.card {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.08),
        rgba(255,255,255,0.02)
    );
    backdrop-filter: blur(16px);
    border: 1px solid rgba(0,240,255,0.25);
    padding: 26px;
    border-radius: 22px;
    margin-bottom: 26px;
    animation: fadeIn 0.8s ease;
    box-shadow: 0 0 28px rgba(0,240,255,0.12);
}

/* ========== VERDICT STATES ========== */
.status-real {
    color: #FFB800;
    font-size: 22px;
    font-weight: 900;
    animation: glowGold 1.8s infinite alternate;
}

.status-fake {
    color: #F000FF;
    font-size: 22px;
    font-weight: 900;
    animation: glowMagenta 1.8s infinite alternate;
}

@keyframes glowGold {
    from {text-shadow: 0 0 6px #FFB800;}
    to {text-shadow: 0 0 26px #FFB800;}
}

@keyframes glowMagenta {
    from {text-shadow: 0 0 6px #F000FF;}
    to {text-shadow: 0 0 26px #F000FF;}
}

/* ========== MUTED TEXT ========== */
.muted {
    color: #B8C0D9;
    font-size: 15px;
}

/* ========== DIVIDERS ========== */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #00F0FF, transparent);
    margin: 30px 0;
}

/* ========== SIDEBAR ========== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060A1A, #0b1a33);
    border-right: 1px solid rgba(0,240,255,0.25);
}

/* ========== SUCCESS MESSAGE (EMBER GOLD) ========== */
div.stAlert-success {
    background-color: rgba(255,184,0,0.12);
    border: 1px solid #FFB800;
    color: #FFB800;
}

/* ========== WARNING / ALERT (HYPER MAGENTA) ========== */
div.stAlert-warning, 
div.stAlert-error {
    background-color: rgba(240,0,255,0.12);
    border: 1px solid #F000FF;
    color: #F000FF;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("Project Panel")
    st.markdown("AI Fake News Detection System")

    st.markdown("---")
    st.markdown("Core Components")
    st.markdown("""
    - AI Classification  
    - Google Fact Check  
    - Wikipedia Verification  
    - Live News Matching  
    - Claim Validation  
    """)

    st.markdown("---")
    st.markdown("Recent Searches")

    if st.session_state.history:
        for i in range(len(st.session_state.history)-1, max(-1, len(st.session_state.history)-6), -1):
            st.markdown(f"- {st.session_state.history[i]['text'][:50]}...")
    else:
        st.caption("No searches yet")

    st.markdown("---")
    st.caption("AI Academic Project")

# ---------------- HEADER ----------------
st.markdown("<h1>AI Fake News Detection System</h1>", unsafe_allow_html=True)
st.markdown("<p class='muted' style='text-align:center;'>Advanced verification using artificial intelligence and trusted sources</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
user_text = st.text_area("Enter a news statement or claim", height=160)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ANALYSIS BUTTON ----------------
if st.button("Analyze Now"):

    if not user_text.strip():
        st.warning("Please enter a valid news statement.")
        st.stop()

    st.session_state.history.append({
        "text": user_text,
        "time": datetime.now().strftime("%H:%M:%S")
    })

    with st.spinner("Artificial intelligence is analyzing the claim..."):

        # ---------------- AI RESULT ----------------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Classification Result")

        prediction = predict_text(user_text)
        scores = {d['label']: d['score'] for d in prediction[0]}

        if scores.get("POSITIVE", 0) > scores.get("NEGATIVE", 0):
            verdict = "REAL"
            confidence = scores["POSITIVE"] * 100
            style = "status-real"
        else:
            verdict = "FAKE"
            confidence = scores["NEGATIVE"] * 100
            style = "status-fake"

        st.markdown(f"<div class='{style}'>{verdict}</div>", unsafe_allow_html=True)
        st.caption(f"Confidence Score: {confidence:.2f}%")
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- FACT SUMMARY ----------------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Knowledge Summary")

        try:
            summary = wikipedia.summary(user_text, sentences=3, auto_suggest=True)
            st.write(summary)

        except:
            st.warning("No direct summary found. Showing related news headlines.")
            articles = fetch_articles(user_text)

            for article in articles[:5]:
                st.markdown(f"- {article['title']}")

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- GOOGLE FACT CHECK ----------------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Google Fact Check")

        claims = search_claims(user_text[:150])

        if claims:
            for c in claims[:3]:
                st.markdown(f"Claim: {c.get('text', 'N/A')}")
                review = c.get("claimReview", [{}])[0]
                st.caption(f"Rating: {review.get('textualRating', 'Not Available')}")
                st.caption(f"Source: {review.get('url', 'Not Available')}")
                st.markdown("---")
        else:
            st.caption("No official fact-check record found for this claim.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.success("Analysis completed successfully.")
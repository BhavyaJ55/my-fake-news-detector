import streamlit as st
from hf_model import predict_text
from news_fetch import fetch_articles
from factcheck import search_claims
from semantic_index import build_index, query_index
import wikipedia

st.set_page_config(page_title="AI Fake News Detector")
st.title("🧠 AI Integrated Fake News Detection System")

user_text = st.text_area("Paste Any News / Claim Here", height=200)

if st.button("Analyze"):

    # --- AI Prediction ---
    st.subheader("🔍 AI Prediction")
    prediction = predict_text(user_text)

    scores = {d['label']: d['score'] for d in prediction[0]}
    if scores.get("POSITIVE", 0) > scores.get("NEGATIVE", 0):
        verdict = "REAL ✅"
        confidence = scores["POSITIVE"] * 100
    else:
        verdict = "FAKE ❌"
        confidence = scores["NEGATIVE"] * 100

    st.markdown(f"*Verdict:* {verdict}  |  *Confidence:* {confidence:.2f}%")

    # --- Fact Summary Section ---
    st.subheader("📝 Fact Summary / Key Information")

    try:
        summary = wikipedia.summary(user_text, sentences=3, auto_suggest=True)
        st.write(summary)
    except:
        st.warning("No direct Wikipedia info found. Showing related live news instead.")
        articles = fetch_articles(user_text)
        for article in articles[:5]:
            st.write("•", article['title'])

    # --- ✅ GOOGLE FACT CHECK (FIXED) ---
    st.subheader("✅ Google Fact Check Result")

    claims = search_claims(user_text[:150])

    if claims and len(claims) > 0:
        for c in claims[:3]:
            st.write("🧾 Claim:", c.get("text", "N/A"))

            review = c.get("claimReview", [{}])[0]
            st.write("📌 Rating:", review.get("textualRating", "Not Available"))
            st.write("🔗 Source:", review.get("url", "Not Available"))
            st.markdown("---")
    else:
        st.warning("❌ No Fact-Check Found in Google Database for this exact claim.")

    st.success("✅ AI Analysis Completed Successfully!")
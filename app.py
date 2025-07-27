import streamlit as st
import requests
import pandas as pd
import re
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

# --- Optional: Only import openai if key exists ---
if OPENAI_API_KEY:
    import openai
    openai.api_key = OPENAI_API_KEY

# --- Streamlit config ---
st.set_page_config(page_title="PaperPal", layout="wide")
st.title("PaperPal: Academic Paper Explorer")

# --- Sidebar filters ---
with st.sidebar:
    keyword = st.text_input("Search Keyword", "")
    conference = st.selectbox("Conference Tier", ["A*", "A", "B", "C", "All"])
    min_year, max_year = st.slider("Year Range", 2000, 2025, (2018, 2024))
    sort_by_year = st.checkbox("Sort by Year (Descending)", value=True)
    summarize = st.checkbox("Summarize Abstracts", value=True)

if not keyword:
    st.info("Enter a keyword to begin searching.")
    st.stop()

# --- Conference tier mapping ---
CONFERENCE_TIER_KEYWORDS = {
    "A*": ["CVPR", "NeurIPS", "ICML", "ACL", "SIGGRAPH"],
    "A": ["ECCV", "ICLR", "COLING", "KDD"],
    "B": ["ICASSP", "EMNLP", "NAACL"],
    "C": ["WACV", "BMVC", "SAC"]
}

# --- Fetch papers ---
@st.cache(suppress_st_warning=True)
def fetch_papers(query: str, limit: int = 50):
    try:
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={limit}&fields=title,year,abstract,url,venue"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception:
        return []

# --- Text highlighting ---
def highlight_keywords(text: str, keyword: str) -> str:
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    return pattern.sub(f"**{keyword}**", text)

# --- Fallback summarizer ---
def simple_summarize(abstract: str) -> str:
    if not abstract:
        return "No abstract available."
    sentences = re.split(r'(?<=[.?!])\s+', abstract.strip())
    return " ".join(sentences[:2])

# --- AI summarizer with fallback ---
def summarize_abstract(abstract: str) -> str:
    if not summarize or not abstract:
        return "No abstract available."

    if OPENAI_API_KEY:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Summarize this academic abstract in 2 concise lines."},
                    {"role": "user", "content": abstract}
                ],
                temperature=0.3,
                max_tokens=100
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception:
            return simple_summarize(abstract)
    else:
        return simple_summarize(abstract)

# --- Filter papers ---
papers = fetch_papers(keyword)
filtered = []

for paper in papers:
    year = paper.get("year", 0)
    venue = paper.get("venue", "").upper()

    if not (min_year <= year <= max_year):
        continue

    if conference != "All":
        tier_keywords = CONFERENCE_TIER_KEYWORDS.get(conference, [])
        if not any(conf in venue for conf in tier_keywords):
            continue

    filtered.append(paper)

if sort_by_year:
    filtered = sorted(filtered, key=lambda x: x.get("year", 0), reverse=True)

if not filtered:
    st.warning("No papers found with the given filters.")
    st.stop()

# --- Display results ---
df = pd.DataFrame([{
    "Title": f"[{p['title']}]({p['url']})",
    "Year": p.get("year", ""),
    "Venue": p.get("venue", ""),
    "Abstract": highlight_keywords(summarize_abstract(p.get("abstract", "")), keyword)
} for p in filtered])

st.markdown("### Search Results")
st.dataframe(df, use_container_width=True)

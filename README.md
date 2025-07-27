# PaperPal – Academic Paper Search Tool

A minimal, fast, and user-friendly academic paper search interface powered by the [Semantic Scholar API](https://api.semanticscholar.org/). It allows you to discover and filter research papers based on keywords, venue tiers, and publication years, all within a clean UI.

## Features

- Keyword-based search for academic papers
- Filter by conference tier (A*, A, B, C, or All)
- Year range selector for publication dates
- Option to summarize abstracts or highlight keywords
- Sort results by year (descending)
- Clean and responsive UI built with Streamlit
---

## Built With

- Python  
- [Streamlit](https://streamlit.io)  
- Semantic Scholar Academic Graph API  

---

## Setup & Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/paperpal.git
cd paperpal

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

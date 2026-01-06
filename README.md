# 🎓 SmartExpense AI (Team DevSprint)

**SmartExpense AI** is a next-generation financial intelligence tool developed for **Namma Hack**. It bridges the gap between passive expense tracking and active financial coaching by integrating **Google Gemini 1.5 Flash** with custom Machine Learning.



---

## 🚀 The Problem
Traditional expense trackers are "digital notebooks"—they tell you what you *did*, but not what you *should do*. Students and young professionals often lack the immediate foresight to know if a small purchase today will impact a major bill next week.

## 💡 The Solution: "Jeeves"
SmartExpense AI uses a two-tier intelligence system:
1. **Google Gemini 1.5 Flash**: A semantic engine that reads receipts (OCR) and understands the *context* of your spending.
2. **Random Forest Classifier**: A predictive model that calculates a **Sustainability Score** based on your balance, upcoming costs, and spending habits.

## ✨ Key Features
- **Smart OCR Scanner**: Snap a photo of a receipt (like a bakery bill) and let Gemini extract the merchant, items, and total automatically.
- **AI Advisor (Jeeves)**: Get real-time "Approve/Deny" suggestions on planned purchases.
- **Generalized Trends**: Advanced data smoothing (3-day moving averages) to see your true spending patterns without daily noise.
- **Google Search Integration**: Built-in "Search & Save" to find better deals before you buy.

## 🛠️ Tech Stack
- **Frontend**: [Streamlit](https://streamlit.io/)
- **LLM**: Google Gemini 1.5 Flash
- **ML Model**: Random Forest (Scikit-Learn)
- **Data Viz**: Plotly, Seaborn, Matplotlib
- **OCR**: PyTesseract / Gemini Vision

---

## 🛠️ Installation & Setup
1. Clone the repo:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/SmartExpense-DevSprint.git](https://github.com/YOUR_USERNAME/SmartExpense-DevSprint.git)

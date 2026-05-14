# ✈️ Voyage AI

Voyage AI is an AI Powered trip planner (Python + Streamlit) web app that helps users plan trips with flight search, hotel search, weather updates, and AI-based suggestions.

---

## 🚀 Features
- Flight search
- Hotel search
- Weather updates
- AI trip suggestions
- Simple Streamlit UI

---

## 🛠️ Tech Stack
- Python
- Streamlit
- APIs (Flights/Hotels/Weather)
- JSON handling

---

## 📁 Project Structure
AI-TRIP-PLANNER/
├── app.py
├── backend/
│   ├── weather.py
│   ├── searchflight.py
│   ├── searchhotel.py
│   ├── llm_service.py
│   ├── formatflight.py
│   ├── formathotel.py
│   └── formatweather.py
├── images/
├── .gitignore
└── requirements.txt

---

## ⚙️ Run Locally

```bash
git clone https://github.com/Irfan-lab700/AI-Trip-Planner.git
cd AI-Trip-Planner
pip install -r requirements.txt
streamlit run app.py

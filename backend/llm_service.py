import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"]
)
MODEL = "Qwen/Qwen2.5-72B-Instruct:novita"

SCHEMA = """
{
  "flight_details": {
    "summary": "string",
    "price": "string",
    "airline": "string"
  },
  "hotels": [
    {
      "name": "string",
      "price": "string",
      "rating": "string",
      "location": "string",
      "reason": "string"
    }
  ],
  "itinerary": [
    {
      "day": 1,
      "theme": "string",
      "weather": "string",
      "morning": "string",
      "afternoon": "string",
      "evening": "string"
    }
  ],
  "budget_breakdown": {
    "flights": "string",
    "hotels": "string",
    "food_activities": "string",
    "total": "string"
  },
  "tips": ["string"]
}
"""

def _clean_json(text):
    """Remove markdown fences and any leading/trailing junk."""
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = text.replace("```", "")
    return text.strip()

def _validate_and_fix(data):
    """Ensure the returned dict matches the schema, fill missing keys with defaults."""
    if not isinstance(data, dict):
        return _fallback_response()

    # flight_details
    if "flight_details" not in data or not isinstance(data["flight_details"], dict):
        data["flight_details"] = {"summary": "Not specified", "price": "Not specified", "airline": "Not specified"}
    else:
        fd = data["flight_details"]
        fd.setdefault("summary", "Not specified")
        fd.setdefault("price", "Not specified")
        fd.setdefault("airline", "Not specified")

    # hotels
    if "hotels" not in data or not isinstance(data["hotels"], list):
        data["hotels"] = []
    else:
        for h in data["hotels"]:
            if isinstance(h, dict):
                h.setdefault("name", "Unknown")
                h.setdefault("price", "Unknown")
                h.setdefault("rating", "Unknown")
                h.setdefault("location", "Unknown")
                h.setdefault("reason", "No reason provided")

    # itinerary
    if "itinerary" not in data or not isinstance(data["itinerary"], list):
        data["itinerary"] = []
    else:
        for i, day in enumerate(data["itinerary"]):
            if isinstance(day, dict):
                day.setdefault("day", i + 1)
                day.setdefault("theme", "Exploration")
                day.setdefault("weather", "Check forecast")
                day.setdefault("morning", "Free time")
                day.setdefault("afternoon", "Free time")
                day.setdefault("evening", "Free time")

    # budget_breakdown
    if "budget_breakdown" not in data or not isinstance(data["budget_breakdown"], dict):
        data["budget_breakdown"] = {"flights": "N/A", "hotels": "N/A", "food_activities": "N/A", "total": "N/A"}
    else:
        bb = data["budget_breakdown"]
        for k in ["flights", "hotels", "food_activities", "total"]:
            bb.setdefault(k, "N/A")

    # tips
    if "tips" not in data or not isinstance(data["tips"], list):
        data["tips"] = []
    else:
        data["tips"] = [t for t in data["tips"] if isinstance(t, str)]

    return data

def _fallback_response():
    return {
        "flight_details": {"summary": "Could not retrieve flights", "price": "N/A", "airline": "N/A"},
        "hotels": [],
        "itinerary": [],
        "budget_breakdown": {"flights": "N/A", "hotels": "N/A", "food_activities": "N/A", "total": "N/A"},
        "tips": ["We're sorry, something went wrong. Please try again."],
    }

def create_prompt(trip_data, weather, hotels, flights):
    return f"""
You are an AI travel planner. Return a **valid JSON object** following the schema below.

**ABSOLUTE RULES:**
- Return ONLY the JSON object, no markdown, no code fences, no explanations.
- Use double quotes for all strings.
- Do NOT include trailing commas.
- All keys are required. If a value is missing, use "N/A".
- The JSON must be parseable by Python's `json.loads()`.

**SCHEMA:**
{SCHEMA}

**TRIP DETAILS:**
Destination: {trip_data['destination']}
Duration: {trip_data['days']} days
Budget: ₹{trip_data['budget']}
Travel Type: {trip_data['travel_type']}
Travellers: {trip_data['num_travellers']}
Interests: {", ".join(trip_data['interests'])}

**WEATHER:**
{weather}

**HOTELS:**
{hotels}

**FLIGHTS:**
{flights}
"""

def generate_itinerary(trip_data, weather, hotels, flights):
    try:
        prompt = create_prompt(trip_data, weather, hotels, flights)

        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict JSON generator. Only output valid JSON objects."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=2500
        )

        raw = completion.choices[0].message.content
        cleaned = _clean_json(raw)

        parsed = json.loads(cleaned)
        return _validate_and_fix(parsed)

    except json.JSONDecodeError as e:

        try:
            repair_prompt = f"The following string should be valid JSON. Clean and return ONLY the corrected JSON:\n\n{cleaned}"
            repair = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a JSON repair tool. Output only valid JSON."},
                    {"role": "user", "content": repair_prompt}
                ],
                temperature=0.1,
                max_tokens=2500
            )
            repaired_raw = _clean_json(repair.choices[0].message.content)
            parsed = json.loads(repaired_raw)
            return _validate_and_fix(parsed)
        except:
            return _fallback_response()

    except Exception as e:
        import traceback
        traceback.print_exc()    
        return {"error": str(e)}
def render_trip_plan(plan_dict, st_module):
    s = st_module

    if "error" in plan_dict:
        s.error(plan_dict["error"])
        return

    flights = plan_dict.get("flight_details", {})
    if flights:
        s.subheader("✈️ Flight Details")
        s.markdown(
            "<div style='background:#F0EDCC;border-radius:16px;padding:20px 24px;"
            "border:1px solid rgba(2,52,63,0.18);"
            "box-shadow:0 4px 14px rgba(0,0,0,0.07);"
            "margin-bottom:14px;color:#02343F;'>"
            f"<h3 style='color:#02343F;margin:0 0 10px 0'>{flights.get('airline','N/A')}</h3>"
            f"<p style='color:#02343F;margin:4px 0'>💰 <b>Price:</b> {flights.get('price','N/A')}</p>"
            f"<p style='color:#02343F;margin:8px 0'>{flights.get('summary','No summary available')}</p>"
            "</div>",
            unsafe_allow_html=True
        )

    s.markdown("<br>", unsafe_allow_html=True)

    hotels = plan_dict.get("hotels", [])
    if hotels:
        s.subheader("🏨 Recommended Hotels")
        cols = s.columns(min(len(hotels), 4))
        for i, h in enumerate(hotels[:4]):
            with cols[i]:
                s.markdown(
                    "<div style='background:#F0EDCC;border-radius:16px;padding:16px;"
                    "border:1px solid rgba(2,52,63,0.18);"
                    "box-shadow:0 4px 14px rgba(0,0,0,0.07);"
                    "color:#02343F;height:100%;'>"
                    f"<h4 style='color:#02343F;margin:0 0 10px 0'>{h.get('name','Unknown')}</h4>"
                    f"<p style='color:#02343F;margin:4px 0'>⭐ <b>Rating:</b> {h.get('rating','N/A')}</p>"
                    f"<p style='color:#02343F;margin:4px 0'>📍 <b>Location:</b> {h.get('location','N/A')}</p>"
                    f"<p style='color:#02343F;margin:4px 0'>💰 <b>Price:</b> {h.get('price','N/A')}</p>"
                    "<hr style='border:none;border-top:1px solid rgba(2,52,63,0.15);margin:10px 0'>"
                    f"<p style='color:#02343F;margin:0;font-size:13px'>{h.get('reason','')}</p>"
                    "</div>",
                    unsafe_allow_html=True
                )

    s.markdown("<br>", unsafe_allow_html=True)

    itinerary = plan_dict.get("itinerary", [])
    if itinerary:
        s.subheader("📅 Daily Itinerary")
        for d in itinerary:
            s.markdown(
                "<div style='background:#F0EDCC;border-radius:16px;padding:20px 24px;"
                "border:1px solid rgba(2,52,63,0.18);"
                "box-shadow:0 4px 14px rgba(0,0,0,0.07);"
                "margin-bottom:14px;color:#02343F;'>"
                f"<h2 style='color:#02343F;margin:0 0 6px 0'>Day {d.get('day','')} — {d.get('theme','')}</h2>"
                f"<p style='color:#02343F;margin:0 0 12px 0'>🌤 <b>Weather:</b> {d.get('weather','')}</p>"
                "<hr style='border:none;border-top:1px solid rgba(2,52,63,0.15);margin:10px 0'>"
                "<p style='color:#02343F;margin:6px 0'><b>🌅 Morning</b></p>"
                f"<p style='color:#02343F;margin:0 0 12px 0'>{d.get('morning','')}</p>"
                "<hr style='border:none;border-top:1px solid rgba(2,52,63,0.15);margin:10px 0'>"
                "<p style='color:#02343F;margin:6px 0'><b>☀️ Afternoon</b></p>"
                f"<p style='color:#02343F;margin:0 0 12px 0'>{d.get('afternoon','')}</p>"
                "<hr style='border:none;border-top:1px solid rgba(2,52,63,0.15);margin:10px 0'>"
                "<p style='color:#02343F;margin:6px 0'><b>🌙 Evening</b></p>"
                f"<p style='color:#02343F;margin:0 0 6px 0'>{d.get('evening','')}</p>"
                "</div>",
                unsafe_allow_html=True
            )

    s.markdown("<br>", unsafe_allow_html=True)

    budget = plan_dict.get("budget_breakdown", {})
    if budget:
        s.subheader("💰 Budget Breakdown")
        items = [
            ("✈️ Flights",           budget.get("flights",         "N/A")),
            ("🏨 Hotels",            budget.get("hotels",          "N/A")),
            ("🍽️ Food & Activities", budget.get("food_activities", "N/A")),
            ("💰 Total",             budget.get("total",           "N/A")),
        ]
        cols = s.columns(4)
        for i, (label, value) in enumerate(items):
            with cols[i]:
                s.markdown(
                    "<div style='background:#F0EDCC;border-radius:14px;padding:18px 14px;"
                    "border:1px solid rgba(2,52,63,0.18);"
                    "box-shadow:0 4px 14px rgba(0,0,0,0.07);"
                    "text-align:center;color:#02343F;'>"
                    f"<p style='color:#02343F;font-size:13px;margin:0 0 6px 0'>{label}</p>"
                    f"<p style='color:#02343F;font-size:20px;font-weight:700;margin:0'>{value}</p>"
                    "</div>",
                    unsafe_allow_html=True
                )

    s.markdown("<br>", unsafe_allow_html=True)

    tips = plan_dict.get("tips", [])
    if tips:
        s.subheader("💡 Travel Tips")
        tips_html = "".join(
            f"<p style='color:#02343F;margin:6px 0'>• {t}</p>"
            for t in tips
        )
        s.markdown(
            "<div style='background:#F0EDCC;border-radius:16px;padding:20px 24px;"
            "border:1px solid rgba(2,52,63,0.18);"
            "box-shadow:0 4px 14px rgba(0,0,0,0.07);"
            "margin-bottom:14px;color:#02343F;'>"
            + tips_html +
            "</div>",
            unsafe_allow_html=True
        )
import streamlit as st
from backend.backend import generate_trip_plan
from backend.llm_service import render_trip_plan
st.set_page_config(page_title="AI Trip Planner", page_icon=":earth_americas:", layout="wide")
st.markdown("""
<style>
.stApp {
    background-color: #02343F;
}
div.stButton > button {
    background-color: #011A20;
    color:  #F0EDCC;
    font-size: 25px;
    font-weight: 700;
    padding: 12px 25px;
    border: none;
    border-radius: 12px;
    transition: 0.3s ease;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #02343F;
    transform: scale(1.02);
    border: 1px solid #F0EDCC;
    box-shadow: 0 8px 22px rgba(200, 119, 64, 0.5);
    cursor: pointer;
}
label {
    color: #F5E9DC !important;
    font-weight: 600 !important;
}
button[data-baseweb="tab"] {
    color: #F5E9DC;
    font-weight: 600;
    background-color: transparent;
}
button[aria-selected="true"] {
    background-color: beige !important;
    color: #2E1F26 ;
    border-radius: 10px;
    padding: 10px 10px;
}
div[data-baseweb="tab-panel"]  {
    color: #F5E9DC;
}
div[data-baseweb="tab-panel"] a {
    color: #C87740 ;
}


</style>
""", unsafe_allow_html=True)
st.markdown("<h1 style = 'text-align:center;color: #02343F;background-color: #F0EDCC;font-size: 40px; font-weight: 700'>Voyage AI</h1>",unsafe_allow_html=True)
st.write("<h2 style = 'text-align:center;color: #F0EDCC;padding-top: 15px; font-size: 20px;font-weight:400'>Plan your perfect trip with AI Trip Planner and Explore the whole world with us !</h2>",unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Plan My Trip", "About", "Help"])
with tab1:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("images/photo1.jpg", width="stretch")

    with col2:
        st.image("images/photo2.jpg", width="stretch")

    with col3:
        st.image("images/photo3.jpg", width="stretch")

    st.markdown("---")
    st.markdown("<h1 style = 'text-align:center;color: #02343F;background-color: #F0EDCC;font-size: 25px; font-weight: 500;padding: 10px;'>Tell us about your Trip</h1>",unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        travel_date = st.date_input("Date of Travel")

    with col2:
        source = st.text_input("Starting City")

    with col3:
        destination = st.text_input("Destination City")

    with col4:
        day = st.number_input(
            "Number of Days",
            min_value=1,
            max_value=30,
            value=1
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        budget = st.number_input(
            "Budget",
            min_value=0.0,
            value=10000.0
        )

    with col2:
        interests = st.multiselect(
            "Interests",
            [
                "Adventure",
                "Historical exploration",
                "Food",
                "Culture",
                "Nature",
                "Relaxation",
                "Shopping",
                "Honeymoon",
                "Family trip",
            ]
        )

    with col3:
        travel_type = st.selectbox(
            "Travelling Type",
            ["Solo", "Partner", "Family/Friends"]
        )

    with col4:

        if travel_type == "Solo":
            num_travellers = 1
            st.text_input(
                "Travellers",
                value="1",
                disabled=True
            )

        elif travel_type == "Partner":
            num_travellers = 2
            st.text_input(
                "Travellers",
                value="2",
                disabled=True
            )

        else:
            num_travellers = st.number_input(
                "Number of Travellers",
                min_value=2,
                max_value=20,
                value=2
            )

    st.markdown("---")

    output = st.empty()

    if st.button("Plan My Trip", use_container_width=True):

        if not source or not destination:
            st.warning("Please enter both source and destination")

        else:

            with st.spinner("Generating your AI trip plan... This may take a moment..."):

                trip = {
                    "source": source,
                    "destination": destination,
                    "days": day,
                    "budget": budget,
                    "interests": interests,
                    "travel_type": travel_type,
                    "num_travellers": num_travellers,
                    "travel_date": str(travel_date)
                }

                result = generate_trip_plan(trip)

            with output.container():
                render_trip_plan(result, st)
with tab2:

    st.subheader("About Voyage AI 🌍")

    st.write("""
    Voyage AI is an AI-powered travel planning platform designed to create personalized and intelligent trip experiences. The application combines real-time travel data, weather forecasts, hotel recommendations, and flight information with AI-generated itineraries to help users plan smarter journeys effortlessly.

    ✨ Key Features:
    - AI-generated personalized travel itineraries
    - Real-time weather forecasting
    - Smart hotel recommendations
    - Flight search integration
    - Budget-based travel planning
    - Multi-interest trip customization
    - Interactive Streamlit dashboard UI

    ⚙️ Technologies Used:
    - Python
    - Streamlit
    - REST APIs
    - OpenAI SDK
    - HuggingFace Router
    - Qwen 2.5 72B LLM
    - Concurrent Programming with ThreadPoolExecutor
    - JSON Schema Validation & Repair Handling

    🔗 APIs Integrated:
    - Open-Meteo Weather API
    - Booking.com API
    - Skyscanner Flights API
    - AeroDataBox API

    🚀 Voyage AI uses intelligent prompt engineering, structured JSON generation, and modular backend architecture to deliver reliable and user-friendly AI travel planning experiences.
    """)
with tab3:

    st.subheader("Connect With Us")

    st.markdown("""

### 👨‍💻 Irfan Khan  
💼 LinkedIn: https://linkedin.com/in/irfan-khan-92185031b  
🔗 GitHub: https://github.com/Irfan-lab700  

### 👨‍💻 Raj Gaurav  
💼 LinkedIn: https://linkedin.com/in/yourprofile  
🔗 GitHub: https://github.com/Irfan-lab700  

---

💡 Built with Python • Streamlit • AI

""")

    

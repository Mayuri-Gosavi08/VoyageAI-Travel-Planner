
import json
import streamlit as st
import requests
import pandas as pd
from datetime import date, timedelta
from pathlib import Path
import os

# ============================================================
# CONFIG
# ============================================================
API_BASE_URL = "http://127.0.0.1:8000"
DATA_DIR = Path("data")  # put your CSVs inside a /data folder

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SESSION
# ============================================================
def init_session():
    defaults = {
        "token": None,
        "user_email": None,
        "page": "Login",
        "trip_budget": 15000,
        "slide_idx": 0,
        "plan_ready": False,
        "last_itinerary": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_csv(filename: str) -> pd.DataFrame:
    path = DATA_DIR / filename
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

def get_data() -> dict:
    return {
        "india": load_csv("india_destinations.csv"),
        "intl": load_csv("international_destinations.csv"),
        "restaurants": load_csv("restaurants.csv"),
        "weather": load_csv("weather_sample.csv"),
        "activities": load_csv("activity_cost.csv"),
        "attractions": load_csv("attractions.csv"),
    }

# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    with st.sidebar:
        st.markdown("## ✈️ AI Travel Planner")
        st.markdown("---")

        if st.session_state.token:
            st.success(f"Logged in as\n**{st.session_state.user_email}**")
            st.markdown("---")

            for page_name in ["Home", "Plan Trip", "My Trips", "Wishlist"]:
                if st.button(page_name, key=f"nav_{page_name}", use_container_width=True):
                    st.session_state.page = page_name
                    st.rerun()

            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.token = None
                st.session_state.user_email = None
                st.session_state.page = "Login"
                st.rerun()
        else:
            st.subheader("🔐 Login")
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True)

                if submitted:
                    if not email or not password:
                        st.error("Please enter email and password")
                    else:
                        try:
                            res = requests.post(
                                f"{API_BASE_URL}/login",
                                data={"username": email, "password": password},
                                timeout=10
                            )
                            data = res.json()
                            if res.status_code == 200 and "access_token" in data:
                                st.session_state.token = data["access_token"]
                                st.session_state.user_email = email
                                st.session_state.page = "Home"
                                st.rerun()
                            else:
                                st.error(data.get("detail", "Invalid email or password"))
                        except requests.exceptions.ConnectionError:
                            st.error("Backend not running. Start FastAPI first.")
                        except Exception as e:
                            st.error(f"Error: {e}")

            st.markdown("---")
            if st.button("📝 Create Account", use_container_width=True):
                st.session_state.page = "Register"
                st.rerun()

# ============================================================
# PAGES
# ============================================================
def page_login():
    st.markdown("<h1 style= 'color:black'>Welcome to AI Travel Planner</h1>",unsafe_allow_html=True)
    st.markdown("<style>.stApp { background-image: url('https://imgs.search.brave.com/Gyhv8_jd1kt-TsNqTWHvse6tBCV8rv6HjNzvhUJteEo/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudmVjdGVlenku/Y29tL3N5c3RlbS9y/ZXNvdXJjZXMvdGh1/bWJuYWlscy8wNDEv/NzYzLzI2Mi9zbWFs/bC90cmF2ZWwtYWNj/ZXNzb3JpZXMtb24t/Ymx1ZS1iYWNrZ3Jv/dW5kLXRyYXZlbC1j/b25jZXB0LXRvcC12/aWV3LXdpdGgtY29w/eS1zcGFjZS1waG90/by5qcGc'); background-size: cover; background-position: center; }</style>", unsafe_allow_html=True)
    st.info("Please login from the **sidebar** to continue.")
    # FOR BACK GROUND IMG AS PER CHOICE
# st.set_page_config(layout="wide")

# custom_css = """
# <style>
#     .stApp {
#         background-image: url('https://imgs.search.brave.com/6NpXRckpZIBoavVHq_km_wRsAp5aNHmiuY_DVZFH60g/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly90aHVt/YnMuZHJlYW1zdGlt/ZS5jb20vYi9jb2xs/YWdlLWZlYXR1cmVz/LXRyYXZlbC1pdGVt/cy1saWtlLWZsYWdz/LXBhc3Nwb3J0cy1z/dWl0Y2FzZXMtcGFz/dGVsLWJhY2tncm91/bmQtc3ltYm9saXpp/bmctYWR2ZW50dXJl/LWZlYXR1cmluZy1i/b2FyZGluZy0zNzQ2/NzEwODQuanBn');
#         background-size: cover;
#         background-position: center;
#         background-repeat: no-repeat;
#         height: 100vh;
#         position: relative;
#     }
#     .stApp::before {
#         content: "";
#         position: absolute;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         background-color: rgba(0, 0, 0, 0.5);  /* Optional overlay for text readability */
#         z-index: -1;
#     }
# </style>
# """

# st.markdown(custom_css, unsafe_allow_html=True)

def page_register():
    st.title("📝 Create New Account")
    st.markdown("Fill the form below to register")

    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Register", use_container_width=True)

        if submitted:
            if not name or not email or not password:
                st.error("All fields are required")
            elif password != confirm:
                st.error("Passwords do not match")
            else:
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/register",
                        json={"name": name, "email": email, "password": password},
                        timeout=10
                    )
                    data = res.json()
                    if res.status_code == 200 and "Successfully" in data.get("message", ""):
                        st.success("Account created successfully! Please login.")
                        st.session_state.page = "Login"
                        st.rerun()
                    else:
                        st.error(data.get("message", "Registration failed"))
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.button("← Back to Login"):
        st.session_state.page = "Login"
        st.rerun()

def page_home():
    # Background only on Home
    st.markdown("""
    <style>
        .stApp {
            background-image: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
                              url('https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1600');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .home-quote { text-align: center; color: white; padding: 2.5rem 1rem 1.5rem; }
        .home-quote h1 { font-size: 2.6rem; font-weight: 700; text-shadow: 2px 2px 8px rgba(0,0,0,0.6); }
        .home-quote p { font-size: 1.2rem; font-style: italic; opacity: 0.95; }
        .feature-card {
            background: rgba(255,255,255,0.93); border-radius: 14px;
            padding: 1.6rem 1.2rem; text-align: center;
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        }
        .welcome-text { text-align: center; color: white; font-size: 1.1rem; margin-bottom: 1.5rem; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="home-quote">
        <h1>🌍 Explore the World</h1>
        <p>"The journey of a thousand miles begins with a single step."</p>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user_email", "Traveler")
    st.markdown(f'<p class="welcome-text">Welcome back, <b>{user}</b> ✈️</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size:2.5rem;">🧭</div>
            <h3 style= 'color:black'>Plan a New Trip</h3>
            <p style= 'color:black'>AI itinerary based on your budget & interests</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Planning", key="btn_plan", use_container_width=True):
            st.session_state.page = "Plan Trip"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size:2.5rem;">❤️</div>
            <h3 style= 'color:black'>Wishlist</h3>
            <p style= 'color:black'>Save places you dream of visiting</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Wishlist", key="btn_wish", use_container_width=True):
            st.session_state.page = "Wishlist"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size:2.5rem;">🗺️</div>
            <h3 style= 'color:black'>My Journeys</h3>
            <p style= 'color:black'>See all your completed trips</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Journeys", key="btn_trips", use_container_width=True):
            st.session_state.page = "My Trips"
            st.rerun()

def page_wishlist():
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("## ❤️ My Wishlist")
        st.caption("Places you want to visit someday")
    with col2:
        if st.button("🏠 Home", key="wish_home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()

    st.markdown("---")
    st.info("Wishlist feature coming soon. You will be able to save destinations here.")

def page_plan_trip():
    data = get_data()

    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("## 🧭 Plan Your Trip")
        st.caption("Choose dates, destination & budget")
    with col2:
        if st.button("🏠 Home", key="plan_home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()

    st.markdown("---")

    # Dates
    c1, c2, c3 = st.columns(3)
    with c1:
        start_date = st.date_input("Start Date", value=date.today())
    with c2:
        end_date = st.date_input("End Date", value=date.today() + timedelta(days=5))
    with c3:
        auto_days = max((end_date - start_date).days, 1)
        days = st.slider("Days", 1, 30, min(auto_days, 30))

    # Destination
    trip_type = st.radio("Travel Type", ["Regional (India)", "International"], horizontal=True)
    selected_dest = None

    if trip_type == "Regional (India)":
        india = data["india"]
        if not india.empty:
            regions = ["All"] + sorted(india["region"].dropna().unique().tolist())
            region = st.selectbox("Region", regions)
            df = india if region == "All" else india[india["region"] == region]
            states = sorted(df["state"].dropna().unique().tolist())
            state = st.selectbox("State", states)
            cities = sorted(df[df["state"] == state]["name"].tolist())
            selected_dest = st.selectbox("Destination", cities)
        else:
            st.warning("India destinations CSV not found")
    else:
        intl = data["intl"]
        if not intl.empty:
            countries = sorted(intl["country"].dropna().unique().tolist())
            country = st.selectbox("Country", countries)
            cities = sorted(intl[intl["country"] == country]["name"].tolist())
            selected_dest = st.selectbox("Destination", cities)
        else:
            st.warning("International destinations CSV not found")

    # Budget
    b1, b2, b3, b4 = st.columns([1, 2, 1, 2])
    with b1:
        if st.button("➖ 1000", use_container_width=True):
            st.session_state.trip_budget = max(1000, st.session_state.trip_budget - 1000)
            st.rerun()
    with b2:
        budget = st.number_input(
            "Budget", min_value=1000, max_value=500000,
            value=st.session_state.trip_budget, step=1000,
            label_visibility="collapsed"
        )
        st.session_state.trip_budget = budget
    with b3:
        if st.button("➕ 1000", use_container_width=True):
            st.session_state.trip_budget += 1000
            st.rerun()
    with b4:
        st.metric("Budget", f"₹{st.session_state.trip_budget:,}")

    if st.session_state.trip_budget < 10000:
        budget_level = "low"
    elif st.session_state.trip_budget < 30000:
        budget_level = "medium"
    else:
        budget_level = "high"
    st.caption(f"Detected level: **{budget_level.upper()}**")

    interest = st.text_input("Interests", value="culture, food")

    if st.button("✨ Generate Plan", type="primary", use_container_width=True):
        if not selected_dest:
            st.warning("Please select a destination")
        else:
            st.session_state.plan_ready = True
            st.session_state.plan_dest = selected_dest
            st.session_state.plan_days = days
            st.session_state.plan_budget = st.session_state.trip_budget
            st.session_state.plan_interest = interest
            st.session_state.hotel_page = 0
            st.session_state.rest_page = 0

    # Results
    if st.session_state.get("plan_ready") and st.session_state.get("plan_dest"):
        dest = st.session_state.plan_dest
        days = st.session_state.plan_days
        budget = st.session_state.plan_budget

        st.markdown("---")
        st.subheader(f"📋 Plan for {dest} ({days} days) • ₹{budget:,}")

        # Weather
        with st.expander("🌤️ Weather", expanded=True):
            weather = data["weather"]
            if not weather.empty:
                wdf = weather[weather["city"].str.lower() == dest.lower()]
                if not wdf.empty:
                    st.dataframe(
                        wdf[["month", "avg_max_temp_c", "avg_min_temp_c", "condition", "good_time_to_visit"]],
                        use_container_width=True, hide_index=True
                    )
                else:
                    st.info(f"No weather data for {dest}")
            else:
                st.warning("Weather CSV not found")

        # Activities
        with st.expander("🎯 Experiences & Activities"):
            acts = data["activities"]
            if not acts.empty:
                adf = acts[acts["destination_name"].str.lower() == dest.lower()]
                if not adf.empty:
                    page = st.session_state.get("hotel_page", 0)
                    chunk = adf.iloc[page*5 : page*5+5]
                    for _, row in chunk.iterrows():
                        st.write(f"**{row['activity_name']}** ({row['category']}) — ₹{row['cost_per_person_inr']:,.0f}")
                    c1, c2 = st.columns(2)
                    with c1:
                        if page > 0 and st.button("← Prev", key="act_prev"):
                            st.session_state.hotel_page = page - 1
                            st.rerun()
                    with c2:
                        if (page+1)*5 < len(adf) and st.button("Next →", key="act_next"):
                            st.session_state.hotel_page = page + 1
                            st.rerun()
                else:
                    st.info(f"No activities found for {dest}")

        # Restaurants
        with st.expander("🍽️ Restaurants"):
            rests = data["restaurants"]
            if not rests.empty:
                rdf = rests[rests["city"].str.lower() == dest.lower()]
                if rdf.empty:
                    rdf = rests[rests["city"].str.lower().str.contains(dest.lower()[:4], na=False)]
                if not rdf.empty:
                    rdf = rdf.sort_values("rating", ascending=False)
                    page = st.session_state.get("rest_page", 0)
                    chunk = rdf.iloc[page*5 : page*5+5]
                    for _, row in chunk.iterrows():
                        st.write(f"**{row['name']}** — {row['cuisine_type']} | ⭐ {row['rating']} | ₹{row['cost_for_two_inr']:,.0f} for two")
                    c1, c2 = st.columns(2)
                    with c1:
                        if page > 0 and st.button("← Prev", key="rest_prev"):
                            st.session_state.rest_page = page - 1
                            st.rerun()
                    with c2:
                        if (page+1)*5 < len(rdf) and st.button("Next →", key="rest_next"):
                            st.session_state.rest_page = page + 1
                            st.rerun()
                else:
                    st.info(f"No restaurants found for {dest}")

        # AI Itinerary
        with st.expander("📜 AI Itinerary (Gemini)", expanded=True):
            if st.button("🤖 Generate Itinerary", use_container_width=True):
                if not st.session_state.token:
                    st.error("Please login first")
                else:
                    with st.spinner("Generating itinerary..."):
                        try:
                            res = requests.post(
                                f"{API_BASE_URL}/plan-trip",
                                json={
                                    "destination": dest,
                                    "days": int(days),
                                    "budget": budget_level,
                                    "interest": st.session_state.plan_interest
                                },
                                headers={"Authorization": f"Bearer {st.session_state.token}"},
                                timeout=90
                            )
                            if res.status_code == 200:
                                st.session_state.last_itinerary = res.json().get("itinerary", "")
                                st.success("Itinerary generated and saved!")
                            else:
                                st.error(res.json().get("detail", "Failed to generate"))
                        except Exception as e:
                            st.error(str(e))

            if st.session_state.get("last_itinerary"):
                st.text_area("Your Itinerary", st.session_state.last_itinerary, height=300)
                st.download_button(
                    "⬇️ Download",
                    data=st.session_state.last_itinerary,
                    file_name=f"itinerary_{dest}.txt",
                    mime="text/plain"
                )

def page_my_trips():

    col1, col2 = st.columns([5, 1])

    with col1:
        st.markdown("## 🧳 My Trips")
        st.caption("Your saved AI-generated travel plans")

    with col2:
        if st.button("🏠 Home", key="trips_home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()

    st.markdown("---")

    # Check login
    if not st.session_state.get("token"):
        st.warning("Please login first.")
        return

    # Get trips from backend
    try:
        res = requests.get(
            f"{API_BASE_URL}/my-trips",
            headers={
                "Authorization": f"Bearer {st.session_state.token}"
            },
            timeout=10
        )

        if res.status_code == 200:

            trips = res.json()

            if not trips:
                st.info(
                    "You haven't generated any trips yet. "
                    "Start planning your first trip! ✈️"
                )
                return

            st.success(f"Found {len(trips)} saved trip(s)!")

            for trip in trips:

                destination = trip.get("destination", "Unknown")
                days = trip.get("days", 0)
                budget = trip.get("budget", "N/A")
                itinerary = trip.get("itinerary", "")
                trip_id = trip.get("id", "unknown")

                # Backend stores itinerary as a string.
                # If it happens to be a dictionary, convert it to text.
                if isinstance(itinerary, dict):
                    itinerary = json.dumps(
                        itinerary,
                        indent=4,
                        ensure_ascii=False
                    )
                else:
                    itinerary = str(itinerary)

                with st.expander(
                    f"🌍 {destination} • {days} days • ₹{budget}"
                ):

                    st.write("### 📋 AI Generated Itinerary")

                    st.text_area(
                        "Itinerary",
                        itinerary,
                        height=400,
                        key=f"itinerary_{trip_id}"
                    )

                    st.download_button(
                        "⬇️ Download Itinerary",
                        data=itinerary.encode("utf-8"),
                        file_name=f"itinerary_{destination}.txt",
                        mime="text/plain",
                        key=f"download_{trip_id}"
                    )

        elif res.status_code == 401:
            st.error("Your login session has expired. Please login again.")

        else:
            st.error(
                f"Failed to load trips. "
                f"Backend returned status {res.status_code}."
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Backend is not running. "
            "Please start FastAPI first."
        )

    except Exception as e:
        st.error(f"❌ Error loading trips: {e}")
        
        
# ============================================================
# MAIN
# ============================================================
def main():
    init_session()
    render_sidebar()

    # Clear background on non-Home pages
    if st.session_state.page != "Home":
        st.markdown("<style>.stApp { background-image: none; }</style>", unsafe_allow_html=True)

    page = st.session_state.page

    if page == "Login":
        page_login()
    elif page == "Register":
        page_register()
    elif page == "Home":
        page_home()
    elif page == "Plan Trip":
        page_plan_trip()
    elif page == "My Trips":
        page_my_trips()
    elif page == "Wishlist":
        page_wishlist()
    else:
        page_login()

if __name__ == "__main__":
    main()

import html
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

# ============================================================
# CONFIG
# ============================================================
API_BASE_URL = "http://127.0.0.1:8000"
DATA_DIR = Path("data")

st.set_page_config(
    page_title="Voyage AI — Travel, Reimagined",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# MODERN UI
# ============================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root{
    --bg:#06101d;
    --bg2:#091827;
    --panel:rgba(15,29,46,.78);
    --panel2:rgba(18,38,58,.92);
    --line:rgba(255,255,255,.09);
    --text:#f6f8fb;
    --muted:#94a4b7;
    --mint:#64e5a1;
    --cyan:#62d9ff;
    --blue:#7394ff;
}

html, body, [class*="css"]{
    font-family:'DM Sans',sans-serif;
}

.stApp{
    background:
        radial-gradient(circle at 85% 5%, rgba(71,148,255,.18), transparent 28%),
        radial-gradient(circle at 8% 30%, rgba(67,224,167,.12), transparent 26%),
        linear-gradient(135deg,#050c16 0%,#071321 50%,#0a1a29 100%);
    color:var(--text);
}

.main .block-container{
    max-width:1480px;
    padding:28px 42px 60px;
}

header[data-testid="stHeader"]{
    background:transparent;
}

#MainMenu, footer { visibility:hidden; }

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"]{
    background:
        linear-gradient(180deg,rgba(8,17,29,.98),rgba(5,13,23,.98));
    border-right:1px solid rgba(255,255,255,.07);
}

section[data-testid="stSidebar"] > div{
    padding:22px 16px;
}

section[data-testid="stSidebar"] *{
    color:#dce7f2;
}

.brand{
    display:flex;
    align-items:center;
    gap:11px;
    padding:4px 8px 20px;
}

.brand-mark{
    width:40px;
    height:40px;
    border-radius:13px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#65e6a1,#58bfff);
    color:#06111d;
    font-size:20px;
    box-shadow:0 10px 30px rgba(76,224,166,.18);
}

.brand-name{
    font-weight:800;
    font-size:18px;
    letter-spacing:-.4px;
}

.brand-sub{
    color:#71839a;
    font-size:10px;
    letter-spacing:1.5px;
    text-transform:uppercase;
    margin-top:2px;
}

.nav-label{
    color:#5e728a;
    font-size:10px;
    font-weight:800;
    letter-spacing:1.7px;
    text-transform:uppercase;
    margin:22px 8px 8px;
}

section[data-testid="stSidebar"] .stButton > button{
    background:transparent;
    border:1px solid transparent;
    color:#aebdcd;
    text-align:left;
    justify-content:flex-start;
    border-radius:11px;
    min-height:42px;
    padding-left:12px;
    transition:.2s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover{
    background:rgba(255,255,255,.055);
    border-color:rgba(255,255,255,.06);
    color:#fff;
    transform:translateX(2px);
}

.user-chip{
    margin:4px 2px 18px;
    padding:13px;
    border:1px solid rgba(100,229,161,.12);
    background:rgba(100,229,161,.045);
    border-radius:14px;
}

.user-chip small{
    color:#6f8797;
    display:block;
    font-size:9px;
    letter-spacing:1.4px;
    font-weight:800;
}

.user-chip div{
    color:#dfeaf3;
    font-size:12px;
    margin-top:4px;
    overflow:hidden;
    text-overflow:ellipsis;
}

/* ---------- TOP PILL ---------- */
.topline{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:18px;
}

.pill{
    display:inline-flex;
    align-items:center;
    gap:7px;
    border:1px solid rgba(100,229,161,.16);
    background:rgba(100,229,161,.055);
    color:#9ae8bd;
    border-radius:999px;
    padding:7px 11px;
    font-size:10px;
    font-weight:800;
    letter-spacing:1.2px;
    text-transform:uppercase;
}

/* ---------- HERO ---------- */
.hero{
    position:relative;
    overflow:hidden;
    min-height:445px;
    border-radius:28px;
    border:1px solid rgba(255,255,255,.10);
    box-shadow:0 30px 80px rgba(0,0,0,.32);
    background-image:
        linear-gradient(90deg,rgba(3,10,18,.96) 0%,rgba(4,13,23,.82) 42%,rgba(4,13,23,.18) 100%),
        linear-gradient(180deg,rgba(4,11,19,.04),rgba(4,11,19,.62)),
        url("https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1800&q=88");
    background-size:cover;
    background-position:center;
    padding:52px 58px;
}

.hero:after{
    content:"";
    position:absolute;
    inset:auto -10% -45% 40%;
    height:380px;
    background:radial-gradient(circle,rgba(93,220,255,.22),transparent 65%);
    pointer-events:none;
}

.hero-copy{
    position:relative;
    z-index:2;
    max-width:720px;
}

.eyebrow{
    color:#83e5ad;
    font-size:10px;
    font-weight:800;
    letter-spacing:2.2px;
    text-transform:uppercase;
    margin-bottom:17px;
}

.hero h1{
    font-family:'Playfair Display',Georgia,serif;
    font-size:clamp(3rem,6vw,5.8rem);
    line-height:.98;
    letter-spacing:-2.5px;
    margin:0 0 22px;
    color:#fff;
}

.hero h1 span{
    color:#73e6ac;
}

.hero p{
    color:#b9c8d7;
    max-width:600px;
    font-size:15px;
    line-height:1.75;
    margin:0;
}

.hero-tags{
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    margin-top:26px;
}

.hero-tag{
    padding:8px 12px;
    border-radius:999px;
    border:1px solid rgba(255,255,255,.11);
    background:rgba(4,13,23,.42);
    backdrop-filter:blur(10px);
    color:#d7e4ee;
    font-size:11px;
}

/* ---------- SECTION ---------- */
.section-head{
    display:flex;
    justify-content:space-between;
    align-items:end;
    margin:38px 0 15px;
}

.section-head h2{
    margin:0;
    font-size:22px;
    letter-spacing:-.5px;
    color:#f4f7fb;
}

.section-head p{
    margin:5px 0 0;
    color:#72869c;
    font-size:12px;
}

/* ---------- FEATURE CARDS ---------- */
.feature{
    position:relative;
    min-height:185px;
    padding:24px;
    border-radius:20px;
    background:linear-gradient(145deg,rgba(18,36,54,.92),rgba(9,22,35,.92));
    border:1px solid var(--line);
    box-shadow:0 15px 40px rgba(0,0,0,.18);
    overflow:hidden;
    transition:.22s ease;
}

.feature:hover{
    transform:translateY(-4px);
    border-color:rgba(100,229,161,.22);
    box-shadow:0 24px 55px rgba(0,0,0,.27);
}

.feature:after{
    content:"";
    position:absolute;
    right:-35px;
    bottom:-55px;
    width:140px;
    height:140px;
    border-radius:50%;
    background:rgba(87,214,255,.08);
}

.feature-icon{
    width:43px;
    height:43px;
    border-radius:13px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:rgba(100,229,161,.08);
    border:1px solid rgba(100,229,161,.13);
    font-size:20px;
    margin-bottom:18px;
}

.feature h3{
    margin:0 0 8px;
    font-size:16px;
    color:#f4f7fb;
}

.feature p{
    margin:0;
    color:#8497ab;
    font-size:12px;
    line-height:1.65;
}

/* ---------- AGENT CARDS ---------- */
.agent{
    min-height:132px;
    padding:18px;
    border-radius:17px;
    background:rgba(11,27,43,.72);
    border:1px solid rgba(255,255,255,.07);
}

.agent-icon{
    font-size:18px;
    margin-bottom:9px;
}

.agent h4{
    margin:0 0 5px;
    color:#edf4fa;
    font-size:13px;
}

.agent p{
    margin:0;
    color:#70859a;
    font-size:10px;
    line-height:1.5;
}

.ready{
    display:inline-block;
    margin-top:9px;
    color:#6fe5a7;
    font-size:8px;
    font-weight:900;
    letter-spacing:1.2px;
}

/* ---------- QUICK ACTION ---------- */
.action-card{
    min-height:90px;
    padding:19px;
    border-radius:17px;
    background:rgba(12,28,44,.72);
    border:1px solid rgba(255,255,255,.07);
}

/* ---------- BUTTONS ---------- */
.stButton > button{
    border-radius:12px !important;
    min-height:43px;
    font-weight:700;
    border:1px solid rgba(255,255,255,.09);
    background:rgba(255,255,255,.045);
    color:#dce7f0;
    transition:.2s ease;
}

.stButton > button:hover{
    border-color:rgba(100,229,161,.30);
    color:#fff;
    transform:translateY(-1px);
}

.stButton > button[kind="primary"]{
    background:linear-gradient(135deg,#4edb99,#63cfff) !important;
    color:#05111b !important;
    border:none !important;
    box-shadow:0 12px 30px rgba(78,219,153,.18);
}

/* ---------- INPUTS ---------- */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div{
    background:rgba(7,18,30,.72) !important;
    color:#edf5fb !important;
    border:1px solid rgba(255,255,255,.09) !important;
    border-radius:12px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus{
    border-color:rgba(100,229,161,.45) !important;
    box-shadow:0 0 0 1px rgba(100,229,161,.12) !important;
}

label, .stSlider label{
    color:#aebdcb !important;
}

/* ---------- PLAN STUDIO ---------- */
.studio{
    padding:26px;
    border-radius:24px;
    background:linear-gradient(145deg,rgba(16,34,52,.9),rgba(8,20,33,.88));
    border:1px solid rgba(255,255,255,.08);
    box-shadow:0 25px 60px rgba(0,0,0,.20);
}

.studio-title{
    font-family:'Playfair Display',Georgia,serif;
    color:#fff;
    font-size:32px;
    margin-bottom:5px;
}

.studio-sub{
    color:#8094a9;
    font-size:12px;
    margin-bottom:22px;
}

/* ---------- ITINERARY ---------- */
.trip-hero{
    padding:30px;
    border-radius:24px;
    background:
        linear-gradient(90deg,rgba(5,15,25,.97),rgba(8,25,37,.80)),
        url("https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1600&q=85");
    background-size:cover;
    background-position:center;
    border:1px solid rgba(255,255,255,.09);
}

.trip-hero h1{
    font-family:'Playfair Display',Georgia,serif;
    margin:5px 0;
    color:#fff;
    font-size:38px;
}

.trip-hero p{
    color:#9eb0c1;
    margin:0;
}

.day-card{
    margin:16px 0;
    padding:22px;
    border-radius:20px;
    background:rgba(12,29,45,.78);
    border:1px solid rgba(255,255,255,.08);
}

.day-number{
    color:#6fe4a6;
    font-size:10px;
    font-weight:900;
    letter-spacing:1.5px;
    text-transform:uppercase;
}

.day-card h3{
    color:#f2f7fb;
    margin:6px 0 16px;
    font-size:19px;
}

.activity{
    padding:13px 15px;
    margin:8px 0;
    border-radius:13px;
    background:rgba(255,255,255,.035);
    border:1px solid rgba(255,255,255,.055);
}

.activity strong{
    color:#e8f0f6;
    font-size:12px;
}

.activity p{
    color:#7f93a7;
    font-size:11px;
    line-height:1.55;
    margin:5px 0 0;
}

/* ---------- TRIP / WISHLIST CARDS ---------- */
.place-card{
    min-height:245px;
    border-radius:21px;
    overflow:hidden;
    position:relative;
    border:1px solid rgba(255,255,255,.09);
    background-size:cover;
    background-position:center;
    box-shadow:0 18px 45px rgba(0,0,0,.24);
}

.place-overlay{
    position:absolute;
    inset:0;
    display:flex;
    flex-direction:column;
    justify-content:flex-end;
    padding:20px;
    background:linear-gradient(transparent 20%,rgba(3,9,16,.92) 100%);
}

.place-overlay h3{
    color:#fff;
    margin:0 0 5px;
    font-size:19px;
}

.place-overlay p{
    color:#aabaca;
    margin:0;
    font-size:11px;
}

/* ---------- ALERTS ---------- */
div[data-testid="stAlert"]{
    border-radius:13px;
}

/* ---------- MOBILE ---------- */
@media(max-width:900px){
    .main .block-container{padding:20px 18px 45px;}
    .hero{padding:34px 26px;min-height:390px;}
    .hero h1{font-size:3rem;}
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SESSION
# ============================================================
def init_session():
    defaults = {
        "token": None,
        "user_email": None,
        "page": "Login",
        "plan_dest": "",
        "plan_days": 5,
        "plan_budget": 15000,
        "plan_interest": "culture, food",
        "travel_group": "Solo",
        "travel_vibe": "Foodie",
        "adventure_level": 3,
        "last_itinerary": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go(page):
    st.session_state.page = page
    st.rerun()


def auth_headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


# ============================================================
# DATA
# ============================================================
@st.cache_data
def load_csv(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def get_destinations():
    frames = [load_csv("india_destinations.csv"), load_csv("international_destinations.csv")]
    frames = [x for x in frames if not x.empty]
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def destination_image(name):
    images = {
        "Goa": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=900&q=85",
        "Kerala": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=900&q=85",
        "Jaipur": "https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=900&q=85",
        "Paris": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=900&q=85",
        "Bali": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=900&q=85",
        "Dubai": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=900&q=85",
        "London": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=900&q=85",
        "Manali": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=900&q=85",
    }
    for key, url in images.items():
        if key.lower() in str(name).lower():
            return url
    return "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=85"


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-mark">✈</div>
                <div>
                    <div class="brand-name">Voyage AI</div>
                    <div class="brand-sub">Intelligent travel</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.token:
            email = html.escape(st.session_state.get("user_email") or "Traveler")
            st.markdown(
                f"""
                <div class="user-chip">
                    <small>TRAVELER</small>
                    <div>{email}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown('<div class="nav-label">Explore</div>', unsafe_allow_html=True)

            if st.button("⌂   Home", use_container_width=True):
                go("Home")
            if st.button("✦   Plan Trip", use_container_width=True):
                go("Plan Trip")
            if st.button("◈   My Trips", use_container_width=True):
                go("My Trips")
            if st.button("♡   Wishlist", use_container_width=True):
                go("Wishlist")

            st.markdown('<div class="nav-label">AI toolkit</div>', unsafe_allow_html=True)
            st.caption("🧠  Preference Intelligence")
            st.caption("💰  Budget Optimization")
            st.caption("🌦️  Weather Awareness")
            st.caption("🗺️  Smart Itinerary")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("↪   Sign out", use_container_width=True):
                st.session_state.token = None
                st.session_state.user_email = None
                st.session_state.page = "Login"
                st.session_state.last_itinerary = None
                st.rerun()
        else:
            st.markdown('<div class="nav-label">Welcome</div>', unsafe_allow_html=True)
            st.caption("Sign in to unlock your AI travel studio.")


# ============================================================
# AUTH
# ============================================================
def page_login():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-copy">
                <div class="eyebrow">✦ AI TRAVEL COMPANION</div>
                <h1>Travel smarter.<br><span>Explore further.</span></h1>
                <p>
                    Voyage AI turns your interests, budget and travel style
                    into a beautifully structured journey designed around you.
                </p>
                <div class="hero-tags">
                    <span class="hero-tag">🧠 Personalized AI</span>
                    <span class="hero-tag">💰 Budget-aware</span>
                    <span class="hero-tag">🗺️ Day-by-day plans</span>
                    <span class="hero-tag">✨ Built for you</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-head"><div><h2>Welcome back</h2><p>Sign in and continue planning.</p></div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.15, .85], gap="large")

    with c1:
        st.markdown(
            """
            <div class="feature">
                <div class="feature-icon">✈️</div>
                <h3>Your personal travel studio</h3>
                <p>Plan destinations, budgets and experiences in one calm, intelligent workspace.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        with st.form("login_form"):
            st.markdown("#### 🔐 Sign in")
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Continue to Voyage AI  →", type="primary", use_container_width=True)

            if submitted:
                if not email or not password:
                    st.error("Please enter your email and password.")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/login",
                            data={"username": email, "password": password},
                            timeout=10,
                        )
                        result = response.json()
                        if response.status_code == 200 and "access_token" in result:
                            st.session_state.token = result["access_token"]
                            st.session_state.user_email = email
                            st.session_state.page = "Home"
                            st.rerun()
                        else:
                            st.error(result.get("detail", "Invalid email or password."))
                    except requests.exceptions.ConnectionError:
                        st.error("Backend is not running. Start FastAPI on port 8000.")
                    except Exception as exc:
                        st.error(f"Login error: {exc}")

        if st.button("Create a new account", use_container_width=True):
            go("Register")


def page_register():
    st.markdown(
        """
        <div class="trip-hero">
            <div class="eyebrow">✦ VOYAGE AI</div>
            <h1>Create your travel account.</h1>
            <p>One account. Smarter journeys. Better adventures.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("register_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
        with c2:
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")

        submitted = st.form_submit_button("Create Account  →", type="primary", use_container_width=True)

        if submitted:
            if not name or not email or not password:
                st.error("All fields are required.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/register",
                        json={"name": name, "email": email, "password": password},
                        timeout=10,
                    )
                    result = response.json()
                    if response.status_code in (200, 201):
                        st.success("Account created successfully. You can sign in now.")
                        st.session_state.page = "Login"
                    else:
                        st.error(result.get("detail", "Registration failed."))
                except requests.exceptions.ConnectionError:
                    st.error("Backend is not running.")
                except Exception as exc:
                    st.error(f"Registration error: {exc}")

    if st.button("← Back to sign in"):
        go("Login")


# ============================================================
# HOME
# ============================================================
def page_home():
    user = html.escape(st.session_state.get("user_email") or "Traveler")

    st.markdown(
        f"""
        <div class="topline">
            <span class="pill">● AI travel studio</span>
            <span style="color:#71869b;font-size:11px;">Welcome, {user}</span>
        </div>

        <div class="hero">
            <div class="hero-copy">
                <div class="eyebrow">✦ YOUR NEXT ADVENTURE</div>
                <h1>Travel smarter.<br><span>Explore further.</span></h1>
                <p>
                    Tell Voyage AI where you want to go and what you love.
                    We'll shape it into a journey that feels uniquely yours.
                </p>
                <div class="hero-tags">
                    <span class="hero-tag">🌍 Any destination</span>
                    <span class="hero-tag">💳 Any budget</span>
                    <span class="hero-tag">🧭 Your travel style</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
    with c1:
        if st.button("✦  Plan my trip", type="primary", use_container_width=True):
            go("Plan Trip")
    with c2:
        if st.button("♡  Explore wishlist", use_container_width=True):
            go("Wishlist")
    with c3:
        if st.button("◈  View my journeys", use_container_width=True):
            go("My Trips")

    st.markdown(
        '<div class="section-head"><div><h2>Everything you need to travel better</h2><p>One intelligent companion from idea to itinerary.</p></div></div>',
        unsafe_allow_html=True,
    )

    cards = [
        ("🧠", "Personalized AI", "Your interests and travel style shape every recommendation."),
        ("💰", "Budget Smart", "Keep the experience meaningful while staying budget-aware."),
        ("🌦️", "Weather Aware", "Use available travel data to make smarter decisions."),
        ("🗺️", "Smart Itinerary", "Turn a destination into a clear day-by-day journey."),
    ]
    cols = st.columns(4, gap="medium")
    for col, (icon, title, text) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="feature">
                    <div class="feature-icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-head"><div><h2>Your AI travel team</h2><p>Multiple intelligent roles working behind one simple experience.</p></div></div>',
        unsafe_allow_html=True,
    )

    agents = [
        ("🧠", "Preference Analyst", "Understands what matters most."),
        ("⚖️", "Conflict Resolver", "Balances group preferences."),
        ("💰", "Budget Optimizer", "Keeps the plan budget-aware."),
        ("🔎", "Destination Researcher", "Works with destination information."),
        ("🗺️", "Itinerary Architect", "Builds the final journey."),
    ]
    cols = st.columns(5, gap="small")
    for col, (icon, title, text) in zip(cols, agents):
        with col:
            st.markdown(
                f"""
                <div class="agent">
                    <div class="agent-icon">{icon}</div>
                    <h4>{title}</h4>
                    <p>{text}</p>
                    <span class="ready">● READY</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# PLAN TRIP
# ============================================================
def page_plan_trip():
    st.markdown(
        """
        <div class="topline"><span class="pill">✦ AI trip studio</span></div>
        <div class="studio">
            <div class="eyebrow">BUILD YOUR JOURNEY</div>
            <div class="studio-title">Where will you go next?</div>
            <div class="studio-sub">Give Voyage AI a few details. We'll take care of the planning.</div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        destination = st.text_input(
            "🌍 Destination",
            value=st.session_state.get("plan_dest", ""),
            placeholder="Goa, Kerala, Paris...",
        )
        days = st.number_input(
            "📅 Number of Days",
            min_value=1,
            max_value=30,
            value=int(st.session_state.get("plan_days", 5)),
        )
        budget = st.number_input(
            "💰 Budget (₹)",
            min_value=1000,
            max_value=10000000,
            value=int(st.session_state.get("plan_budget", 15000)),
            step=1000,
        )

    with c2:
        interest = st.text_input(
            "♡ Interests",
            value=st.session_state.get("plan_interest", "culture, food"),
            placeholder="food, beaches, culture, shopping...",
        )
        travel_group = st.selectbox(
            "👥 Travel Group",
            ["Solo", "Couple", "Family", "Friends"],
            index=["Solo", "Couple", "Family", "Friends"].index(
                st.session_state.get("travel_group", "Solo")
            ),
        )
        vibe = st.selectbox(
            "✦ Travel Vibe",
            ["Foodie", "Relaxing", "Adventure", "Cultural", "Luxury", "Budget"],
            index=["Foodie", "Relaxing", "Adventure", "Cultural", "Luxury", "Budget"].index(
                st.session_state.get("travel_vibe", "Foodie")
            ),
        )

    adventure = st.slider(
        "🔥 Adventure Level",
        min_value=1,
        max_value=5,
        value=int(st.session_state.get("adventure_level", 3)),
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✦  GENERATE MY AI JOURNEY", type="primary", use_container_width=True):
        if not destination.strip():
            st.warning("Please enter a destination.")
        elif not interest.strip():
            st.warning("Please enter at least one interest.")
        else:
            st.session_state.plan_dest = destination.strip()
            st.session_state.plan_days = days
            st.session_state.plan_budget = budget
            st.session_state.plan_interest = interest.strip()
            st.session_state.travel_group = travel_group
            st.session_state.travel_vibe = vibe
            st.session_state.adventure_level = adventure

            # The current backend schema expects exactly:
            # destination: str, days: int, budget: str, interest: str
            # Extra UI preferences are folded into the interest string.
            enriched_interest = (
                f"{interest.strip()}; "
                f"travel group: {travel_group}; "
                f"travel vibe: {vibe}; "
                f"adventure level: {adventure}"
            )

            payload = {
                "destination": destination.strip(),
                "days": int(days),
                "budget": str(int(budget)),
                "interest": enriched_interest,
            }

            with st.spinner("✦ Voyage AI is designing your journey..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/plan-trip",
                        json=payload,
                        headers=auth_headers(),
                        timeout=120,
                    )

                    if response.status_code == 200:
                        st.session_state.last_itinerary = response.json()
                        st.success("Your personalized journey is ready ✦")
                        st.rerun()
                    elif response.status_code in (401, 403):
                        st.error("Your session has expired. Please sign in again.")
                    else:
                        try:
                            detail = response.json()
                        except Exception:
                            detail = response.text
                        st.error(f"Backend error ({response.status_code})")
                        st.code(str(detail))

                except requests.exceptions.ConnectionError:
                    st.error("Backend is not running. Start FastAPI on port 8000.")
                except requests.exceptions.Timeout:
                    st.error("The AI took too long to respond. Please try again.")
                except Exception as exc:
                    st.error(f"Error generating itinerary: {exc}")

    itinerary = st.session_state.get("last_itinerary")
    if itinerary:
        render_itinerary(itinerary)

# ============================================================
# ITINERARY
# ============================================================

def render_itinerary(itinerary):
    if not isinstance(itinerary, dict):
        st.write(itinerary)
        return

    # --------------------------------------------------------
    # BACKEND KA ACTUAL TRIP DATA
    # --------------------------------------------------------

    trip = itinerary.get("itinerary")

    if not isinstance(trip, dict):
        trip = itinerary

    title = (
        trip.get("title")
        or trip.get("trip_name")
        or trip.get("destination")
        or itinerary.get("destination")
        or st.session_state.get("plan_dest")
        or "Your Journey"
    )

    budget = (
        trip.get("budget")
        or itinerary.get("budget")
        or st.session_state.get("plan_budget")
        or "—"
    )

    days = (
        trip.get("days")
        or itinerary.get("days")
        or st.session_state.get("plan_days")
        or "—"
    )

    weather = trip.get("weather") or {}

    ai_response = (
        trip.get("response")
        or trip.get("ai_response")
        or itinerary.get("response")
        or itinerary.get("ai_response")
        or ""
    )

    budget_response = (
        trip.get("budget_response")
        or trip.get("budget_analysis")
        or itinerary.get("budget_response")
        or ""
    )

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        "### ✦ PERSONALIZED JOURNEY"
    )

    st.title(
        f"✈️ {title}"
    )

    st.caption(
        f"{days} days  •  ₹{budget} budget  •  Built by Voyage AI"
    )

    # --------------------------------------------------------
    # SUMMARY CARDS
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "📅 DURATION",
            f"{days} Days"
        )

    with c2:
        st.metric(
            "💰 BUDGET",
            f"₹{budget}"
        )

    with c3:

        temperature = "—"
        condition = "Not available"

        if isinstance(weather, dict):

            temperature = (
                weather.get("temperature")
                or weather.get("temp")
                or "—"
            )

            condition = (
                weather.get("weather")
                or weather.get("condition")
                or weather.get("description")
                or "Not available"
            )

        st.metric(
            "🌤️ WEATHER",
            f"{temperature}°C"
        )

        st.caption(
            str(condition).title()
        )

    # ========================================================
    # WEATHER SNAPSHOT
    # ========================================================

    if isinstance(weather, dict) and weather:

        st.markdown(
            "### ✦ WEATHER SNAPSHOT"
        )

        city = (
            weather.get("city")
            or weather.get("location")
            or str(title)
        )

        temperature = (
            weather.get("temperature")
            or weather.get("temp")
            or "—"
        )

        condition = (
            weather.get("weather")
            or weather.get("condition")
            or weather.get("description")
            or "Not available"
        )

        humidity = weather.get("humidity")

        wind = (
            weather.get("wind")
            or weather.get("wind_speed")
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write("📍 **City**")
            st.write(str(city))

        with col2:

            st.write("🌡️ **Temperature**")
            st.write(f"{temperature}°C")

        with col3:

            st.write("☁️ **Condition**")
            st.write(
                str(condition).title()
            )

        if humidity is not None or wind is not None:

            col4, col5 = st.columns(2)

            with col4:

                if humidity is not None:

                    st.write("💧 **Humidity**")
                    st.write(str(humidity))

            with col5:

                if wind is not None:

                    st.write("💨 **Wind**")
                    st.write(str(wind))

    # ========================================================
    # AI TRAVEL GUIDE
    # ========================================================

    if ai_response:

        st.markdown(
            "### ✦ AI TRAVEL GUIDE"
        )

        response_text = (
            str(ai_response)
            .replace("\\n", "\n")
        )

        with st.container(border=True):

            st.markdown(
                "🤖 **VOYAGE AI RECOMMENDATIONS**"
            )

            st.markdown(
                response_text
            )

    # ========================================================
    # SMART BUDGET ANALYSIS
    # ========================================================

    if budget_response:

        st.markdown(
            "### ✦ SMART BUDGET ANALYSIS"
        )

        budget_text = (
            str(budget_response)
            .replace("\\n", "\n")
        )

        with st.container(border=True):

            st.markdown(
                "💰 **BUDGET INTELLIGENCE**"
            )

            st.markdown(
                budget_text
            )

    # ========================================================
    # DAY-BY-DAY ITINERARY
    # ========================================================

    days_data = (
        trip.get("days_data")
        or trip.get("day_wise_itinerary")
        or trip.get("plan")
    )

    # Backend may return itinerary as a list
    if days_data is None:

        candidate = trip.get("itinerary")

        if isinstance(candidate, list):

            days_data = candidate

    # Backend may return days as a list
    if days_data is None:

        candidate = trip.get("days")

        if isinstance(candidate, list):

            days_data = candidate

    # --------------------------------------------------------
    # RENDER DAYS
    # --------------------------------------------------------

    if isinstance(days_data, list):

        st.markdown(
            "### ✦ DAY-BY-DAY ITINERARY"
        )

        for index, day in enumerate(
            days_data,
            1
        ):

            # ------------------------------------------------
            # DAY IS DICT
            # ------------------------------------------------

            if isinstance(day, dict):

                day_title = (
                    day.get("title")
                    or day.get("name")
                    or day.get("day")
                    or f"Day {index}"
                )

                activities = (
                    day.get("activities")
                    or day.get("plans")
                    or day.get("items")
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### DAY {index:02d} — {day_title}"
                    )

                    # ----------------------------------------
                    # ACTIVITIES
                    # ----------------------------------------

                    if isinstance(
                        activities,
                        list
                    ):

                        for activity in activities:

                            if isinstance(
                                activity,
                                dict
                            ):

                                name = (
                                    activity.get("name")
                                    or activity.get("title")
                                    or activity.get("activity")
                                    or "Activity"
                                )

                                description = (
                                    activity.get("description")
                                    or activity.get("details")
                                    or activity.get("location")
                                    or ""
                                )

                                st.markdown(
                                    f"📍 **{name}**"
                                )

                                if description:

                                    st.write(
                                        description
                                    )

                            else:

                                st.markdown(
                                    f"📍 {activity}"
                                )

                    # ----------------------------------------
                    # NO ACTIVITY LIST
                    # ----------------------------------------

                    else:

                        description = (
                            day.get("description")
                            or day.get("details")
                            or day.get("activities")
                        )

                        if description:

                            if isinstance(
                                description,
                                list
                            ):

                                for item in description:

                                    st.markdown(
                                        f"📍 {item}"
                                    )

                            else:

                                st.write(
                                    description
                                )

            # ------------------------------------------------
            # DAY IS STRING / OTHER VALUE
            # ------------------------------------------------

            else:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### DAY {index:02d}"
                    )

                    st.write(
                        day
                    )

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    elif not ai_response and not budget_response:

        st.info(
            "Your AI itinerary was generated, "
            "but detailed itinerary data was not returned."
        )


# ============================================================
# MY TRIPS
# ============================================================

def page_my_trips():
    st.markdown(
        """
<div class="eyebrow">✦ YOUR JOURNEYS</div>
<h1>My Trips</h1>
<p style="color:#9badbf;">Your saved AI travel plans, all in one place.</p>
""",
        unsafe_allow_html=True,
    )

    try:
        response = requests.get(
            f"{API_BASE_URL}/my-trips",
            headers=auth_headers(),
            timeout=10,
        )

        if response.status_code in (401, 403):
            st.error("Please sign in again.")
            return

        if response.status_code != 200:
            st.error(f"Could not load trips. Status: {response.status_code}")
            return

        trips = response.json()

        if not trips:
            st.markdown(
                """
<div class="feature">
<div class="feature-icon">🧳</div>
<h3>No journeys yet</h3>
<p>Your first AI-planned adventure will appear here.</p>
</div>
""",
                unsafe_allow_html=True,
            )

            if st.button("✦ Plan my first trip", type="primary"):
                go("Plan Trip")

            return

        cols = st.columns(2, gap="medium")

        for i, trip in enumerate(trips):
            destination = str(
                trip.get("destination") or "Unknown"
            )

            budget = str(
                trip.get("budget") or "—"
            )

            days = str(
                trip.get("days") or "—"
            )

            image = destination_image(destination)

            with cols[i % 2]:
                st.markdown(
                    f"""
<div style="position:relative;height:260px;margin-bottom:18px;border-radius:18px;overflow:hidden;border:1px solid rgba(255,255,255,0.15);background-image:linear-gradient(rgba(3,15,28,0.25),rgba(3,15,28,0.90)),url('{html.escape(str(image))}');background-size:cover;background-position:center;display:flex;align-items:flex-end;">
<div style="width:100%;padding:24px;background:linear-gradient(transparent,rgba(3,10,20,0.95));">
<div style="color:#61d8c5;font-size:11px;font-weight:700;letter-spacing:2px;margin-bottom:8px;">✦ YOUR JOURNEY</div>
<div style="color:white;font-size:25px;font-weight:700;margin-bottom:8px;">✈️ {html.escape(destination)}</div>
<div style="color:#d5e0ea;font-size:14px;">{html.escape(days)} days&nbsp; · &nbsp;Budget ₹{html.escape(budget)}</div>
</div>
</div>
""",
                    unsafe_allow_html=True,
                )

    except requests.exceptions.ConnectionError:
        st.error("Backend is not running.")

    except Exception as exc:
        st.error(f"Could not load journeys: {exc}")

        # ----------------------------------------------------
        # AUTH ERROR
        # ----------------------------------------------------

        if response.status_code in (401, 403):

            st.error(
                "Please sign in again."
            )

            return

        # ----------------------------------------------------
        # OTHER BACKEND ERROR
        # ----------------------------------------------------

        if response.status_code != 200:

            st.error(
                f"Could not load trips. "
                f"Status: {response.status_code}"
            )

            return

        trips = response.json()

        # ----------------------------------------------------
        # NO TRIPS
        # ----------------------------------------------------

        if not trips:

            st.markdown(
                """
                <div class="feature">

                    <div class="feature-icon">
                        🧳
                    </div>

                    <h3>
                        No journeys yet
                    </h3>

                    <p>
                        Your first AI-planned adventure
                        will appear here.
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "✦ Plan my first trip",
                type="primary",
            ):

                go("Plan Trip")

            return

        # ----------------------------------------------------
        # TRIP CARDS
        # ----------------------------------------------------

        cols = st.columns(
            2,
            gap="medium"
        )

        for i, trip_item in enumerate(
            trips
        ):

            destination = str(
                trip_item.get(
                    "destination",
                    "Unknown"
                )
            )

            budget = str(
                trip_item.get(
                    "budget",
                    "—"
                )
            )

            trip_days = str(
                trip_item.get(
                    "days",
                    "—"
                )
            )

            image = destination_image(
                destination
            )

            with cols[i % 2]:

                st.markdown(
                    f"""
                    <div
                        class="place-card"
                        style="
                            background-image:
                            url('{image}');
                            margin-bottom:18px;
                        "
                    >

                        <div class="place-overlay">

                            <h3>
                                ✈️
                                {html.escape(destination)}
                            </h3>

                            <p>
                                {html.escape(trip_days)}
                                days ·
                                Budget ₹
                                {html.escape(budget)}
                            </p>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    except requests.exceptions.ConnectionError:

        st.error(
            "Backend is not running."
        )

    except Exception as exc:

        st.error(
            f"Could not load journeys: {exc}"
        )

# ============================================================
# WISHLIST
# ============================================================

def page_wishlist():
    st.markdown(
        """
<div class="eyebrow">✦ DISCOVER</div>
<h1>Wishlist</h1>
<p style="color:#9badbf;">Places worth putting on your next adventure.</p>
""",
        unsafe_allow_html=True,
    )

    names = []

    try:
        df = get_destinations()

        if df is not None and not df.empty and "name" in df.columns:
            names = (
                df["name"]
                .dropna()
                .astype(str)
                .drop_duplicates()
                .tolist()
            )

    except Exception:
        names = []

    if not names:
        names = [
            "Goa",
            "Manali",
            "Jaipur",
            "Kerala",
            "Kashmir",
            "Mumbai",
            "Rajasthan",
            "Andaman",
            "Meghalaya",
        ]

    names = names[:9]

    cols = st.columns(3, gap="medium")

    for i, name in enumerate(names):
        image = destination_image(name)

        with cols[i % 3]:
            st.markdown(
                f"""
<div style="position:relative;height:240px;margin-bottom:18px;border-radius:18px;overflow:hidden;border:1px solid rgba(255,255,255,0.15);background-image:linear-gradient(rgba(3,15,28,0.25),rgba(3,15,28,0.90)),url('{html.escape(str(image))}');background-size:cover;background-position:center;display:flex;align-items:flex-end;">
<div style="width:100%;padding:20px;background:linear-gradient(transparent,rgba(3,10,20,0.95));">
<div style="color:#61d8c5;font-size:11px;font-weight:700;letter-spacing:1.5px;margin-bottom:7px;">✦ DISCOVER</div>
<div style="color:white;font-size:21px;font-weight:700;margin-bottom:6px;">♡ {html.escape(name)}</div>
<div style="color:#c5d2df;font-size:13px;">Explore with your AI travel planner.</div>
</div>
</div>
""",
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # GET DESTINATIONS
    # --------------------------------------------------------

    df = get_destinations()

    if (
        df.empty
        or "name" not in df.columns
    ):

        st.info(
            "Destination data is not available."
        )

        return

    names = (
        df["name"]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .tolist()[:9]
    )

    # --------------------------------------------------------
    # DESTINATION CARDS
    # --------------------------------------------------------

    cols = st.columns(
        3,
        gap="medium"
    )

    for i, name in enumerate(
        names
    ):

        image = destination_image(
            name
        )

        with cols[i % 3]:

            st.markdown(
                f"""
                <div
                    class="place-card"
                    style="
                        background-image:
                        url('{image}');
                        margin-bottom:18px;
                    "
                >

                    <div class="place-overlay">

                        <h3>
                            ♡
                            {html.escape(name)}
                        </h3>

                        <p>
                            Explore with your
                            AI travel planner.
                        </p>

                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# ROUTER
# ============================================================

def main():

    init_session()

    render_sidebar()

    page = st.session_state.get(
        "page",
        "Login"
    )

    # --------------------------------------------------------
    # LOGIN PROTECTION
    # --------------------------------------------------------

    if (
        page in {
            "Home",
            "Plan Trip",
            "My Trips",
            "Wishlist",
        }
        and not st.session_state.token
    ):

        page = "Login"

        st.session_state.page = "Login"

    # --------------------------------------------------------
    # ROUTES
    # --------------------------------------------------------

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

        st.session_state.page = "Login"

        page_login()


# ============================================================
# START APP
# ============================================================

if __name__ == "__main__":
    main()
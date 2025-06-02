import streamlit as st
from datetime import datetime, timedelta, date
from zoneinfo import available_timezones, ZoneInfo
import time


st.set_page_config(page_title="Time Zone App", page_icon="🕒")


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #00000000 0%, #00000000 50%, #6b8dd6 100%);
        color: white;
        min-height: 100vh;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        font-weight: 700;
    }
    div.stButton > button {
        background-color: #764ba2;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #5a357a;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("🕒 Time Zone App")

Time_Zones = sorted(available_timezones())

time_format = st.radio("Choose Time Format", ["12-hour", "24-hour"], horizontal=True)
time_fmt_str = "%Y-%m-%d %I:%M:%S %p" if time_format == "12-hour" else "%Y-%m-%d %H:%M:%S"


if "selected_time" not in st.session_state:
    st.session_state.selected_time = datetime.now().time()

tz_input = st.time_input("Select Local Time", value=st.session_state.selected_time)
if tz_input != st.session_state.selected_time:
    st.session_state.selected_time = tz_input

selected_time_zones = st.multiselect("Select Time Zones", Time_Zones)

if selected_time_zones:
    st.subheader("Current Times in Selected Zones")
    with st.spinner("Fetching current times..."):
        for tz in selected_time_zones:
            time.sleep(0.1)
            current_time = datetime.now(ZoneInfo(tz)).strftime(time_fmt_str)
            st.write(f"🕓 **{tz}** → `{current_time}`")
    st.success(f"✅ Successfully fetched current times for {len(selected_time_zones)} time zone(s).")
else:
    st.warning("Please select at least one time zone.")

st.subheader("Convert Time Between Time Zones")

from_tz = st.selectbox("From Time Zone", Time_Zones, key="from")
to_tz = st.selectbox("To Time Zone", Time_Zones, key="to")

if st.button("Convert Time"):
    try:
        
        today = date.today()

        
        naive_dt = datetime.combine(today, st.session_state.selected_time)

        
        aware_dt = naive_dt.replace(tzinfo=ZoneInfo(from_tz))

        
        converted_dt = aware_dt.astimezone(ZoneInfo(to_tz))

       
        converted_time = converted_dt.strftime(time_fmt_str)

        
        from_offset = aware_dt.utcoffset() or timedelta(0)
        to_offset = converted_dt.utcoffset() or timedelta(0)
        diff_hours = (to_offset - from_offset).total_seconds() / 3600

        st.success(f"🕓 `{from_tz}` → `{to_tz}` = `{converted_time}`")
        st.info(f"⏱️ Time difference between `{from_tz}` and `{to_tz}` is `{diff_hours}` hours.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

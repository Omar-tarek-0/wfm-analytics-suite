import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="WFM Operations Analytics Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS UI ENHANCEMENT ---
st.markdown("""
    <style>
        .main { padding: 1.5rem; }
        .stMetric {
            background-color: #F8F9FA;
            border: 1px solid #E9ECEF;
            padding: 12px 18px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 48px;
            border-radius: 6px;
            padding-left: 18px;
            padding-right: 18px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 WFM Operations Analytics Suite")
st.caption("Upload raw operational files below to instantly process workforce metrics and download SLA reports.")

# Tab Navigation
tab1, tab2, tab3 = st.tabs([
    "⏰ Agent Lateness Report", 
    "🍱 Meal Exceeded Report",
    "☕ Break Summary & Exceeded Report"
])

# Master Mappings & Exclusions
exclude_agents = [
    "Raneem Elsheikh", "Radwa Abdelaal", "Mohamed Tantawy",
    "Ahmed Ebrahim", "Nouran Elsayed", "Alaa Elsebakhy",
    "Hassan Hussein", "Zainab Atifi", "Omar Mahmoud"
]
exclude_set = set(name.strip().lower() for name in exclude_agents)

iex_mapping = {
    "Kenzie Mohamed": 222463, "Mahmoud Salama": 222464, "Ahmed Ibrahim": 197745,
    "Ahmed Moustafa": 222465, "Abanob Fahmy": 223785, "Abdallah Mortada": 223778,
    "Abdelrahman Ibrahim": 223783, "Abdullah Ali": 223770, "Ahmad Zayton": 223769,
    "Ahmed Ahmed": 223761, "Ammar Yasser": 223776, "Maha Ali": 223765,
    "Malak Ramadan": 223768, "Marco Khalil": 223766, "Mariam Ansary": 223762,
    "Marwan Mohammed": 223779, "Marwan Ahmed": 223763, "Mohamed Mohamed": 223764,
    "Mohamed Salama": 223771, "Mohamed Elsaadny": 223760, "Mohamed Hassan Hathoot": 213847,
    "Mohamed Abass": 223780, "Mohamed Abdelwahab": 213729, "Osama Ali": 223777,
    "Shahd Salah": 223774, "Yassin Fahmy": 223782, "Youssef Taher": 223775,
    "Youssef Mahmoud": 223759, "Youssef Abdelkader": 223781, "Youssef Eldesouky": 223784,
    "Yusuf Abdulfattah": 223773, "Muhmad Abdelmajid": 226173, "Mahmohd El Kafas": 226174,
    "Mohamed Fawzy": 226176, "Omnia Emam": 226177, "Hoda Ouis": 226178,
    "Ziad Saeed": 226179, "Youssef Hamed": 226180, "Monzer Manaa": 226181,
    "Youssef Abdelhamid": 226182, "Eslam Attia": 226184, "Ahmed Hassan": 226185,
    "Mohamed Hussein": 226186, "Mohamed Abdel Kader": 226187, "Mohamed Said": 226188,
    "Moaz Saleh": 226189, "Omar Eissa": 226190, "Shada Mohamed": 226191,
    "Youssef Hashim": 226192, "Hagar Mohamed": 226194, "Mohamed Hytham Mohamed": 226195,
    "Mohamed Abdelazizi": 222902
}
iex_mapping_clean = {" ".join(k.split()).lower(): v for k, v in iex_mapping.items()}


# ==========================================
# --- TAB 1: LATENESS ---
# ==========================================
with tab1:
    st.subheader("Daily Shift Lateness Audit")
    
    col1, col2 = st.columns(2)
    with col1:
        file_sched = st.file_uploader("Upload Master Schedule (`Scheduale.csv`)", type=["csv"], key="sched_upload")
    with col2:
        file_ts_late = st.file_uploader("Upload Timestamps (`agent_timestamps.csv`)", type=["csv"], key="ts_late_upload")

    if file_sched and file_ts_late:
        if st.button("Generate Lateness Audit", type="primary", use_container_width=True):
            try:
                df_sched = pd.read_csv(file_sched, low_memory=False)
                df_ts = pd.read_csv(file_ts_late)

                df_sched.columns = df_sched.columns.astype(str).str.strip()
                df_ts.columns = df_ts.columns.astype(str).str.strip()
                df_sched["IEX_ID_Clean"] = pd.to_numeric(df_sched["IEX ID"], errors="coerce")

                ts_strings = df_ts["Timestamp"].astype(str).str.strip().str.replace("Z", "", regex=False)
                df_ts["Timestamp_dt"] = pd.to_datetime(ts_strings, format="%Y-%d-%m %H:%M", errors="coerce")
                if df_ts["Timestamp_dt"].isnull().all():
                    df_ts["Timestamp_dt"] = pd.to_datetime(ts_strings, format="%Y-%d-%m %H:%M:%S", errors="coerce")
                if df_ts["Timestamp_dt"].isnull().all():
                    df_ts["Timestamp_dt"] = pd.to_datetime(ts_strings, format="mixed", dayfirst=True, errors="coerce")

                df_ts["Agent_Clean"] = df_ts["Agent"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
                df_ts_filtered = df_ts[~df_ts["Agent_Clean"].str.lower().isin(exclude_set)].dropna(subset=["Timestamp_dt"])

                if df_ts_filtered.empty:
                    st.error("No valid timestamp entries found after filtering.")
                else:
                    df_ts_filtered["Date_Key"] = df_ts_filtered["Timestamp_dt"].dt.strftime("%Y-%m-%d")
                    detected_date_key = df_ts_filtered["Date_Key"].iloc[0]
                    display_date_str = df_ts_filtered["Timestamp_dt"].dt.strftime("%m/%d/%Y").iloc[0]

                    df_sched_clean = df_sched.dropna(subset=["Date"]).copy()
                    df_sched_clean["Date_dt"] = pd.to_datetime(df_sched_clean["Date"], format="mixed", dayfirst=True, errors="coerce")
                    df_sched_clean["Date_Key"] = df_sched_clean["Date_dt"].dt.strftime("%Y-%m-%d")
                    df_sched_day = df_sched_clean[df_sched_clean["Date_Key"] == detected_date_key]

                    login_events = df_ts_filtered[df_ts_filtered["Type"].astype(str).str.upper() == "AGENT_STATUS/LOGGED_IN"]
                    first_logins = []
                    for agent, group in login_events.groupby("Agent_Clean"):
                        first_login = group.sort_values(by="Timestamp_dt").iloc[0]["Timestamp_dt"]
                        first_logins.append({"Agent": agent, "Timestamp": first_login})
                    df_logins = pd.DataFrame(first_logins)

                    lateness_results = []
                    for idx, row in df_logins.iterrows():
                        agent = row["Agent"]
                        first_login = row["Timestamp"]
                        agent_key = " ".join(agent.split()).lower()
                        iex_id = iex_mapping_clean.get(agent_key)
                        matched_rows = df_sched_day[df_sched_day["IEX_ID_Clean"] == iex_id] if iex_id else pd.DataFrame()

                        if not matched_rows.empty and pd.notna(matched_rows["Sched Start"].iloc[0]):
                            sched_start_raw = str(matched_rows["Sched Start"].iloc[0]).strip()
                            sched_name = matched_rows["Agent Name"].iloc[0]
                            if sched_start_raw.lower() not in ["--:--", "nan"]:
                                sched_time_dt = pd.to_datetime(sched_start_raw, format="mixed", errors="coerce")
                                if pd.notna(sched_time_dt):
                                    sched_dt = first_login.replace(hour=sched_time_dt.hour, minute=sched_time_dt.minute, second=0, microsecond=0)
                                    diff_sec = (first_login - sched_dt).total_seconds()
                                    if diff_sec > 0:
                                        mins, secs = int(diff_sec // 60), int(diff_sec % 60)
                                        lateness_str = f"{mins // 60}h {mins % 60:02d}m {secs:02d}s" if mins >= 60 else f"{mins}m {secs:02d}s"
                                        late_mins = round(diff_sec / 60.0, 2)
                                        status = "❌ Late"
                                    else:
                                        lateness_str, late_mins, status = "0m 0s", 0.0, "✅ On Time"
                                    formatted_shift = sched_time_dt.strftime("%I:%M %p")
                                else:
                                    formatted_shift, lateness_str, late_mins, status = "N/A", "0m 0s", 0.0, "⚪ Off / Unscheduled"
                            else:
                                formatted_shift, lateness_str, late_mins, status = "Off", "0m 0s", 0.0, "⚪ Off / Unscheduled"
                        else:
                            formatted_shift, lateness_str, late_mins, status, sched_name = "N/A", "0m 0s", 0.0, "⚪ Off / Unscheduled", "N/A"

                        lateness_results.append({
                            "Agent": agent, "Date": display_date_str, "IEX ID": iex_id if iex_id else "N/A",
                            "Scheduled Shift Start": formatted_shift, "Actual First Login": first_login.strftime("%H:%M:%S"),
                            "Status": status, "Lateness": lateness_str, "Lateness (Mins)": late_mins,
                            "Matched Schedule Name": sched_name
                        })

                    df_final = pd.DataFrame(lateness_results).sort_values(by=["Lateness (Mins)", "Scheduled Shift Start", "Agent"], ascending=[False, True, True])
                    
                    # Metrics Banner
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Total Agents Audited", len(df_final))
                    m2.metric("Late Logins", len(df_final[df_final["Status"] == "❌ Late"]))
                    m3.metric("On-Time / Unscheduled", len(df_final[df_final["Status"] != "❌ Late"]))

                    st.dataframe(df_final, use_container_width=True)
                    st.download_button("📥 Download Lateness CSV Report", data=df_final.to_csv(index=False).encode("utf-8"), file_name="agent_lateness_report_daily.csv", mime="text/csv")
            except Exception as e:
                st.error(f"An error occurred while processing: {e}")


# ==========================================
# --- TAB 2: MEAL EXCEEDED ---
# ==========================================
with tab2:
    st.subheader("Meal Duration Audit (>60 Mins)")
    file_ts_meal = st.file_uploader("Upload Timestamps (`agent_timestamps.csv`)", type=["csv"], key="ts_meal_upload")

    if file_ts_meal:
        if st.button("Generate Meal Audit", type="primary", use_container_width=True):
            try:
                df = pd.read_csv(file_ts_meal)
                df["Timestamp"] = pd.to_datetime(df["Timestamp"])
                df = df.sort_values(by=["Agent", "Timestamp"]).reset_index(drop=True)

                meal_records = []
                MEAL_LIMIT_MINS = 60

                for agent, group in df.groupby("Agent"):
                    group = group.reset_index(drop=True)
                    in_meal = False
                    meal_start = None

                    for idx, row in group.iterrows():
                        if row["Type"] == "AGENT_STATUS/WENT_AWAY" and row.get("Away Reason") == "Meal":
                            in_meal = True
                            meal_start = row["Timestamp"]
                        elif in_meal:
                            is_returned_away = (row["Type"] == "AGENT_STATUS/RETURNED_FROM_AWAY")
                            avail_val = str(row.get("Available For", ""))
                            is_voice_avail = (row["Type"] == "AGENT_AVAILABILITY/UPDATED" and ("VOICE" in avail_val or "MESSAGING" in avail_val))
                            is_floor_support = (row["Type"] == "AGENT_STATUS/CHANGED_ACTIVE_REASON" and row.get("Active Reason") == "Floor Support (Unavailable)")

                            if is_returned_away or is_voice_avail or is_floor_support:
                                meal_end = row["Timestamp"]
                                duration_sec = (meal_end - meal_start).total_seconds()
                                duration_min = duration_sec / 60.0

                                limit_sec = MEAL_LIMIT_MINS * 60
                                exceeded_sec = max(0, duration_sec - limit_sec)
                                exceeded_str = f"{int(exceeded_sec // 60)}m {int(exceeded_sec % 60)}s" if exceeded_sec > 0 else "0m 0s"
                                return_activity = "Floor Support (SME)" if is_floor_support else "Back to Voice"

                                meal_records.append({
                                    "Agent": agent, "Meal Start": meal_start.strftime("%H:%M:%S"),
                                    "Meal Return": meal_end.strftime("%H:%M:%S"), "Return Activity": return_activity,
                                    "Actual Duration": f"{int(duration_min)}m {int(duration_sec % 60)}s",
                                    "Total Minutes": round(duration_min, 2), "Exceeded (vs 60m)": exceeded_str,
                                    "Exceeded Minutes": round(exceeded_sec / 60.0, 2),
                                    "Status": "❌ Exceeded SLA" if exceeded_sec > 0 else "✅ Within SLA"
                                })
                                in_meal = False
                                meal_start = None

                df_meals = pd.DataFrame(meal_records).drop_duplicates(subset=["Agent", "Meal Start"]).sort_values(by="Exceeded Minutes", ascending=False)
                
                # Metrics Banner
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Meals Logged", len(df_meals))
                m2.metric("Meals Exceeding 60m", len(df_meals[df_meals["Exceeded Minutes"] > 0]))
                m3.metric("Compliant Meals", len(df_meals[df_meals["Exceeded Minutes"] == 0]))

                st.dataframe(df_meals, use_container_width=True)
                st.download_button("📥 Download Meal Exceeded CSV Report", data=df_meals.to_csv(index=False).encode("utf-8"), file_name="meal_exceeded_report.csv", mime="text/csv")
            except Exception as e:
                st.error(f"An error occurred while processing: {e}")


# ==========================================
# --- TAB 3: BREAK EXCEEDED (WIDE FORMAT) ---
# ==========================================
with tab3:
    st.subheader("Break Summary & Duration Audit (>15 Mins)")
    file_ts_break = st.file_uploader("Upload Timestamps (`agent_timestamps.csv`)", type=["csv"], key="ts_break_wide_upload")

    if file_ts_break:
        if st.button("Generate Break Summary", type="primary", use_container_width=True):
            try:
                df = pd.read_csv(file_ts_break)
                df["Timestamp"] = pd.to_datetime(df["Timestamp"])
                df = df.sort_values(by=["Agent", "Timestamp"]).reset_index(drop=True)

                agent_map = {}
                max_breaks = 2
                BREAK_LIMIT_MINS = 15

                for agent, group in df.groupby("Agent"):
                    if agent not in agent_map:
                        agent_map[agent] = {"breaks": [], "total_exceeded": 0}

                    group = group.reset_index(drop=True)
                    in_break = False
                    break_start = None

                    for idx, row in group.iterrows():
                        if row["Type"] == "AGENT_STATUS/WENT_AWAY" and row.get("Away Reason") == "Break":
                            in_break = True
                            break_start = row["Timestamp"]
                        elif in_break:
                            is_returned_away = (row["Type"] == "AGENT_STATUS/RETURNED_FROM_AWAY")
                            avail_val = str(row.get("Available For", ""))
                            is_voice_avail = (row["Type"] == "AGENT_AVAILABILITY/UPDATED" and ("VOICE" in avail_val or "MESSAGING" in avail_val))

                            if is_returned_away or is_voice_avail:
                                break_end = row["Timestamp"]
                                duration_sec = (break_end - break_start).total_seconds()
                                duration_min = int(round(duration_sec / 60.0))

                                start_str = break_start.strftime("%H:%M")
                                end_str = break_end.strftime("%H:%M")

                                exceeded_mins = max(0, duration_min - BREAK_LIMIT_MINS)
                                break_str = f"{duration_min} mins ({start_str} - {end_str})"
                                
                                if exceeded_mins > 0:
                                    break_str += f" ⚠️ +{exceeded_mins}m"
                                
                                agent_map[agent]["breaks"].append(break_str)
                                agent_map[agent]["total_exceeded"] += exceeded_mins
                                max_breaks = max(max_breaks, len(agent_map[agent]["breaks"]))
                                
                                in_break = False
                                break_start = None

                # Build the wide-format table rows
                final_rows = []
                for agent in sorted(agent_map.keys()):
                    data = agent_map[agent]
                    row_data = {"Agent": agent}
                    
                    # Pad out break columns (Break 1, Break 2, etc.)
                    for i in range(max_breaks):
                        col_name = f"Break {i+1}"
                        if i < len(data["breaks"]):
                            row_data

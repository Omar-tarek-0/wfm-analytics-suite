import pandas as pd
import streamlit as st
import os

# Page Configuration
st.set_page_config(
    page_title="WFM Operations Analytics Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# --- DESIGN SYSTEM (UI ONLY) ---
# ==========================================
# Palette: Ink #14213D | Teal #0E9F8E | Amber #F59E0B | Indigo #5B6CFF | Coral #EF4444
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"], .stApp, button, input, textarea {
            font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
        }

        /* Clean up Streamlit chrome */
        #MainMenu, footer { visibility: hidden; }
        header[data-testid="stHeader"] { background: transparent; }
        .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1280px; }

        /* ---------- Hero ---------- */
        .hero {
            background:
                radial-gradient(circle at 92% 8%, rgba(14,159,142,0.45) 0, transparent 38%),
                radial-gradient(circle at 70% 120%, rgba(91,108,255,0.40) 0, transparent 45%),
                #14213D;
            border-radius: 20px;
            padding: 34px 40px 30px 40px;
            margin-bottom: 1.4rem;
            color: #FFFFFF;
        }
        .hero h1 {
            font-size: 2.3rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0 0 6px 0;
            padding: 0;
            color: #FFFFFF;
        }
        .hero p {
            font-size: 1.02rem;
            margin: 0 0 20px 0;
            max-width: 640px;
            color: rgba(255,255,255,0.78);
            line-height: 1.55;
        }
        .hero-chips { display: flex; flex-wrap: wrap; gap: 10px; }
        .chip {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 14px;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.18);
            color: #FFFFFF;
        }
        .chip .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

        /* ---------- Tabs (pill style) ---------- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(128,128,128,0.10);
            padding: 6px;
            border-radius: 14px;
            border-bottom: none;
        }
        .stTabs [data-baseweb="tab"] {
            height: 46px;
            border-radius: 10px;
            padding: 0 22px;
            font-weight: 700;
            background: transparent;
            border: none;
        }
        .stTabs [aria-selected="true"] {
            background: #14213D !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 14px rgba(20,33,61,0.30);
        }
        .stTabs [aria-selected="true"] p { color: #FFFFFF !important; }
        .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

        /* ---------- Section header ---------- */
        .sec-head { display: flex; align-items: center; gap: 14px; margin: 1.3rem 0 0.4rem 0; }
        .sec-icon {
            width: 46px; height: 46px; border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.4rem;
        }
        .sec-title { font-size: 1.35rem; font-weight: 800; letter-spacing: -0.01em; margin: 0; line-height: 1.2; }
        .sec-sub { font-size: 0.92rem; opacity: 0.68; margin: 2px 0 0 0; }

        /* ---------- Upload area ---------- */
        [data-testid="stFileUploader"] section {
            border: 2px dashed rgba(128,128,128,0.40);
            border-radius: 14px;
            background: rgba(128,128,128,0.06);
            padding: 1rem 1.2rem;
        }
        [data-testid="stFileUploader"] section:hover { border-color: #0E9F8E; background: rgba(14,159,142,0.07); }
        [data-testid="stFileUploader"] label p { font-weight: 700; }

        /* ---------- Buttons ---------- */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0E9F8E 0%, #5B6CFF 100%);
            border: none;
            border-radius: 12px;
            height: 3.1rem;
            font-weight: 700;
            font-size: 1rem;
            color: #FFFFFF;
            box-shadow: 0 6px 18px rgba(91,108,255,0.28);
        }
        .stButton > button[kind="primary"]:hover { filter: brightness(1.07); }
        .stDownloadButton > button {
            border-radius: 12px;
            font-weight: 700;
            border: 2px solid #0E9F8E;
            color: #0E9F8E;
            background: transparent;
        }
        .stDownloadButton > button:hover { background: #0E9F8E; color: #FFFFFF; border-color: #0E9F8E; }

        /* ---------- KPI cards ---------- */
        .kpi {
            background: rgba(128,128,128,0.08);
            border: 1px solid rgba(128,128,128,0.18);
            border-left: 6px solid var(--accent);
            border-radius: 14px;
            padding: 16px 20px;
            margin: 14px 0 6px 0;
        }
        .kpi-label { font-size: 0.86rem; font-weight: 600; opacity: 0.7; margin: 0; }
        .kpi-value { font-size: 2.2rem; font-weight: 800; line-height: 1.15; margin: 4px 0 0 0; color: var(--accent); }

        /* ---------- Table + misc ---------- */
        [data-testid="stDataFrame"] {
            border: 1px solid rgba(128,128,128,0.22);
            border-radius: 14px;
            overflow: hidden;
        }
        .table-title { font-size: 1.02rem; font-weight: 700; margin: 1.2rem 0 0.5rem 0; }
        [data-testid="stAlert"] { border-radius: 12px; }

        @media (max-width: 768px) {
            .hero { padding: 24px 20px; }
            .hero h1 { font-size: 1.7rem; }
        }
    </style>
""", unsafe_allow_html=True)

# --- UI helper functions (display only) ---
ACCENT_AMBER = "#F59E0B"
ACCENT_TEAL = "#0E9F8E"
ACCENT_INDIGO = "#5B6CFF"
ACCENT_CORAL = "#EF4444"

def section_header(icon, title, subtitle, tint):
    st.markdown(
        f"""
        <div class="sec-head">
            <div class="sec-icon" style="background:{tint}22;">{icon}</div>
            <div>
                <p class="sec-title">{title}</p>
                <p class="sec-sub">{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def kpi_card(col, label, value, accent):
    col.markdown(
        f"""
        <div class="kpi" style="--accent:{accent};">
            <p class="kpi-label">{label}</p>
            <p class="kpi-value">{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def style_status(df, col):
    def _color(v):
        s = str(v)
        if "Late" in s or "Exceeded" in s:
            return "background-color: rgba(239,68,68,0.16); color: #EF4444; font-weight: 700"
        if "On Time" in s or "Within" in s:
            return "background-color: rgba(14,159,142,0.16); color: #0E9F8E; font-weight: 700"
        if "Off" in s:
            return "background-color: rgba(128,128,128,0.16); font-weight: 600"
        return ""
    return df.style.apply(lambda s: s.map(_color), subset=[col])

def table_title(text):
    st.markdown(f'<p class="table-title">{text}</p>', unsafe_allow_html=True)


# --- HERO ---
st.markdown("""
    <div class="hero">
        <h1>📊 WFM Operations Analytics Suite</h1>
        <p>Upload your raw operational files, review agent performance at a glance, and download ready-to-share SLA reports.</p>
        <div class="hero-chips">
            <span class="chip"><span class="dot" style="background:#F59E0B;"></span>Lateness audit</span>
            <span class="chip"><span class="dot" style="background:#0E9F8E;"></span>Meals over 60 min</span>
            <span class="chip"><span class="dot" style="background:#5B6CFF;"></span>Breaks over 15 min</span>
        </div>
    </div>
""", unsafe_allow_html=True)

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

# --- DYNAMIC MAPPING FROM CSV ---
def load_mapping():
    if os.path.exists("mapping.csv"):
        try:
            df_map = pd.read_csv("mapping.csv")
            
            clean_mapping = {}
            for idx, row in df_map.iterrows():
                iex_id = row.iloc[0]
                name = row.iloc[1]
                
                if pd.notna(name) and pd.notna(iex_id):
                    clean_name = " ".join(str(name).split()).lower()
                    try:
                        clean_iex = int(float(iex_id))
                    except ValueError:
                        clean_iex = iex_id
                        
                    clean_mapping[clean_name] = clean_iex
                    
            return clean_mapping
        except Exception as e:
            st.error(f"Error reading mapping.csv: {e}")
            return {}
    else:
        st.warning("⚠️ mapping.csv not found in the repository. Lateness audit will not map IEX IDs.")
        return {}

iex_mapping_clean = load_mapping()


# ==========================================
# --- TAB 1: LATENESS ---
# ==========================================
with tab1:
    section_header("⏰", "Daily Shift Lateness Audit",
                   "Compare each agent's first login against their scheduled shift start.", ACCENT_AMBER)

    col1, col2 = st.columns(2)
    with col1:
        file_sched = st.file_uploader("1 · Master Schedule (`Scheduale.csv`)", type=["csv"], key="sched_upload")
    with col2:
        file_ts_late = st.file_uploader("2 · Timestamps (`agent_timestamps.csv`)", type=["csv"], key="ts_late_upload")

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
                    kpi_card(m1, "Total Agents Audited", len(df_final), ACCENT_INDIGO)
                    kpi_card(m2, "Late Logins", len(df_final[df_final["Status"] == "❌ Late"]), ACCENT_CORAL)
                    kpi_card(m3, "On-Time / Unscheduled", len(df_final[df_final["Status"] != "❌ Late"]), ACCENT_TEAL)

                    table_title(f"Results for {display_date_str}")
                    st.dataframe(style_status(df_final, "Status"), use_container_width=True, hide_index=True)
                    st.download_button("📥 Download Lateness CSV Report", data=df_final.to_csv(index=False).encode("utf-8"), file_name="agent_lateness_report_daily.csv", mime="text/csv")
            except Exception as e:
                st.error(f"An error occurred while processing: {e}")
        else:
            st.info("Upload both files above to unlock the audit.", icon="📂")


# ==========================================
# --- TAB 2: MEAL EXCEEDED ---
# ==========================================
with tab2:
    section_header("🍱", "Meal Duration Audit (>60 Mins)",
                   "Find every meal that ran past the 60-minute allowance and see how far over it went.", ACCENT_TEAL)

    file_ts_meal = st.file_uploader("Timestamps (`agent_timestamps.csv`)", type=["csv"], key="ts_meal_upload")

   elif in_meal:
                            event_type = str(row["Type"]).upper()
                            
                            is_returned_away = (event_type == "AGENT_STATUS/RETURNED_FROM_AWAY")
                            is_floor_support = (event_type == "AGENT_STATUS/CHANGED_ACTIVE_REASON" and str(row.get("Active Reason")) == "Floor Support (Unavailable)")
                            
                            # ONLY check channels if the event is officially an availability update
                            channels = []
                            if event_type == "AGENT_AVAILABILITY/UPDATED":
                                avail_val = str(row.get("Available For", "")).upper()
                                if "VOICE" in avail_val: channels.append("Voice")
                                if "MESSAGING" in avail_val: channels.append("Messaging")
                                if "MAIL" in avail_val or "EMAIL" in avail_val: channels.append("Email")
                                if "TASK" in avail_val: channels.append("Task")
                                
                            is_any_avail = len(channels) > 0

                            if is_returned_away or is_any_avail or is_floor_support:
                                meal_end = row["Timestamp"]
                                duration_sec = (meal_end - meal_start).total_seconds()
                                
                                # Safety net: Ignore simultaneous 0-second glitches from Gladly
                                if duration_sec > 0:
                                    duration_min = duration_sec / 60.0
                                    limit_sec = MEAL_LIMIT_MINS * 60
                                    exceeded_sec = max(0, duration_sec - limit_sec)
                                    exceeded_str = f"{int(exceeded_sec // 60)}m {int(exceeded_sec % 60)}s" if exceeded_sec > 0 else "0m 0s"
                                    
                                    if is_floor_support:
                                        return_activity = "Floor Support (SME)"
                                    elif channels:
                                        return_activity = f"Back to {' & '.join(channels)}"
                                    else:
                                        return_activity = "Returned from Away"

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
                kpi_card(m1, "Total Meals Logged", len(df_meals), ACCENT_INDIGO)
                kpi_card(m2, "Meals Exceeding 60m", len(df_meals[df_meals["Exceeded Minutes"] > 0]), ACCENT_CORAL)
                kpi_card(m3, "Compliant Meals", len(df_meals[df_meals["Exceeded Minutes"] == 0]), ACCENT_TEAL)

                table_title("Meal details")
                st.dataframe(style_status(df_meals, "Status"), use_container_width=True, hide_index=True)
                st.download_button("📥 Download Meal Exceeded CSV Report", data=df_meals.to_csv(index=False).encode("utf-8"), file_name="meal_exceeded_report.csv", mime="text/csv")
            except Exception as e:
                st.error(f"An error occurred while processing: {e}")
    else:
        st.info("Upload the timestamps file above to unlock the audit.", icon="📂")


# ==========================================
# --- TAB 3: BREAK EXCEEDED (WIDE FORMAT) ---
# ==========================================
with tab3:
    section_header("☕", "Break Summary & Duration Audit (>15 Mins)",
                   "See every break per agent in one row, with the minutes over the 15-minute allowance.", ACCENT_INDIGO)

    file_ts_break = st.file_uploader("Timestamps (`agent_timestamps.csv`)", type=["csv"], key="ts_break_wide_upload")

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
                                    break_str += f"  +{exceeded_mins}m"

                                agent_map[agent]["breaks"].append(break_str)
                                agent_map[agent]["total_exceeded"] += exceeded_mins
                                max_breaks = max(max_breaks, len(agent_map[agent]["breaks"]))

                                in_break = False
                                break_start = None

                # Build the wide-format table rows
                # Build the wide-format table rows
                final_rows = []
                for agent in sorted(agent_map.keys()):
                    data = agent_map[agent]
                    row_data = {"Agent": agent}

                    # 1. First, build all Break columns in order
                    for i in range(max_breaks):
                        col_name = f"Break {i+1}"
                        if i < len(data["breaks"]):
                            row_data[col_name] = data["breaks"][i]
                        else:
                            row_data[col_name] = "-"

                    # 2. Then, append the summary columns at the very end
                    row_data["Total Exceeded (Mins)"] = data["total_exceeded"]
                    row_data["Status"] = "❌ Exceeded SLA" if data["total_exceeded"] > 0 else "✅ Within SLA"
                    
                    # 3. Finally, append the single row for this agent
                    final_rows.append(row_data)

                df_breaks_wide = pd.DataFrame(final_rows)
                # Metrics Banner
                m1, m2, m3 = st.columns(3)
                kpi_card(m1, "Agents with Breaks", len(df_breaks_wide), ACCENT_INDIGO)
                kpi_card(m2, "Agents Exceeding Allowance", len(df_breaks_wide[df_breaks_wide["Total Exceeded (Mins)"] > 0]), ACCENT_CORAL)
                kpi_card(m3, "Highest Break Count", max_breaks, ACCENT_AMBER)

                table_title("Break details by agent")
                st.dataframe(style_status(df_breaks_wide, "Status"), use_container_width=True, hide_index=True)
                st.download_button(
                    "📥 Download Break Summary CSV",
                    data=df_breaks_wide.to_csv(index=False).encode("utf-8"),
                    file_name="break_summary_report.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"An error occurred while processing: {e}")
    else:
        st.info("Upload the timestamps file above to unlock the summary.", icon="📂")

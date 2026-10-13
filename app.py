import pandas as pd
import streamlit as st

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
    "Mohamed Abdelazizi": 222902,"Kevin Lloyd Nacu": 116832,
    "Antonio Tayag": 116879,
    "Mark Paul Angelo Adiviento": 116890,
    "Kurt Mamangun": 116890,
    "Joanna Marie Solomon": 117009,
    "Jennix Ann Pedragas": 117007,
    "Arnold Ii Casem": 116980,
    "Restituto Magsalos": 116956,
    "Gretchen Paz": 116843,
    "Kristina Paula Espiridion": 117011,
    "Shaina Shanel Raptos": 117020,
    "Raphael Vincent Labriaga": 117018,
    "Jazzer Mirabueno": 116846,
    "Fillard Patrick Giraldo": 117005,
    "Crecielito Palo": 116881,
    "Juancho Villaceran": 116970,
    "Angelo Suliguin": 116888,
    "Ryan Chrissie Bilan": 116995,
    "Joyce Ann Gajultos": 116968,
    "DigiAna Concepcion": 116844,
    "Jennyllyn Villaflor": 116909,
    "Hazelie Bufete": 116867,
    "Adora Sandra Banzuela": 117000,
    "Daniela Louise Beltran": 117003,
    "Diana Rose Perena": 117004,
    "John Dave Ramos": 117010,
    "Markjose Lirio": 117011,
    "Mary Jane Tarrayo": 117013,
    "Mary Rose Payot": 117014,
    "Melvyn Angelo Daza": 117016,
    "Nomer Fontaron": 117017,
    "Ruth Anne Soriano": 116839,
    "Geraldine Rivera": 116921,
    "Marjorie Mae Reyes": 117397,
    "Erica Manlangit": 116884,
    "Anjelica Plata": 116841,
    "Clarisse Rubaine Feliciano": 116842,
    "Jaybie Ceralde": 116845,
    "Jullienne Santiago": 116847,
    "Karli Kaye Daguimol": 116848,
    "Manuel Piñon": 116849,
    "Marilou Zambo": 116850,
    "Mary Rose Pongan": 116851,
    "Maryam Jaya Kiram": 116852,
    "Patricia Daryelle Rayos": 116853,
    "Paul William Palad": 116912,
    "Princess Diamola": 116913,
    "Rhocell Toga": 116914,
    "Triccia Mae De Guzman": 116915,
    "Wendy Tolentino": 116916,
    "Arnold Ricardo": 116901,
    "Caleb Francisco": 116902,
    "Carlo Daelo": 116903,
    "Christian Earl Robes": 116904,
    "Crisna Mae Concepcion": 116905,
    "Hanna Clarizel Jarquio": 116906,
    "Jems Madera Beleber": 116908,
    "John Erick Bejucos": 116910,
    "Kyla Anne Iderosa": 116911,
    "Rose Marie Balones": 116854,
    "Rosemarie Quinto": 116855,
    "Alyanna Mae Real": 117001,
    "Angela May Villamor": 117002,
    "Jemimah Lalangan": 117006,
    "Jo-An Camasura": 117008,
    "Nhica Mae Perea": 117016,
    "Reyjett Depillo": 117019,
    "Daphne Padilla": 116982,
    "Paul Vincent Escorpizo": 116975,
    "Ronela Basaen": 116770,
    "Michelle Marquez": 110351,
    "Romlyn Salvador": 112517,
    "Jhen Kenneth Cabatuan": 116946,
    "Tereze Cuadraza": 116825,
    "Genevieve Guarte": 116826,
    "Sabeth Satulto": 116875,
    "Sonny Pendioco": 116840,
    "Angelica Mae Velasco": 116861,
    "Kenneth Patrick Ali-Ali": 116868,
    "Kyra Lee Cruz": 116870,
    "Ryan Adeline Ducat": 116893,
    "Gwyneth Ramos Regis": 116894,
    "Marvin Flamiano": 116891,
    "Fred Earl Balleras": 116944,
    "Merryl Jane Encio": 116951,
    "Morisette Manzano": 116955,
    "Jelly Grace De Belen": 116964,
    "Romalyn Magno": 116838,
    "Hector Armando Sarion": 116892,
    "Anabell Parale": 116919,
    "Jerickson Jacinto": 116923,
    "Cristine Joy Fajardo": 116958,
    "Mark Lawrence Cruz": 116971,
    "Rona Mae Jimenez": 116977,
    "Domelyn Almorfo": 116864,
    "Emil Jordan Bernardino": 116885,
    "Jessica Palmiario": 116988,
    "David Ko": 116920,
    "Khin Zhi Acuña": 116949,
    "Reynold Natividad": 116934,
    "Brixz Andrada": 116877,
    "Villanueva Hazel": 116866,
    "Jen Jen Rosas": 116946,
    "M. Sachi Nagayo": 116950,
    "Ma. Shirlyn Suela": 116951,
    "Raul Galo": 116896,
    "Jemuel Teruel": 116927,
    "Carmela Magayo": 116938,
    "Rowena Avila Santeco": 141917,
    "Shire Angeli Arimado": 116928,
    "Etheniel Clutario": 116865,
    "Paul Nielson Clemente": 116922,
    "Maniza Miano": 116927,
    "Sarnie Nakajima": 116876,
    "Rotsan Baisa y Muji": 116869,
    "Kassandra Fesalbon": 116831,
    "Ella Marie Dizon": 116942,
    "Milca Pambidagan": 116926,
    "Ma. Theresa Mejica": 116933,
    "Julie Anne Baron": 116971,
    "Jose Tapanan": 116987,
    "Maria Amor Macapallag": 116952,
    "Judy Ann Soro": 116989,
    "April Cagas": 116862,
    "Romarie Madiroga Cecilia": 133776,
    "Joemelyn Batangon": 133781,
    "Arlan San Juan Feuntes": 133793,
    "Shayne Mae Pagilao Marilao": 133779,
    "Amor Jr Revera Carag": 134612,
    "Casamj Andrei Baterbonia Palo": 134593,
    "Justine Mae Diaz Carag": 134596,
    "Hazel Joyce Serca Francisco": 134597,
    "Elvira Hortaleza San Juan": 134783,
    "Ma. Cristina Pagaduan": 133790,
    "Roberto Paquia Cruz": 134591,
    "Angelika San Pascual David": 133787,
    "Edward Alvarez Almario": 133777,
    "Pia Antonette Fider Montes": 133788,
    "Angelika Balbin Tugonon": 134628,
    "Joanni Carl Tamghal De Jesus": 134630,
    "Carl Lirio Maderia Velasco Panti": 134782,
    "Catrine Lea Mojica": 136567,
    "Jonnel Malinao": 133780,
    "Lorelyn Valentos Bunoa": 137105,
    "Franciel Mae Guarino Guarino": 134598,
    "Sattella Golino Padero": 134606,
    "John Harold Zamora Piornato": 134592,
    "Maja Prado Patajo": 136553,
    "Samirah Afdal Dalinding": 137556,
    "Risa Seth Emano": 133878,
    "Hannah Jisselle Gabrielle Mercado Ponce": 134592,
    "Bea Angeline Lozano Maturan": 136550,
    "Joy Tremares Colango": 137090,
    "Bernadette Janulgue Libro": 134608,
    "Teresa Reyes Martin": 134629,
    "Isabelle Frances Lapuz": 142478,
    "Eimiel Khen Oraye": 142484,
    "Princess Chaire Ablay Serrano": 136551,
    "Daimiel Roby Villar Olayres": 143064,
    "Liza Mores": 134583,
    "April Lorenzo Espinosa": 134602,
    "Kristhel Ann Joy Timola": 137559,
    "Jastine Joyce Mercurio Rosas": 140697,
    "Harry Lontok Fernandez": 142479,
    "Cyril Moises": 142494,
    "Ella Cairo": 137137,
    "Sam Clarisse Matito": 137560,
    "Rhiccia Zhenquaine Lacaba Eusebio": 137570,
    "Frederick De Leon Drapite": 137577,
    "Erica May Joan Garbero": 143232,
    "Edgar Gunda Jr": 143048,
    "Arvin Ramos": 142500,
    "James Lagumbay": 146628,
    "Maria Shaina Mallari": 144214,
    "Phyllicia Ann Rodrigo": 134590,
    "Stephanie Reanzares Maghari": 140682,
    "John Carlo Magalao Camara": 141752,
    "John Enriquez Maturan": 141753,
    "Ashlee Mae Maurice Caseda": 142790,
    "Clarisse Cantila Josef": 143230,
    "John Lester Rondero": 144222,
    "Dan Vincent Policarpio": 144981,
    "Jhunel Jeff Panotes Macalam": 141938,
    "Jaime Diaz Medes": 141740,
    "Alexander Asis": 142475,
    "Roxanne Olaso": 142471,
    "Dianne Jennifer De Belen": 143048,
    "Ma. Shaira Aureo": 143238,
    "Brixie Kiano Juralo": 142526,
    "Maria Chinly Enriquez": 143220,
    "Riza Mae Maglanque": 142493,
    "August Hugo Orto": 136552,
    "Ruth Valdez Quinto": 137110,
    "Stephine Joy Bayogo": 137557,
    "Alyanna Miyaka Suarez Cortez": 140678,
    "Andre Joshua Sanalila Tolentino": 143704,
    "Jessa Mae D. Refe": 141939,
    "Golden Jeffer Bernat": 142490,
    "Torellos Bejer": 142888,
    "Althea Mendinueta": 134603,
    "Maru Bautista Batayola": 144883,
    "Lara Nicole Espina": 137126,
    "Polo James Sioson": 137131,
    "Imee Fiorenz Galapon": 140686,
    "Helen Oble": 142880,
    "Clarence Chavez": 143303,
    "Trixia Mae Diaz": 142274,
    "Rica Labong": 143221,
    "Kyla Mones": 144223,
    "Claire Baltar": 144863,
    "Vincent Joshua Telan": 137109,
    "John Vincent Olayres": 137111,
    "Carlito Jr. Tumbaga": 144867,
    "Sofia Chrystelle Reyes Sangines": 136571,
    "Justine Penafiel": 137136,
    "Tricia de Ocampo": 141940,
    "Erma Camacam": 137139,
    "Kristel Jhoie Adriano": 136571,
    "Pia Danya Rosalyn Alcanar Domingo": 137142,
    "Jasmin Aquino Luna": 137543,
    "Jonalie Patawaran": 146621,
    "Diana Lee Hipolito": 136569,
    "Cababao Gretchen": 139208,
    "Jasmin Cacanindin": 142468,
    "Abegail Deltomas Secopito": 143063,
    "Russell Melizza Tugade": 142496,
    "Shiela Pano": 142883,
    "Mary Joy Montano Nilo": 143062,
    "Rod Joseph Luna Medina": 143061,
    "Liezle Ann Espallardo": 142885,
    "Gian De Castro": 142890,
    "Mary Jane Perote": 142887,
    "Magno Riolflorido": 142894,
    "Caolie De Lumen": 142895,
    "Minerva Dedel": 142891,
    "Jerrelyn Nisay": 142901,
    "Revillez Panglinan": 142899,
    "Jerelyn Carrera": 142881,
    "Maricelo Gooden": 142896,
    "Maria Angelica Pariñas": 143067,
    "Michael Balinas": 143228,
    "Joiada Elcana Guerrero": 143282,
    "Irene Joy Alano": 143290,
    "Maria Elizabeth Canlas": 143299,
    "Lovely Grafil": 143284,
    "Maverick Baltazar Morales": 144211,
    "Ruben Samuel Espinas": 144218,
    "Carla Joy Mendoza": 144375,
    "Danielle Lanuza": 144365,
    "Paul Brian Mizal": 144222,
    "Jopet Constantino": 144377,
    "Rosemarie Sumugat": 144383,
    "Hazelene Ann Victoria Elipedes": 144379,
    "Kate Carla Salvedia": 144378,
    "Aileen Ramirez": 144379,
    "Cindy Grace Sadag": 144881,
    "Ma. Erica Grande": 144878,
    "Naul Jacqueline Antonio": 144811,
    "Ritzie Mae Balquin": 144868,
    "Ana Loren Davocol": 144867,
    "John Lester Pasing": 144877,
    "Christian Carl Rosell": 144872,
    "Edgar Del Fierro": 144882,
    "Camille Garcia": 144884,
    "Lou Grace Mansalapus": 144885,
    "Rose Marie Mateo": 144870,
    "Mc Lawrence Feras": 144869,
    "Milagrosa Amarilloo": 144868,
    "Pearl Angelle Barredo": 144869,
    "Clarisse Mae Cayetano": 144869,
    "Abellera Patrick Daryl": 144603,
    "Alcausin Darlyn": 144625,
    "Agustin Gilbert": 144623,
    "Fulgado April Ruth": 144624,
    "Areglado Maruel": 144626,
    "Penera Dimple Fe": 144629,
    "Roman Albarria": 144881,
    "Eugenio Ariston": 144879,
    "Beverly Manuel": 144026,
    "Ma. Cherish Arciaga": 144230,
    "Maryan Alagos": 144887,
    "Evelyn Ramos": 144512,
    "Gerry Neil Belbes": 144233,
    "Danniel Lynn Villegas Palaganas": 144216,
    "Ion Banne Aspera": 137138,
    "Alvin Casimiro": 141945,
    "Katherine Candaza Mendoza": 137540,
    "Lynette Martinez San Juan": 137574,
    "Krisha Marie Larena": 137576,
    "Jennerose Ompoc Muerto": 137576,
    "Ericson Latorino": 139212,
    "Ria Angelica Basa": 139216,
    "Izza Mitira Martin": 140687,
    "Mary Jane Daez Macaraeg": 140679,
    "Cheymie Coraza Dano": 140679,
    "Shea Villarubia Sumagaysay": 140680,
    "Noreen De La Pena": 140693,
    "Czar Kyle Trinidad Corpuz": 141734,
    "Vergel Pobadora": 142506,
    "Paulo Ocampo": 143041,
    "Remar Bayangos Llanes": 143043,
    "Janelll Fiona Martinez": 143252,
    "Archie Gardonia": 142473,
    "Gerralyn Rebario": 142485,
    "Bong Espina": 142492,
    "Aiko Luciano": 142519,
    "Marlon Gelsano": 144206,
    "Cynthia Ann Manrique": 143229,
    "Rhea Jane Tuazon": 143231,
    "Mary Joy Manayang Coloma": 143239,
    "Mark Anthony De Leon Pacis": 143250,
    "Iana Krizza Malong Mendoza": 143252,
    "Mariel Angela Relleve Ramos": 143253,
    "Mary Joyselle Atillo": 144045,
    "Junior Adlaon Samson": 143258,
    "Ericka Llagas Alcala": 143261,
    "Jonathan Yambao": 143227,
    "Melody Perez Rueda": 143261,
    "Yazid Lou Nual Molo": 143272,
    "Christian Rodriguez Beltran": 143248,
    "April Joy Macutay": 143276,
    "Aimee Therese Taberna": 143236,
    "Noel Villarim Jr": 143285,
    "JOHN ALDRIN ARNO JR": 143284,
    "Cristina Bagtas": 143277,
    "Donna Rose Abraham": 143286,
    "Mariane Mendiola": 143286,
    "Celeste Recente": 143290,
    "Krishah Alexis Abrilla": 141472,
    "Clarisse Bantilan": 142078,
    "Reymark Padulle": 142089,
    "Neil Joshua Madali": 144212,
    "Jemimah Albarillo": 144229,
    "Corinne Anne Pasion": 144361,
    "Marissa Macaldo": 144376,
    "Ma. Cristina Casas": 144877,
    "Jeffrey Renz Dorado": 144879,
    "Apolexa Mae Ruiz": 144876,
    "Soliman Ren Ryan": 144867,
    "Tenedora Jann Jeremy": 144608,
    "Bandoy Rotsen Obienio": 144834,
    "Tambunting Keanu Aljur": 142820,
    "Crispina Ma. Lily Flor": 144228,
    "Ocampo Louis Jose": 144366,
    "Cabrera Crisundy Mae": 144609,
    "Oxima Nikole": 144620,
    "Oximer Felybin": 144627,
    "Maricar Aragon": 144876,
    "Erodelia Ruth Heinrich": 144618,
    "Revit Armida": 144617,
    "Michelle Ladonga": 144826,
    "Riza Therese Manalang": 144869,
    "Jenifer Lim": 144525,
    "Glaiza Batinga": 144377,
    "Jan Janco Chavez": 144305,
    "Josephine Dianne Ceralde": 145099,
    "Reighcel Cruzada": 145097,
    "Andrea Vilen Tague": 145099,
    "Maria Theresa Quisagan": 145101,
    "Jhonpaol Miranda": 145068,
    "John Qhaylynx Labaye": 145080,
    "Angela Mhae De Asis": 145050,
    "Marvin Abendano": 145266,
    "Nizza Mhae Caraan": 145087,
    "Karm Aragon Fernando": 140433,
    "Virgilio Dionisio": 145233,
    "Crisel Villanueva": 145237,
    "Heidi Aguas": 145221,
    "Darwin Reanzares": 145265,
    "Juliet Marasigan": 145264,
    "Anthony Delos Santos": 145275,
    "Mark Bryan Robleza": 145262,
    "Rommel Santos": 145255,
    "Marissa Roxas": 145260,
    "Reycel Manalang": 145256,
    "Geleen Aiza Alvarez": 137093,
    "Sean Aslie Wenceslao": 137101,
    "Clara Mae Barit": 137130,
    "Clarisse Beth Santiago Congzon": 137456,
    "Kevin Herrerra Reyes": 137567,
    "Fiel Jerald Pascua": 137548,
    "Jessah Libradilla Simangan": 137548,
    "Ma. Angelica Arandia Nunez": 137550,
    "Kristy Marie Labsan Camungol": 137558,
    "Emileen Macalinao Maure": 137545,
    "Maricel Aldave": 137555,
    "Elinel Ortega": 139215,
    "Jediaelne Irie": 139217,
    "Ma. Virginia Alcazar Sebastian": 140699,
    "Erwilyn Ballesteros Mariano": 140699,
    "July Ann Dalanon Balbon": 140693,
    "Wilbert Bayani Montas": 140697,
    "Nadine Orande": 141898,
    "Leonelyn Cadayday": 141900,
    "John Lester Rualda": 141904,
    "Jana Lomayno": 141907,
    "Rochelle Ann Elison": 141908,
    "Myriel Laloen": 141909,
    "Rea Cañeda": 141911,
    "Joanna Panaguagan": 141912,
    "Kristy Ramos": 141913,
    "Antoinette Del Rosario": 141918,
    "Roy Ann Quintos": 141919,
    "Christine Joy Ubalde": 141905,
    "Edna Margarette Boado": 141916,
    "Donabel Mae Laquias": 141918,
    "Pereyra April": 141914,
    "Ruby Lyne Oliveros": 141899,
    "Angela Surigao": 141901,
    "Queen Danica Eso": 141902,
    "Charmaine Pacay": 141910,
    "Maria Paguirigan": 141911,
    "Irene Diening": 141922,
    "Marlyn Onga": 141924,
    "Jefferson Bernabe": 141924,
    "Christne Adduatu Castillones": 141744,
    "Mark Vincent Consuterio Nana": 141745,
    "Josephine Bautista": 141750,
    "Sean Nicole Abadiong": 142469,
    "Aria Sabina Legaspi": 142481,
    "Ryan Jake Ladrido": 142491,
    "John Nomer Salalac": 142512,
    "Bryan Ragie Balitao Serrano": 143052,
    "Marvin Pecundo Maronilla": 143042,
    "Angela Ocampo": 143046,
    "Rhonali Mae Tamparong": 143054,
    "Mica Jimenez": 141747,
    "Rochelle Deuda": 142501,
    "Cedrick Jade Arambulo": 142518,
    "Charlotte Puatu": 142785,
    "Jiana Mae Alarba": 142788,
    "Bryan Tria": 142791,
    "Christian Calilung": 142792,
    "Mary June Tan": 142794,
    "Ianne Jois Sarmiento": 142796,
    "Rachel Mae Lucenio": 142797,
    "Erika De Jesus": 142799,
    "Paul Michael Macaraig": 142803,
    "Rachelle Tolentino": 142824,
    "Gigi Lucero": 142787,
    "Alexandra Valdez": 142513,
    "Rica Mae Legaspi": 142514,
    "Jerrson Kendrick Santos": 142795,
    "Khrystel Marianne Cañada": 142801,
    "Earlvin Cañete": 142802,
    "Pauline Mae Quintia": 142804,
    "Christian Aries Furio": 142805,
    "Marves Beronio": 142809,
    "Princess Banzuela": 142810,
    "Christian Corsega": 142812,
    "Charlotte Dawn Deñoso": 142470,
    "John Matthew Pagdigan": 142472,
    "Vann Dio Lopez": 142473,
    "Monica Jose": 142474,
    "Cedric Andrel Flores": 142811,
    "Eunice Coyoca Nepangue": 143283,
    "Aprilynne Rose Gaston": 143287,
    "B-Jay Alvez": 143307,
    "Carlo Monreal": 142505,
    "Jessica Canillo": 143296,
    "Mark Roldan": 143299,
    "Keith Marden Bundalian": 143304,
    "Althea Jasmine Lianza": 143316,
    "Hannah Margaritha Lianza": 143224,
    "Ma. Jennifer Barrientos": 143241,
    "Jennifer Dimaranan": 143270,
    "Maricris Gilo": 143271,
    "Rozette Hazel San Juan": 143281,
    "Nikko Adlawan": 143287,
    "Marydel Jahaziel Galus": 144212,
    "Ron Kenneth Villanueva": 144215,
    "Fiel Jerald Pascua": 144215,
    "Mary Rose Ann Fontillas": 144213,
    "Krisha Bonita": 144219,
    "Lemyer Andaya": 144211,
    "Reinier Rabadan": 144205,
    "John Paul Echaloring": 144207,
    "Renso Cruizel Cosico": 144215,
    "John Michael Almaden": 144218,
    "Shirley Reyes": 134595,
    "Louie Andrew Duclayan": 144308,
    "Geline Josephine": 144613,
    "Ruel Fami": 144883,
    "Tiongo Mariel Nico": 144605,
    "Cruz Gille Pobejal": 144622,
    "Steven James Soleybar": 136565,
    "Justin Lesley Tolentino": 145218,
    "Rayden Roi Santos": 145216,
    "Ma. Rain Alcantara Abudanza": 136558,
    "Pia Danya Alcantara Domingo": 136561,
    "Vea Christine Na Posadas": 136554,
    "Joana Zantua": 136555,
    "Michael Adame Cruz": 136556,
    "Junrey Villafuerte Acebedo": 136565,
    "Tine Marie Dela Virgen": 136577,
    "Sherryl Pasaylo Asis": 137116,
    "Carl Kiennon Bagonoc Suelto": 137084,
    "Ralph Joseph Pernia": 137133,
    "Fermar Pilarta": 137123,
    "Sheryl Villanueva Hilado": 137113,
    "John Rene Gonzal Brecia": 137100,
    "Ezequel Bautista Batara": 137103,
    "Cariel Lou Tiosan Reyes": 137097,
    "Mary Rose Camila Desabelle": 137675,
    "Noemi Mingua": 137129,
    "Francis James Naong": 137144,
    "John Denver Destreza": 137128,
    "Mary Grace Esguerra": 137132,
    "Raziel Carisheila Rey": 137127,
    "Joy Candelaria": 137135,
    "Kimberly Joy Mondonedo Silva": 137099,
    "Mickaella Jhane Velasco Despi": 137546,
    "Danica Marianne Angeles": 137554,
    "Jinky Daang Magpala": 137578,
    "Renz Jalandoni Almohin": 137580,
    "Reizyl Orio Erna": 137585,
    "Maria Victoria Suyu Almacen": 137553,
    "Patrick Ray Cayaba Yanga": 137569,
    "Christian Carlo Delacruz Baticas": 137571,
    "James Gabriel Agustin Samson": 137575,
    "Rea Ella Busion Luanzo": 137542,
    "Jose Ma. Nunez Mabunay Jr": 137549,
    "Marycaille Bacalso Gomez": 137575,
    "William Villanueva": 137581,
    "Odessa Salditos Ramos": 137579,
    "Jeanne Lorraine Siute": 139220,
    "Princesa Gomez": 139214,
    "Rose Angelica Ayuson": 139226,
    "Neil Eusubio": 139227,
    "Jeremie Ortega": 139211,
    "Beatriz Omadle": 139229,
    "Gellian Yson": 139230,
    "Kenzo Chloe Frivaldo": 139207,
    "Abegail Joyce Garduque": 139201,
    "Donnalyn Manalo": 140685,
    "Jerome Abonales Santos": 140685,
    "Jade Resuello": 140691,
    "Xiaoya Mae Mendoza Loreha": 140704,
    "Mark Emmanuel Rabulan Salvador": 140705,
    "Jorizelyn Oba Orosco": 140686,
    "Apple Jane Tugao Ruado": 141748,
    "Aeron Jericho Pamatian Allado": 141731,
    "Manuelle Cariaso": 141735,
    "Kathleen Carezza Masola Zuela": 141737,
    "Joan Nicole Albano Ortiz": 141746,
    "Joanne Marie Singson": 141754,
    "Jenamie Gardena": 142471,
    "Cristopher Obrique": 142477,
    "Joammarc Rayvell Espinoza": 142480,
    "Edrill Seno": 142493,
    "Jonalyn Reyes": 143046,
    "Mary Cris C. Caysyab": 143049,
    "Dane Cridan Magat Azores": 143049,
    "Mark Anthony Llesol": 143050,
    "Brizel Joy De Leon Gonzales": 143041,
    "Roisin Cayce Castro Nava": 143045,
    "John Harold Escobin Manal": 143047,
    "Fideliza Jade Serrano": 143054,
    "Micko Magpantay": 143065,
    "Michell Esteban": 142497,
    "Fedjile Cabanado Mandalunes": 143044,
    "Gianne Rose Olasis Sandoval": 143048,
    "Adrian Parinilo": 142509,
    "Joseph Rebanal": 142499,
    "John Anthony Tames Baes": 142488,
    "Jeanboe Sacanle": 142507,
    "Erica May Gines": 142503,
    "Princess Carmile Carpio": 142508,
    "Carmela Salonga Armenta": 143047,
    "Regina Ira Tolentino": 143066,
    "Gabriel Delos Santos Gazes": 143057,
    "Jherilyn Escobilla Sagum": 143040,
    "Bernas Alvarez": 142896,
    "Abijah Jerusalem Riego": 143240,
    "Rodel Erese Macalino": 143257,
    "Anee Ciyel Pantoja": 143256,
    "Dara Shane Magno Soriano": 143259,
    "Angelica Jance Baltis": 143231,
    "Jerelyn Timbang": 143231,
    "Ronalyn Martinez": 143302,
    "Will Hector Jallorina": 143311,
    "Betty Mae Libunao": 143292,
    "Francis Bernard Gasmen": 143298,
    "Elaine Morales": 144042,
    "Hazel Celis": 144046,
    "Iy Hazel Caranguian": 144048,
    "Reian Aivrie Roasa": 144053,
    "Geneva May Dizon Balverde": 143239,
    "Larie Chavez": 143283,
    "Bryan Guirra": 143295,
    "Niño Verge Divina": 144050,
    "Marie Chris Uy": 144051,
    "Sarah Mae Cacerez": 144059,
    "Carl Johnriel Yadao": 144208,
    "Christian Bernardo": 144217,
    "Lyle Marie Nalangan": 144226,
    "Kenth Lester Antonio": 144364,
    "Christine Joy Tungcul": 144366,
    "Zenisa Garcia": 144359,
    "Erika Mae Dionisio": 144372,
    "Jhastine Mabasa": 144864,
    "Sederlyn Sergio": 144865,
    "Ian Guntalilib": 144882,
    "Portifio Aeron Paul": 144631,
    "Joshlyn Joy Garcia": 144880,
    "Robert Solancho": 144886,
    "Micheline April Fong": 144874,
    "Jerald Salvaleon": 144876,
    "Jessa Arevalo": 145227,
    "Czarina Day Almonte": 145264,
    "Kris Fernandez": 145266,
    "Alyssa Perez": 145278,
    "Ranwilyn Nievas": 145217,
    "Domingo Miranda": 145219,
    "Aaron Moises Libiran": 145228,
    "Alexi Manangan": 145281,
    "Catherine Goc": 145104,
    "Daisy Romero": 145063,
    "Judy Mae Hudale": 116949,
    "Leonalyn Gonzales": 145226,
    "Eduardo Gonzaga Borja": 136551,
    "Gladys Alexa Valenzuela Ambos": 136564,
    "Jessica Lara Hernandez": 136568,
    "Romel Oraye": 136585,
    "Ryan Joseph Casuncad Prado": 137102,
    "Rafael Allen Cuesta Masangkay": 137106,
    "Angelo Sabater": 137142,
    "Cedrick Enriquez": 137140,
    "Rachelle Ann Francisco Salvador": 137105,
    "Joemahma Codilla Amatong": 137107,
    "Jennifer Magno": 137146,
    "Melissa Navorra": 137145,
    "John Rodolf Paeste": 137125,
    "Khaycee Atienza": 137129,
    "Rona Joi Turalba": 137130,
    "Frrianne Torres": 137134,
    "John Rey Baquilar": 137139,
    "Jillian Hugo": 137145,
    "Johnaen Rebaldo Macabantad": 137104,
    "Mark Anthony Corsino": 137095,
    "Loreno Antonio Miguel": 137106,
    "Patricia Agatha Mae Perales": 137141,
    "Rachelle Ann Francisco Salvador": 137105,
    "Juan Miguel Apgoon Li": 137581,
    "Ma. Angelica Beatrice Andres Reyes": 137547,
    "Angelika Aquino": 137551,
    "Jayzel Capa": 137561,
    "Janesse Layne Lagumbay": 137565,
    "Renz Ivan De Guzman": 137565,
    "Adrianne Gawaran": 139216,
    "Airisha Poliquit": 139227,
    "Ana Mae Cruz": 139223,
    "Faith Bautista": 139210,
    "Leah Joy Estavillo": 139204,
    "Numbrado Jane Princess": 139209,
    "Aiza B. Bote": 139212,
    "Mark David Dio": 139218,
    "Ralie Joy Ramos": 139221,
    "Jessa Joy Pineda": 139222,
    "Kaycee Ann Francisco": 139222,
    "Mary Rose Marcelino": 139225,
    "Loriemae Olayvar": 139230,
    "Monica Caborda Villacora": 140695,
    "Jayson Belita": 140683,
    "Ma. Paulik Ysabelle Perez": 140686,
    "Michael Paul Mateo": 141901,
    "Andrea Mae Fabroa": 141903,
    "Jan Ramil Baloloy": 141913,
    "Erica Ysabel Ramirez": 141921,
    "Rowena Avila Santeco": 141917,
    "Mark Angelo Baligao": 141919,
    "John Rick Mancilla": 141920,
    "Kiara Mae Lee Vaal Villasis": 141727,
    "Vittorio Gabriel Talosig": 142491,
    "Alyssa Faye Latanes": 142492,
    "Erika Fajardo": 142499,
    "Angelica Flores De Gala": 142501,
    "Ma. Mikaela Zobel Ubaldo": 142498,
    "Ana Rose Villacorte": 142500,
    "Jane Polinario": 142468,
    "Chesa Mae Perez": 142487,
    "Jhon Oliver Pamintuan": 142475,
    "Joenela Cloud": 142792,
    "Ma. Elaine Capili": 142793,
    "Tracy Roco": 142798,
    "Cynthia Gacis": 142799,
    "Ghener Aliza Faye Manansala": 142900,
    "April Joy Barara": 142903,
    "Aljhune Alcantara Almario": 142882,
    "Cruz Vergara": 142887,
    "Jhon Rick Baun": 143048,
    "Jonathan Tenerifa": 143234,
    "JUDD ANDRE HABITAN BRUNO": 143235,
    "Vincent Puatu": 143238,
    "Christian Bernardo": 144217,
    "Hanna Siera Jean Pintor": 144052,
    "Maria Eloisa Cocamas": 144054,
    "Lourigie Bahatan": 143309,
    "Ashley Elianne Gamis": 143273,
    "Glaiza Mae Sadiwa": 144042,
    "Mhia Elamira Abella": 144313,
    "Samantha Bruza": 144060,
    "Vincent Joa Emmanuel Pelaez Rumbaoa": 144325,
    "Jeremy Regala": 144216,
    "Aileen Grace Garcia": 144321,
    "Joshua Danielle Quain Castro": 144362,
    "Philip Ray Destreza": 144363,
    "Maricar Inamarga": 144607,
    "Letada Jessa": 144601,
    "Elijah Jhaile Avellana": 144889,
    "Nicole Roxas": 145050,
    "Allira Jean Habanez": 145111,
    "Bryan Moneda": 146048,
    "Shierley Manalo": 146049,
    "Celestino Mendoza": 145096,
    "Renato Olivo Jr.": 145098,
    "Ericson Pabua": 145228,
    "Lhuzell Teffany Cruz": 145116,
    "Mary Jane Nabong": 145226,
    "Jeben Villasis": 145279,
    "Bill Dominick Oblipeas": 145264,
    "Edgardo O Tan Guat": 145233,
    "Jhudiel Mabini": 144021,
    "Aimee Co": 145095,
    "Julius Pastor": 145230,
    "Maricar Inamarga": 144607,
    "Ericson Pabua": 145228,
    "Meljane Cadudu-an": 145098,
    "Louis Andrei Dulla": 145209,
    "Cleirf Nierra": 145206,
    "Beavoll Casama Montalban": 137111,
    "Cromwell Peguet": 143306,
    "Rachelle Mae Fontillan": 144211,
    "Cromwell Peguet": 143306,
    "Princess Amanda Radaza Repomanta": 133778,
    "Arje Malandog": 144225,
    "Paulo Jennifer": 144619,
    "Mary Grace Marcelino": 139225,
    "Joenela Cloud": 142792,
    "Charina Dacanay Cruz": 144618,
    "Jennifer Valle Garcia": 134620,
    "April Lorenzo Espinosa": 134602,
    "Catherine Goc": 145104,
    "Caryl Mayuga": 145108,
    "Mark Francis Esquivias Millares": 145226,
    "Edgar Manacap Jr.": 145091,
    "Mary Joy Cale": 143242,
    "Dennir C Roscam": 103087,
    "Charlyn Rosacena Tames": 137117,
    "Mary Kathleen Abdon": 145221,
    "Meljane Cadudu-an": 145098,
    "Gilbert Beltran": 142496,
    "Christian Dave Villanen": 116922,
    "Kiara Mae Lee Vaal Villasis": 141727,
    "Ghener Aliza Faye Manansala": 142900,
    "Johnaen Rebaldo Macabantad": 137104,
    "Roselo Balasta": 116958,
    "Mairry Grace Rebomantan": 116934,
    "Angelica Ibrahim": 116860,
    "Odette Toraja": 133792,
    "Erica Rose Gamas": 116905,
    "Adrian Fortozo": 116878,
    "Mary Grace Rebamontan": 116934,
    "Jazzer Mirabueno": 116846,
    "Kate Allyon Frias": 153355,
    "Marian Mallorca": 116898,
    "Windy Manangan": 105033,
    "Maria Eloisa Cocamas": 144054,
    "Karie Shine Fulgar": 155694,
    "Gail Añonuevo": 157014,
    "Iris Bulawit": 116985,
    "Aimee Co": 145095,
    "Loreno Antonio Miguel Recede": 137106,
    "Julius Pastor": 145230,
    "Danielle Jhan Arias": 145229,
    "Kaila Belle Andarzo": 124230,
    "Mary Joecel Jr. Cano": 150244,
    "Marielle Jordas": 157023,
    "Jhena Mae Setier": 157034,
    "Ruth Janie Pabiana": 157038,
    "Hanz Dale Majerano": 157016,
    "Adrianne Gawaran": 139216,
    "Christian Dave Beltran": 116922,
    "Patrick Gian Joselino Balao": 141826,
    "Anna Liza Malco": 150046,
    "Vincent Joe Emmanuel Pelaez Rumbaoa": 144325,
    "John Timothy Espinosa": 144618,
    "John Isaac Benitez": 117011,
    "Bettina Tubog": 145119,
    "Esther Manalang": 144626,
    "Maria Sophia Diongzon": 133780,
    "Glenda Espinosa": 157015,
    "Sixto Bidhong": 116931,
    "Michael Brian Dela Cruz": 116931,
    "Sixto Bidhong": 116931,
    "Joan Dizon": 157019,
    "Janice Fabristante": 157022,
    "Joyce Marie Galarido": 164033,
    "Aaron Velasco": 160857,
    "Irish Garcia": 155696,
    "Marianne Valleador": 160867,
    "Angeline Perez": 157045,
    "Jonalyn A. Artaste": 164045,
    "Adelfa Theresa Celestino": 164050,
    "Ronette Borreta": 164022,
    "Gemmalyn Krizza Salangit": 157032,
    "Aimee Crizelda Romero": 157035,
    "John Millard Calixto": 162535,
    "Melliza Cerveza": 162535,
    "Rachelle Ann Batac": 155685,
    "Aaron Louis Rodriguez": 165575,
    "Maria Sarah Leonora Reyes": 165577,
    "John Mark Magasullo": 150240,
    "Sheremhel Bugayong Tangonan": 166000,
    "Charles John Vicencio": 164376,
    "Nerissa Bania": 164344,
    "Jenessy Allueen": 154762,
    "John Macalinao": 164075,
    "Chris June Balon": 165083,
    "Aira Esguerra": 165072,
    "Allyn Perea Alona": 165601,
    "Jona Mikaela Del Rosario": 165602,
    "Sophia Bolanos": 166380,
    "Maria Ysabel Seladuga": 166380,
    "Jheryyl Joy Esguerra": 166383,
    "Jheryyl Joy Esguerra": 166379,
    "Maureen Alba Ramos": 162521,
    "Lovely Queen Batan": 162534,
    "Jazaire Irinco": 165027,
    "Alain Duo": 164031,
    "Glaziele Aloquiza": 165023,
    "Danielle Jhan Arias": 145229,
    "Argyllne Jean Jaeleniel Moriones": 162514,
    "Harvey Manlangit": 162529,
    "Danica Gonzalez": 164032,
    "Dieny Dipay": 164037,
    "Gabrielle A. Pangilinan": 164028,
    "Jhimmy Sio": 164043,
    "Cherry Mae K. Bilagot": 164021,
    "Romato M. Lorenzo": 164020,
    "Mark Anthony D. Pacis": 164042,
    "Roslyn Agoto": 185130,
    "Aira Mae Bosegro": 164010,
    "Luvisito Clores": 164096,
    "Carmela Zamudio": 164061,
    "Nina Villanueva": 164063,
    "Aira Mae Layo": 164291,
    "Glen Gumabao": 164284,
    "Jhon Vergel Alap": 166300,
    "Ma. Joana Mae Bajado": 166295,
    "Menjel Alberca": 166293,
    "Raymond Abonero": 166290,
    "Cyril Mae Ogriman": 165187,
    "Ruffa Sacdalan": 164066,
    "Sophia Marasigan": 165059,
    "Job Cozbi David": 165089,
    "Lorella Amang": 165060,
    "Cristine Badlis": 165086,
    "Mariah Roxey Domasig": 165572,
    "Loricelo Tercero": 165580,
    "Modelyn Maerina": 165583,
    "Crisza Camao": 165587,
    "Nelvera Diolata": 165592,
    "Gian Calingasan": 165593,
    "Kian James Buco": 166377,
    "Joanne Lim": 166318,
    "Rosanna Guiling": 166321,
    "Christian Joy Sto Domingo": 166328,
    "Isaiah Anthony Forcadela": 166333,
    "John Noel Cano": 166338,
    "Neil Jhayr Batigas": 168346,
    "Rica Joy Manzanades": 168342,
    "Gerald Aviso": 168350,
    "Jene Domulo Nañez": 168343,
    "Aaisa Leilyne Mariano": 166343,
    "Junell Tayan": 116830,
    "Juliana Maratas": 133792,
    "Joyce Muty": 136846,
    "Mary Anne Battung": 160147,
    "Isabel Bandaay": 166278,
    "Cynthia Capistrano": 166279,
    "Trisha Serverino": 165060,
    "Sharay Joy Lontoc": 165077,
    "Ann Clarisse Gutierrez": 165085,
    "Jovilyn Molleno": 165087,
    "Joana Grace Mabanan": 165073,
    "Edmark Ian Ordiz": 165079,
    "Chastine Ocampo": 165084,
    "Zennith Joy Adrias": 166358,
    "Lester Caparas": 166360,
    "Cynthia Reboldera": 166363,
    "Rey Ann Sinfuego": 166369,
    "Diana Rose Seguros": 166373,
    "Belinda Castro": 166381,
    "Arianne May Baldonado": 166383,
    "Alice Gaite": 166385,
    "Jessica Tan": 166386,
    "Almond Chris Desiar": 166404,
    "Flordeliza Caco": 166406,
    "Lizzy Sheena Geneta": 166389,
    "Micaella Carille Antonio": 166403,
    "Tricia Mayne Latorre": 166409,
    "Genelyn Bobadilla": 166413,
    "Jomel Balaong": 166348,
    "Angel Atos": 166361,
    "Sunshine Blue Abasiar": 166355,
    "Ferdinand Abalos": 166362,
    "Ferdinand Foronda": 166347,
    "Ivorne Morado": 166846,
    "Siti Hadjer Mustapha": 166405,
    "Ma. Angela Ubaldo Andres": 164054,
    "Rachelle Ann Andres": 164056,
    "Mharipe Fesico": 166895,
    "Danielle Joyce Cruz": 166395,
    "Kevin Arcent David": 134425,
    "Maria Ana Alagao": 164082,
    "Victoria Anne Pineda": 164084,
    "Irish Melissa Bentijaba": 164090,
    "Reian Aivrie Roasa": 144053,
    "Jhon Ylron Laquian": 165065,
    "Juny Ann Christorado": 165653,
    "Mark Christoper Andria": 166357,
    "Delmar Agpalza": 166361,
    "Patrick Espanola": 166362,
    "Jithro Menzon": 166364,
    "Norald Navarro": 166379,
    "Dianne Bacud": 166388,
    "Joshua Hero Bagonoc": 166389,
    "Mary Grace Laurino": 166393,
    "Althea Montenegro": 166394,
    "Julius Ceasar Bautista": 166589,
    "Mikaela Balaba": 166599,
    "Aravhilla Dolano": 166627,
    "Daniele Casinsinan": 166276,
    "Edward Gerona": 166273,
    "Mariel Sadioa": 166281,
    "Maura Ebuen": 166285,
    "Mary Charmaine Poliquit": 166287,
    "Gwyneth Ramos": 166289,
    "Princess May Imperial": 166297,
    "Ivan Torren": 166328,
    "Grace Simon": 167330,
    "Alvin Ceria": 167335,
    "Christian Manabat": 167343,
    "Shiela Bate Mendoza": 167345,
    "Ma. Andrea Ann Gloria": 167352,
    "Rose Peñaranda": 167329,
    "Matthew Lorenz Sotto": 167348,
    "Jessa Mae Ularte": 167356,
    "Ryan Drin Vincent Singson": 167362,
    "Ma. Bernadette Moreno": 170266,
    "Bryan Oczar Albino": 164067,
    "Johnny Red": 164105,
    "Rachelle Cruz": 164106,
    "Jerelyn Moldero": 164084,
    "Leah Joy Estavillo": 164088,
    "Mark Lactaotao": 164109,
    "Charmaine Grace Pasomanero": 164094,
    "Lovely Pecson": 164080,
    "Donita Rose Nana": 164090,
    "Mitzi Caroline Hankins": 165074,
    "Zary Anne Magay": 164089,
    "Charlene Barrientos": 164098,
    "Rachelle Cruz": 164106,
    "Jennylyn Faelnar": 165574,
    "Emmanuel James Imperial": 165581,
    "Lea Mae Mendoza": 165584,
    "Darylle Anne Sagun": 165588,
    "Razer Antolin": 165686,
    "Romeo San Antonio Jr": 166365,
    "Cynthia Capistrano": 166279,
    "Nancy Alalan": 165590,
    "Marifel Cabilic": 166370,
    "Raymond Soriano": 166384,
    "Aira Mariel Pardoce": 166392,
    "Raf Sy": 166393,
    "Christian San Juan": 166396,
    "Aaron Joshua Hermogino": 166399,
    "Jerome Rabe": 166401,
    "Michael Carluto": 166409,
    "Meryl Castigador": 166402,
    "Lorenzo Jay Evasco": 166407,
    "Manny Hann Francisco": 166418,
    "Jillianne Liana Bamba": 166416,
    "Queniter Natañon": 166417,
    "Emmethone Corrales": 166410,
    "Kyla Camaso": 166322,
    "Leane Mae Barlongay": 168326,
    "Lindsay Grona": 168314,
    "Rechelle Ann Ayala": 168329,
    "Camille Alconez": 168347,
    "Jade Murillo": 168340,
    "Art Balandon": 168342,
    "Jade Murillo": 168340,
    "Jonna Borlas": 168341,
    "Ma Alexia Benitez": 116972,
    "Charito Lontoc Valerios": 164025,
    "Catherine Grace Consulta Alonzo": 164026,
    "Arnel Hermogino": 167340,
    "Mark Angelo Elauria": 165060,
    "Mark Joseph Jamilano": 165062,
    "Precious Marie Canuelos": 165050,
    "Bryan Alfarejos": 165078,
    "Jefferson Ramiscal": 166581,
    "Regie Fajarillo": 165585,
    "Rachelle Cruz": 164106,
    "John Wesley Dela Cruz": 159053,
    "Jonalyn Joy Rodriguez": 166373,
    "Darlene Grace Labita": 160136,
    "Shiela Mae Gunayan": 161073,
    "Rachelle Ann Bueno Lacson": 166031,
    "Euderlyn Daquia": 160150,
    "Hanna Siera Jean Pintor": 144052,
    "Arlene Castro": 160156,
    "Ashley Ali": 166331,
    "Hensell Sabino": 166296,
    "Jay Anna Isabelle Lumabang": 166298,
    "Jherald Salvador": 167338,
    "Rhea Ann Calimag": 167341,
    "Sydney Buenaventura": 167339,
    "Trisha Serverino": 165060,
    "Yuril Nolan": 170272,
    "Tashna Ann Estrada": 165234,
    "Xyerla Toralba": 170268,
    "Fahad Santos": 164079,
    "Reyniel Daile Aqui": 164080,
    "Ma. Kasandra Ansley Austria": 164082,
    "Norahln Nocos": 164096,
    "Justine Cañares": 164100,
    "Adrielle Menes": 166385,
    "Mark Justin Pabelo/Ree Vffda": 166825,
    "Marjorie Comahig": 168330,
    "Pauline De Luna": 168340,
    "Marie Antoniette De Guzman": 166416,
    "Sakio Tanfuji": 155739,
    "Mariane Taneo": 141935,
    "Maria Leigh Palama": 155735,
    "KRISTELLE monica de gracia": 160154,
    "Joel Doblada": 133984,
    "Darlene Grace Baguio": 137096,
    "Mia Mae Alias Alias": 116973,
    "Rhanein De Jesus": 154256,
    "Jillian Hugo": 137145,
    "Kyla Espina Casquejo": 166316,
    "John Alfred Llaneta": 161066,
    "Maricar Onrubia": 153351,
    "Nomarita Madrigal": 157057,
    "Jonathan Viray": 160141,
    "John Lloyd Canlas": 157061,
    "Reuben Bhen Ruben Calina": 160862,
    "Gynella Mae Sol": 161071,
    "Jeffrey Santos": 166986,
    "Michelle Dioras": 166885,
    "Vannesa Mariel Dagaraga": 134375,
    "Jhennefer Micaela Manela": 133709,
    "Donnae Tanterna": 116883,
    "Mikaela Tiu": 116921,
    "Bernadette Ann Cabali Pestañas": 164254,
    "Jessica Miranda": 116987,
    "Jillianne Caspe": 164024,
    "Diosa Marie Bagang": 166313,
    "Jazmin Erika Rico Malarde": 134451,
    "Glady-Jenn Camposano": 134581,
    "Hannah Lanchico": 134139,
    "John Mervin Masangya": 134591,
}
iex_mapping_clean = {" ".join(k.split()).lower(): v for k, v in iex_mapping.items()}


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
                            avail_val = str(row.get("Available For", "")).upper()
                            
                            is_avail_update = (row["Type"] == "AGENT_AVAILABILITY/UPDATED")
                            is_voice = is_avail_update and "VOICE" in avail_val
                            is_msg = is_avail_update and "MESSAGING" in avail_val
                            is_mail = is_avail_update and ("MAIL" in avail_val or "EMAIL" in avail_val)
                            is_task = is_avail_update and "TASK" in avail_val
                            
                            is_any_avail = is_voice or is_msg or is_mail or is_task
                            is_floor_support = (row["Type"] == "AGENT_STATUS/CHANGED_ACTIVE_REASON" and row.get("Active Reason") == "Floor Support (Unavailable)")

                            if is_returned_away or is_any_avail or is_floor_support:
                                meal_end = row["Timestamp"]
                                duration_sec = (meal_end - meal_start).total_seconds()
                                duration_min = duration_sec / 60.0

                                limit_sec = MEAL_LIMIT_MINS * 60
                                exceeded_sec = max(0, duration_sec - limit_sec)
                                exceeded_str = f"{int(exceeded_sec // 60)}m {int(exceeded_sec % 60)}s" if exceeded_sec > 0 else "0m 0s"
                                
                                # Determine specific return activity text
                                if is_floor_support:
                                    return_activity = "Floor Support (SME)"
                                elif is_msg:
                                    return_activity = "Back to Messaging"
                                elif is_mail:
                                    return_activity = "Back to Email"
                                elif is_task:
                                    return_activity = "Back to Task"
                                elif is_voice:
                                    return_activity = "Back to Voice"
                                

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
                final_rows = []
                for agent in sorted(agent_map.keys()):
                    data = agent_map[agent]
                    row_data = {"Agent": agent}

                    # Pad out break columns (Break 1, Break 2, etc.)
                    for i in range(max_breaks):
                        col_name = f"Break {i+1}"
                        if i < len(data["breaks"]):
                            row_data[col_name] = data["breaks"][i]
                        else:
                            row_data[col_name] = "-"

                    row_data["Total Exceeded (Mins)"] = data["total_exceeded"]
                    row_data["Status"] = "❌ Exceeded SLA" if data["total_exceeded"] > 0 else "✅ Within SLA"
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

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

st.set_page_config(
    page_title="EV Data Insights",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp { background-color: #121212 !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a1a 0%, #212121 100%) !important; }
[data-testid="stSidebar"] * { color: #FFFFFF !important; }
[data-testid="stSidebar"] hr { border-color: #2e4a6b !important; }
/* Sidebar nav items */
[data-testid="stSidebar"] .stRadio label div[data-testid="stMarkdownContainer"] ~ div,
[data-testid="stSidebar"] .stRadio label > div:first-child {
    display: none !important;
}
[data-testid="stSidebar"] .stRadio label {
    padding: 8px 16px !important;
    border-radius: 8px !important;
    display: block !important;
    cursor: pointer !important;
    color: #b0c4de !important;
    font-size: 0.88rem !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255, 255, 255, 0.08) !important;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: rgba(103, 25, 41, 0.35) !important;
    border-left: 3px solid #671929 !important;
    color: #671929 !important;
    font-weight: 700 !important;
}

/* Remove default white block backgrounds */
[data-testid="stVerticalBlock"] > div { background: transparent !important; }
section[data-testid="stMain"] > div { background: transparent !important; }

.module-header {
    padding: 1.4rem 1.8rem;
    border-radius: 14px;
    margin-bottom: 1.8rem;
    color: white;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}
.metric-card {
    background: #121212;
    border: 1px solid #FFFFFF;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
}
.metric-card h3 { font-size: 0.72rem; color: #FFFFFF; margin: 0; text-transform: uppercase; letter-spacing: 0.07em; }
.metric-card h2 { font-size: 2rem; font-weight: 800; color: white !important; margin: 6px 0 2px 0; }
.metric-card p  { font-size: 0.78rem; color: #FFFFFF; margin: 0; }

.mod-card {
    background: #252525;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    margin-bottom: 1rem;
    height: 130px;
}
.mod-card .name { font-size: 1rem; font-weight: 700; color: #5ba989; margin: 5px 0 7px 0; }
.mod-card .desc { font-size: 0.78rem; color: #FFFFFF; line-height: 1.5; }

/* Nav button — pulled up into bottom-right of mod-card */
.mod-card + div[data-testid="stButton"] {
    margin-top: -2.6rem !important;
    display: flex !important;
    justify-content: flex-end !important;
    padding-right: 1rem !important;
    position: relative !important;
    z-index: 10 !important;
}
.mod-card + div[data-testid="stButton"] button {
    background: transparent !important;
    border: 1px solid #5ba989 !important;
    color: #5ba989 !important;
    border-radius: 6px !important;
    padding: 0.15rem 0.55rem !important;
    font-size: 0.8rem !important;
    min-height: unset !important;
    height: 1.6rem !important;
    width: auto !important;
    line-height: 1 !important;
}
.mod-card + div[data-testid="stButton"] button:hover {
    background: #5ba989 !important;
    color: #121212 !important;
}

.finding-box {
    background: #252525;
    border-left: 4px solid #21498a;
    border-radius: 14px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.8rem;
    font-size: 0.88rem;
    color: #e2e8f0;
    line-height: 1.6;
}
.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #000000;
    background: #ba945a;
    border-radius: 8px;
    padding: 0.4rem 0.8rem;
    display: inline-block;
    margin: 1.5rem 0 1rem 0;
}

.chart-label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #555;
    margin-bottom: 0.5rem;
}

/* Tab static */
.stTabs [data-baseweb="tab"] {
    color: #ffffff !important;
}
/* Tab hover */
.stTabs [data-baseweb="tab"]:hover {
    color: #5ba989 !important;
    transition: all 0.2s ease;
}
/* Tab active */
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #5ba989 !important;
}
/* Active tab underline bar */
.stTabs [data-baseweb="tab-highlight"] {
    background-color: #5ba989 !important;
}
</style>
""", unsafe_allow_html=True)

PAGES = [
    "Overview",
    "Data Preprocessing",
    "The OLAP Analysis",
    "Clustering Outcomes",
    "Association Rules",
    "Outlier Detection",
    "The Predictive Model",
]

MODULE_COLORS = {
    "Overview":             "#a78bfa",
    "Data Preprocessing":   "#22d3ee",
    "The OLAP Analysis":    "#f472b6",
    "Clustering Outcomes":  "#818cf8",
    "Association Rules":    "#34d399",
    "Outlier Detection":    "#fb7185",
    "The Predictive Model":  "#38bdf8",
}

GRADIENT_MAP = {
    "Overview":            ("135deg", "#671929", "#9b2335"),
    "Data Preprocessing":  ("135deg", "#671929", "#9b2335"),
    "The OLAP Analysis":   ("135deg", "#671929", "#9b2335"),
    "Clustering Outcomes": ("135deg", "#671929", "#9b2335"),
    "Association Rules":   ("135deg", "#671929", "#9b2335"),
    "Outlier Detection":   ("135deg", "#671929", "#9b2335"),
    "The Predictive Model":("135deg", "#671929", "#9b2335"),
}

if "page" not in st.session_state:
    st.session_state.page = "Overview"

with st.sidebar:
    st.markdown("# EV Data Insights")
    page = st.radio("Navigate", PAGES,
                index=PAGES.index(st.session_state.page),
                label_visibility="hidden")
    st.session_state.page = page
    st.markdown("---")
    st.caption("EV Population Dataset (Washington State)\n271,103 registrations · 246 counties")
    st.caption("©Soundarya Lahari Singaraju")

color  = MODULE_COLORS[page]
deg, c1_grad, c2_grad = GRADIENT_MAP[page]

def module_header(title, subtitle):
    st.markdown(f"""
    <div class="module-header" style="background: linear-gradient({deg}, {c1_grad}, {c2_grad});">
        {title}<br>
        <span style="font-size:0.88rem; font-weight:400; opacity:0.88;">{subtitle}</span>
    </div>""", unsafe_allow_html=True)

def metric_card(label, value, sub, accent):
    st.markdown(f"""
    <div class="metric-card">
        <h3>{label}</h3>
        <h2 style="color:{accent};">{value}</h2>
        <p>{sub}</p>
    </div>""", unsafe_allow_html=True)

def finding(text,accent):
    st.markdown(f"""
    <div class="finding-box">
        {text}
    </div>""", unsafe_allow_html=True)

def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)

def show_fig(path, caption=""):
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.warning(f"Figure not found: {path}")

# ── OVERVIEW ───────────────────────────────────────────────────
if page == "Overview":
    module_header("EV Population Insights (Washington State)", "CSCI 5455: Data Mining Project")

    col1, col2, col3, col4 = st.columns(4)
    with col1: metric_card("Total Records",   "271,103", "vehicle registrations", "#1F3864")
    with col2: metric_card("Counties",        "246",     "incl. out-of-state",    "#7b2d8b")
    with col3: metric_card("BEV Share",       "79.8%",   "vs 20.2% PHEV",         "#1a6b3c")
    with col4: metric_card("Model Accuracy",  "100%",    "Random Forest F1",      "#2d6b4f")

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Project Modules")

    cols = st.columns(3)
    modules_info = [
        ("Data Preprocessing",  "271,103 rows cleaned · 4 features engineered · 246 county profiles built"),
        ("The OLAP Analysis",   "5 research questions answered · Tesla 6× dominance · 68.9% Modern Era"),
        ("Clustering Outcomes", "K=4 clusters · Silhouette=0.44 · King County isolated as solo cluster"),
        ("Association Rules",   "1,240 rules mined · Luxury brand clustering · Make weak type predictor"),
        ("Outlier Detection",   "King County flagged by all 4 methods · Z-score = 14.79 · 8 secondary outliers"),
        ("The Predictive Model","RF Accuracy 100% · 2 errors on 54,221 test records · CV F1 = 1.000 ± 0.000"),
    ]
    for i, (name, desc) in enumerate(modules_info):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="mod-card">
                <div class="name">{name}</div>
                <div class="desc">{desc}</div>
            </div>""", unsafe_allow_html=True)
            if st.button("→", key=f"btn_{i}"):
                st.session_state.page = name
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Key Findings Across All Modules")
    finding("EV adoption exploded post-2022 — the Modern Era accounts for <b>68.9%</b> of all registrations despite covering only 3–4 model years.", "#1F3864")
    finding("King County is a <b>formal multivariate outlier</b> — flagged by all 4 detection methods with Z-score of 14.79 on Total EVs.", "#8b1a1a")
    finding("Tesla has <b>6× more registrations</b> than #2 Chevrolet and appears in 76.8% of all counties statewide.", "#7b2d8b")
    finding("BEV vs PHEV is determined by <b>vehicle design, not geography</b> — County and Cluster contribute 0% to predictive importance.", "#2d6b4f")
    finding("The 59 PHEV-dominant counties in Cluster 1 are <b>primarily out-of-state registrations</b>, not a Washington State pattern.", "#b85c00")

# ── MODULE 01 — PREPROCESSING ──────────────────────────────────
elif page == "Data Preprocessing":
    module_header("Data Preprocessing", "Data cleaning, type fixing, feature engineering, county aggregation")

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Raw Records",    "271,103", "rows × 16 columns",        "#1a6b3c")
    with c2: metric_card("Rows Dropped",   "10",      "missing county/city",       "#e87c20")
    with c3: metric_card("New Features",   "4",       "engineered columns",        "#1a6b3c")
    with c4: metric_card("County Profiles","246",     "aggregated county table",   "#2d6b4f")

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Key Preprocessing Decisions")
    finding("<b>5 columns dropped</b> — VIN, DOL Vehicle ID, Base MSRP, 2020 Census Tract, Legislative District (not useful for analysis).", "#1a6b3c")
    finding("<b>Type corrections</b> — Postal Code and Legislative District converted from float to string. Electric Range from float to int.", "#1a6b3c")
    finding("<b>Electric Range zeros are NOT errors</b> — 170,816 PHEVs record 0 miles. This is standard DOL database behaviour for PHEVs.", "#e87c20")
    finding("<b>4 features engineered</b> — CAFV_Category (3-label), EV_Type (BEV/PHEV), Range_Category (4-bucket), EV_Era (4-era).", "#1a6b3c")
    finding("<b>246 counties found</b> — dataset includes out-of-state registrations, not just Washington State counties.", "#2d6b4f")

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Feature Engineering Summary")
    feat_data = {
        "Feature":      ["CAFV_Category", "EV_Type", "Range_Category", "EV_Era"],
        "Derived From": ["CAFV Eligibility string", "Electric Vehicle Type string", "Electric Range (miles)", "Model Year"],
        "Values":       ["Eligible / Not Eligible / Unknown", "BEV / PHEV", "No Range / Low / Medium / High", "Early EV / Growth / Mainstream / Modern"],
        "Used In":      ["OLAP, Predictive Model", "All modules (target variable)", "Association Rules, OLAP", "OLAP, Clustering"],
    }
    st.dataframe(pd.DataFrame(feat_data), use_container_width=True, hide_index=True)

# ── MODULE 02 — OLAP ───────────────────────────────────────────
elif page == "The OLAP Analysis":
    module_header("The OLAP Analysis", "Exploratory Analysis of EV Registration Patterns")

    c1, c2, c3 = st.columns(3)
    with c1: metric_card("Tesla Registrations","110,530","6× above #2 Chevrolet",    "#7b2d8b")
    with c2: metric_card("Modern Era Share",   "68.9%",  "2022+ model years",        "#b44fcf")
    with c3: metric_card("BEV Statewide",      "79.8%",  "vs 20.2% PHEV",            "#1a5c8b")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Registrations Over Time", "Manufacturers", "BEV vs PHEV", "Range & CAFV", "Utilities"])

    with tab1:
        finding("<b>68.9% of all registrations are from the Modern Era (2022+)</b> despite it covering only 3–4 model years. Growth is exponential.", "#7b2d8b")
        show_fig("outputs/figures/q1_ev_registrations_over_time.png")
    with tab2:
        finding("<b>Tesla dominates with 110,530 registrations</b> — nearly 6× Chevrolet (19,044). Rivian is already at #9 despite being a new entrant.", "#7b2d8b")
        show_fig("outputs/figures/q2_manufacturer_distribution.png")
    with tab3:
        finding("<b>79.8% BEV statewide</b>. Most counties trend above the 80% BEV baseline. PHEV-heavy counties are primarily out-of-state registrations.", "#7b2d8b")
        show_fig("outputs/figures/q3_bev_phev_proportions.png")
    with tab4:
        finding("<b>CAFV-eligible vehicles</b> have median range of 87 mi vs 21 mi for ineligible. BEV range shows bimodal distribution: ~100 mi older and 250+ mi modern.", "#7b2d8b")
        show_fig("outputs/figures/q4_range_vs_cafv.png")
    with tab5:
        finding("<b>Puget Sound Energy dominates</b> — serves 96,386 + 56,993 vehicles across two service entries. Far ahead of all other utilities.", "#7b2d8b")
        show_fig("outputs/figures/q5_utility_ev_counts.png")

# ── MODULE 03 — CLUSTERING ─────────────────────────────────────
elif page == "Clustering Outcomes":
    module_header("Clustering Outcomes", "K-Means on 246 county profiles · K=4 · Silhouette = 0.4421")

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Optimal K",       "4",      "elbow + silhouette",      "#b85c00")
    with c2: metric_card("Silhouette Score","0.4421", "confirmed at K=4",        "#b85c00")
    with c3: metric_card("PCA Variance",    "63.7%",  "PC1=41% · PC2=22.7%",    "#e87c20")
    with c4: metric_card("King County",     "Alone",  "solo cluster — 133,815 EVs", "#8b1a1a")

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Cluster Profiles")

    cl1, cl2, cl3, cl4 = st.columns(4)
    clusters = [
        (cl1, "Cluster 0", "Low Adoption BEV-Leaning", "#1a5c8b", "156 counties", "Avg 6.93 EVs · 92% BEV · 2.7 unique makes"),
        (cl2, "Cluster 1", "Low Adoption PHEV-Dominant", "#b85c00", "59 counties", "Avg 2.20 EVs · 75% PHEV · Out-of-state registrations"),
        (cl3, "Cluster 2", "High Adoption Mixed Fleet", "#1a6b3c", "30 counties", "Avg 4,535 EVs · 74% BEV · 32 makes · 107 models"),
        (cl4, "Cluster 3", "King County Mega Hub", "#8b1a1a", "1 county", "133,815 EVs · 82% BEV · 44 makes · 179 models"),
    ]
    for col, cname, label, clr, counties, stats in clusters:
        with col:
            st.markdown(f"""
            <div class="mod-card" style="border-top: 4px solid #4b6ca2;">
                <div class="name">{label}</div>
                <div class="desc">{counties}<br>{stats}</div>
            </div>""", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        show_fig("outputs/figures/pca_clusters.png", "PCA scatter — clusters in 2D space")
    with col_b:
        show_fig("outputs/figures/cluster_heatmap.png", "Cluster feature heatmap")

# ── MODULE 04 — ASSOCIATION RULES ──────────────────────────────
elif page == "Association Rules":
    module_header("Association Rules", "Apriori mining · 1,240 rules · 3 analyses")

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Total Rules",      "1,240",  "min_support = 0.05",      "#1a5c8b")
    with c2: metric_card("Top Lift",         "10.70",  "Jaguar → Acura",          "#1a5c8b")
    with c3: metric_card("Type Rules",       "35",     "make → BEV/PHEV",         "#2a8bc4")
    with c4: metric_card("Cluster Rules",    "37",     "make → county cluster",   "#1a5c8b")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Co-occurrence Rules", "Make → EV Type", "Make → Cluster"])
    with tab1:
        finding("<b>Niche luxury brands cluster together</b> — Jaguar+Acura (lift 10.70), Fisker+Smart (10.56). They appear in the same small set of affluent counties.", "#1a5c8b")
        finding("<b>Tesla rules are trivial</b> — Tesla appears in 76.8% of counties, making its rules low-lift and uninformative for pattern discovery.", "#8b1a1a")
        col_a, col_b = st.columns(2)
        with col_a: show_fig("outputs/figures/association_rules_scatter.png", "Support vs Confidence scatter")
        with col_b: show_fig("outputs/figures/top_rules_by_lift.png", "Top rules by lift")
    with tab2:
        finding("<b>Make is a weak EV type predictor</b> — 34 of 35 type rules predict BEV at uniform lift=1.2. Only Jeep predicts PHEV (lift=1.18). Make presence alone does not determine BEV/PHEV county preference.", "#1a5c8b")
        show_fig("outputs/figures/make_type_cluster_rules.png", "Make → Type and Make → Cluster rules")
    with tab3:
        finding("<b>Niche brands predict high-adoption counties</b> — Acura (lift=7.84), Smart (7.83), Fisker (7.74) are strong proxies for Cluster 2 (High Adoption) counties.", "#1a5c8b")
        show_fig("outputs/figures/make_cooccurrence_heatmap.png", "Make co-occurrence heatmap")

# ── MODULE 05 — OUTLIER DETECTION ──────────────────────────────
elif page == "Outlier Detection":
    module_header("Outlier Detection", "IQR · Z-Score · Isolation Forest · LOF · 4-method consensus")

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("King Z-Score",    "14.79",  "nearly 15 std devs above mean", "#8b1a1a")
    with c2: metric_card("Methods Flagged", "4 / 4",  "King County — unanimous",       "#8b1a1a")
    with c3: metric_card("IF Score",        "0.2769", "highest in dataset",            "#c43030")
    with c4: metric_card("3-Method Counties","8",     "Snohomish, Pierce + 6 more",    "#8b1a1a")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["IQR", "Z-Score", "Isolation Forest", "LOF", "Consensus"])
    with tab1:
        finding("<b>IQR upper fence = 11 EVs</b> — 75% of all counties have ≤11 EVs. This extreme skew means 47 counties are technically flagged, confirming how concentrated EV adoption is.", "#8b1a1a")
        show_fig("outputs/figures/outlier_iqr.png")
    with tab2:
        finding("<b>King County Z-score = 14.79</b> on Total EVs — essentially impossible under a normal distribution. Snohomish is second at 3.98. King is flagged on 5 features simultaneously.", "#8b1a1a")
        show_fig("outputs/figures/outlier_zscore.png")
    with tab3:
        finding("<b>Isolation Forest anomaly score = 0.2769</b> for King County — highest in the dataset. 13 counties flagged total at contamination=0.05.", "#8b1a1a")
        show_fig("outputs/figures/outlier_isolation_forest.png")
    with tab4:
        finding("<b>LOF top score goes to Clackamas County (19.10)</b> — only 5 EVs but 100% BEV and unusual range. King County is #2 at 13.38. LOF captures local neighborhood anomalies.", "#8b1a1a")
        show_fig("outputs/figures/outlier_lof.png")
    with tab5:
        finding("<b>King County is flagged by ALL 4 methods</b> — the only county with unanimous consensus. It is not merely the largest urban county — it is a formal multivariate statistical outlier.", "#8b1a1a")
        show_fig("outputs/figures/outlier_consensus.png")

# ── MODULE 06 — PREDICTIVE MODEL ───────────────────────────────
elif page == "The Predictive Model":
    module_header("The Predictive Model", "Decision Tree baseline vs Random Forest · BEV vs PHEV classification")

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("RF Accuracy",  "100%",   "1.0000 on 54,221 test rows", "#2d6b4f")
    with c2: metric_card("DT Accuracy",  "99.95%", "baseline — max_depth=5",     "#3da870")
    with c3: metric_card("CV F1",        "1.0000", "± 0.0000 across 5 folds",   "#2d6b4f")
    with c4: metric_card("RF Errors",    "2",      "out of 54,221 test records", "#2d6b4f")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        section_title("Model Comparison")
        comp_data = {
            "Metric":    ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC", "Errors on test set"],
            "Decision Tree": ["0.9995", "0.9995", "0.9995", "0.9995", "1.0000", "25"],
            "Random Forest": ["1.0000", "1.0000", "1.0000", "1.0000", "1.0000", "2"],
        }
        st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)

        section_title("Feature Importance")
        fi_data = {
            "Feature":    ["Electric Range", "CAFV_Category", "Make", "Model Year", "Cluster", "County"],
            "Importance": ["49.1%", "29.6%", "11.3%", "9.9%", "0.0%", "0.0%"],
        }
        st.dataframe(pd.DataFrame(fi_data), use_container_width=True, hide_index=True)

    with col_b:
        show_fig("outputs/figures/feature_importance.png", "Random Forest feature importance")

    st.markdown("<br>", unsafe_allow_html=True)
    show_fig("outputs/figures/confusion_matrix_dt.png", "Confusion matrices — Decision Tree vs Random Forest")

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Key Findings")
    finding("<b>Perfect classification</b> — Random Forest achieves 1.0000 across all metrics with only 2 errors on 54,221 test records.", "#2d6b4f")
    finding("<b>Electric Range dominates at 49.1%</b> — PHEVs record 0 miles in the DOL database while BEVs record true battery range, making this a near-perfect separator.", "#2d6b4f")
    finding("<b>CAFV_Category is the surprise at 29.6%</b> — eligibility is battery-range-dependent, structurally correlated with EV type through vehicle design.", "#2d6b4f")
    finding("<b>County and Cluster = 0% importance</b> — EV type is a vehicle property, not a geographic one. Where it's registered tells you nothing about its type.", "#2d6b4f")
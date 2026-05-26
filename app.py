import streamlit as st
import pandas as pd
import numpy as np
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Brand Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg-base:        #0A0A0A;
        --bg-panel:       #111111;
        --border-dark:    rgba(212, 175, 55, 0.12);
        --border-bright:  rgba(212, 175, 55, 0.35);
        --gold:           #D4AF37;
        --gold-light:     #F1C40F;
        --gold-dim:       rgba(212, 175, 55, 0.60);
        --accent:         #E67E22;
        --sidebar-text:   #B0B0B0;
        --sidebar-accent: #D4AF37;
    }

    * { font-family: 'Outfit', sans-serif; box-sizing: border-box; }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg-base) !important;
    }

    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed; inset: 0;
        background-image: radial-gradient(circle, rgba(212,175,55,0.03) 1px, transparent 1px);
        background-size: 28px 28px;
        pointer-events: none;
        z-index: 0;
    }

    /* ── Report title — now the main heading ─────────────────────────── */
    .report-title {
        background: linear-gradient(135deg, #1A1A1A 0%, #0E0E0E 100%);
        color: #D4AF37;
        padding: 18px 28px;
        border-radius: 12px;
        text-align: center;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 28px;
        font-weight: 900;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 14px;
        border: 1px solid var(--border-bright);
        box-shadow: 0 8px 30px rgba(0,0,0,0.8), 0 0 15px rgba(212,175,55,0.15);
        position: relative;
        overflow: hidden;
    }
    .report-title::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #D4AF37, #F1C40F, #E67E22, transparent);
    }

    /* ── KPI cards ───────────────────────────────────────────────────── */
    .kpi-card {
        background: linear-gradient(145deg, #1A1A1A 0%, #101010 100%);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 12px;
        padding: 14px 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(0,0,0,0.7), 0 0 8px rgba(212,175,55,0.08);
    }
    .kpi-card::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #D4AF37, #F1C40F, transparent);
    }
    .kpi-title {
        font-size: 14px;
        font-weight: 1800;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #FFFFFF;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 36px;
        font-weight: 900 !important;
        letter-spacing: 2px;
        color: #D4AF37;
        line-height: 1;
    }

    /* ── Card / table titles ─────────────────────────────────────────── */
    .card-title {
        background: #1C1C1C;
        color: #D4AF37;
        padding: 9px 16px;
        border-radius: 10px 10px 0 0;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        text-align: center;
        border: 1px solid rgba(212,175,55,0.25);
        border-bottom: 1px solid rgba(212,175,55,0.15);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }

    /* ── Tables ──────────────────────────────────────────────────────── */
    .table-scroll {
        overflow-y: auto;
        border: 1px solid rgba(212,175,55,0.2);
        border-top: none;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 6px 22px rgba(0,0,0,0.6);
        margin-bottom: 0;
    }

    .table-scroll table {
        width: 100%;
        border-collapse: collapse;
        table-layout: auto;
        font-family: 'Outfit', sans-serif;
        font-size: 13px;
        font-weight: 800;
        color: #FFFFFF;
        background: #131313;
    }

    .table-scroll th {
        background-color: #F0F0F0 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 12.5px !important;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        padding: 10px 12px;
        text-align: left !important;
        border-bottom: 2px solid rgba(212,175,55,0.6);
        border-right: 1px solid rgba(212,175,55,0.10);
    }

    .table-scroll th:nth-child(2),
    .table-scroll th:nth-child(3) {
        text-align: center !important;
    }

    .table-scroll td {
        padding: 7px 12px;
        border-bottom: 1px solid rgba(212,175,55,0.10);
        border-right: 1px solid rgba(212,175,55,0.10);
        font-weight: 800;
        font-size: 13px;
        text-align: left;
        color: #FFFFFF;
    }

    .table-scroll td:nth-child(2),
    .table-scroll td:nth-child(3),
    .table-scroll td:nth-child(4),
    .table-scroll td:nth-child(5) {
        text-align: center;
        font-weight: 900;
        color: #D4AF37;
    }

    .table-scroll tr:nth-child(even) td { background-color: #191919; }
    .table-scroll tr:nth-child(odd)  td { background-color: #131313; }
    .table-scroll tr:hover td {
        background-color: #2A2A2A !important;
        color: #F1C40F !important;
    }

    /* ── Sidebar ─────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0C0C0C 0%, #0A0A0A 100%) !important;
        border-right: 1px solid var(--border-dark) !important;
    }
    [data-testid="stSidebar"] * { color: var(--sidebar-text) !important; }
    [data-testid="stSidebar"] h3 {
        color: var(--sidebar-accent) !important;
        font-size: 11px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"] strong { color: #E6C300 !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label {
        color: var(--gold-dim) !important;
        font-weight: 600 !important;
        font-size: 10px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #888 !important;
        font-size: 11px !important;
    }

    .stat-pill {
        background: #1A1A1A;
        border: 1px solid var(--border-dark);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 11px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 5px;
    }
    .stat-pill span:first-child { color: #999; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; }
    .stat-pill span:last-child  { font-weight: 700; color: var(--gold-light); }

    .region-badge {
        display: block;
        background: rgba(212,175,55,0.04);
        border: 1px solid var(--border-dark);
        border-radius: 6px;
        padding: 4px 12px;
        font-size: 10px;
        letter-spacing: 0.8px;
        color: var(--sidebar-text) !important;
        margin: 3px 0;
    }
    .region-badge strong { color: var(--sidebar-accent) !important; font-size: 10px; }

    [data-testid="stSelectbox"] > div > div {
        background: #1A1A1A !important;
        border: 1px solid var(--border-dark) !important;
        color: #D4AF37 !important;
        border-radius: 8px !important;
        font-size: 12px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #1A1A1A 0%, #0E0E0E 100%) !important;
        color: var(--gold-light) !important;
        border: 1px solid var(--border-bright) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 11px !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        box-shadow: 0 2px 10px rgba(212,175,55,0.12) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2A2A2A 0%, #1A1A1A 100%) !important;
        box-shadow: 0 4px 18px rgba(212,175,55,0.30) !important;
        border-color: var(--gold-light) !important;
    }

    [data-testid="stFileUploader"] {
        background: #1A1A1A !important;
        border: 2px dashed rgba(212,175,55,0.25) !important;
        border-radius: 12px !important;
        padding: 28px !important;
    }

    [data-testid="stAlert"] {
        background: #1A1A1A !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: 8px !important;
        color: var(--sidebar-text) !important;
    }

    hr { border-color: var(--border-dark) !important; margin: 12px 0 !important; }
    p, .stMarkdown p { color: var(--sidebar-text) !important; font-size: 12px !important; }
    label { color: var(--gold-dim) !important; }

    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #0A0A0A; }
    ::-webkit-scrollbar-thumb { background: rgba(212,175,55,0.25); border-radius: 2px; }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding: 0.5rem 1rem 0.5rem; }
    div[data-testid="stVerticalBlock"] > div { margin-top: 0; padding-top: 0; }
    .stColumn { padding: 3px; }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ──────────────────────────────────────────────────────────────────
ASIAN_COUNTRIES = [
    'malaysia','hong kong','singapore','indonesia','philippines',
    'taiwan','japan','myanmar','brunei','thailand','vietnam',
    'south korea','china','bangladesh','pakistan',
    'sri lanka','nepal','bhutan','maldives','cambodia',
    'laos','mongolia','north korea','macau','timor-leste'
]
USA_COUNTRY   = ["usa"]
UAE_COUNTRY   = ["uae"]
INDIA_COUNTRY = ["india"]

REGION_BRANDS = ['lr.com', 'rag & co']

BRAND_DISPLAY = {
    'lr.com':    'LR.com',
    'rag & co':  'Rag & Co',
}


def clean_str(series):
    return series.astype(str).str.strip().str.lower()


def load_excel_file(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, sheet_name='a')
        df.columns = df.columns.str.strip()

        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        for col in ['Category', 'Country', 'Traffic Source', 'Channel', 'Brand', 'SKU', 'Disc Coupon']:
            if col in df.columns:
                df[col] = clean_str(df[col])

        for col in ['Qty', 'Amount']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def calculate_kpis(df):
    kpis = {}
    try:
        kpis['Gross Sales Qty']    = df['Qty'].sum()    if 'Qty'    in df.columns else 0
        kpis['Gross Amount (USD)'] = df['Amount'].sum() if 'Amount' in df.columns else 0

        if 'Date' in df.columns and not df['Date'].isna().all():
            ld = df['Date'].max()
            kpis['Report Date'] = ld.strftime('%d %b %Y') if pd.notna(ld) else "N/A"
        else:
            kpis['Report Date'] = "N/A"

        kpis['Brands'] = sorted(df['Brand'].dropna().unique().tolist()) if 'Brand' in df.columns else []
        return kpis
    except Exception as e:
        st.error(f"KPI error: {e}")
        return None


def display_kpi_card(title, value):
    fv = f"${value:,.2f}" if 'Amount' in title else f"{int(value):,}"
    return f'<div class="kpi-card"><div class="kpi-title">{title}</div><div class="kpi-value">{fv}</div></div>'


def apply_region_filter(df, region):
    if 'Country' not in df.columns:
        return df
    country_col = df['Country']
    if region == "ASIA":
        return df[country_col.isin(ASIAN_COUNTRIES)]
    elif region == "UAE":
        return df[country_col.isin(UAE_COUNTRY)]
    elif region == "USA":
        return df[country_col.isin(USA_COUNTRY)]
    elif region == "INDIA":
        return df[country_col.isin(INDIA_COUNTRY)]
    return df


def capitalize_text(v):
    return str(v).strip().upper() if pd.notna(v) else v


def make_table(df, group_cols, sort_col='Amount'):
    needed = group_cols + ['Qty', 'Amount']
    if not all(c in df.columns for c in needed):
        return pd.DataFrame()
    result = (
        df.groupby(group_cols, as_index=False)
          .agg({'Qty': 'sum', 'Amount': 'sum'})
          .sort_values(sort_col, ascending=False)
    )
    for col in group_cols:
        result[col] = result[col].apply(capitalize_text)
    result['Amount'] = result['Amount'].apply(lambda x: f"${x:,.2f}")
    result['Qty']    = result['Qty'].apply(lambda x: f"{int(x):,}")
    return result.reset_index(drop=True)


def show_table(tbl, group_cols, height):
    if tbl.empty:
        tbl = pd.DataFrame(columns=group_cols + ['Qty', 'Amount'])
    html = tbl.to_html(index=False, escape=False)
    st.markdown(
        f'<div class="table-scroll" style="max-height:{height}px;">{html}</div>',
        unsafe_allow_html=True
    )


def brand_label(raw_key):
    return BRAND_DISPLAY.get(raw_key, raw_key.title())


def main():
    if 'file_loaded' not in st.session_state:
        st.session_state.file_loaded = False
    if 'df' not in st.session_state:
        st.session_state.df = None

    # ── Upload screen ─────────────────────────────────────────────────────────
    if not st.session_state.file_loaded:
        _, col_c, _ = st.columns([1, 2, 1])
        with col_c:
            uploaded_file = st.file_uploader(
                "Upload Excel File", type=['xlsx', 'xls'],
                help="Sheet must be named 'a'"
            )
            if uploaded_file is not None:
                df = load_excel_file(uploaded_file)
                if df is not None and not df.empty:
                    st.session_state.df = df
                    st.session_state.file_loaded = True
                    st.rerun()
            else:
                st.info("Upload an Excel file with sheet named **'a'**")
                with st.expander("Expected Data Format", expanded=False):
                    st.markdown("""
**Sheet:** `a`  
**Columns:** SKU, Category, Qty, Amount, Disc Coupon, Country, Traffic Source, Channel, Brand, Date  
**Region filter** works for **LR.com** and **Rag & Co**
""")
        return

    # ── Dashboard ─────────────────────────────────────────────────────────────
    df   = st.session_state.df
    kpis = calculate_kpis(df)
    if not kpis:
        return

    available_brands = kpis.get('Brands', [])

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### FILTERS")

        if not available_brands:
            st.warning("No brands found")
            selected_brand_key = None
        else:
            label_to_key = {brand_label(b): b for b in available_brands}
            brand_labels  = list(label_to_key.keys())

            chosen_label       = st.selectbox("Brand", brand_labels, key="brand_filter")
            selected_brand_key = label_to_key[chosen_label]

        brand_supports_region = (
            selected_brand_key is not None
            and selected_brand_key in REGION_BRANDS
        )

        if brand_supports_region:
            selected_region = st.selectbox(
                "Region",
                ["All", "ASIA", "UAE", "USA", "INDIA"],
                key="region_filter"
            )
        else:
            st.selectbox(
                "Region",
                ["All"],
                key="region_filter",
                disabled=True,
                help="Region filter is available for LR.com and Rag & Co only"
            )
            selected_region = "All"

        st.markdown("---")
        st.markdown("### TABLE HEIGHT")
        table_height = st.slider("Height (px):", 150, 1500, 1000, 10)

        st.markdown("---")
        st.markdown("### DATASET")
        st.markdown(f"""
<div class="stat-pill"><span>Records</span><span>{len(df):,}</span></div>
<div class="stat-pill"><span>Brands</span><span>{len(available_brands)}</span></div>
""", unsafe_allow_html=True)
        if 'Date' in df.columns:
            md = df['Date'].max()
            if pd.notna(md):
                st.markdown(
                    f'<div class="stat-pill"><span>Latest Date</span>'
                    f'<span>{md.strftime("%d %b %Y")}</span></div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")
        st.markdown("### REGIONS")
        for lbl, desc in [
            ("ASIA",  "Asian Countries"),
            ("UAE",   "United Arab Emirates"),
            ("USA",   "United States"),
            ("INDIA", "India"),
        ]:
            st.markdown(
                f'<div class="region-badge"><strong>{lbl}</strong> &nbsp;— {desc}</div>',
                unsafe_allow_html=True
            )

        st.markdown("---")
        if st.button("↺  Upload New File", use_container_width=True):
            st.session_state.file_loaded = False
            st.session_state.df = None
            st.rerun()

    # ── Apply filters ─────────────────────────────────────────────────────────
    filtered_df = df.copy()

    if selected_brand_key:
        filtered_df = filtered_df[filtered_df['Brand'] == selected_brand_key]

    if brand_supports_region and selected_region != "All":
        filtered_df = apply_region_filter(filtered_df, selected_region)

    filtered_kpis = calculate_kpis(filtered_df)

    # ── Report title (now the main / only heading) ────────────────────────────
    display_brand = brand_label(selected_brand_key) if selected_brand_key else "All Brands"
    rt = f"◈  {display_brand}  ·  Daily Sales Report"
    if selected_region != "All":
        rt += f"  ·  {selected_region}"
    rt += f"  ·  {filtered_kpis.get('Report Date', 'N/A')}"
    st.markdown(f'<div class="report-title">{rt}</div>', unsafe_allow_html=True)

    # ── KPI row ───────────────────────────────────────────────────────────────
    _, col_kpi, _ = st.columns([1, 2, 1])
    with col_kpi:
        k1, k2 = st.columns(2)
        with k1:
            st.markdown(
                display_kpi_card("Gross Sales Qty", filtered_kpis['Gross Sales Qty']),
                unsafe_allow_html=True
            )
        with k2:
            st.markdown(
                display_kpi_card("Gross Amount (USD)", filtered_kpis['Gross Amount (USD)']),
                unsafe_allow_html=True
            )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── Table configs ─────────────────────────────────────────────────────────
    table_configs = [
        (['Country'],                           "◆  Country Wise Sales"),
        (['Disc Coupon'],                       "◆  Discount Coupon Sales"),
        (['Category'],                          "◆  Category Wise Sales"),
        (['Traffic Source'],                    "◆  Traffic Source Sales"),
        (['Channel'],                           "◆  Channel Wise Sales"),
        (['Channel', 'Country', 'Disc Coupon'], "◆  Channel × Country × Coupon"),
    ]

    # ── Row 1 ─────────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    for col_ctx, (group_cols, title) in zip([c1, c2, c3], table_configs[:3]):
        with col_ctx:
            tbl = make_table(filtered_df, group_cols)
            st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)
            show_table(tbl, group_cols, table_height)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Row 2 ─────────────────────────────────────────────────────────────────
    c4, c5, c6 = st.columns(3)
    for col_ctx, (group_cols, title) in zip([c4, c5, c6], table_configs[3:]):
        with col_ctx:
            tbl = make_table(filtered_df, group_cols)
            st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)
            show_table(tbl, group_cols, table_height)


if __name__ == "__main__":
    main()

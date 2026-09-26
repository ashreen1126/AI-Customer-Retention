# ============================================================
# AI-POWERED CUSTOMER RETENTION & BUSINESS INTELLIGENCE
# Streamlit Dashboard
# ============================================================

from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np

# Plotly
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    st.error("Plotly is not installed.")
    st.code("pip install plotly")
    st.stop()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RetainAI | Customer Retention Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# VISUAL DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- MAIN BACKGROUND ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(99, 102, 241, 0.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(6, 182, 212, 0.14),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(139, 92, 246, 0.10),
                transparent 35%
            ),
            #f5f7fb;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #07111f 0%,
                #0b1730 45%,
                #101d3d 100%
            );
        border-right: 1px solid rgba(255,255,255,0.08);
    }


    /* ---------- MAIN FONT COLOURS ---------- */

    .stApp,
    .stApp p,
    .stApp label,
    .stApp span,
    .stApp div {
        color: #172033;
    }

    h1 {
        color: #0f172a !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    h2 {
        color: #172033 !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
    }


    /* ---------- SIDEBAR TEXT ---------- */

    section[data-testid="stSidebar"] {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] small {
        color: #cbd5e1 !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stRadio"] label {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"]
    div[data-testid="stWidgetLabel"] label {
        color: #ffffff !important;
    }


    /* ---------- INPUT TEXT ---------- */

    input {
        color: #111827 !important;
    }


    /* ---------- METRICS ---------- */

    div[data-testid="stMetricLabel"] {
        color: #475569 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
    }

    div[data-testid="stMetricDelta"] {
        color: #334155 !important;
    }


    /* ---------- METRIC CARDS ---------- */

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(148,163,184,0.20);
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(15,23,42,0.07);
    }

    div[data-testid="stMetric"]:hover {
        box-shadow: 0 12px 32px rgba(15,23,42,0.12);
        transform: translateY(-2px);
        transition: 0.2s ease;
    }


    /* ---------- DATAFRAME ---------- */

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(15,23,42,0.06);
    }


    /* ---------- BUTTON ---------- */

    .stButton > button {
        border-radius: 10px;
        font-weight: 650;
        border: 1px solid rgba(99,102,241,0.25);
    }


    /* ---------- DOWNLOAD BUTTON ---------- */

    .stDownloadButton > button {
        border-radius: 10px;
        font-weight: 650;
    }


    /* ---------- INPUTS ---------- */

    div[data-baseweb="select"] > div {
        border-radius: 10px;
    }

    div[data-baseweb="input"] > div {
        border-radius: 10px;
    }


    /* ---------- ALERTS ---------- */

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }


    /* ---------- GENERAL TEXT ---------- */

    .stMarkdown {
        color: #172033 !important;
    }

    .stCaption {
        color: #64748b !important;
    }


    /* ---------- REMOVE FOOTER ---------- */

    footer {
        visibility: hidden;
    }

    #MainMenu {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    project_root = Path(__file__).resolve().parents[1]

    data_path = (
        project_root
        / "notebooks"
        / "data"
        / "customer_retention_priority.csv"
    )

    if not data_path.exists():
        return None, data_path

    df = pd.read_csv(data_path)

    return df, data_path


df, data_path = load_data()


# ============================================================
# DATA VALIDATION
# ============================================================

if df is None:

    st.error("Customer retention dataset was not found.")

    st.write("Expected file:")

    st.code(str(data_path))

    st.info(
        "Make sure customer_retention_priority.csv exists inside "
        "notebooks/data/"
    )

    st.stop()


required_columns = [
    "customer_unique_id",
    "Recency",
    "Frequency",
    "Monetary",
    "Retention_Priority_Score",
    "Priority_Tier"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error("Required columns are missing from the dataset.")

    st.write(missing_columns)

    st.stop()


# ============================================================
# DATA CLEANING
# ============================================================

df = df.copy()

df["customer_unique_id"] = (
    df["customer_unique_id"]
    .astype(str)
)

numeric_columns = [
    "Recency",
    "Frequency",
    "Monetary",
    "Retention_Priority_Score"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

df = df.dropna(
    subset=[
        "customer_unique_id",
        "Retention_Priority_Score"
    ]
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def money(value):

    if pd.isna(value):
        return "R$ 0.00"

    return f"R$ {value:,.2f}"


def percentage(value, total):

    if total == 0:
        return "0.0%"

    return f"{(value / total) * 100:.1f}%"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎯 RetainAI")

    st.caption(
        "AI-Powered Customer Retention "
        "& Business Intelligence"
    )

    st.divider()

    st.markdown("### 🧭 Navigation")

    page = st.radio(
        "Go to",
        [
            "Executive Overview",
            "Retention Action Center",
            "Customer 360",
            "Campaign Dashboard",
            "Business Insights"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 🔎 Dashboard Filters")

    priority_values = sorted(
        df["Priority_Tier"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_priority = st.multiselect(
        "Priority Tier",
        priority_values,
        default=priority_values
    )

    if "Retention_Opportunity" in df.columns:

        opportunity_values = sorted(
            df["Retention_Opportunity"]
            .dropna()
            .unique()
            .tolist()
        )

    else:

        opportunity_values = []

    selected_opportunity = st.multiselect(
        "Retention Opportunity",
        opportunity_values,
        default=opportunity_values
    )

    if "Customer_Value_Category" in df.columns:

        value_values = sorted(
            df["Customer_Value_Category"]
            .dropna()
            .unique()
            .tolist()
        )

    else:

        value_values = []

    selected_value = st.multiselect(
        "Customer Value",
        value_values,
        default=value_values
    )

    min_score = st.slider(
        "Minimum Priority Score",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=5.0
    )

    customer_search = st.text_input(
        "Search Customer ID",
        placeholder="Enter customer ID..."
    )

    st.divider()

    st.caption(
        "Data source: Brazilian E-Commerce "
        "Customer Retention Dataset"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_priority:

    filtered_df = filtered_df[
        filtered_df["Priority_Tier"].isin(
            selected_priority
        )
    ]

if (
    selected_opportunity
    and "Retention_Opportunity" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["Retention_Opportunity"].isin(
            selected_opportunity
        )
    ]

if (
    selected_value
    and "Customer_Value_Category" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["Customer_Value_Category"].isin(
            selected_value
        )
    ]

filtered_df = filtered_df[
    filtered_df["Retention_Priority_Score"]
    >= min_score
]

if customer_search:

    filtered_df = filtered_df[
        filtered_df["customer_unique_id"]
        .str.contains(
            customer_search,
            case=False,
            na=False
        )
    ]


# ============================================================
# GLOBAL VARIABLES
# ============================================================

total_customers = len(filtered_df)

average_value = (
    filtered_df["Monetary"].mean()
    if total_customers > 0
    else 0
)

average_priority = (
    filtered_df["Retention_Priority_Score"].mean()
    if total_customers > 0
    else 0
)

high_priority_count = len(
    filtered_df[
        filtered_df["Priority_Tier"].isin(
            ["Critical", "High"]
        )
    ]
)


# ============================================================
# HEADER
# ============================================================

st.title("🎯 AI-Powered Customer Retention")

st.caption(
    "Customer intelligence • Retention prediction • "
    "Personalized actions • Business insights"
)

st.divider()


# ============================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.subheader("📊 Executive Overview")

    st.write(
        "Monitor customer value, retention priority, "
        "and recommended retention opportunities."
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👥 Total Customers",
            f"{total_customers:,}"
        )

    with col2:

        st.metric(
            "💰 Average Customer Value",
            money(average_value)
        )

    with col3:

        st.metric(
            "🚨 High Priority Customers",
            f"{high_priority_count:,}"
        )

    with col4:

        st.metric(
            "🎯 Average Priority Score",
            f"{average_priority:.1f}"
        )

    st.write("")

    # --------------------------------------------------------
    # PRIORITY + OPPORTUNITY
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.subheader("🎯 Retention Priority")

        priority_data = (
            filtered_df["Priority_Tier"]
            .value_counts()
            .reindex(
                ["Critical", "High", "Medium", "Low"],
                fill_value=0
            )
            .reset_index()
        )

        priority_data.columns = [
            "Priority",
            "Customers"
        ]

        fig_priority = px.pie(
            priority_data,
            names="Priority",
            values="Customers",
            hole=0.55
        )

        fig_priority.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            ),
            legend_title=""
        )

        st.plotly_chart(
            fig_priority,
            width="stretch"
        )

    with chart_col2:

        st.subheader("🔄 Retention Opportunities")

        if "Retention_Opportunity" in filtered_df.columns:

            opportunity_data = (
                filtered_df[
                    "Retention_Opportunity"
                ]
                .value_counts()
                .reset_index()
            )

            opportunity_data.columns = [
                "Opportunity",
                "Customers"
            ]

            opportunity_data = (
                opportunity_data
                .sort_values(
                    "Customers",
                    ascending=True
                )
            )

            fig_opportunity = px.bar(
                opportunity_data,
                x="Customers",
                y="Opportunity",
                orientation="h",
                text="Customers"
            )

            fig_opportunity.update_traces(
                textposition="outside"
            )

            fig_opportunity.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=10,
                    r=30,
                    t=20,
                    b=10
                ),
                xaxis_title="Customers",
                yaxis_title=""
            )

            st.plotly_chart(
                fig_opportunity,
                width="stretch"
            )

    # --------------------------------------------------------
    # VALUE + CUSTOMER BEHAVIOUR
    # --------------------------------------------------------

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:

        st.subheader("💎 Customer Value")

        if "Customer_Value_Category" in filtered_df.columns:

            value_data = (
                filtered_df[
                    "Customer_Value_Category"
                ]
                .value_counts()
                .reset_index()
            )

            value_data.columns = [
                "Category",
                "Customers"
            ]

            fig_value = px.pie(
                value_data,
                names="Category",
                values="Customers",
                hole=0.55
            )

            fig_value.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                )
            )

            st.plotly_chart(
                fig_value,
                width="stretch"
            )

        else:

            st.info(
                "Customer value category is not available."
            )

    with chart_col4:

        st.subheader("📈 Recency vs Customer Value")

        if len(filtered_df) > 4000:

            scatter_data = filtered_df.sample(
                4000,
                random_state=42
            )

        else:

            scatter_data = filtered_df.copy()

        fig_scatter = px.scatter(
            scatter_data,
            x="Recency",
            y="Monetary",
            size="Frequency",
            hover_data=[
                "customer_unique_id",
                "Retention_Priority_Score"
            ],
            opacity=0.65
        )

        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="white",
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            ),
            xaxis_title="Recency (Days)",
            yaxis_title="Customer Value"
        )

        st.plotly_chart(
            fig_scatter,
            width="stretch"
        )

    # --------------------------------------------------------
    # TOP CUSTOMERS
    # --------------------------------------------------------

    st.subheader("🚨 Top Priority Customers")

    top_customers = (
        filtered_df
        .sort_values(
            "Retention_Priority_Score",
            ascending=False
        )
        .head(10)
        .copy()
    )

    display_columns = [
        "customer_unique_id",
        "Priority_Tier",
        "Recency",
        "Frequency",
        "Monetary",
        "Retention_Priority_Score"
    ]

    if "Retention_Opportunity" in top_customers.columns:

        display_columns.append(
            "Retention_Opportunity"
        )

    top_table = top_customers[
        display_columns
    ].copy()

    top_table["Monetary"] = (
        top_table["Monetary"]
        .map(money)
    )

    top_table["Retention_Priority_Score"] = (
        top_table["Retention_Priority_Score"]
        .round(2)
    )

    st.dataframe(
        top_table,
        width="stretch",
        hide_index=True
    )


# ============================================================
# PAGE 2 — RETENTION ACTION CENTER
# ============================================================

elif page == "Retention Action Center":

    st.subheader("🚀 Retention Action Center")

    st.write(
        "Convert customer intelligence into "
        "practical retention actions."
    )

    if "Retention_Opportunity" in filtered_df.columns:

        action_summary = (
            filtered_df
            .groupby("Retention_Opportunity")
            .agg(
                Customers=(
                    "customer_unique_id",
                    "count"
                ),
                Average_Recency=(
                    "Recency",
                    "mean"
                ),
                Average_Value=(
                    "Monetary",
                    "mean"
                ),
                Average_Priority=(
                    "Retention_Priority_Score",
                    "mean"
                )
            )
            .reset_index()
        )

        action_summary["Customer Share"] = (
            action_summary["Customers"]
            / total_customers
            * 100
        ).round(2)

        st.subheader("📋 Retention Opportunity Summary")

        display_action = action_summary.copy()

        display_action["Average_Recency"] = (
            display_action["Average_Recency"]
            .round(1)
        )

        display_action["Average_Value"] = (
            display_action["Average_Value"]
            .map(money)
        )

        display_action["Average_Priority"] = (
            display_action["Average_Priority"]
            .round(2)
        )

        display_action["Customer Share"] = (
            display_action["Customer Share"]
            .map(lambda x: f"{x:.1f}%")
        )

        st.dataframe(
            display_action,
            width="stretch",
            hide_index=True
        )

    st.write("")

    st.subheader("🚨 Critical Customers")

    critical_customers = (
        filtered_df[
            filtered_df["Priority_Tier"] == "Critical"
        ]
        .sort_values(
            "Retention_Priority_Score",
            ascending=False
        )
        .head(20)
        .copy()
    )

    if len(critical_customers) == 0:

        st.success(
            "No critical customers match the current filters."
        )

    else:

        critical_columns = [
            "customer_unique_id",
            "Priority_Tier",
            "Recency",
            "Frequency",
            "Monetary",
            "Retention_Priority_Score"
        ]

        if "Retention_Opportunity" in critical_customers.columns:

            critical_columns.append(
                "Retention_Opportunity"
            )

        critical_table = critical_customers[
            critical_columns
        ].copy()

        critical_table["Monetary"] = (
            critical_table["Monetary"]
            .map(money)
        )

        critical_table["Retention_Priority_Score"] = (
            critical_table[
                "Retention_Priority_Score"
            ]
            .round(2)
        )

        st.dataframe(
            critical_table,
            width="stretch",
            hide_index=True
        )

        csv_data = critical_customers.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Critical Customers",
            data=csv_data,
            file_name="critical_customers.csv",
            mime="text/csv"
        )


# ============================================================
# PAGE 3 — CUSTOMER 360
# ============================================================

elif page == "Customer 360":

    st.subheader("👤 Customer 360")

    st.write(
        "View an individual customer's behaviour, "
        "value, retention priority, segmentation, "
        "and recommended action."
    )

    # --------------------------------------------------------
    # CUSTOMER SEARCH
    # --------------------------------------------------------

    customer_ids = (
        filtered_df[
            "customer_unique_id"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if len(customer_ids) == 0:

        st.warning(
            "No customers match the current filters."
        )

    else:

        search_360 = st.text_input(
            "🔎 Search Customer ID",
            placeholder="Type part of a customer ID..."
        )

        if search_360:

            matching_ids = [
                customer_id
                for customer_id in customer_ids
                if search_360.lower()
                in customer_id.lower()
            ]

        else:

            matching_ids = customer_ids

        if len(matching_ids) == 0:

            st.warning(
                "No matching customer was found."
            )

        else:

            selected_customer = st.selectbox(
                "Select Customer",
                matching_ids
            )

            customer_rows = filtered_df[
                filtered_df[
                    "customer_unique_id"
                ] == selected_customer
            ]

            if customer_rows.empty:

                st.warning(
                    "Customer information is not available."
                )

            else:

                customer = (
                    customer_rows
                    .iloc[0]
                )

                # ------------------------------------------------
                # CUSTOMER PROFILE
                # ------------------------------------------------

                st.subheader("👤 Customer Profile")

                profile_col1, profile_col2 = st.columns(2)

                with profile_col1:

                    st.metric(
                        "Customer ID",
                        str(
                            customer[
                                "customer_unique_id"
                            ]
                        )
                    )

                with profile_col2:

                    st.metric(
                        "Priority Tier",
                        str(
                            customer[
                                "Priority_Tier"
                            ]
                        )
                    )

                st.write("")

                metric1, metric2, metric3, metric4 = st.columns(4)

                with metric1:

                    st.metric(
                        "⏱️ Recency",
                        f"{customer['Recency']:.0f} days"
                    )

                with metric2:

                    st.metric(
                        "🛒 Frequency",
                        f"{customer['Frequency']:.0f}"
                    )

                with metric3:

                    st.metric(
                        "💰 Monetary Value",
                        money(
                            customer["Monetary"]
                        )
                    )

                with metric4:

                    st.metric(
                        "🎯 Priority Score",
                        f"{customer['Retention_Priority_Score']:.2f}"
                    )

                st.write("")

                # ------------------------------------------------
                # PRIORITY GAUGE
                # ------------------------------------------------

                gauge_col, segment_col = st.columns(
                    [1, 1]
                )

                with gauge_col:

                    st.subheader(
                        "🎯 Retention Priority"
                    )

                    priority_score = float(
                        customer[
                            "Retention_Priority_Score"
                        ]
                    )

                    gauge = go.Figure(
                        go.Indicator(
                            mode="gauge+number",
                            value=priority_score,
                            number={
                                "suffix": "/100"
                            },
                            title={
                                "text": "Priority Score"
                            },
                            gauge={
                                "axis": {
                                    "range": [0, 100]
                                },
                                "bar": {
                                    "color": "#4f46e5"
                                },
                                "steps": [
                                    {
                                        "range": [0, 25],
                                        "color": "#dcfce7"
                                    },
                                    {
                                        "range": [25, 50],
                                        "color": "#fef9c3"
                                    },
                                    {
                                        "range": [50, 75],
                                        "color": "#fed7aa"
                                    },
                                    {
                                        "range": [75, 100],
                                        "color": "#fecaca"
                                    }
                                ]
                            }
                        )
                    )

                    gauge.update_layout(
                        height=280,
                        margin=dict(
                            l=20,
                            r=20,
                            t=50,
                            b=10
                        ),
                        paper_bgcolor="rgba(0,0,0,0)"
                    )

                    st.plotly_chart(
                        gauge,
                        width="stretch"
                    )

                with segment_col:

                    st.subheader(
                        "🧩 Customer Segmentation"
                    )

                    if "RFM_Segment" in customer.index:

                        st.info(
                            "RFM Segment: "
                            + str(
                                customer[
                                    "RFM_Segment"
                                ]
                            )
                        )

                    if "Cluster_Profile" in customer.index:

                        st.info(
                            "ML Cluster Profile: "
                            + str(
                                customer[
                                    "Cluster_Profile"
                                ]
                            )
                        )

                    if "Customer_Value_Category" in customer.index:

                        st.info(
                            "Customer Value: "
                            + str(
                                customer[
                                    "Customer_Value_Category"
                                ]
                            )
                        )

                # ------------------------------------------------
                # IMPORTANT FACTORS
                # ------------------------------------------------

                st.subheader("🔍 Important Factors")

                factors = pd.DataFrame(
                    {
                        "Factor": [
                            "Recency",
                            "Frequency",
                            "Monetary Value",
                            "Retention Priority"
                        ],
                        "Customer Value": [
                            f"{customer['Recency']:.0f} days",
                            f"{customer['Frequency']:.0f} orders",
                            money(
                                customer["Monetary"]
                            ),
                            f"{customer['Retention_Priority_Score']:.2f}/100"
                        ]
                    }
                )

                st.dataframe(
                    factors,
                    width="stretch",
                    hide_index=True
                )

                # ------------------------------------------------
                # RETENTION RECOMMENDATION
                # ------------------------------------------------

                st.subheader(
                    "💡 Recommended Retention Action"
                )

                recommendation_col1, recommendation_col2 = st.columns(2)

                with recommendation_col1:

                    if "Retention_Opportunity" in customer.index:

                        st.info(
                            "Retention Opportunity\n\n"
                            + str(
                                customer[
                                    "Retention_Opportunity"
                                ]
                            )
                        )

                    if "Personalized_Strategy" in customer.index:

                        st.success(
                            "Personalized Strategy\n\n"
                            + str(
                                customer[
                                    "Personalized_Strategy"
                                ]
                            )
                        )

                    elif "Retention_Action" in customer.index:

                        st.success(
                            "Recommended Action\n\n"
                            + str(
                                customer[
                                    "Retention_Action"
                                ]
                            )
                        )

                with recommendation_col2:

                    if "Suggested_Channel" in customer.index:

                        st.info(
                            "Suggested Channel\n\n"
                            + str(
                                customer[
                                    "Suggested_Channel"
                                ]
                            )
                        )

                    if "Suggested_Incentive" in customer.index:

                        st.success(
                            "Suggested Incentive\n\n"
                            + str(
                                customer[
                                    "Suggested_Incentive"
                                ]
                            )
                        )

                # ------------------------------------------------
                # PERSONALIZED MESSAGE
                # ------------------------------------------------

                if "Suggested_Message" in customer.index:

                    st.subheader(
                        "✉️ Suggested Customer Message"
                    )

                    st.info(
                        str(
                            customer[
                                "Suggested_Message"
                            ]
                        )
                    )

                if "Campaign_Group" in customer.index:

                    st.subheader(
                        "📢 Campaign Group"
                    )

                    st.write(
                        str(
                            customer[
                                "Campaign_Group"
                            ]
                        )
                    )


# ============================================================
# PAGE 4 — CAMPAIGN DASHBOARD
# ============================================================

elif page == "Campaign Dashboard":

    st.subheader("🎯 Retention Campaign Dashboard")

    st.write(
        "Analyze customer retention campaigns, "
        "campaign size, customer value, and campaign priority."
    )

    # --------------------------------------------------------
    # CAMPAIGN DATA
    # --------------------------------------------------------

    if "Campaign_Group" not in filtered_df.columns:

        st.warning(
            "Campaign_Group is not available in the dataset."
        )

    else:

        campaign_summary = (
            filtered_df
            .groupby("Campaign_Group")
            .agg(
                Customers=(
                    "customer_unique_id",
                    "count"
                ),
                Average_Value=(
                    "Monetary",
                    "mean"
                ),
                Average_Priority=(
                    "Retention_Priority_Score",
                    "mean"
                )
            )
            .reset_index()
        )

        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        campaign_count = (
            filtered_df[
                "Campaign_Group"
            ]
            .nunique()
        )

        critical_campaign_customers = len(
            filtered_df[
                filtered_df[
                    "Priority_Tier"
                ] == "Critical"
            ]
        )

        campaign_average_value = (
            filtered_df["Monetary"].mean()
            if len(filtered_df) > 0
            else 0
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "📢 Campaign Groups",
                f"{campaign_count:,}"
            )

        with col2:

            st.metric(
                "👥 Target Customers",
                f"{len(filtered_df):,}"
            )

        with col3:

            st.metric(
                "🚨 Critical Customers",
                f"{critical_campaign_customers:,}"
            )

        with col4:

            st.metric(
                "💰 Avg Customer Value",
                money(
                    campaign_average_value
                )
            )

        st.write("")

        # ----------------------------------------------------
        # CUSTOMERS BY CAMPAIGN
        # ----------------------------------------------------

        st.subheader(
            "📊 Customers by Campaign"
        )

        campaign_chart_data = (
            campaign_summary
            .sort_values(
                "Customers",
                ascending=False
            )
        )

        fig_campaign = px.bar(
            campaign_chart_data,
            x="Campaign_Group",
            y="Customers",
            text="Customers",
            title=""
        )

        fig_campaign.update_traces(
            textposition="outside"
        )

        fig_campaign.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="white",
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=80
            ),
            xaxis_title="Campaign",
            yaxis_title="Customers"
        )

        st.plotly_chart(
            fig_campaign,
            width="stretch"
        )

        # ----------------------------------------------------
        # CAMPAIGN SUMMARY
        # ----------------------------------------------------

        st.subheader(
            "📋 Campaign Summary"
        )

        campaign_display = campaign_summary.copy()

        campaign_display["Average_Value"] = (
            campaign_display[
                "Average_Value"
            ]
            .map(money)
        )

        campaign_display["Average_Priority"] = (
            campaign_display[
                "Average_Priority"
            ]
            .round(2)
        )

        campaign_display["Customer Share"] = (
            campaign_display["Customers"]
            / len(filtered_df)
            * 100
        ).round(2)

        campaign_display["Customer Share"] = (
            campaign_display[
                "Customer Share"
            ]
            .map(lambda x: f"{x:.1f}%")
        )

        st.dataframe(
            campaign_display,
            width="stretch",
            hide_index=True
        )

        # ----------------------------------------------------
        # CAMPAIGN VALUE CHART
        # ----------------------------------------------------

        chart1, chart2 = st.columns(2)

        with chart1:

            st.subheader(
                "💰 Average Customer Value"
            )

            fig_campaign_value = px.bar(
                campaign_summary.sort_values(
                    "Average_Value",
                    ascending=True
                ),
                x="Average_Value",
                y="Campaign_Group",
                orientation="h",
                text="Average_Value"
            )

            fig_campaign_value.update_traces(
                texttemplate="R$ %{text:.2f}",
                textposition="outside"
            )

            fig_campaign_value.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="white",
                margin=dict(
                    l=20,
                    r=50,
                    t=20,
                    b=20
                ),
                xaxis_title="Average Value",
                yaxis_title=""
            )

            st.plotly_chart(
                fig_campaign_value,
                width="stretch"
            )

        with chart2:

            st.subheader(
                "🎯 Campaign Priority"
            )

            fig_campaign_priority = px.bar(
                campaign_summary.sort_values(
                    "Average_Priority",
                    ascending=True
                ),
                x="Average_Priority",
                y="Campaign_Group",
                orientation="h",
                text="Average_Priority"
            )

            fig_campaign_priority.update_traces(
                texttemplate="%{text:.1f}",
                textposition="outside"
            )

            fig_campaign_priority.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="white",
                margin=dict(
                    l=20,
                    r=40,
                    t=20,
                    b=20
                ),
                xaxis_title="Average Priority Score",
                yaxis_title=""
            )

            st.plotly_chart(
                fig_campaign_priority,
                width="stretch"
            )

        # ----------------------------------------------------
        # CAMPAIGN INSIGHT
        # ----------------------------------------------------

        st.subheader(
            "💡 Campaign Insight"
        )

        largest_campaign = (
            campaign_summary
            .sort_values(
                "Customers",
                ascending=False
            )
            .iloc[0]
        )

        highest_value_campaign = (
            campaign_summary
            .sort_values(
                "Average_Value",
                ascending=False
            )
            .iloc[0]
        )

        highest_priority_campaign = (
            campaign_summary
            .sort_values(
                "Average_Priority",
                ascending=False
            )
            .iloc[0]
        )

        st.info(
            f"The largest campaign group is "
            f"**{largest_campaign['Campaign_Group']}** "
            f"with **{int(largest_campaign['Customers']):,} customers**."
        )

        st.info(
            f"The campaign with the highest average customer value is "
            f"**{highest_value_campaign['Campaign_Group']}** "
            f"at **{money(highest_value_campaign['Average_Value'])}**."
        )

        st.info(
            f"The campaign with the highest average priority score is "
            f"**{highest_priority_campaign['Campaign_Group']}** "
            f"with a score of "
            f"**{highest_priority_campaign['Average_Priority']:.2f}**."
        )

        # ----------------------------------------------------
        # DOWNLOAD CAMPAIGN DATA
        # ----------------------------------------------------

        st.subheader(
            "⬇️ Campaign Data"
        )

        campaign_csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Campaign Customer Data",
            data=campaign_csv,
            file_name="campaign_customer_data.csv",
            mime="text/csv"
        )


# ============================================================
# PAGE 5 — BUSINESS INSIGHTS
# ============================================================

elif page == "Business Insights":

    st.subheader("💡 Business Insights")

    st.write(
        "Translate customer retention analytics "
        "into business-level observations."
    )

    # --------------------------------------------------------
    # INSIGHT 1
    # --------------------------------------------------------

    st.subheader(
        "👥 Customer Base"
    )

    st.info(
        f"The current filtered customer population contains "
        f"**{total_customers:,} customers**."
    )

    # --------------------------------------------------------
    # INSIGHT 2
    # --------------------------------------------------------

    st.subheader(
        "💰 Customer Value"
    )

    st.info(
        f"The average customer monetary value is "
        f"**{money(average_value)}**."
    )

    # --------------------------------------------------------
    # INSIGHT 3
    # --------------------------------------------------------

    st.subheader(
        "🚨 Retention Priority"
    )

    st.info(
        f"There are **{high_priority_count:,}** customers "
        f"in the Critical or High priority tiers "
        f"under the current filters."
    )

    # --------------------------------------------------------
    # PRIORITY DISTRIBUTION
    # --------------------------------------------------------

    st.subheader(
        "📊 Priority Distribution"
    )

    priority_insight = (
        filtered_df[
            "Priority_Tier"
        ]
        .value_counts()
        .reindex(
            ["Critical", "High", "Medium", "Low"],
            fill_value=0
        )
        .reset_index()
    )

    priority_insight.columns = [
        "Priority",
        "Customers"
    ]

    fig_business_priority = px.bar(
        priority_insight,
        x="Priority",
        y="Customers",
        text="Customers"
    )

    fig_business_priority.update_traces(
        textposition="outside"
    )

    fig_business_priority.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig_business_priority,
        width="stretch"
    )

    # --------------------------------------------------------
    # RETENTION OPPORTUNITY INSIGHTS
    # --------------------------------------------------------

    if "Retention_Opportunity" in filtered_df.columns:

        st.subheader(
            "🔄 Retention Opportunity Insights"
        )

        opportunity_counts = (
            filtered_df[
                "Retention_Opportunity"
            ]
            .value_counts()
        )

        for opportunity, count in opportunity_counts.items():

            share = percentage(
                count,
                total_customers
            )

            st.write(
                f"**{opportunity}** — "
                f"{count:,} customers "
                f"({share})"
            )

    # --------------------------------------------------------
    # CUSTOMER VALUE INSIGHTS
    # --------------------------------------------------------

    if "Customer_Value_Category" in filtered_df.columns:

        st.subheader(
            "💎 Customer Value Insights"
        )

        value_counts = (
            filtered_df[
                "Customer_Value_Category"
            ]
            .value_counts()
        )

        for category, count in value_counts.items():

            share = percentage(
                count,
                total_customers
            )

            st.write(
                f"**{category}** — "
                f"{count:,} customers "
                f"({share})"
            )

    # --------------------------------------------------------
    # METHODOLOGY
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🧠 Methodology"
    )

    st.write(
        """
        The dashboard combines customer-level RFM analytics,
        machine-learning-based customer segmentation,
        retention opportunity classification,
        personalized retention recommendations,
        and retention priority scoring.

        **Recency** measures how recently a customer purchased.

        **Frequency** measures how often a customer purchased.

        **Monetary Value** measures the customer's total purchase value.

        The Retention Priority Score combines recency risk,
        monetary value, and purchase frequency into a single
        business prioritization score.

        The Campaign Dashboard then groups customers into
        actionable retention campaigns.
        """
    )

    st.success(
        "The dashboard is designed to support data-driven "
        "customer retention decisions."
    )


# ============================================================
# END OF APPLICATION
# ============================================================
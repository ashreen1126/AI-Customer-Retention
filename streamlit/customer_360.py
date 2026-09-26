# ============================================================
# RETAINAI - AI-POWERED CUSTOMER RETENTION PLATFORM
# Final Streamlit Dashboard
# ============================================================

from pathlib import Path

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RetainAI | Customer Retention",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATA PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    BASE_DIR
    / "notebooks"
    / "data"
    / "customer_retention_priority.csv"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- MAIN PAGE ---------- */

    .stApp {
        background: #f5f7fb;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #111827 0%,
            #172033 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 28px;
        font-weight: 800;
    }


    /* ---------- HEADINGS ---------- */

    h1 {
        color: #111827;
        font-weight: 800;
        letter-spacing: -1px;
    }

    h2 {
        color: #111827;
        font-weight: 750;
    }

    h3 {
        color: #1f2937;
        font-weight: 700;
    }


    /* ---------- HERO ---------- */

    .hero {
        background:
            linear-gradient(
                135deg,
                #111827 0%,
                #1e3a8a 55%,
                #2563eb 100%
            );

        padding: 36px 42px;
        border-radius: 24px;
        margin-bottom: 25px;
        box-shadow: 0 12px 35px rgba(30, 64, 175, 0.22);
    }

    .hero-small {
        color: #bfdbfe;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        color: white;
        font-size: 42px;
        font-weight: 850;
        line-height: 1.1;
        margin-bottom: 12px;
    }

    .hero-title span {
        color: #93c5fd;
    }

    .hero-subtitle {
        color: #dbeafe;
        font-size: 17px;
        line-height: 1.6;
        max-width: 850px;
    }


    /* ---------- STATUS ---------- */

    .status {
        background: white;
        padding: 14px 20px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        margin-bottom: 25px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
    }

    .status-dot {
        color: #16a34a;
        font-size: 18px;
    }


    /* ---------- METRIC CARDS ---------- */

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #111827;
        font-weight: 800;
    }


    /* ---------- SECTION ---------- */

    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #111827;
        margin-top: 20px;
        margin-bottom: 4px;
    }

    .section-description {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 18px;
    }


    /* ---------- CUSTOMER CARD ---------- */

    .customer-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.07);
    }


    /* ---------- INFO BOX ---------- */

    .info-box {
        background: #eff6ff;
        border-left: 5px solid #2563eb;
        padding: 18px;
        border-radius: 12px;
        margin: 10px 0;
    }


    /* ---------- ACTION BOX ---------- */

    .action-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 18px;
        border-radius: 14px;
        margin-bottom: 12px;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        margin-top: 40px;
        padding: 20px;
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

    if not DATA_PATH.exists():
        return None

    df = pd.read_csv(DATA_PATH)

    numeric_columns = [
        "Recency",
        "Frequency",
        "Monetary",
        "RFM_Score",
        "Retention_Priority_Score"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


df = load_data()


# ============================================================
# ERROR HANDLING
# ============================================================

if df is None:

    st.error(
        "Dataset not found."
    )

    st.write(
        "Expected file:"
    )

    st.code(
        str(DATA_PATH)
    )

    st.stop()


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "customer_unique_id",
    "Recency",
    "Frequency",
    "Monetary",
    "Retention_Priority_Score",
    "Priority_Tier",
    "Retention_Opportunity",
    "Customer_Value_Category"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        "Some required columns are missing from the dataset:"
    )

    st.write(missing_columns)

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        # 🎯 RetainAI

        **AI-Powered Customer Retention**

        Business Intelligence Platform
        """
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

    st.markdown("### 🔎 Smart Filters")

    priority_options = [
        "Critical",
        "High",
        "Medium",
        "Low"
    ]

    selected_priority = st.multiselect(
        "Priority Tier",
        priority_options,
        default=priority_options
    )

    opportunity_options = sorted(
        df["Retention_Opportunity"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_opportunity = st.multiselect(
        "Retention Opportunity",
        opportunity_options,
        default=opportunity_options
    )

    value_options = sorted(
        df["Customer_Value_Category"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_value = st.multiselect(
        "Customer Value",
        value_options,
        default=value_options
    )

    min_score = st.slider(
        "Minimum Priority Score",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=5.0
    )

    st.divider()

    st.caption(
        f"📊 {len(df):,} customers loaded"
    )

    st.caption(
        "Olist Brazilian E-Commerce Dataset"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    df["Priority_Tier"].isin(selected_priority)
    &
    df["Retention_Opportunity"].isin(selected_opportunity)
    &
    df["Customer_Value_Category"].isin(selected_value)
    &
    (
        df["Retention_Priority_Score"]
        >= min_score
    )
].copy()


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-small">
            AI & DATA SCIENCE • CUSTOMER INTELLIGENCE
        </div>

        <div class="hero-title">
            AI-Powered <span>Customer Retention</span>
        </div>

        <div class="hero-subtitle">
            Transforming customer behavior into intelligent
            retention decisions, priority actions and
            personalized strategies.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# STATUS
# ============================================================

st.markdown(
    f"""
    <div class="status">

        <span class="status-dot">●</span>
        <b> Retention Intelligence Engine Active</b>
        &nbsp; • &nbsp;
        {len(filtered_df):,} customers currently analyzed

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.markdown(
        '<div class="section-title">📊 Executive Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'A management-level view of customer value, retention '
        'priority and actionable opportunities.'
        '</div>',
        unsafe_allow_html=True
    )

    total_customers = len(filtered_df)

    avg_value = (
        filtered_df["Monetary"].mean()
        if total_customers > 0
        else 0
    )

    high_priority = filtered_df[
        filtered_df["Priority_Tier"].isin(
            ["Critical", "High"]
        )
    ]

    high_priority_count = len(high_priority)

    avg_score = (
        filtered_df["Retention_Priority_Score"].mean()
        if total_customers > 0
        else 0
    )

    avg_recency = (
        filtered_df["Recency"].mean()
        if total_customers > 0
        else 0
    )


    # ---------- METRICS ----------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "👥 Total Customers",
            f"{total_customers:,}"
        )

    with c2:
        st.metric(
            "💰 Avg Customer Value",
            f"R$ {avg_value:,.2f}"
        )

    with c3:
        st.metric(
            "🚨 High Priority",
            f"{high_priority_count:,}"
        )

    with c4:
        st.metric(
            "🎯 Avg Priority Score",
            f"{avg_score:.1f}"
        )


    st.markdown("")


    # ========================================================
    # CHARTS
    # ========================================================

    col1, col2 = st.columns(2)

    # ---------- PRIORITY ----------

    with col1:

        st.markdown(
            "### 🎯 Retention Priority"
        )

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

        fig = px.bar(
            priority_data,
            x="Priority",
            y="Customers",
            text="Customers",
            category_orders={
                "Priority":
                ["Critical", "High", "Medium", "Low"]
            }
        )

        fig.update_layout(
            template="plotly_white",
            height=390,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),
            showlegend=False
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


    # ---------- CUSTOMER VALUE ----------

    with col2:

        st.markdown(
            "### 💰 Customer Value"
        )

        value_data = (
            filtered_df["Customer_Value_Category"]
            .value_counts()
            .reset_index()
        )

        value_data.columns = [
            "Category",
            "Customers"
        ]

        fig = px.pie(
            value_data,
            names="Category",
            values="Customers",
            hole=0.55
        )

        fig.update_layout(
            template="plotly_white",
            height=390,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            )
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


    # ========================================================
    # OPPORTUNITIES
    # ========================================================

    st.markdown(
        "### 🚀 Retention Opportunities"
    )

    opportunity_data = (
        filtered_df["Retention_Opportunity"]
        .value_counts()
        .reset_index()
    )

    opportunity_data.columns = [
        "Opportunity",
        "Customers"
    ]

    opportunity_data = opportunity_data.sort_values(
        "Customers",
        ascending=True
    )

    fig = px.bar(
        opportunity_data,
        x="Customers",
        y="Opportunity",
        orientation="h",
        text="Customers"
    )

    fig.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        showlegend=False
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


    # ========================================================
    # SCORE VS VALUE
    # ========================================================

    st.markdown(
        "### 🔍 Customer Value vs Retention Priority"
    )

    scatter_df = filtered_df.sample(
        min(4000, len(filtered_df)),
        random_state=42
    )

    fig = px.scatter(
        scatter_df,
        x="Recency",
        y="Monetary",
        color="Priority_Tier",
        size="Retention_Priority_Score",
        hover_data=[
            "customer_unique_id",
            "Frequency",
            "Retention_Opportunity"
        ],
        opacity=0.65
    )

    fig.update_layout(
        template="plotly_white",
        height=520,
        xaxis_title="Recency (Days)",
        yaxis_title="Customer Value (R$)"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# RETENTION ACTION CENTER
# ============================================================

elif page == "Retention Action Center":

    st.markdown(
        "## 🚨 Retention Action Center"
    )

    st.write(
        "Identify customers who require attention and "
        "connect them with the recommended retention strategy."
    )

    action_summary = (
        filtered_df
        .groupby("Retention_Opportunity")
        .agg(
            Customers=(
                "customer_unique_id",
                "count"
            ),
            Avg_Value=(
                "Monetary",
                "mean"
            ),
            Avg_Recency=(
                "Recency",
                "mean"
            ),
            Avg_Score=(
                "Retention_Priority_Score",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "Customers",
            ascending=False
        )
    )

    st.dataframe(
        action_summary,
        width="stretch",
        hide_index=True,
        column_config={
            "Retention_Opportunity":
                st.column_config.TextColumn(
                    "Retention Opportunity"
                ),
            "Customers":
                st.column_config.NumberColumn(
                    "Customers",
                    format="%d"
                ),
            "Avg_Value":
                st.column_config.NumberColumn(
                    "Avg Value",
                    format="R$ %.2f"
                ),
            "Avg_Recency":
                st.column_config.NumberColumn(
                    "Avg Recency",
                    format="%.0f days"
                ),
            "Avg_Score":
                st.column_config.NumberColumn(
                    "Avg Priority Score",
                    format="%.1f"
                )
        }
    )


    st.markdown(
        "### 🔥 Top Priority Customers"
    )

    top_customers = (
        filtered_df
        .sort_values(
            "Retention_Priority_Score",
            ascending=False
        )
        .head(25)
        .copy()
    )

    display_columns = [
        "customer_unique_id",
        "Priority_Tier",
        "Retention_Opportunity",
        "Customer_Value_Category",
        "Recency",
        "Frequency",
        "Monetary",
        "Retention_Priority_Score"
    ]

    st.dataframe(
        top_customers[display_columns],
        width="stretch",
        hide_index=True,
        column_config={
            "customer_unique_id":
                st.column_config.TextColumn(
                    "Customer ID"
                ),
            "Priority_Tier":
                st.column_config.TextColumn(
                    "Priority"
                ),
            "Retention_Opportunity":
                st.column_config.TextColumn(
                    "Recommended Opportunity"
                ),
            "Customer_Value_Category":
                st.column_config.TextColumn(
                    "Customer Value"
                ),
            "Recency":
                st.column_config.NumberColumn(
                    "Recency",
                    format="%d days"
                ),
            "Frequency":
                st.column_config.NumberColumn(
                    "Frequency",
                    format="%.0f"
                ),
            "Monetary":
                st.column_config.NumberColumn(
                    "Monetary",
                    format="R$ %.2f"
                ),
            "Retention_Priority_Score":
                st.column_config.NumberColumn(
                    "Priority Score",
                    format="%.1f"
                )
        }
    )


# ============================================================
# CUSTOMER 360
# ============================================================

elif page == "Customer 360":

    st.subheader("👤 Customer 360")
    st.write(
        "View an individual customer's retention profile, value, risk indicators, "
        "and recommended retention action."
    )

    st.info(
        "Search for a customer ID below. If you leave the search empty, "
        "the highest-priority customers are shown."
    )

    # ---------------------------------------------------------
    # CUSTOMER SEARCH
    # ---------------------------------------------------------

    customer_search = st.text_input(
        "🔎 Customer ID",
        placeholder="Enter customer ID...",
        help="Enter the complete customer_unique_id to find a specific customer."
    )

    if customer_search.strip():

        search_text = customer_search.strip().lower()

        customer_options = filtered_df[
            filtered_df["customer_unique_id"]
            .astype(str)
            .str.lower()
            .str.contains(search_text, na=False)
        ].copy()

    else:

        customer_options = (
            filtered_df
            .sort_values(
                "Retention_Priority_Score",
                ascending=False
            )
            .head(200)
            .copy()
        )

    if customer_options.empty:

        st.warning(
            "No customer found. Please check the Customer ID or change the dashboard filters."
        )

    else:

        # -----------------------------------------------------
        # CUSTOMER SELECTION
        # -----------------------------------------------------

        customer_ids = customer_options["customer_unique_id"].astype(str).tolist()

        selected_customer_id = st.selectbox(
            "Select Customer",
            customer_ids,
            key="customer_360_selector"
        )

        customer_row = filtered_df[
            filtered_df["customer_unique_id"].astype(str)
            == selected_customer_id
        ]

        if customer_row.empty:

            st.error("Customer details could not be loaded.")

        else:

            customer = customer_row.iloc[0]

            # -------------------------------------------------
            # BASIC VALUES
            # -------------------------------------------------

            priority_tier = str(customer["Priority_Tier"])
            priority_score = float(customer["Retention_Priority_Score"])

            recency = float(customer["Recency"])
            frequency = float(customer["Frequency"])
            monetary = float(customer["Monetary"])

            rfm_segment = str(customer["RFM_Segment"])
            cluster_profile = str(customer["Cluster_Profile"])
            value_category = str(customer["Customer_Value_Category"])

            retention_opportunity = str(
                customer["Retention_Opportunity"]
            )

            personalized_strategy = str(
                customer["Personalized_Strategy"]
            )

            suggested_channel = str(
                customer["Suggested_Channel"]
            )

            suggested_incentive = str(
                customer["Suggested_Incentive"]
            )

            suggested_message = str(
                customer["Suggested_Message"]
            )

            # -------------------------------------------------
            # PRIORITY COLOR
            # -------------------------------------------------

            priority_colors = {
                "Critical": "#dc2626",
                "High": "#ea580c",
                "Medium": "#ca8a04",
                "Low": "#16a34a"
            }

            priority_color = priority_colors.get(
                priority_tier,
                "#475569"
            )

            # -------------------------------------------------
            # CUSTOMER HEADER
            # -------------------------------------------------

            st.markdown("---")

            st.markdown("## 👤 Customer Profile")

            header_col1, header_col2 = st.columns([3, 1])

            with header_col1:

                st.markdown("**Customer ID**")

                st.code(
                    selected_customer_id,
                    language=None
                )

            with header_col2:

                st.markdown("**Priority Tier**")

                if priority_tier == "Critical":
                    st.error(f"🔴 {priority_tier}")

                elif priority_tier == "High":
                    st.warning(f"🟠 {priority_tier}")

                elif priority_tier == "Medium":
                    st.info(f"🟡 {priority_tier}")

                else:
                    st.success(f"🟢 {priority_tier}")

            # -------------------------------------------------
            # KEY CUSTOMER METRICS
            # -------------------------------------------------

            st.markdown("### 📊 Customer Value & Risk")

            metric1, metric2, metric3, metric4 = st.columns(4)

            with metric1:
                st.metric(
                    "Recency",
                    f"{recency:,.0f} days"
                )

            with metric2:
                st.metric(
                    "Frequency",
                    f"{frequency:,.0f}"
                )

            with metric3:
                st.metric(
                    "Monetary Value",
                    f"R$ {monetary:,.2f}"
                )

            with metric4:
                st.metric(
                    "Priority Score",
                    f"{priority_score:.2f}"
                )

            # -------------------------------------------------
            # PRIORITY GAUGE
            # -------------------------------------------------

            st.markdown("### 🎯 Retention Priority")

            gauge_col, explanation_col = st.columns([1, 1])

            with gauge_col:

                gauge = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=priority_score,
                        title={
                            "text": "Retention Priority Score"
                        },
                        number={
                            "font": {
                                "size": 36
                            }
                        },
                        gauge={
                            "axis": {
                                "range": [0, 100],
                                "tickwidth": 1,
                                "tickcolor": "#64748b"
                            },
                            "bar": {
                                "color": priority_color
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
                                    "color": "#ffedd5"
                                },
                                {
                                    "range": [75, 100],
                                    "color": "#fee2e2"
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
                        t=60,
                        b=20
                    )
                )

                st.plotly_chart(
                    gauge,
                    width="stretch"
                )

            with explanation_col:

                st.markdown("#### What this score means")

                if priority_tier == "Critical":

                    st.error(
                        "This customer has a very high retention priority. "
                        "The customer should be considered for immediate "
                        "retention or win-back action."
                    )

                elif priority_tier == "High":

                    st.warning(
                        "This customer has a high retention priority. "
                        "A targeted retention action should be considered."
                    )

                elif priority_tier == "Medium":

                    st.info(
                        "This customer has a medium retention priority. "
                        "Regular engagement and repeat-purchase activity "
                        "can help maintain the relationship."
                    )

                else:

                    st.success(
                        "This customer currently has a lower retention "
                        "priority based on the scoring model."
                    )

                st.metric(
                    "Customer Value",
                    value_category
                )

            # -------------------------------------------------
            # CUSTOMER SEGMENTATION
            # -------------------------------------------------

            st.markdown("---")
            st.markdown("## 🧩 Customer Segmentation")

            segment_col1, segment_col2, segment_col3 = st.columns(3)

            with segment_col1:

                st.markdown("**RFM Segment**")

                st.info(rfm_segment)

            with segment_col2:

                st.markdown("**ML Cluster Profile**")

                st.info(cluster_profile)

            with segment_col3:

                st.markdown("**Customer Value Category**")

                st.info(value_category)

            # -------------------------------------------------
            # IMPORTANT FACTORS
            # -------------------------------------------------

            st.markdown("---")
            st.markdown("## 🔍 Important Customer Factors")

            factor_col1, factor_col2 = st.columns(2)

            with factor_col1:

                st.markdown("### Risk Indicators")

                if recency > 365:
                    st.error(
                        f"🔴 Very high recency: {recency:.0f} days "
                        "since the customer's latest purchase."
                    )

                elif recency > 180:
                    st.warning(
                        f"🟠 High recency: {recency:.0f} days "
                        "since the customer's latest purchase."
                    )

                else:
                    st.success(
                        f"🟢 Recent activity: {recency:.0f} days "
                        "since the customer's latest purchase."
                    )

                if frequency <= 1:
                    st.warning(
                        "The customer has made only one purchase."
                    )

                else:
                    st.success(
                        f"The customer has made {frequency:.0f} purchases."
                    )

            with factor_col2:

                st.markdown("### Value Indicators")

                st.metric(
                    "Total Customer Spending",
                    f"R$ {monetary:,.2f}"
                )

                if monetary >= 300:
                    st.success(
                        "High monetary value customer."
                    )

                elif monetary >= 150:
                    st.info(
                        "Medium monetary value customer."
                    )

                else:
                    st.caption(
                        "Lower monetary value customer."
                    )

            # -------------------------------------------------
            # RETENTION ACTION
            # -------------------------------------------------

            st.markdown("---")
            st.markdown("## 🚀 Recommended Retention Action")

            action_col1, action_col2 = st.columns(2)

            with action_col1:

                st.markdown("### Retention Opportunity")

                if "Win-Back" in retention_opportunity:

                    st.warning(
                        retention_opportunity
                    )

                elif "Loyalty" in retention_opportunity:

                    st.success(
                        retention_opportunity
                    )

                else:

                    st.info(
                        retention_opportunity
                    )

                st.markdown("### Suggested Channel")

                st.write(
                    suggested_channel
                )

                st.markdown("### Suggested Incentive")

                st.write(
                    suggested_incentive
                )

            with action_col2:

                st.markdown("### Personalized Strategy")

                st.info(
                    personalized_strategy
                )

                st.markdown("### Suggested Customer Message")

                st.write(
                    f'"{suggested_message}"'
                )

            # -------------------------------------------------
            # BUSINESS ACTION SUMMARY
            # -------------------------------------------------

            st.markdown("---")
            st.markdown("## 💡 Business Action Summary")

            if priority_tier == "Critical":

                st.error(
                    "ACTION NOW: This customer belongs to the critical "
                    "retention-priority group. Consider a personalized "
                    "retention or win-back campaign."
                )

            elif priority_tier == "High":

                st.warning(
                    "ACTION SOON: This customer has high retention "
                    "priority. Consider targeted engagement."
                )

            elif priority_tier == "Medium":

                st.info(
                    "MONITOR & ENGAGE: Maintain customer engagement "
                    "and encourage future purchases."
                )

            else:

                st.success(
                    "MAINTAIN: Continue normal customer engagement "
                    "and retention activities."
                )


elif page == "Campaign Dashboard":

    st.subheader("🎯 Retention Campaign Dashboard")

    st.write(
        "Analyze customer retention campaigns, campaign size, "
        "customer value, and campaign priority."
    )

    # ---------------------------------------------------------
    # CAMPAIGN SUMMARY
    # ---------------------------------------------------------

    campaign_summary = (
        filtered_df
        .groupby("Campaign_Group")
        .agg(
            Customers=("customer_unique_id", "count"),
            Average_Value=("Monetary", "mean"),
            Average_Priority=("Retention_Priority_Score", "mean"),
            Critical_Customers=(
                "Priority_Tier",
                lambda x: (x == "Critical").sum()
            ),
            High_Customers=(
                "Priority_Tier",
                lambda x: (x == "High").sum()
            )
        )
        .reset_index()
        .sort_values(
            "Customers",
            ascending=False
        )
    )

    # ---------------------------------------------------------
    # TOP METRICS
    # ---------------------------------------------------------

    total_campaigns = campaign_summary["Campaign_Group"].nunique()

    total_campaign_customers = len(filtered_df)

    total_critical = (
        filtered_df["Priority_Tier"]
        .eq("Critical")
        .sum()
    )

    average_campaign_value = filtered_df["Monetary"].mean()

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            "Campaign Groups",
            total_campaigns
        )

    with metric2:
        st.metric(
            "Target Customers",
            f"{total_campaign_customers:,}"
        )

    with metric3:
        st.metric(
            "Critical Customers",
            f"{total_critical:,}"
        )

    with metric4:
        st.metric(
            "Avg Customer Value",
            f"R$ {average_campaign_value:,.2f}"
        )

    # ---------------------------------------------------------
    # CAMPAIGN CUSTOMER DISTRIBUTION
    # ---------------------------------------------------------

    st.markdown("---")

    st.markdown("### 📊 Customers by Campaign")

    campaign_chart = go.Figure(
        go.Bar(
            x=campaign_summary["Campaign_Group"],
            y=campaign_summary["Customers"],
            text=campaign_summary["Customers"],
            textposition="auto"
        )
    )

    campaign_chart.update_layout(
        height=400,
        xaxis_title="Campaign Group",
        yaxis_title="Number of Customers",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=100
        )
    )

    st.plotly_chart(
        campaign_chart,
        width="stretch"
    )

    # ---------------------------------------------------------
    # CAMPAIGN VALUE
    # ---------------------------------------------------------

    st.markdown("### 💰 Average Customer Value by Campaign")

    value_chart = go.Figure(
        go.Bar(
            x=campaign_summary["Campaign_Group"],
            y=campaign_summary["Average_Value"],
            text=campaign_summary["Average_Value"].round(2),
            texttemplate="R$ %{text}",
            textposition="auto"
        )
    )

    value_chart.update_layout(
        height=380,
        xaxis_title="Campaign Group",
        yaxis_title="Average Customer Value",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=100
        )
    )

    st.plotly_chart(
        value_chart,
        width="stretch"
    )

    # ---------------------------------------------------------
    # CAMPAIGN PRIORITY
    # ---------------------------------------------------------

    st.markdown("---")

    st.markdown("### 🚨 Campaign Priority")

    priority_summary = (
        filtered_df
        .groupby(
            ["Campaign_Group", "Priority_Tier"]
        )
        .size()
        .reset_index(
            name="Customers"
        )
    )

    priority_chart = go.Figure()

    for tier in ["Critical", "High", "Medium", "Low"]:

        tier_data = priority_summary[
            priority_summary["Priority_Tier"] == tier
        ]

        if not tier_data.empty:

            priority_chart.add_trace(
                go.Bar(
                    x=tier_data["Campaign_Group"],
                    y=tier_data["Customers"],
                    name=tier
                )
            )

    priority_chart.update_layout(
        barmode="stack",
        height=450,
        xaxis_title="Campaign Group",
        yaxis_title="Customers",
        legend_title="Priority Tier",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=100
        )
    )

    st.plotly_chart(
        priority_chart,
        width="stretch"
    )

    # ---------------------------------------------------------
    # CAMPAIGN SUMMARY TABLE
    # ---------------------------------------------------------

    st.markdown("---")

    st.markdown("### 📋 Campaign Summary")

    display_campaign_summary = campaign_summary.copy()

    display_campaign_summary["Average_Value"] = (
        display_campaign_summary["Average_Value"]
        .round(2)
    )

    display_campaign_summary["Average_Priority"] = (
        display_campaign_summary["Average_Priority"]
        .round(2)
    )

    display_campaign_summary = (
        display_campaign_summary
        .rename(
            columns={
                "Campaign_Group": "Campaign",
                "Customers": "Customers",
                "Average_Value": "Avg Customer Value",
                "Average_Priority": "Avg Priority Score",
                "Critical_Customers": "Critical",
                "High_Customers": "High"
            }
        )
    )

    st.dataframe(
        display_campaign_summary,
        width="stretch",
        hide_index=True
    )

    # ---------------------------------------------------------
    # TARGET CUSTOMER LIST
    # ---------------------------------------------------------

    st.markdown("---")

    st.markdown("### 🎯 Campaign Target Customers")

    selected_campaign = st.selectbox(
        "Select a campaign",
        sorted(
            filtered_df["Campaign_Group"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    campaign_customers = filtered_df[
        filtered_df["Campaign_Group"] == selected_campaign
    ].copy()

    campaign_customers = (
        campaign_customers
        .sort_values(
            "Retention_Priority_Score",
            ascending=False
        )
    )

    target_columns = [
        "customer_unique_id",
        "Priority_Tier",
        "Retention_Priority_Score",
        "Monetary",
        "Recency",
        "Frequency"
    ]

    available_target_columns = [
        col
        for col in target_columns
        if col in campaign_customers.columns
    ]

    target_display = campaign_customers[
        available_target_columns
    ].head(50).copy()

    target_display = target_display.rename(
        columns={
            "customer_unique_id": "Customer ID",
            "Priority_Tier": "Priority",
            "Retention_Priority_Score": "Priority Score",
            "Monetary": "Customer Value",
            "Recency": "Recency",
            "Frequency": "Frequency"
        }
    )

    st.dataframe(
        target_display,
        width="stretch",
        hide_index=True
    )

    # ---------------------------------------------------------
    # DOWNLOAD CAMPAIGN LIST
    # ---------------------------------------------------------

    csv_data = campaign_customers.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Campaign Customer List",
        data=csv_data,
        file_name=(
            selected_campaign
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
            + "_customers.csv"
        ),
        mime="text/csv"
    )

    # ---------------------------------------------------------
    # BUSINESS INTERPRETATION
    # ---------------------------------------------------------

    st.markdown("---")

    st.markdown("### 💡 Campaign Insight")

    largest_campaign = campaign_summary.iloc[0]

    st.info(
        f"The largest campaign is **{largest_campaign['Campaign_Group']}**, "
        f"containing **{int(largest_campaign['Customers']):,} customers**. "
        f"The average customer value in this campaign is "
        f"**R$ {largest_campaign['Average_Value']:,.2f}**."
    )

# ============================================================
# BUSINESS INSIGHTS
# ============================================================

elif page == "Business Insights":

    st.markdown(
        "## 💡 Business Intelligence & Insights"
    )

    st.write(
        "Translate customer analytics into clear business observations."
    )

    total = len(filtered_df)

    if total == 0:

        st.warning(
            "No customers match the selected filters."
        )

    else:

        critical = len(
            filtered_df[
                filtered_df["Priority_Tier"] == "Critical"
            ]
        )

        high = len(
            filtered_df[
                filtered_df["Priority_Tier"] == "High"
            ]
        )

        priority_count = critical + high

        priority_percentage = (
            priority_count / total * 100
        )

        avg_value = filtered_df["Monetary"].mean()

        avg_recency = filtered_df["Recency"].mean()

        largest_opportunity = (
            filtered_df["Retention_Opportunity"]
            .value_counts()
            .idxmax()
        )

        largest_opportunity_count = (
            filtered_df["Retention_Opportunity"]
            .value_counts()
            .max()
        )


        # ---------- INSIGHT METRICS ----------

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "🚨 Critical",
                f"{critical:,}"
            )

        with c2:
            st.metric(
                "⚠️ High",
                f"{high:,}"
            )

        with c3:
            st.metric(
                "💰 Avg Value",
                f"R$ {avg_value:,.2f}"
            )

        with c4:
            st.metric(
                "📅 Avg Recency",
                f"{avg_recency:.0f} days"
            )


        st.markdown("")


        # ---------- KEY INSIGHTS ----------

        left, right = st.columns(2)

        with left:

            st.markdown(
                "### 🚨 Retention Priority"
            )

            st.info(
                f"""
                **{priority_count:,} customers**
                are currently classified as Critical or High priority.

                That represents approximately
                **{priority_percentage:.1f}%**
                of the selected customer population.
                """
            )

        with right:

            st.markdown(
                "### 🎯 Main Opportunity"
            )

            st.success(
                f"""
                The largest identified retention opportunity is:

                **{largest_opportunity}**

                Customer count:
                **{largest_opportunity_count:,}**

                This group can be used to organize targeted
                retention campaigns.
                """
            )


        # ---------- BEHAVIOR ----------

        st.markdown(
            "### 📈 Customer Behavior"
        )

        behavior = (
            filtered_df
            .groupby("Priority_Tier")
            .agg(
                Customers=(
                    "customer_unique_id",
                    "count"
                ),
                Avg_Recency=(
                    "Recency",
                    "mean"
                ),
                Avg_Frequency=(
                    "Frequency",
                    "mean"
                ),
                Avg_Value=(
                    "Monetary",
                    "mean"
                )
            )
            .reset_index()
        )

        st.dataframe(
            behavior,
            width="stretch",
            hide_index=True
        )


        # ---------- DOWNLOAD ----------

        st.markdown(
            "### 📥 Export Analysis"
        )

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Filtered Customer Data",
            data=csv_data,
            file_name="retainai_filtered_customers.csv",
            mime="text/csv"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        RetainAI • AI-Powered Customer Retention Platform
        <br>
        RFM Analytics • Customer Segmentation • Priority Scoring
        • Personalized Retention
    </div>
    """,
    unsafe_allow_html=True
)
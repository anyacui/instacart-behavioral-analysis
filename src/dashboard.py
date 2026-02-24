import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Instacart Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .big-font {
        font-size: 48px !important;
        font-weight: bold;
    }
    [class*="st-key-chart"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.caption(
    "**Note:** Analysis excludes 'missing' department. Insights based on 20 product categories.")

# ==================== SIDEBAR ====================

st.sidebar.title("🛒 Dashboard")

st.sidebar.markdown("### Navigation")
st.session_state.page = st.sidebar.radio(
    "Navigate",
    ["Home", "Department Segmentation", "Reorder Analysis"],
    index=["Home", "Department Segmentation",
           "Reorder Analysis"].index(st.session_state.page)
)

st.sidebar.markdown("### Quick Stats")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Orders", "3.4M")
    st.metric("Avg Basket", "10.1")
with col2:
    st.metric("Customers", "206K")
    st.metric("Reorder %", "59.8%")

st.sidebar.markdown("---")
st.sidebar.caption("**Dataset:** Instacart 2017")
st.sidebar.caption("**Analysis:** Anya Cui")
st.sidebar.caption("**Last Updated:** Jan 2026")

# ==================== HELPER FUNCTIONS ====================


def create_dept_scatter(dept_data, height=600):
    """Create department segmentation scatter plot with quadrants"""

    fig = px.scatter(
        dept_data,
        x='avg_basket_size',
        y='reorder_rate_pct',
        size='order_count',
        hover_name='department',
        title='Department Segmentation: Shopping Behavior vs Customer Loyalty',
        labels={
            'avg_basket_size': 'Average Basket Size',
            'reorder_rate_pct': 'Reorder Rate (%)',
            'order_count': 'Total Orders'
        },
        color_continuous_scale='Viridis'
    )

    fig.update_traces(textposition='top center')

    median_basket = dept_data['avg_basket_size'].median()
    median_reorder = dept_data['reorder_rate_pct'].median()

    fig.add_vline(x=median_basket, line_dash="dash", line_color="gray")
    fig.add_hline(y=median_reorder, line_dash="dash", line_color="gray")

    # Quadrant labels
    labels = [
        (median_basket - 3, median_reorder + 8, "High Loyalty<br>Small Baskets"),
        (median_basket - 3, median_reorder - 12, "Low Loyalty<br>Small Baskets"),
        (median_basket + 2.4, median_reorder + 8, "High Loyalty<br>Large Baskets"),
        (median_basket + 2.4, median_reorder - 12, "Low Loyalty<br>Large Baskets")
    ]

    for x, y, text in labels:
        fig.add_annotation(x=x, y=y, text=text, showarrow=False,
                           font=dict(size=12, color="gray"))

    fig.update_layout(height=height)
    return fig


def create_kpi_card(title, value, color_rgba):
    """Generate HTML for styled KPI card"""
    return f"""
        <div style='
            background-color: {color_rgba};
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid {color_rgba.replace("0.15", "0.3")};
        '>
            <p style='font-size: 20px; color: #888; margin: 0; font-weight: 500;'>{title}</p>
            <p style='font-size: 40px; font-weight: bold; margin: 10px 0; color: #000000;'>{value}</p>
        </div>
    """

# ==================== HOME PAGE ====================


if st.session_state.page == "Home":

    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Instacart Analytics Dashboard")

    with st.expander('About this dataset'):
        st.write("""This dataset contains anonymized customer order data including products purchased, 
                 reorder patterns, and department classifications. 32.4M product orders across 20 departments 
                 and 49.7K products from the Instacart Kaggle competition.""")

    st.markdown("---")

    # Top row: Heatmap, Donut, Loyalty gauge
    col1, col2, col3 = st.columns([1, 1, 0.75])

    # Heatmap
    with col1:
        with st.container(height=500, key="chart1"):
            st.markdown("<h4 style='text-align: center; font-size: 25px;'>Peak Shopping Hours</h4>",
                        unsafe_allow_html=True)

            days_hours = pd.read_csv('data/processed_data/days_hours.csv')
            heatmap_matrix = days_hours.pivot(
                index='order_hour', columns='day', values='orders')

            fig_heatmap = px.imshow(
                heatmap_matrix,
                labels=dict(x="Day of Week", y="Hour of Day",
                            color="Number of Orders"),
                x=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                color_continuous_scale='Blues'
            )

            fig_heatmap.update_yaxes(
                tickmode='array',
                tickvals=list(range(0, 24, 3)),
                ticktext=[f'{h}:00' for h in range(0, 24, 3)],
                autorange='reversed'
            )

            fig_heatmap.update_layout(
                height=400,
                margin=dict(l=60, r=20, t=20, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                shapes=[dict(
                    type="rect", xref="paper", yref="paper",
                    x0=0, y0=0, x1=1, y1=1,
                    line=dict(color="rgba(255, 255, 255, 0.2)", width=2)
                )]
            )

            st.plotly_chart(fig_heatmap, use_container_width=True)

    # Donut chart
    with col2:
        with st.container(key="chart2"):
            st.markdown("<h4 style='text-align: center; font-size: 25px;'>Category Distribution</h4>",
                        unsafe_allow_html=True)

            dept_orders = pd.read_csv('data/processed_data/dept_orders.csv')

            fig_donut = px.pie(
                dept_orders, values='products_ordered', names='department', hole=0.5)
            fig_donut.update_layout(
                height=400,
                showlegend=True,
                legend=dict(orientation="v", yanchor="middle",
                            y=0.5, xanchor="left", x=1.02)
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent')

            st.plotly_chart(fig_donut, use_container_width=True)

    # Loyalty gauge
    with col3:
        kpi1, kpi2 = st.columns(2)

        with kpi1:
            st.markdown(create_kpi_card("Orders", "3.4M",
                        "rgba(46, 134, 171, 0.15)"), unsafe_allow_html=True)

        with kpi2:
            st.markdown(create_kpi_card("Customers", "206K",
                        "rgba(106, 153, 78, 0.15)"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(key="chart3", height=297):
            col_spacer, col_title, col_badge = st.columns([1, 4, 1])

            with col_title:
                st.markdown("<h4 style='text-align: center; font-size: 25px;'>Customer Loyalty</h4>",
                            unsafe_allow_html=True)

            with col_badge:
                if st.button("→", key="nav_time", type="secondary", use_container_width=True):
                    st.session_state.page = "Reorder Analysis"
                    st.rerun()

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=59.8,
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2E86AB"},
                    'steps': [
                        {'range': [0, 40], 'color': "#FEE5D9"},
                        {'range': [40, 70], 'color': "#FCBBA1"},
                        {'range': [70, 100], 'color': "#A50F15"}
                    ],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 70}
                },
                title={'text': "Reorder Rate %"}
            ))

            fig_gauge.update_layout(
                height=180, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

    # Second row: Basket size, Top products, Loyalty line, Scatter
    col1, col2, col3 = st.columns([0.5, 0.5, 1.2])

    with col1:
        st.markdown("""
            <div style='
                background-color: rgba(173, 216, 230, 0.2);
                padding: 30px 20px;
                border-radius: 12px;
                text-align: center;
            '>     
                <p style='font-size: 20px; color: #888; margin: 0; font-weight: 500;'>Average Basket Size</p>
                <p style='font-size: 40px; font-weight: bold; margin: 10px 0; color: #000000;'>10.1</p>
                <p style='font-size: 16px; color: #888; margin: 10px 0 0 0;'>items per order</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        with st.container(height=328, key="chart4"):
            st.markdown("<h4 style='text-align: center; font-size: 25px;'>Top Products</h4>",
                        unsafe_allow_html=True)

            popular_products = pd.read_csv(
                'data/processed_data/popular_products.csv')
            popular_products = popular_products[popular_products['department'] != 'missing']

            top_10 = popular_products.nlargest(10, 'product_count')[
                ['product_name', 'pct_of_total', 'department']
            ].copy()

            top_10['product_name'] = top_10['product_name'].str.title()
            top_10['department'] = top_10['department'].str.title()
            top_10.columns = ['Product', '% of Orders', 'Department']

            st.dataframe(
                top_10.style.format({'% of Orders': '{:.2f}%'}),
                use_container_width=True,
                hide_index=True,
                height=380
            )

    with col2:
        with st.container(height=550, key="chart5",  vertical_alignment="center", horizontal_alignment="center"):
            st.markdown("<h4 style='text-align: center; font-size: 25px;'>Loyalty Growth</h4>",
                        unsafe_allow_html=True)

            loyalty = pd.read_csv('data/processed_data/loyalty_growth.csv')
            loyalty_first_10 = loyalty[loyalty['order_number'] <= 10]

            fig_loyalty = px.line(
                loyalty_first_10, x='order_number', y='reorder_rate_pct', markers=True)
            fig_loyalty.update_traces(line=dict(width=3, color='#2E86AB'))
            fig_loyalty.update_layout(
                height=300,
                showlegend=False,
                xaxis_title="Order #",
                yaxis_title="Reorder %",
                margin=dict(l=0, r=0, t=30, b=0)
            )

            st.plotly_chart(fig_loyalty, height=400)

    with col3:
        with st.container(height=550, key="chart6", vertical_alignment="center", horizontal_alignment="center"):
            col_spacer, col_title, col_badge = st.columns([1, 9, 1])

            with col_title:
                st.markdown("<h4 style='text-align: center; font-size: 25px;'>Customer Behavior by Department</h4>",
                            unsafe_allow_html=True)

            with col_badge:
                if st.button("→", key="nav_dept", type="secondary", use_container_width=True):
                    st.session_state.page = "Department Segmentation"
                    st.rerun()

            dept_data = pd.read_csv('data/processed_data/dept_data.csv')
            fig_scatter = create_dept_scatter(dept_data, height=400)
            st.plotly_chart(fig_scatter, width=800)

    st.markdown("---")

    # Product pairs
    with st.container(height=600, key="chart7", vertical_alignment="center", horizontal_alignment="center"):
        st.markdown("<h4 style='text-align: center; font-size: 25px;'>Top Product Pairs</h4>",
                    unsafe_allow_html=True)

        top_products = pd.read_csv('data/processed_data/top_product_pairs.csv')
        top_products['product_pairs'] = top_products['p1'] + \
            ' + ' + top_products['p2']

        fig = px.bar(
            top_products,
            x='pair_orders',
            y='product_pairs',
            orientation='h',
            labels={'pair_orders': 'Number of Orders',
                    'product_pairs': 'Product Combinations'},
            text='pair_orders'
        )

        st.plotly_chart(fig, width=2000)

# ==================== DEPARTMENT SEGMENTATION ====================

elif st.session_state.page == "Department Segmentation":

    st.header("Department Segmentation Deep Dive")

    st.markdown("""Analyzing how departments differ in customer loyalty and basket contribution. 
                We examine both positioning (loyalty vs basket size) and how department share evolves 
                over repeated purchases.""")

    col1, col2 = st.columns(2)

    with col1:
        dept_data = pd.read_csv('data/processed_data/dept_data.csv')
        fig_scatter = create_dept_scatter(dept_data, height=600)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        concentration_df = pd.read_csv(
            'data/processed_data/dept_conc_simple.csv')

        fig = px.bar(
            concentration_df,
            x='avg_dept_conc',
            y='department',
            orientation='h',
            title='Average Basket Concentration by Department',
            labels={'avg_dept_conc': 'Average % of Basket',
                    'department': 'Department'},
            text='avg_dept_conc',
            color='avg_dept_conc',
            color_continuous_scale='Blues'
        )

        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=600)

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Key Insights")
    st.markdown("""
Four behavioral clusters emerge from the loyalty-basket size relationship:

- Platform anchors (Produce 65%, Dairy 67%) occupy the top-center at median basket size (15.5 items) with exceptional loyalty, accounting for 46% of total volume.
- Focused purchases (top-left: Beverages 65%, Alcohol 57%) show loyalty with smaller baskets.
- Stock-up departments (Babies 58%/19.4 items, Dry Goods 46%/17.3 items) extend rightward with bulk purchasing patterns.
- Exploratory categories (bottom-left: Personal Care 32%, Household 40%) show low habit formation across varied basket sizes.

The concentration of high-volume departments near median basket size with above-median loyalty reveals the behavioral profile driving repeat platform engagement..
""")

    st.divider()

    st.header("Basket Concentration Over Lifecycle")
    st.markdown(
        "Select a department to see how its basket share changes across repeated purchases.")

    lifecycle_conc = pd.read_csv(
        'data/processed_data/lifecycle_concentration.csv')

    dept_list = lifecycle_conc['department'].unique().tolist()
    selected_dept = st.selectbox(
        "", dept_list, format_func=lambda x: x.title())

    dept_data = lifecycle_conc[
        (lifecycle_conc['department'] == selected_dept) &
        (lifecycle_conc['dept_purchase_number'] <= 15)
    ]

    st.subheader(f"{selected_dept.title()} - Basket Concentration Trend")

    fig = px.line(
        dept_data,
        x='dept_purchase_number',
        y='avg_concentration_pct',
        title=f'Basket Share: {selected_dept.title()}',
        labels={
            'dept_purchase_number': 'Purchase Occasion',
            'avg_concentration_pct': '% of Basket'
        },
        markers=True,
        color_discrete_sequence=['#2E86AB']
    )

    avg_conc = dept_data['avg_concentration_pct'].mean()
    fig.add_hline(
        y=avg_conc,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Average: {avg_conc:.1f}%",
        annotation_position="right"
    )

    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(height=500, hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)

# ==================== REORDER ANALYSIS ====================

elif st.session_state.page == "Reorder Analysis":

    st.header("Customer Loyalty Evolution")

    loyalty = pd.read_csv('data/processed_data/loyalty_growth.csv')

    fig = px.line(
        loyalty,
        x='order_number',
        y='reorder_rate_pct',
        labels={'order_number': 'Customer Order Number',
                'reorder_rate_pct': 'Reorder Rate (%)'},
        markers=True
    )

    fig.update_traces(line=dict(width=4, color='#2E86AB'), marker=dict(size=8))

    # Milestone annotations
    first_order = loyalty.iloc[0]['reorder_rate_pct']
    fifth_order = loyalty.iloc[4]['reorder_rate_pct']
    tenth_order = loyalty.iloc[9]['reorder_rate_pct']

    annotations = [
        (1, first_order, f"{first_order:.0f}%<br>First order", -40, -40),
        (5, fifth_order, f"{fifth_order:.0f}%<br>Rapid growth", 0, -40),
        (10, tenth_order,
         f"{tenth_order:.0f}%<br>Established loyalty", 40, -40)
    ]

    for x, y, text, ax, ay in annotations:
        fig.add_annotation(x=x, y=y, text=text,
                           showarrow=True, arrowhead=2, ax=ax, ay=ay)

    fig.update_layout(height=500, hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)

    # Find plateau
    plateau_order = None
    for i in range(1, len(loyalty)):
        if abs(loyalty.iloc[i]['reorder_rate_pct'] - loyalty.iloc[i-1]['reorder_rate_pct']) < 2:
            plateau_order = loyalty.iloc[i]['order_number']
            break

    st.info(f"""
**Reorder rate tracks repeat purchases across customers' first 20 orders.**

**Findings:**  
Reorder rate increases from {first_order:.0f}% (order 1) to {tenth_order:.0f}% (order 10). 
Steepest growth occurs between orders 1–3. Growth slows after order {plateau_order}, 
suggesting behavioral stabilization.

**Interpretation:**  
Customer purchasing patterns become habitual within 5–7 orders, after which reorder behavior 
plateaus. Early purchase cycles are the primary period of habit formation.
    """)

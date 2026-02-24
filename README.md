# Instacart Customer Analytics

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://instacart-behavioral-analysis.streamlit.app)

Interactive analytics platform analyzing 3.4M grocery orders to identify customer behavior patterns, department segmentation, and loyalty trends.

## Live Demo

**[View Dashboard →](https://instacart-behavioral-analysis.streamlit.app)**

## Screenshots

*Main dashboard with peak hours heatmap and category distribution*
![Dashboard Overview](https://i.imgur.com/NWiNLsV.png)
![Dashboard Overview 2](https://i.imgur.com/pdyrMtQ.png)

*Behavioral clustering showing power categories vs. exploratory segments*
![Department Segmentation](https://i.imgur.com/WqwmMO9.png)
![Department Segmentation 2](https://i.imgur.com/GsoCj4Q.png)

*Loyalty evolution shows quick habit formation*
![Loyalty Evolution](https://i.imgur.com/mzyePuw.png)

## Key Features

- **Temporal Analysis**: Peak shopping hours heatmap revealing Sunday 10am-2pm as highest traffic period
- **Department Segmentation**: Behavioral clustering identifying power categories (Produce, Dairy) vs. exploratory segments (Personal Care, Household)
- **Loyalty Tracking**: Reorder rate evolution showing habit formation within 5-7 orders
- **Product Analytics**: Top products and frequently bought together analysis

## Tech Stack

- **Backend**: Python, Pandas, DuckDB (SQL)
- **Visualization**: Plotly, Streamlit
- **Data Processing**: 32M+ records analyzed with window functions and CTEs

## Key Findings

- Customer loyalty stabilizes at 70% reorder rate by order 7
- Produce and Dairy account for 46% of platform volume with 65%+ loyalty
- Babies category shows 2x larger baskets (19.4 vs 10.1 avg) indicating stock-up behavior
- Personal Care exhibits 32% reorder rate suggesting brand experimentation over habit formation

## Installation
```bash
# Clone repository
git clone https://github.com/anyacui/instacart-behavioral-analysis.git
cd instacart-behavioral-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download data (see Data section below)

# Run dashboard
streamlit run src/dashboard.py
```

## Project Structure
```
├── data/
│   ├── processed_data/      # Aggregated datasets for dashboard
│   └── [raw files]          # Download from Kaggle (not in repo)
├── notebooks/
│   └── exploratory_analysis.ipynb
├── src/
│   └── dashboard.py
├── requirements.txt
└── README.md
```

## Data

This project uses the [Instacart Market Basket Analysis dataset](https://www.kaggle.com/datasets/yasserh/instacart-online-grocery-basket-analysis-dataset/data) from Kaggle.

**To run locally:**
1. Download dataset from Kaggle
2. Place CSV files in `data/` directory:
   - `orders.csv`
   - `products.csv`
   - `departments.csv`
   - `aisles.csv`
   - `order_products__prior.csv`
3. Run `notebooks/exploratory_analysis.ipynb` to generate processed data

## Analysis Highlights

**Department Behavioral Clustering:**
- **Power categories** (Produce 65%, Dairy 67%): High loyalty at median basket size, driving 46% of volume
- **Stock-up departments** (Babies 58%, Household 40%): Large baskets (19.4 items) with lower frequency
- **Exploratory categories** (Personal Care 32%, Pantry 35%): Low loyalty indicating brand switching

**Loyalty Formation:**
- Reorder rate increases from 5% (order 1) to 70% (order 10)
- Steepest growth in first 3 orders
- Behavioral stabilization after order 7


import streamlit as st
import json
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="Uranium Indexes Live Chart",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .title {
            text-align: center;
            color: #2c3e50;
            padding: 20px;
        }
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            padding-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1 class='title'>Uranium Indexes Live Chart</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Interactive visualization of uranium market indexes</p>", unsafe_allow_html=True)

# Function to load and process data
@st.cache_data(ttl=3600)  # Cache data for 1 hour
def load_data():
    with open('pr.json', 'r') as file:
        data = json.load(file)
    return data

# Load data
try:
    data = load_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Create Plotly figure
def create_plotly_chart(data):
    fig = go.Figure()

    colors = {
        "Utracker Prop Index": "#1f77b4",
        "Utracker Prod Index": "#ff7f0e",
        "Utracker Planned Prod Index": "#2ca02c",
        "Utracker Jr Miners Index": "#d62728"
    }

    for index_name, index_data in data.items():
        dates = list(index_data.keys())
        values = list(index_data.values())
        
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=values,
                name=f"{index_name} (Current: {values[-1]:.2f})",
                line=dict(color=colors[index_name], width=2),
                hovertemplate="<b>Date:</b> %{x}<br>" +
                             "<b>Value:</b> %{y:.2f}<br>" +
                             "<extra></extra>"
            )
        )

    fig.update_layout(
        title={
            'text': "Uranium Indexes Performance",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        },
        xaxis_title="Date",
        yaxis_title="Value",
        hovermode='x unified',
        plot_bgcolor='white',
        width=1000,
        height=600,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.05
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='LightGrey'
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='LightGrey'
    )

    return fig

# Create tabs for different views
tab1, tab2 = st.tabs(["Chart", "Data"])

with tab1:
    try:
        fig = create_plotly_chart(data)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        ### Chart Features:
        - 🔍 Hover over lines to see exact values
        - 🖱️ Use mouse wheel or box zoom to zoom in/out
        - 🤚 Click and drag to pan
        - 🔄 Double click to reset view
        - ⭐ Click legend items to show/hide lines
        """)
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")

with tab2:
    try:
        st.markdown("### Raw Data")
        df_dict = {index_name: pd.Series(index_data) 
                  for index_name, index_data in data.items()}
        df = pd.DataFrame(df_dict)
        st.dataframe(df)
        
        csv = df.to_csv().encode('utf-8')
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name="uranium_indexes.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"Error displaying data: {str(e)}")

# Add footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666;'>
    <p>Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <p>Data source: Custom Index Calculation</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("About")
    st.write("""
    This dashboard shows the performance of various uranium market indexes.
    The data is updated regularly and provides interactive visualization capabilities.
    """)
    
    st.header("Index Descriptions")
    st.write("""
    - **Utracker Prop Index**: Proprietary index tracking uranium companies
    - **Utracker Prod Index**: Index of uranium producers
    - **Utracker Planned Prod Index**: Index of planned production companies
    - **Utracker Jr Miners Index**: Index of junior mining companies
    """)

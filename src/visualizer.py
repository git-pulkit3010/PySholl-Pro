import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def plot_sholl_profile(csv_path: str, output_path: str):
    """
    Creates an interactive Plotly graph from Sholl analysis results.
    """
    if not os.path.exists(csv_path):
        logging.error(f"Data file not found: {csv_path}")
        return

    # Load data
    df = pd.read_csv(csv_path)

    # Create the figure
    fig = go.Figure()

    # Add the Sholl Profile line
    fig.add_trace(go.Scatter(
        x=df['radius'], 
        y=df['intersections'],
        mode='lines+markers',
        name='Intersections',
        line=dict(color='#00d4ff', width=3), # Modern blue accent
        marker=dict(size=8, symbol='circle')
    ))

    # Professional Layout
    fig.update_layout(
        title={
            'text': "Sholl Analysis Profile",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Distance from Soma (Radius)",
        yaxis_title="Number of Intersections",
        template="plotly_dark", # Matches your preferred dark aesthetic
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Courier New, monospace", size=14),
        hovermode="x unified"
    )

    # Save as interactive HTML
    fig.write_html(output_path)
    logging.info(f"Interactive plot saved to: {output_path}")

if __name__ == "__main__":
    # Integration test
    data_file = "data/results/sholl_data.csv"
    report_file = "reports/figures/sholl_interactive.html"
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    
    plot_sholl_profile(data_file, report_file)
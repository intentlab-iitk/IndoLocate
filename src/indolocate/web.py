"""
File            : indolocate/web.py  
Description     : Indolocate server file.  
"""

# Imports
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import pandas as pd
import copy

def webserver():
    """Factory function to create and configure the Dash app"""

    app = Dash(__name__, suppress_callback_exceptions=True)
    app.title = "Indolocate"

    # Static AP data
    ap_data = {
        'x': [-4.525536, 4.905565, 17.176555, 17.543673, 6.774813, -4.038577],
        'y': [2.057204, 2.670063, 2.416904, -15.814430, -15.379450, -15.279211],
        'ap_num': [1, 2, 3, 4, 5, 6]
    }
    ap_df = pd.DataFrame(ap_data)

    base_fig = go.Figure()

    base_fig.add_trace(go.Scatter(
        x=ap_df['x'],
        y=ap_df['y'],
        mode='markers',
        marker=dict(size=16, color='red', symbol='triangle-up'),
        name='AP Locations',
    ))

    for i, row in ap_df.iterrows():
        y_offset = 20 if i < 3 else -20
        base_fig.add_annotation(
            x=row['x'],
            y=row['y'],
            text=f'AP {row["ap_num"]}',
            showarrow=False,
            yshift=y_offset,
            font=dict(color='red', size=14)
        )

    base_fig.update_layout(
        yaxis=dict(range=[-18, 5]),
        xaxis=dict(range=[-7, 20], scaleanchor='y'),
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=0),
        autosize=True,
    )

    # App layout
    app.layout = html.Div([
        html.Div([
            dcc.Graph(id='location-plot', style={'height': '95vh', 'width': '95vw'}),
            dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
        ],
        style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
        })
    ],
    style={
        'display': 'flex',
        'height': '98vh',
        'alignItems': 'center',
        'justifyContent': 'center',
        'margin': '0',
        'padding': '0',
        'overflow': 'hidden',         # Prevents scrollbars
        'boxSizing': 'border-box'
    })



    @app.callback(
        Output('location-plot', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_graph_live(n):
        fig = copy.deepcopy(base_fig)

        # Simulated dynamic user location
        x_pos = 0 + 0.5 * (n % 30)
        y_pos = -10 + 0.2 * ((n * 2) % 30)

        fig.add_trace(go.Scatter(
            x=[x_pos],
            y=[y_pos],
            mode='markers',
            marker=dict(size=12, color='blue'),
            name='User'
        ))

        return fig

    return app

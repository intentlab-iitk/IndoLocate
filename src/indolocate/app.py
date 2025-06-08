"""
File            : indolocate/web.py  
Description     : Indolocate server file.  
"""

import logging
from math import log
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
from .algorithms.base import Algorithm
from .structs import app
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import socket
import threading
import copy
import json
import queue

# Global variable
packet_queue = queue.Queue()
user_location = np.array([0, 0])

def packet_listener(ip='0.0.0.0', port=9050):
    """Thread: Receive UDP packets and enqueue raw data."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, port))
        logging.info(f"App is listening on {port}\n")
        while True:
                data, _ = sock.recvfrom(65535)
                packet_queue.put(data)
    except Exception as e:
        logging.error(f"Listener error: {e}")

def webserver(model: Algorithm) -> app:
    app = Dash(__name__, suppress_callback_exceptions=True)
    app.title = "Indolocate"

    # Create and start PacketListener instance
    listener_thread = threading.Thread(target=packet_listener, daemon=True)
    listener_thread.start()

    ap_locs = [
        {'apid': 1, 'x': -4.525536, 'y': 2.057204},
        {'apid': 2, 'x': 4.905565,  'y': 2.670063},
        {'apid': 3, 'x': 17.176555, 'y': 2.416904},
        {'apid': 4, 'x': 17.543673, 'y': -15.814430},
        {'apid': 5, 'x': 6.774813,  'y': -15.379450},
        {'apid': 6, 'x': -4.038577, 'y': -15.279211},
    ]

    ap_df = pd.DataFrame(ap_locs)

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
            text=f'AP {row["apid"]}',
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

    app.layout = html.Div([
        html.Div([
            dcc.Graph(id='location-plot', style={'height': '95vh', 'width': '95vw'}),
            dcc.Interval(id='interval-component', interval=50, n_intervals=0)
        ],
        style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',})
    ],
    style={'display': 'flex', 'height': '98vh', 'alignItems': 'center', 'justifyContent': 'center',
           'margin': '0', 'padding': '0', 'boxSizing': 'border-box'})

    @app.callback(
        Output('location-plot', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_graph_live(n):
        global user_location
        fig = copy.deepcopy(base_fig)
        while not packet_queue.empty():
            try:
                data = packet_queue.get()
                packet = json.loads(data.decode('utf-8'))

                rssi = packet.get('rssi')
                csi_mag = packet.get('csi_mag')
                csi_phase = packet.get('csi_phase')
                feats = np.concatenate([rssi, csi_mag, csi_phase])

                user_location = model.predict(feats)
                logging.debug(user_location)
            except Exception as e:
                logging.error(f"Error processing packet in UI thread: {e}")
        fig.add_trace(go.Scatter(
            x=[user_location[0]],
            y=[user_location[1]],
            mode='markers',
            marker=dict(size=12, color='blue'),
            name='Predicted User'
        ))
        return fig

    return app


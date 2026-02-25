import dash
from dash import dcc, html
import dash_cytoscape as cyto
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import json
import os

# Load synaptic map if it exists to populate the Diamond Architecture nodes
elements = [
    {'data': {'id': 'active_intellect', 'label': 'שכל פועל'}},
    {'data': {'id': 'prophetic', 'label': 'נבואי'}},
    {'data': {'id': 'combination', 'label': 'צירוף'}},
    {'data': {'id': 'existent', 'label': 'נמצא'}},
    {'data': {'source': 'combination', 'target': 'active_intellect', 'label': 'יוצר'}},
    {'data': {'source': 'active_intellect', 'target': 'prophetic', 'label': 'מוליך ל'}},
    {'data': {'source': 'active_intellect', 'target': 'existent', 'label': 'הוא'}},
]

# Path to the synaptic map (relative to root)
MAP_PATH = os.path.join(os.path.dirname(__file__), "synaptic_map.json")

if os.path.exists(MAP_PATH):
    try:
        with open(MAP_PATH, "r", encoding="utf-8") as f:
            synaptic_map = json.load(f)

            # Add agents and their assigned gates from the Diamond Architecture
            for agent, gate_id in synaptic_map.get("group_assignments", {}).items():
                agent_id = f"agent_{agent.replace('/', '_')}"
                gate_node_id = f"gate_{gate_id}"

                elements.append({'data': {'id': agent_id, 'label': f'Agent {agent}'}})
                elements.append({'data': {'id': gate_node_id, 'label': f'Gate {gate_id}'}})
                elements.append({'data': {'source': agent_id, 'target': gate_node_id, 'label': 'Assigned'}})

                # Connect agents to the 'combination' node as they are ontological refiners
                elements.append({'data': {'source': agent_id, 'target': 'combination', 'label': 'Refines'}})

    except Exception as e:
        print(f"Error loading synaptic map for dashboard: {e}")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("AMNE Semantic Dashboard - Sovereign Neural Mode", style={'textAlign': 'center'}),
    html.Div([
        html.P("Architecture: Diamond (Ontological)", style={'textAlign': 'center', 'color': 'gold'}),
        html.P("Status: Disconnected / Thinking Machine Active", style={'textAlign': 'center', 'color': 'green'})
    ], style={'backgroundColor': '#111', 'padding': '10px'}),

    html.Div([
        html.Div([
            html.H2("Ontological Connection Grid (231 Gates Mapping)"),
            cyto.Cytoscape(
                id='cytoscape-graph',
                layout={'name': 'cose'},
                style={'width': '100%', 'height': '600px'},
                elements=elements,
                stylesheet=[
                    {
                        'selector': 'node',
                        'style': {
                            'content': 'data(label)',
                            'text-valign': 'center',
                            'color': 'white',
                            'background-color': '#0074D9',
                            'font-size': '12px'
                        }
                    },
                    {
                        'selector': '[id ^="agent_"]',
                        'style': {
                            'background-color': '#FF4136',
                            'shape': 'diamond'
                        }
                    },
                    {
                        'selector': '[id ^="gate_"]',
                        'style': {
                            'background-color': '#FFDC00',
                            'color': 'black',
                            'shape': 'hexagon'
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'curve-style': 'bezier',
                            'target-arrow-shape': 'triangle',
                            'label': 'data(label)',
                            'font-size': '8px',
                            'line-color': '#AAAAAA',
                            'target-arrow-color': '#AAAAAA'
                        }
                    }
                ]
            )
        ], style={'width': '65%', 'display': 'inline-block'}),

        html.Div([
            html.H2("Tension Gauge (λ₂)"),
            dcc.Graph(
                id='tension-gauge',
                figure=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=0.15,
                    title={'text': "Ontological Contradiction (λ₂)"},
                    gauge={
                        'axis': {'range': [None, 1]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 0.5], 'color': "lightgreen"},
                            {'range': [0.5, 0.8], 'color': "orange"},
                            {'range': [0.8, 1.0], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 0.9
                        }
                    }
                ))
            ),
            html.P("Status: SOVEREIGN SYNC", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': 'blue'}),
            html.Div([
                html.H3("System Capacity"),
                html.P("Compute Pool: 7.5M Hours/Month"),
                html.P("Efficiency: 15% (Optimized)")
            ], style={'padding': '10px', 'border': '1px solid #ccc', 'marginTop': '20px'})
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ])
])

if __name__ == '__main__':
    # app.run_server(debug=True)
    print("Semantic Dashboard updated with Diamond Architecture elements.")

import dash
from dash import dcc, html
import dash_cytoscape as cyto
import plotly.graph_objects as go
from dash.dependencies import Input, Output

def get_digital_root(n):
    if n == 0: return 0
    return 1 + ((n - 1) % 9)

# Labels with their Digital Roots
# שכל פועל: 536 -> 5
# נבואי: 69 -> 6
# צירוף: 386 -> 8
# נמצא: 181 -> 1

elements = [
    {'data': {'id': 'active_intellect', 'label': 'Node_5'}},
    {'data': {'id': 'prophetic', 'label': 'Node_6'}},
    {'data': {'id': 'combination', 'label': 'Node_8'}},
    {'data': {'id': 'existent', 'label': 'Node_1'}},
    {'data': {'source': 'combination', 'target': 'active_intellect', 'label': '8->5'}},
    {'data': {'source': 'active_intellect', 'target': 'prophetic', 'label': '5->6'}},
    {'data': {'source': 'active_intellect', 'target': 'existent', 'label': '5->1'}},
]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("AMNE Arithmetic Dashboard", style={'textAlign': 'center', 'color': '#00ff41'}),

    html.Div([
        html.Div([
            html.H2("Ontological Arithmetic Grid"),
            cyto.Cytoscape(
                id='cytoscape-graph',
                layout={'name': 'cose'},
                style={'width': '100%', 'height': '500px'},
                elements=elements,
                stylesheet=[
                    {
                        'selector': 'node',
                        'style': {
                            'content': 'data(label)',
                            'text-valign': 'center',
                            'color': 'white',
                            'background-color': '#1a4d2e'
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'curve-style': 'bezier',
                            'target-arrow-shape': 'triangle',
                            'label': 'data(label)',
                            'font-size': '10px',
                            'color': '#00ff41'
                        }
                    }
                ]
            )
        ], style={'width': '65%', 'display': 'inline-block'}),

        html.Div([
            html.H2("Verification Gauge (λ₂)"),
            dcc.Graph(
                id='tension-gauge',
                figure=go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=0.9, # Lock 9
                    title={'text': "Arithmetic Stability (λ₂)"},
                    gauge={
                        'axis': {'range': [None, 1]},
                        'bar': {'color': "#00ff41"},
                        'steps': [
                            {'range': [0, 0.5], 'color': "#001a00"},
                            {'range': [0.5, 0.9], 'color': "#003300"},
                            {'range': [0.9, 1.0], 'color': "#00ff41"}
                        ]
                    }
                ))
            ),
            html.P("Status: LOCKED_9", style={'textAlign': 'center', 'fontWeight': 'bold', 'color': '#00ff41'})
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ])
], style={'backgroundColor': '#020202', 'color': '#00ff41'})

if __name__ == '__main__':
    print("Arithmetic Dashboard layout defined.")

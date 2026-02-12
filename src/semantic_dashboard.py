import dash
from dash import dcc, html
import dash_cytoscape as cyto
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Sample data for the graph
elements = [
    {'data': {'id': 'active_intellect', 'label': 'שכל פועל'}},
    {'data': {'id': 'prophetic', 'label': 'נבואי'}},
    {'data': {'id': 'combination', 'label': 'צירוף'}},
    {'data': {'id': 'existent', 'label': 'נמצא'}},
    {'data': {'source': 'combination', 'target': 'active_intellect', 'label': 'יוצר'}},
    {'data': {'source': 'active_intellect', 'target': 'prophetic', 'label': 'מוליך ל'}},
    {'data': {'source': 'active_intellect', 'target': 'existent', 'label': 'הוא'}},
]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("AMNE Semantic Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.H2("Ontological Connection Grid"),
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
                            'background-color': '#0074D9'
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'curve-style': 'bezier',
                            'target-arrow-shape': 'triangle',
                            'label': 'data(label)',
                            'font-size': '10px'
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
                    value=0.42,
                    title={'text': "System Contradiction Level (λ₂)"},
                    gauge={
                        'axis': {'range': [None, 1]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 0.5], 'color': "lightgray"},
                            {'range': [0.5, 0.8], 'color': "gray"},
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
            html.P("Status: Stable", style={'textAlign': 'center', 'fontWeight': 'bold'})
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ])
])

if __name__ == '__main__':
    # Not running the server here to avoid blocking, but providing the structure
    # app.run_server(debug=True)
    print("Semantic Dashboard layout defined.")

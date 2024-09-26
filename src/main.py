import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

data=pd.read_csv(r'C:\Users\ingde\Documents\DAP\PRCF_Reservation\data\processed\df_filtered.csv')
df=pd.DataFrame(data)

df_filtered_1= df.sort_values(by='event_start_mounth_numeric', ascending=True)

df_filtered_2= df.sort_values(by='day_of_week_numeric', ascending=True)


# Crear la aplicación Dash
app = dash.Dash(__name__)

# Definir el tema oscuro
dark_theme = {
    'background': '#111111',
    'text': '#A3F565',
    'grid': '#333333',
    'paper': '#222222'
}

# Estilos globales
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                margin: 0;
                padding: 0;
                background-color: #111111;
            }
            .Select-control {
                background-color: #222222 !important;
                color: #FFFF00 !important;
                border-color: #FFFF00 !important;
            }
            .Select-menu-outer {
                background-color: #222222 !important;
            }
            .Select-value-label {
                color: #FFFF00 !important;
            }
            .Select-menu-outer .Select-option {
                background-color: #222222;
                color: #FFFF00;
            }
            .Select-menu-outer .Select-option:hover {
                background-color: #444444;
            }
            .Select-arrow {
                border-color: #FFFF00 transparent transparent !important;
            }
            .Select.is-open > .Select-control {
                background-color: #222222;
                border-color: #FFFF00 !important;
            }
            .Select-placeholder, .Select--single > .Select-control .Select-value {
                color: #FFFF00 !important;
            }
            .Select-menu-outer .Select-option.is-selected {
                background-color: #444444;
            }
            .Select-option.is-focused {
                background-color: #333333 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Estilos comunes
common_styles = {
    'width': '32%',
    'display': 'inline-block',
    'backgroundColor': dark_theme['background'],
    'padding': '10px',
    'marginBottom': '10px'
}

dropdown_style = {
    'backgroundColor': dark_theme['paper'],
    'color': '#FFFF00',
    'font-family': 'Roboto, sans-serif'
}

# Función para crear una sección
def create_section(title, dropdown_id, graph_id, options, value):
    return html.Div([
        html.H3(title, style={'font-family': 'Roboto, sans-serif', 'color': dark_theme['text']}),
        dcc.Dropdown(
            id=dropdown_id,
            options=[{'label': i, 'value': i} for i in options],
            value=value,
            style=dropdown_style
        ),
        dcc.Graph(id=graph_id)
    ], style=common_styles)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("PRCF_Reservation Dashboard", style={'font-family': 'Roboto, sans-serif', 'fontSize': '40px', 'color': dark_theme['text'], 'marginBottom': '20px'}),
    create_section("Residency Flag by Month", 'dropdown_1', 'fig_1', df_filtered_1['event_start_mounth_numeric'].unique(),''),
    create_section("Transaction Site by Day", 'dropdown_2', 'fig_2', df_filtered_2['day_of_week_numeric'].unique(), ''),
    create_section("Attendance in every hour by gender", 'dropdown_3', 'fig_3', df_filtered_2['customer_gender'].unique(), ''),
    create_section("Attendance per day", 'dropdown_4', 'fig_4', df_filtered_2['day_of_week_numeric'].unique(), ''),

], style={'backgroundColor': dark_theme['background'], 'padding': '20px', 'margin': '0px'})

# Función para aplicar el tema oscuro a las gráficas
def apply_dark_theme(fig):
    fig.update_layout(
        plot_bgcolor=dark_theme['background'],
        paper_bgcolor=dark_theme['paper'],
        font_color=dark_theme['text'],
        margin=dict(l=10, r=10, t=30, b=10)
    )
    fig.update_xaxes(gridcolor=dark_theme['grid'], zeroline=False)
    fig.update_yaxes(gridcolor=dark_theme['grid'], zeroline=False)
    return fig

# Callbacks (sin cambios)
@app.callback(
    Output('fig_1', 'figure'),
    Input('dropdown_1', 'value')
)
def update_graph_residency_flag_by_permit_year(selected_month):
    filtered_df = df_filtered_1[df_filtered_1['event_start_mounth_numeric'] == selected_month]
    fig = px.bar(filtered_df, x="residency_flag")
    return apply_dark_theme(fig)

@app.callback(
    Output('fig_2', 'figure'),
    Input('dropdown_2', 'value')
)
def update_graph_transaction_site_by_day(selected_day):   
    filtered_df = df_filtered_1[df_filtered_1['day_of_week_numeric'] == selected_day]
    fig = px.pie(filtered_df, values=df_filtered_1['transaction_site'].value_counts(), names=df_filtered_1['transaction_site'].unique())
    return apply_dark_theme(fig)

@app.callback(
    Output('fig_3', 'figure'),
    Input('dropdown_3', 'value')
)
def update_graph_hours_reserved_by_year(selected_gender):
    filtered_df = df_filtered_2[df_filtered_2['customer_gender'] == selected_gender]
    fig = px.line(filtered_df, x="day_of_week_numeric", y="attendance", color="customer_gender")
    return apply_dark_theme(fig)

@app.callback(
    Output('fig_4', 'figure'),
    Input('dropdown_4', 'value')
)
def update_graph_attendance_per_day(selected_day_of_week):
    filtered_df = df_filtered_2[df_filtered_2['day_of_week'] == selected_day_of_week]
    fig = px.violin(filtered_df, x='mes', y='attendance')
    return apply_dark_theme(fig)


if __name__ == '__main__':
    app.run_server(debug=True)
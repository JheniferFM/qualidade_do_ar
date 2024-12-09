import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

# Carregar os dados CSV
arquivo = 'qualidade_do_ar_brasil_capitais.csv'
df = pd.read_csv(arquivo)

# Iniciar o aplicativo Dash
app = dash.Dash(__name__)

# Layout da aplicação Dash
app.layout = html.Div([
    html.H1('Qualidade do Ar nas Capitais do Brasil', style={'text-align': 'center'}),

    dcc.Dropdown(
        id='capital-dropdown',
        options=[{'label': capital, 'value': capital} for capital in df['Capital'].unique()],
        value=df['Capital'].iloc[0],  # Capital padrão selecionada
        style={'width': '50%', 'margin': 'auto'}
    ),
    
    dcc.Graph(id='grafico-air-quality'),
])

# Função de callback para atualizar o gráfico com base na capital selecionada
@app.callback(
    dash.dependencies.Output('grafico-air-quality', 'figure'),
    [dash.dependencies.Input('capital-dropdown', 'value')]
)
def update_graph(selected_capital):
    # Filtrar o dataframe pela capital selecionada
    df_filtered = df[df['Capital'] == selected_capital]
    
    # Criar o gráfico (aqui, usando um gráfico de barras como exemplo)
    fig = px.bar(df_filtered, x='Poluente', y='Valor', title=f'Qualidade do Ar em {selected_capital}',
                 labels={'Poluente': 'Poluente', 'Valor': 'Concentração (µg/m³)'})
    
    return fig

# Rodar o aplicativo Dash
if __name__ == '__main__':
    app.run_server(debug=True)

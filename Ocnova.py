import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Загрузка данных
df = pd.read_csv(r'C:\Users\xolox\PycharmProjects\pythonProject\csvdash.csv')

# Создание экземпляра приложения
app = dash.Dash(__name__)

# Определение структуры дашборда
app.layout = html.Div([
    html.Div([
        html.H1('Дашборд  для анализа финансовых данных', style={'textAlign': 'center'}),
        html.P('Этот дашборд предоставляет аналитику ваших финансовых данных.',
               style={'textAlign': 'center'}),
        html.Div([
            html.Label('Выберите дату:', style={'fontSize': 18}),
            dcc.Dropdown(
                id='date-dropdown',
                options=[{'label': date, 'value': date} for date in df['Дата']],
                value=df['Дата'].iloc[0],
                clearable=False,
                style={'width': '50%', 'margin': '0 auto'}
            ),
        ], style={'textAlign': 'center', 'marginBottom': '30px'}),
    ], style={'marginBottom': '30px'}),

    #---------------------------!!!!!!!!!!!!!!!
    #НАШ ГРАФИК
    #---------------------------!!!!!!!!!!!!!!!

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
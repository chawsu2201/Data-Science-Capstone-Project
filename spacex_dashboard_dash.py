# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[{'label': 'ALL SITES', 'value': 'ALL'}] + 
                                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                value='ALL',
                                placeholder='Select Launch Site',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks= {i: str(i) for i in range(0,10001, 1000)},
                                value= [0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart', 'figure'), Input('site-dropdown', 'value'))
def update_pie_chart(selected_site):
    filtered_df = spacex_df
    if selected_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names= 'Launch Site',
        title='Success Rate for all Launch Site')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        filtered_df = filtered_df['class'].replace({1:'Success', 0:'Failure'})
        fig = px.pie(filtered_df,
        names= 'class',
        color='class',
        color_discrete_map={'Success':'blue', 'Failure':'red'},
        title=f'Success Rate for Launch Site: {selected_site}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( 
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), 
    Input('payload-slider', 'value')]
)
def update_scatter_plot(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
    (spacex_df['Payload Mass (kg)'] <= high)]
    if selected_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
        color= 'Booster Version Category',
        title='Correlation of Payload and Mission Outcome at all Launch Site')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
        color= 'Booster Version Category',
        title=f'Correlation of Payload and Mission Outcome at {selected_site}')
        return fig


# Run the app
if __name__ == '__main__':
    app.run()



# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
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
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id = 'site-dropdown', options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'Site1', 'value': 'CCAFS LC-40'},
                                    {'label': 'Site2', 'value': 'KSC LC-39A'},
                                    {'label': 'Site3', 'value' : 'CCAFS SLC-40'}
                                ],
                                             value='ALL',
                                             placeholder = 'Choose a launch site',
                                             searchable = True # Providing a value to dropdown
                                            ),
                            

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Label("Select Payload Range:"),
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=min_payload,
                                    max=max_payload,
                                    step=1000,
                                    marks={0: '0', 100: '100'},
                                    value=[min_payload, max_payload]
                                ),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'))
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # If ALL sites are selected, use all rows in the dataframe to render a pie chart
        fig = px.pie(spacex_df, names='class', title='Total Success Launches',
                     labels={'class': 'Mission Outcome'})
    else:
        # If a specific launch site is selected, filter the dataframe to include only data for that site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Render a pie chart to show success (class=1) and failed (class=0) count for the selected site
        fig = px.pie(filtered_df, names='class', title=f'Success vs. Failed for {selected_site}',
                     labels={'class': 'Mission Outcome'})

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
[Input(component_id='site-dropdown',component_property='value'), 
Input(component_id='payload-slider',component_property='value')])
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        # If ALL sites are selected, use all rows in the dataframe to render a scatter plot
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class',
                         color='class', title='Payload vs. Launch Outcome (All Sites)',
                         labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Mission Outcome'},
                         hover_data=['class'])
    else:
        # If a specific launch site is selected, filter the dataframe to include only data for that site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Render a scatter chart to show payload vs. launch outcome for the selected site
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='class', title=f'Payload vs. Launch Outcome ({selected_site})',
                         labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'Mission Outcome'},
                         hover_data=['class'])

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

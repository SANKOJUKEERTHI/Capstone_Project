
# Import required libraries
import pandas as pd
import dash
#import dash_html_components as html
from dash import html
from dash import dcc
#import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
#print(spacex_df.dtypes)
#spacex_df['Launch Site'] = spacex_df['Launch Site'].str.strip()
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
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {"label": "All Sites", "value": "All Sites"},
                                    {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                                    {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
                                    {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                                    {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
                                ],
                                value='All Sites',
                                placeholder="Launch Site",
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,marks={0 : '0',1000:'1000',2000:'2000',3000:'3000',4000:'4000',5000:'5000',6000:'6000',7000:'7000',8000:'8000',9000:'9000',10000:'10000'},value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown',component_property='value'))
def get_pie(entered_site):
    df = spacex_df
    if entered_site=='All Sites':
        # All sites selected
        total_success = df['class'].sum()
        m,n = df.shape
        fig = px.pie(df,values=[total_success, m - total_success],
                     names=['Success', 'Failed'],
                     title='Total Success Launches')
        return fig
    else:
        # Specific launch site selected
        site_df = df[df['Launch Site'] == entered_site]
        print(site_df.head())
        success_count = site_df[site_df['class'] == 1]['class'].count()
        failed_count = site_df[site_df['class'] == 0]['class'].count()
        fig = px.pie(site_df,values=[success_count,failed_count],
                     names=['Success', 'Failed'],
                     title=f'Success and Failed Launches - {entered_site}')

        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
[Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])
def update_scatter_chart(entered_site, payload_range):
    df = spacex_df
    if entered_site == 'All Sites':
        # All sites selected
        fig = px.scatter(df[(df['Payload Mass (kg)'] >= payload_range[0]) & (df['Payload Mass (kg)'] <= payload_range[1])],
                         x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Payload Mass vs. Launch Outcome (All Sites)')
        return fig
    else:
        # Specific launch site selected
        site_df = df[df['Launch Site'] == entered_site]
        filtered_site_df = site_df[
        (site_df['Payload Mass (kg)'] >= payload_range[0]) &
        (site_df['Payload Mass (kg)'] <= payload_range[1])
        ]

        fig = px.scatter(filtered_site_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                 title=f'Payload Mass vs. Launch Outcome - {entered_site}')

        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
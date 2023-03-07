# Plotly Dash App for Analysis of Traffic on an Enterprise Network

from dash import Dash, dcc, Output, Input  # pip install dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd  # pip install pandas
import dash_daq as daq # pip install dash_daq
import math

DEBUG = False

# region Section_Dataframes

# Dataset of subnets' outgoing connections with all the rankings for different variables.
df_subs_out = pd.read_csv("input_type_1/subnets_outgoing.csv")
# Dataset of subnets' incoming connections with all the rankings for different variables.
df_subs_in = pd.read_csv("input_type_2/subnets_incoming.csv")
# Dataset of outgoing connections from all active IPs of all subnets.
df_subs_out_dep = pd.read_csv("input_type_3/sourceIPs_outgoing.csv")
# Dataset of incoming connections from all active IPs of all subnets.
df_subs_in_dep = pd.read_csv("input_type_4/targetIPs_incoming.csv")
# endregion

# region Section_Components

# Choosing the theme of the app.
app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])

# Graphs for outgoing connections
title_subs_out = dcc.Markdown(children='## Source Subnets on Outgoing Connections - ')
graph_subs_out = dcc.Graph(figure={})
text_dropdown_subs_out = dcc.Markdown(children='###### Choose graph type:')
dropdown_subs_out = dcc.Dropdown(options=['Total Bytes', 'Inbound', 'Outbound', 'Difference', 'Connections',
                                          'Source IPs', 'Target IPs', 'Source Ports', 'Target Ports'],
                                 value='Total Bytes',  # initial value displayed when page first loads
                                 clearable=False)
text_dropdown_subs_out_sort = dcc.Markdown(children='###### Choose sort type:')
dropdown_subs_out_sort = dcc.Dropdown(options=['Source Subnets', 'Total Bytes', 'Inbound', 'Outbound', 'Connections',
                                               'Source IPs', 'Target IPs', 'Source Ports', 'Target Ports'],
                                      value='Source Subnets',  # initial value displayed when page first loads
                                      clearable=False)
text_choice_subs_out = dcc.Markdown(children='###### Number of tops to see:')
choice_subs_out = daq.NumericInput(min=1, max=257, value=257)

depGraph_subs_out = dcc.Graph(figure={})
depTitle_subs_out = dcc.Markdown(children='#### Distribution of the Selected Subnet in Outgoing Connections - ')

# Graphs for incoming connections
title_subs_in = dcc.Markdown(children='## Target Subnets on Incoming Connections - ')
graph_subs_in = dcc.Graph(figure={})
text_dropdown_subs_in = dcc.Markdown(children='###### Choose graph type:')
dropdown_subs_in = dcc.Dropdown(options=['Total Bytes', 'Inbound', 'Outbound', 'Difference', 'Connections',
                                         'Source IPs', 'Target IPs', 'Source Ports', 'Target Ports'],
                                value='Total Bytes',  # initial value displayed when page first loads
                                clearable=False)
text_dropdown_subs_in_sort = dcc.Markdown(children='###### Choose sort type:')
dropdown_subs_in_sort = dcc.Dropdown(options=['Target Subnets', 'Total Bytes', 'Inbound', 'Outbound', 'Connections',
                                              'Source IPs', 'Target IPs', 'Source Ports', 'Target Ports'],
                                     value='Target Subnets',  # initial value displayed when page first loads
                                     clearable=False)
text_choice_subs_in = dcc.Markdown(children='###### Number of tops to see:')
choice_subs_in = daq.NumericInput(min=1, max=257, value=257)

depGraph_subs_in = dcc.Graph(figure={})
depTitle_subs_in = dcc.Markdown(children='#### Distribution of the Selected Subnet in Incoming Connections - ')

# Graphs for groups - outgoing connections
title_groups_out = dcc.Markdown(children='## Outgoing Connections from Subnet Groups - ')
graph_groups_out_conns = dcc.Graph(figure={})
graph_groups_out_bytes = dcc.Graph(figure={})
graph_groups_out_inout = dcc.Graph(figure={})
graph_groups_out_asym = dcc.Graph(figure={})
dropdown_groups_out = dcc.Dropdown(
    options=['WiFi', 'WLAN', 'Services', 'VPN', 'Science', 'Schulich', 'Medical', 'Arts', 'CPSC', 'PHAS', 'Reznet',
             'Admin'],
    value='WiFi',  # initial value displayed when page first loads
    clearable=False)

# Graphs for groups - incoming connections
title_groups_in = dcc.Markdown(children='## Incoming Connections to Subnet Groups - ')
graph_groups_in_conns = dcc.Graph(figure={})
graph_groups_in_bytes = dcc.Graph(figure={})
graph_groups_in_inout = dcc.Graph(figure={})
graph_groups_in_asym = dcc.Graph(figure={})
dropdown_groups_in = dcc.Dropdown(
    options=['WiFi', 'WLAN', 'Services', 'VPN', 'Science', 'Schulich', 'Medical', 'Arts', 'CPSC', 'PHAS', 'Reznet',
             'Admin'],
    value='WiFi',  # initial value displayed when page first loads
    clearable=False)

# Graphs for orgs - outgoing connections
title_orgs_out = dcc.Markdown(children='## External Targets of the Outgoing Connections from Groups - ')
graph_orgs_out_conns = dcc.Graph(figure={})
graph_orgs_out_bytes = dcc.Graph(figure={})
graph_orgs_out_src_ips = dcc.Graph(figure={})
graph_orgs_out_trg_ips = dcc.Graph(figure={})
graph_orgs_out_src_ports = dcc.Graph(figure={})
graph_orgs_out_trg_ports = dcc.Graph(figure={})
dropdown_orgs_out = dcc.Dropdown(
    options=['WiFi', 'WLAN', 'Services', 'VPN', 'Science', 'Schulich', 'Medical', 'Arts', 'CPSC', 'PHAS', 'Reznet',
             'Admin'],
    value='WiFi',  # initial value displayed when page first loads
    clearable=False)

# Graphs for orgs - incoming connections
title_orgs_in = dcc.Markdown(children='## External Sources of the Incoming Connections to Groups - ')
graph_orgs_in_conns = dcc.Graph(figure={})
graph_orgs_in_bytes = dcc.Graph(figure={})
graph_orgs_in_src_ips = dcc.Graph(figure={})
graph_orgs_in_trg_ips = dcc.Graph(figure={})
graph_orgs_in_src_ports = dcc.Graph(figure={})
graph_orgs_in_trg_ports = dcc.Graph(figure={})
dropdown_orgs_in = dcc.Dropdown(
    options=['WiFi', 'WLAN', 'Services', 'VPN', 'Science', 'Schulich', 'Medical', 'Arts', 'CPSC', 'PHAS', 'Reznet',
             'Admin'],
    value='Services',  # initial value displayed when page first loads
    clearable=False)
# endregion

# region Section_Layout

# Designing the app's layout. The placing and sizes of all components are specified here.
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([dcc.Markdown('# ** Plotly Dash **')], style={"color": "white"}, width=2)
    ], style={"background-color": "#003060"}, justify='center'),

    dbc.Row([
        dbc.Col([dcc.Markdown('### ** A Subnet Analysis on UCalgary\'s Campus Network **')], style={"color": "white"},
                width=5)], style={"background-color": "#003060"}, justify='center'),

    dbc.Row([dbc.Col([dcc.Markdown('&nbsp;')])]),

    # Section layout for outgoing connections
    dbc.Row([
        dbc.Col([title_subs_out], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([text_dropdown_subs_out], width=3),
        dbc.Col([text_dropdown_subs_out_sort], width=3),
        dbc.Col([text_choice_subs_out], width=2)
    ], justify='center'),
    dbc.Row([
        dbc.Col([dropdown_subs_out], width=3),
        dbc.Col([dropdown_subs_out_sort], width=3),
        dbc.Col([choice_subs_out], width=2)
    ], justify='center'),
    dbc.Row([
        dbc.Col([graph_subs_out], width=12)
    ]),

    dbc.Row([dbc.Col([depTitle_subs_out], width=7)], justify='center'),
    dbc.Row([dbc.Col([depGraph_subs_out], width=12)]),

    # Divider
    dbc.Row([dbc.Col([dcc.Markdown('&nbsp;')])]),
    dbc.Row([dbc.Col([dcc.Markdown('---')])]),

    # Section layout for incoming connections
    dbc.Row([
        dbc.Col([title_subs_in], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([text_dropdown_subs_in], width=3),
        dbc.Col([text_dropdown_subs_in_sort], width=3),
        dbc.Col([text_choice_subs_in], width=2)
    ], justify='center'),
    dbc.Row([
        dbc.Col([dropdown_subs_in], width=3),
        dbc.Col([dropdown_subs_in_sort], width=3),
        dbc.Col([choice_subs_in], width=2)
    ], justify='center'),
    dbc.Row([
        dbc.Col([graph_subs_in], width=12)
    ]),

    dbc.Row([dbc.Col([dcc.Markdown('## __')])]),
    dbc.Row([dbc.Col([depTitle_subs_in], width=7)], justify='center'),
    dbc.Row([dbc.Col([depGraph_subs_in], width=12)]),

    # Divider
    dbc.Row([dbc.Col([dcc.Markdown('&nbsp;')])]),
    dbc.Row([dbc.Col([dcc.Markdown('---')])]),

    # Section layout for groups - outgoing connections
    dbc.Row([
        dbc.Col([title_groups_out], width=5)
    ], justify='center'),
    dbc.Row([
        dbc.Col([dropdown_groups_out], width=3),
    ], justify='center'),
    dbc.Row([
        dbc.Col([graph_groups_out_conns], width=3),
        dbc.Col([graph_groups_out_bytes], width=3),
        dbc.Col([graph_groups_out_inout], width=3),
        dbc.Col([graph_groups_out_asym], width=3),
    ]),

    # Divider
    dbc.Row([dbc.Col([dcc.Markdown('&nbsp;')])]),
    dbc.Row([dbc.Col([dcc.Markdown('---')])]),

    # Section layout for groups - incoming connections
    dbc.Row([
        dbc.Col([title_groups_in], width=5)
    ], justify='center'),
    dbc.Row([
        dbc.Col([dropdown_groups_in], width=3),
    ], justify='center'),
    dbc.Row([
        dbc.Col([graph_groups_in_conns], width=3),
        dbc.Col([graph_groups_in_bytes], width=3),
        dbc.Col([graph_groups_in_inout], width=3),
        dbc.Col([graph_groups_in_asym], width=3),
    ]),

    # Divider
    dbc.Row([dbc.Col([dcc.Markdown('&nbsp;')])]),
    dbc.Row([dbc.Col([dcc.Markdown('---')])]),

    # Section layout for orgs - outgoing connections
    dbc.Row([
        dbc.Col([title_orgs_out], width=7)
    ], justify='center'),
    dbc.Row([
        dbc.Col([dropdown_orgs_out], width=3),
    ], justify='center'),
    dbc.Row([
        dbc.Col([graph_orgs_out_conns], width=5),
        dbc.Col([graph_orgs_out_bytes], width=7),
    ]),
    dbc.Row([
        dbc.Col([graph_orgs_out_src_ips], width=5),
        dbc.Col([graph_orgs_out_trg_ips], width=7),
    ]),
    dbc.Row([
        dbc.Col([graph_orgs_out_src_ports], width=5),
        dbc.Col([graph_orgs_out_trg_ports], width=7),
    ]),

    # Divider
    dbc.Row([dbc.Col([dcc.Markdown('&nbsp;')])]),
    dbc.Row([dbc.Col([dcc.Markdown('---')])]),

    # Section layout for orgs - incoming connections
    dbc.Row([
        dbc.Col([title_orgs_in], width=7)
    ], justify='center'),
    dbc.Row([
        dbc.Col([dropdown_orgs_in], width=3),
    ], justify='center'),
    dbc.Row([
        dbc.Col([graph_orgs_in_conns], width=5),
        dbc.Col([graph_orgs_in_bytes], width=7),
    ]),
    dbc.Row([
        dbc.Col([graph_orgs_in_src_ips], width=5),
        dbc.Col([graph_orgs_in_trg_ips], width=7),
    ]),
    dbc.Row([
        dbc.Col([graph_orgs_in_src_ports], width=5),
        dbc.Col([graph_orgs_in_trg_ports], width=7),
    ]),

    dbc.Row([dbc.Col([dcc.Markdown('&nbsp;')])], style={"background-color": "#003060"}),

    dbc.Row([
        dbc.Col([dcc.Markdown('###### This app is developed to support the research presented in the Chapter 5 of the '
                              'PhD dissertation of ** Mehdi Karamollahi ** at the Department of Computer Science, University'
                              ' of Calgary.')], style={"color": "#dddddd"}, width=9)
    ], style={"background-color": "#003060"}, justify='center'),

    dbc.Row([
        dbc.Col([dcc.Markdown('###### January 2023')], style={"color": "#aaaaaa"}, width=1)
    ], style={"background-color": "#003060"}, justify='center'),

    dbc.Row([dbc.Col([dcc.Markdown('&nbsp;')])], style={"background-color": "#003060"}),

], fluid=True)
# endregion


# region Section_Callbacks_1

# The callback specifies all the inputs and outputs of the function that is defined right below it. Both graphs for
# subnets (outgoing and incoming connections), the 12 campus groups (4 graphs for outgoing connections and 4 for
# incoming), and the top 10 organizations (6 graphs for outgoing connections and 6 for incoming) are defined here.
@app.callback(
    # subnets: graph for outgoing connections
    Output(graph_subs_out, 'figure'),
    # subnets: title of graph for outgoing connections
    Output(title_subs_out, 'children'),
    # subnets: graph for incoming connections
    Output(graph_subs_in, 'figure'),
    # subnets: title of graph for incoming connections
    Output(title_subs_in, 'children'),
    # groups - outgoing connections: graph for total connections
    Output(graph_groups_out_conns, 'figure'),
    # groups - outgoing connections: graph for total bytes
    Output(graph_groups_out_bytes, 'figure'),
    # groups - outgoing connections: graph for inbound/outbound traffic
    Output(graph_groups_out_inout, 'figure'),
    # groups - outgoing connections: graph for the asymmetry in traffic
    Output(graph_groups_out_asym, 'figure'),
    # groups - outgoing connections: title for the four graphs
    Output(title_groups_out, 'children'),
    # groups - incoming connections: graph for total connections
    Output(graph_groups_in_conns, 'figure'),
    # groups - incoming connections: graph for total bytes
    Output(graph_groups_in_bytes, 'figure'),
    # groups - incoming connections: graph for inbound/outbound traffic
    Output(graph_groups_in_inout, 'figure'),
    # groups - incoming connections: graph for the asymmetry in traffic
    Output(graph_groups_in_asym, 'figure'),
    # groups - incoming connections: title for the four graphs
    Output(title_groups_in, 'children'),
    # Top 10 orgs - outgoing connections: graph for total connections
    Output(graph_orgs_out_conns, 'figure'),
    # Top 10 orgs - outgoing connections: graph for total bytes
    Output(graph_orgs_out_bytes, 'figure'),
    # Top 10 orgs - outgoing connections: graph for number of source IPs
    Output(graph_orgs_out_src_ips, 'figure'),
    # Top 10 orgs - outgoing connections: graph for number of target IPs
    Output(graph_orgs_out_trg_ips, 'figure'),
    # Top 10 orgs - outgoing connections: graph for number of source ports
    Output(graph_orgs_out_src_ports, 'figure'),
    # Top 10 orgs - outgoing connections: graph for number of target ports
    Output(graph_orgs_out_trg_ports, 'figure'),
    # Top 10 orgs - outgoing connections: title of all 6 graphs
    Output(title_orgs_out, 'children'),
    # Top 10 orgs - incoming connections: graph for total connections
    Output(graph_orgs_in_conns, 'figure'),
    # Top 10 orgs - incoming connections: graph for total bytes
    Output(graph_orgs_in_bytes, 'figure'),
    # Top 10 orgs - incoming connections: graph for number of source IPs
    Output(graph_orgs_in_src_ips, 'figure'),
    # Top 10 orgs - incoming connections: graph for number of target IPs
    Output(graph_orgs_in_trg_ips, 'figure'),
    # Top 10 orgs - incoming connections: graph for number of source ports
    Output(graph_orgs_in_src_ports, 'figure'),
    # Top 10 orgs - incoming connections: graph for number of target ports
    Output(graph_orgs_in_trg_ports, 'figure'),
    # Top 10 orgs - incoming connections: title of all 6 graphs
    Output(title_orgs_in, 'children'),
    # subnets - outgoing connections: dropdown option to choose graph type
    Input(dropdown_subs_out, 'value'),
    # subnets - outgoing connections: dropdown option to choose sort type
    Input(dropdown_subs_out_sort, 'value'),
    # subnets - outgoing connections: numeric option to choose among the top subnets based on sort option
    Input(choice_subs_out, 'value'),
    # subnets - incoming connections: dropdown option to choose graph type
    Input(dropdown_subs_in, 'value'),
    # subnets - incoming connections: dropdown option to choose sort type
    Input(dropdown_subs_in_sort, 'value'),
    # subnets - incoming connections: numeric option to choose among the top subnets based on sort option
    Input(choice_subs_in, 'value'),
    # groups - outgoing connections: dropdown option to choose the campus group
    Input(dropdown_groups_out, 'value'),
    # groups - incoming connections: dropdown option to choose the campus group
    Input(dropdown_groups_in, 'value'),
    # Top 10 orgs - outgoing connections: dropdown option to choose the campus group
    Input(dropdown_orgs_out, 'value'),
    # Top 10 orgs - incoming connections: dropdown option to choose the campus group
    Input(dropdown_orgs_in, 'value'),
)
# endregion
# function arguments come from the component property of the Input.
def update_graph(type_graph_subs_out, type_sort_subs_out, top_picks_subs_out, type_graph_subs_in, type_sort_subs_in,
                 top_picks_subs_in, type_graph_groups_out, type_graph_groups_in, type_graph_orgs_out,
                 type_graph_orgs_in):
    # Calling the rank_field function (defined at the bottom) to map the sort types to the appropriate columns in
    # the DataFrames.
    rankChoice_out = rank_field(type_sort_subs_out)
    rankChoice_in = rank_field(type_sort_subs_in)

    # Calling the rank_title function (defined at the bottom) to choose the appropriate axis titles for the sort types.
    rankTitle_out = rank_title(type_sort_subs_out)
    rankTitle_in = rank_title(type_sort_subs_in)

    # ==================================================================================================================

    if DEBUG: print("=================== subnets graphs - outgoing ===================")
    if DEBUG: print("<type_graph_subs_out>: ", type_graph_subs_out)
    if DEBUG: print("<type_sort_subs_out>: ", type_sort_subs_out)
    if DEBUG: print("<top_picks_subs_out>: ", top_picks_subs_out)
    if DEBUG: print("<rankChoice_out>: ", rankChoice_out)
    if DEBUG: print("<rankTitle_out>: ", rankTitle_out)

    # region Section_Subs_Out

    if type_graph_subs_out == "Connections":
        new_df_subs_out = df_subs_out.drop(df_subs_out[df_subs_out.Rank_Conns > int(top_picks_subs_out)].index)

        min_Conns = new_df_subs_out["Connections"].min()
        max_Conns = new_df_subs_out["Connections"].max()

        fig_subs_out = px.bar(data_frame=new_df_subs_out, x=rankChoice_out, y="Connections", range_x=[0, 256],
                              range_y=[min_Conns, max_Conns], height=500, animation_frame='Week', log_y=True,
                              hover_data=["Week"], text="SourceSubnet")
        fig_subs_out.update_xaxes(title=rankTitle_out)

    elif type_graph_subs_out == "Total Bytes":
        new_df_subs_out = df_subs_out.drop(df_subs_out[df_subs_out.Rank_Bytes > int(top_picks_subs_out)].index)

        min_TotalBytes = new_df_subs_out["TotalBytes"].min()
        max_TotalBytes = new_df_subs_out["TotalBytes"].max()

        fig_subs_out = px.bar(data_frame=new_df_subs_out, x=rankChoice_out, y="TotalBytes", range_x=[0, 256],
                              range_y=[min_TotalBytes, max_TotalBytes], height=500, animation_frame='Week', log_y=True,
                              hover_data=["Week"], text="SourceSubnet")
        fig_subs_out.update_xaxes(title=rankTitle_out)
        fig_subs_out.update_yaxes(title="Total Bytes")

    elif type_graph_subs_out == "Inbound":
        new_df_subs_out = df_subs_out.drop(df_subs_out[df_subs_out.Rank_In > int(top_picks_subs_out)].index)

        min_Inbound = new_df_subs_out["Inbound"].min()
        max_Inbound = new_df_subs_out["Inbound"].max()

        fig_subs_out = px.bar(data_frame=new_df_subs_out, x=rankChoice_out, y="Inbound", range_x=[0, 256],
                              range_y=[min_Inbound, max_Inbound], height=500, animation_frame='Week', log_y=True,
                              hover_data=["Week"], text="SourceSubnet")
        fig_subs_out.update_xaxes(title=rankTitle_out)
        fig_subs_out.update_yaxes(title="Inbound Bytes")

    elif type_graph_subs_out == "Outbound":
        new_df_subs_out = df_subs_out.drop(df_subs_out[df_subs_out.Rank_Out > int(top_picks_subs_out)].index)

        min_Outbound = new_df_subs_out["Outbound"].min()
        max_Outbound = new_df_subs_out["Outbound"].max()

        fig_subs_out = px.bar(data_frame=new_df_subs_out, x=rankChoice_out, y="Outbound", range_x=[0, 256],
                              range_y=[min_Outbound, max_Outbound], height=500, animation_frame='Week', log_y=True,
                              hover_data=["Week"], text="SourceSubnet")
        fig_subs_out.update_xaxes(title=rankTitle_out)
        fig_subs_out.update_yaxes(title="Outbound Bytes")

    elif type_graph_subs_out == "Difference":
        new_df_subs_out = df_subs_out.drop(df_subs_out[df_subs_out.Rank_Bytes > int(top_picks_subs_out)].index)

        min_Diff = new_df_subs_out["Difference"].min()
        max_Diff = new_df_subs_out["Difference"].max()

        fig_subs_out = px.bar(data_frame=new_df_subs_out, x=rankChoice_out, y="Difference", range_x=[0, 256],
                              range_y=[min_Diff, max_Diff], height=500, animation_frame='Week', log_y=True,
                              color="Color", color_discrete_map={"In > Out": "blue", "Out > In": "red"},
                              hover_data=["Week"], text="SourceSubnet")
        fig_subs_out.update_xaxes(title=rankTitle_out)
        fig_subs_out.update_yaxes(title="Difference Between Inbound and Outbound")

    elif type_graph_subs_out == "Source IPs":
        new_df_subs_out = df_subs_out.drop(df_subs_out[df_subs_out.Rank_Sources > int(top_picks_subs_out)].index)

        min_SourceIPs = new_df_subs_out["SourceIPs"].min()
        max_SourceIPs = new_df_subs_out["SourceIPs"].max()

        fig_subs_out = px.bar(data_frame=new_df_subs_out, x=rankChoice_out, y="SourceIPs", range_x=[0, 256],
                              range_y=[min_SourceIPs, max_SourceIPs], height=500, animation_frame='Week',
                              hover_data=["Week"], text="SourceSubnet")
        fig_subs_out.update_xaxes(title=rankTitle_out)
        fig_subs_out.update_yaxes(title="Number of Distinct Source IPs")

    elif type_graph_subs_out == "Target IPs":
        new_df_subs_out = df_subs_out.drop(df_subs_out[df_subs_out.Rank_Targets > int(top_picks_subs_out)].index)

        min_TargetIPs = new_df_subs_out["TargetIPs"].min()
        max_TargetIPs = new_df_subs_out["TargetIPs"].max()

        fig_subs_out = px.bar(data_frame=new_df_subs_out, x=rankChoice_out, y="TargetIPs", range_x=[0, 256],
                              range_y=[min_TargetIPs, max_TargetIPs], height=500, animation_frame='Week',
                              hover_data=["Week"], text="SourceSubnet")
        fig_subs_out.update_xaxes(title=rankTitle_out)
        fig_subs_out.update_yaxes(title="Number of Distinct Target IPs")

    elif type_graph_subs_out == "Source Ports":
        new_df_subs_out = df_subs_out.drop(df_subs_out[df_subs_out.Rank_SrcPorts > int(top_picks_subs_out)].index)

        min_SourcePorts = new_df_subs_out["SourcePorts"].min()
        max_SourcePorts = new_df_subs_out["SourcePorts"].max()

        fig_subs_out = px.bar(data_frame=new_df_subs_out, x=rankChoice_out, y="SourcePorts", range_x=[0, 256],
                              range_y=[min_SourcePorts, max_SourcePorts], height=500, animation_frame='Week',
                              hover_data=["Week"], text="SourceSubnet")
        fig_subs_out.update_xaxes(title=rankTitle_out)
        fig_subs_out.update_yaxes(title="Number of Distinct Source Ports")

    elif type_graph_subs_out == "Target Ports":
        new_df_subs_out = df_subs_out.drop(df_subs_out[df_subs_out.Rank_TrgPorts > int(top_picks_subs_out)].index)

        min_TargetPorts = new_df_subs_out["TargetPorts"].min()
        max_TargetPorts = new_df_subs_out["TargetPorts"].max()

        fig_subs_out = px.bar(data_frame=new_df_subs_out, x=rankChoice_out, y="TargetPorts", range_x=[0, 256],
                              range_y=[min_TargetPorts, max_TargetPorts], height=500, animation_frame='Week',
                              hover_data=["Week"], text="SourceSubnet")
        fig_subs_out.update_xaxes(title=rankTitle_out)
        fig_subs_out.update_yaxes(title="Number of Distinct Target Ports")

    else:
        new_df_subs_out = df_subs_out.drop(df_subs_out[df_subs_out.Rank_Bytes > int(top_picks_subs_out)].index)

        fig_subs_out = px.bar(data_frame=new_df_subs_out, x=rankChoice_out, y=type_graph_subs_out, height=500,
                              range_x=[1, 257],
                              animation_frame='Week', hover_data=["Week"], text="SourceSubnet")
        fig_subs_out.update_xaxes(title=rankTitle_out)

    fig_subs_out.update_xaxes(range=[0, 256], autorange=False)
    fig_subs_out.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 800
    fig_subs_out.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
    fig_subs_out.update_traces(width=1, textangle=0, textposition='outside')
    # endregion

    # ==================================================================================================================

    # region Section_Subs_In

    if DEBUG: print("=================== subnets graphs - incoming ===================")
    if DEBUG: print("<type_graph_subs_in>: ", type_graph_subs_in)
    if DEBUG: print("<type_sort_subs_in>: ", type_sort_subs_in)
    if DEBUG: print("<top_picks_subs_in>: ", top_picks_subs_in)
    if DEBUG: print("<rankChoice_in>: ", rankChoice_in)
    if DEBUG: print("<rankTitle_in>: ", rankTitle_in)

    if type_graph_subs_in == "Connections":
        new_df_subs_in = df_subs_in.drop(df_subs_in[df_subs_in.Rank_Conns > int(top_picks_subs_in)].index)

        min_Conns = new_df_subs_in["Connections"].min()
        max_Conns = new_df_subs_in["Connections"].max()
        fig_subs_in = px.bar(data_frame=new_df_subs_in, x=rankChoice_in, y="Connections", range_x=[0, 256],
                             range_y=[min_Conns, max_Conns], height=500, animation_frame='Week', log_y=True,
                             hover_data=["Week", "TargetSubnet"], text="TargetSubnet")
        fig_subs_in.update_xaxes(title=rankTitle_in)

    elif type_graph_subs_in == "Total Bytes":
        new_df_subs_in = df_subs_in.drop(df_subs_in[df_subs_in.Rank_Bytes > int(top_picks_subs_in)].index)

        min_TotalBytes = new_df_subs_in["TotalBytes"].min()
        max_TotalBytes = new_df_subs_in["TotalBytes"].max()
        fig_subs_in = px.bar(data_frame=new_df_subs_in, x=rankChoice_in, y="TotalBytes", range_x=[0, 256],
                             range_y=[min_TotalBytes, max_TotalBytes], height=500, animation_frame='Week', log_y=True,
                             hover_data=["Week", "TargetSubnet"], text="TargetSubnet")
        fig_subs_in.update_xaxes(title=rankTitle_in)
        fig_subs_in.update_yaxes(title="Total Bytes")

    elif type_graph_subs_in == "Inbound":
        new_df_subs_in = df_subs_in.drop(df_subs_in[df_subs_in.Rank_In > int(top_picks_subs_in)].index)

        min_Inbound = new_df_subs_in["Inbound"].min()
        max_Inbound = new_df_subs_in["Inbound"].max()
        fig_subs_in = px.bar(data_frame=new_df_subs_in, x=rankChoice_in, y="Inbound", range_x=[0, 256],
                             range_y=[min_Inbound, max_Inbound], height=500, animation_frame='Week', log_y=True,
                             hover_data=["Week", "TargetSubnet"], text="TargetSubnet")
        fig_subs_in.update_xaxes(title=rankTitle_in)
        fig_subs_in.update_yaxes(title="Inbound Bytes")

    elif type_graph_subs_in == "Outbound":
        new_df_subs_in = df_subs_in.drop(df_subs_in[df_subs_in.Rank_Out > int(top_picks_subs_in)].index)

        min_Outbound = new_df_subs_in["Outbound"].min()
        max_Outbound = new_df_subs_in["Outbound"].max()
        fig_subs_in = px.bar(data_frame=new_df_subs_in, x=rankChoice_in, y="Outbound", range_x=[0, 256],
                             range_y=[min_Outbound, max_Outbound], height=500, animation_frame='Week', log_y=True,
                             hover_data=["Week", "TargetSubnet"], text="TargetSubnet")
        fig_subs_in.update_xaxes(title=rankTitle_in)
        fig_subs_in.update_yaxes(title="Outbound Bytes")

    elif type_graph_subs_in == "Difference":
        new_df_subs_in = df_subs_in.drop(df_subs_in[df_subs_in.Rank_Bytes > int(top_picks_subs_in)].index)

        min_Diff = new_df_subs_in["Difference"].min()
        max_Diff = new_df_subs_in["Difference"].max()
        fig_subs_in = px.bar(data_frame=new_df_subs_in, x=rankChoice_in, y="Difference", range_x=[0, 256],
                             range_y=[min_Diff, max_Diff], height=500, animation_frame='Week', log_y=True,
                             color="Color", color_discrete_map={"In > Out": "blue", "Out > In": "red"},
                             hover_data=["Week", "TargetSubnet"], text="TargetSubnet")
        fig_subs_in.update_xaxes(title=rankTitle_in)
        fig_subs_in.update_yaxes(title="Difference Between Inbound and Outbound")

    elif type_graph_subs_in == "Source IPs":
        new_df_subs_in = df_subs_in.drop(df_subs_in[df_subs_in.Rank_Sources > int(top_picks_subs_in)].index)

        min_SourceIPs = new_df_subs_in["SourceIPs"].min()
        max_SourceIPs = new_df_subs_in["SourceIPs"].max()
        fig_subs_in = px.bar(data_frame=new_df_subs_in, x=rankChoice_in, y="SourceIPs", range_x=[0, 256],
                             range_y=[min_SourceIPs, max_SourceIPs], height=500, animation_frame='Week',
                             hover_data=["Week", "TargetSubnet"], text="TargetSubnet")
        fig_subs_in.update_xaxes(title=rankTitle_in)
        fig_subs_in.update_yaxes(title="Number of Distinct Source IPs")

    elif type_graph_subs_in == "Target IPs":
        new_df_subs_in = df_subs_in.drop(df_subs_in[df_subs_in.Rank_Targets > int(top_picks_subs_in)].index)

        min_TargetIPs = new_df_subs_in["TargetIPs"].min()
        max_TargetIPs = new_df_subs_in["TargetIPs"].max()
        fig_subs_in = px.bar(data_frame=new_df_subs_in, x=rankChoice_in, y="TargetIPs", range_x=[0, 256],
                             range_y=[min_TargetIPs, max_TargetIPs], height=500, animation_frame='Week',
                             hover_data=["Week", "TargetSubnet"], text="TargetSubnet")
        fig_subs_in.update_xaxes(title=rankTitle_in)
        fig_subs_in.update_yaxes(title="Number of Distinct Target IPs")

    elif type_graph_subs_in == "Source Ports":
        new_df_subs_in = df_subs_in.drop(df_subs_in[df_subs_in.Rank_SrcPorts > int(top_picks_subs_in)].index)

        min_SourcePorts = new_df_subs_in["SourcePorts"].min()
        max_SourcePorts = new_df_subs_in["SourcePorts"].max()
        fig_subs_in = px.bar(data_frame=new_df_subs_in, x=rankChoice_in, y="SourcePorts", range_x=[0, 256],
                             range_y=[min_SourcePorts, max_SourcePorts], height=500, animation_frame='Week',
                             hover_data=["Week", "TargetSubnet"], text="TargetSubnet")
        fig_subs_in.update_xaxes(title=rankTitle_in)
        fig_subs_in.update_yaxes(title="Number of Distinct Source Ports")

    elif type_graph_subs_in == "Target Ports":
        new_df_subs_in = df_subs_in.drop(df_subs_in[df_subs_in.Rank_TrgPorts > int(top_picks_subs_in)].index)

        min_TargetPorts = new_df_subs_in["TargetPorts"].min()
        max_TargetPorts = new_df_subs_in["TargetPorts"].max()
        fig_subs_in = px.bar(data_frame=new_df_subs_in, x=rankChoice_in, y="TargetPorts", range_x=[0, 256],
                             range_y=[min_TargetPorts, max_TargetPorts], height=500, animation_frame='Week',
                             hover_data=["Week", "TargetSubnet"], text="TargetSubnet")
        fig_subs_in.update_xaxes(title=rankTitle_in)
        fig_subs_in.update_yaxes(title="Number of Distinct Target Ports")

    else:
        new_df_subs_in = df_subs_in.drop(df_subs_in[df_subs_in.Rank_Bytes > int(top_picks_subs_in)].index)

        fig_subs_in = px.bar(data_frame=new_df_subs_in, x=rankChoice_in, y=type_graph_subs_out, height=500,
                             range_x=[1, 257],
                             animation_frame='Week', hover_data=["Week", "TargetSubnet"], text="TargetSubnet")
        fig_subs_in.update_xaxes(title=rankTitle_in)

    fig_subs_in.update_xaxes(range=[0, 256], autorange=False)
    fig_subs_in.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 800
    fig_subs_in.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
    fig_subs_in.update_traces(width=1, textangle=0, textposition='outside')
    # endregion

    # ==================================================================================================================

    # region Section_Groups_Out

    if DEBUG: print("=================== groups graphs - outgoing ===================")
    if DEBUG: print("<type_graph_groups_out>: ", type_graph_groups_out)

    if type_graph_groups_out == "WiFi":
        df_groups_out = pd.read_csv("input_type_5/group_wifi_outgoing.csv")

    elif type_graph_groups_out == "WLAN":
        df_groups_out = pd.read_csv("input_type_5/group_wlan_outgoing.csv")

    elif type_graph_groups_out == "Services":
        df_groups_out = pd.read_csv("input_type_5/group_services_outgoing.csv")

    elif type_graph_groups_out == "VPN":
        df_groups_out = pd.read_csv("input_type_5/group_vpn_outgoing.csv")

    elif type_graph_groups_out == "Science":
        df_groups_out = pd.read_csv("input_type_5/group_science_outgoing.csv")

    elif type_graph_groups_out == "Schulich":
        df_groups_out = pd.read_csv("input_type_5/group_schulich_outgoing.csv")

    elif type_graph_groups_out == "Medical":
        df_groups_out = pd.read_csv("input_type_5/group_medical_outgoing.csv")

    elif type_graph_groups_out == "Arts":
        df_groups_out = pd.read_csv("input_type_5/group_arts_outgoing.csv")

    elif type_graph_groups_out == "CPSC":
        df_groups_out = pd.read_csv("input_type_5/group_cpsc_outgoing.csv")

    elif type_graph_groups_out == "PHAS":
        df_groups_out = pd.read_csv("input_type_5/group_phas_outgoing.csv")

    elif type_graph_groups_out == "Reznet":
        df_groups_out = pd.read_csv("input_type_5/group_reznet_outgoing.csv")

    elif type_graph_groups_out == "Admin":
        df_groups_out = pd.read_csv("input_type_5/group_admin_outgoing.csv")

    fig_groups_out_conns = px.bar(data_frame=df_groups_out, x="Week", y="Connections", height=600, log_y=True,
                                  range_y=[2000, 40000000], color_discrete_sequence=['#523a28'])
    fig_groups_out_conns.update_layout(yaxis_title="Outgoing Connections")
    fig_groups_out_conns.update_yaxes(tickvals=[10000, 100000, 1000000, 10000000])

    # Annotations for maximum connections
    maxOut_Conns = df_groups_out["Connections"].max()
    maxOut_ConnsWeek = df_groups_out.loc[df_groups_out["Connections"] == maxOut_Conns, "Week"].max()

    fig_groups_out_conns.add_annotation(text='<b>' + str(conn_format(maxOut_Conns)) + '</b>', font_size=18,
                                        x=week_number(maxOut_ConnsWeek),
                                        y=math.log10(maxOut_Conns) + 0.11, showarrow=False
                                        )

    # ------------------------------------------------------------------------------------------------------------------

    fig_groups_out_bytes = px.bar(data_frame=df_groups_out, x="Week", y="TotalBytes", height=600)
    fig_groups_out_bytes.update_yaxes(title="Total Bytes")

    # ------------------------------------------------------------------------------------------------------------------

    fig_groups_out_inout = go.Figure()
    fig_groups_out_inout.add_trace(
        go.Bar(x=df_groups_out["Week"], y=df_groups_out["Inbound"], name="Inbound", marker_color='rgb(104,187,227)'))
    fig_groups_out_inout.add_trace(
        go.Bar(x=df_groups_out["Week"], y=df_groups_out["Outbound"], name="Outbound"))
    fig_groups_out_inout.update_layout(height=600, margin=dict(l=30, r=30, t=60, b=80, pad=0),
                                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
                                       yaxis_title="Bytes on Outgoing Connections", yaxis_type="log",
                                       yaxis_range=[9, math.log10(200000000000000)])
    fig_groups_out_inout.update_xaxes(title="Week")
    fig_groups_out_inout.update_yaxes(tickvals=[1073741824, 10737418240, 107374182400, 1099511627776, 10995116277760,
                                                109951162777600],
                                      ticktext=["1 GB", "10 GB", "100 GB", "1 TB", "10 TB", "100 TB"])

    # Annotations for maximum inbound/outbound values
    maxOut_InboundBytes = df_groups_out["Inbound"].max()
    maxOut_InboundWeek = df_groups_out.loc[df_groups_out["Inbound"] == maxOut_InboundBytes, "Week"].max()
    maxOut_OutboundBytes = df_groups_out["Outbound"].max()
    maxOut_OutboundWeek = df_groups_out.loc[df_groups_out["Outbound"] == maxOut_OutboundBytes, "Week"].max()

    fig_groups_out_inout.add_annotation(text='<b>' + str(byte_format(maxOut_InboundBytes)) + '</b>', textangle=-90,
                                        x=week_number(maxOut_InboundWeek) - 0.2,
                                        y=math.log10(maxOut_InboundBytes) - 0.8, showarrow=False,
                                        font_size=18, font_color='black'
                                        )
    fig_groups_out_inout.add_annotation(text='<b>' + str(byte_format(maxOut_OutboundBytes)) + '</b>', textangle=-90,
                                        x=week_number(maxOut_OutboundWeek) + 0.2,
                                        y=math.log10(maxOut_OutboundBytes) - 0.8, showarrow=False,
                                        font_size=18, font_color='black'
                                        )

    # ------------------------------------------------------------------------------------------------------------------

    fig_groups_out_asym = go.Figure()
    fig_groups_out_asym.add_trace(
        go.Bar(x=df_groups_out["Week"], y=(df_groups_out["Inbound"] - df_groups_out["Outbound"]), name='In > Out',
               offsetgroup=0, marker_color='rgb(104,187,227)'))
    fig_groups_out_asym.add_trace(
        go.Bar(x=df_groups_out["Week"], y=(df_groups_out["Outbound"] - df_groups_out["Inbound"]), name='Out > In',
               offsetgroup=0))
    fig_groups_out_asym.update_layout(height=600, margin=dict(l=0, r=0, t=60, b=80, pad=0))
    fig_groups_out_asym.update_xaxes(title="Week")
    fig_groups_out_asym.update_yaxes(title="Difference in Asymmetry", type="log")
    # endregion

    # ==================================================================================================================

    # region Section_Groups_In

    if DEBUG: print("=================== groups graphs - incoming ===================")
    if DEBUG: print("<type_graph_groups_in>: ", type_graph_groups_in)

    if type_graph_groups_in == "WiFi":
        df_groups_in = pd.read_csv("input_type_6/group_wifi_incoming.csv")

    elif type_graph_groups_in == "WLAN":
        df_groups_in = pd.read_csv("input_type_6/group_wlan_incoming.csv")

    elif type_graph_groups_in == "Services":
        df_groups_in = pd.read_csv("input_type_6/group_services_incoming.csv")

    elif type_graph_groups_in == "VPN":
        df_groups_in = pd.read_csv("input_type_6/group_vpn_incoming.csv")

    elif type_graph_groups_in == "Science":
        df_groups_in = pd.read_csv("input_type_6/group_science_incoming.csv")

    elif type_graph_groups_in == "Schulich":
        df_groups_in = pd.read_csv("input_type_6/group_schulich_incoming.csv")

    elif type_graph_groups_in == "Medical":
        df_groups_in = pd.read_csv("input_type_6/group_medical_incoming.csv")

    elif type_graph_groups_in == "Arts":
        df_groups_in = pd.read_csv("input_type_6/group_arts_incoming.csv")

    elif type_graph_groups_in == "CPSC":
        df_groups_in = pd.read_csv("input_type_6/group_cpsc_incoming.csv")

    elif type_graph_groups_in == "PHAS":
        df_groups_in = pd.read_csv("input_type_6/group_phas_incoming.csv")

    elif type_graph_groups_in == "Reznet":
        df_groups_in = pd.read_csv("input_type_6/group_reznet_incoming.csv")

    elif type_graph_groups_in == "Admin":
        df_groups_in = pd.read_csv("input_type_6/group_admin_incoming.csv")

    fig_groups_in_conns = px.bar(data_frame=df_groups_in, x="Week", y="Connections", height=600, log_y=True,
                                 range_y=[2000, 40000000], color_discrete_sequence=['#523a28'])
    fig_groups_in_conns.update_layout(yaxis_title="Incoming Connections")
    fig_groups_in_conns.update_yaxes(tickvals=[10000, 100000, 1000000, 10000000])

    # Annotations for maximum connections
    maxIn_Conns = df_groups_in["Connections"].max()
    maxIn_ConnsWeek = df_groups_in.loc[df_groups_in["Connections"] == maxIn_Conns, "Week"].max()

    fig_groups_in_conns.add_annotation(text='<b>' + str(conn_format(maxIn_Conns)) + '</b>', font_size=18,
                                       x=week_number(maxIn_ConnsWeek),
                                       y=math.log10(maxIn_Conns) + 0.11, showarrow=False
                                       )

    # ------------------------------------------------------------------------------------------------------------------

    fig_groups_in_bytes = px.bar(data_frame=df_groups_in, x="Week", y="TotalBytes", height=600)
    fig_groups_in_bytes.update_yaxes(title="Total Bytes")

    # ------------------------------------------------------------------------------------------------------------------

    fig_groups_in_inout = go.Figure()
    fig_groups_in_inout.add_trace(
        go.Bar(x=df_groups_in["Week"], y=df_groups_in["Inbound"], name="Inbound", marker_color='rgb(104,187,227)'))
    fig_groups_in_inout.add_trace(
        go.Bar(x=df_groups_in["Week"], y=df_groups_in["Outbound"], name="Outbound"))
    fig_groups_in_inout.update_layout(height=600, margin=dict(l=30, r=30, t=60, b=80, pad=0),
                                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
                                      yaxis_title="Bytes on Incoming Connections", yaxis_type="log",
                                      yaxis_range=[9, math.log10(200000000000000)])
    fig_groups_in_inout.update_xaxes(title="Week")
    fig_groups_in_inout.update_yaxes(tickvals=[1073741824, 10737418240, 107374182400, 1099511627776, 10995116277760,
                                               109951162777600],
                                     ticktext=["1 GB", "10 GB", "100 GB", "1 TB", "10 TB", "100 TB"])

    # Annotations for maximum inbound/outbound values
    maxIn_InboundBytes = df_groups_in["Inbound"].max()
    maxIn_InboundWeek = df_groups_in.loc[df_groups_in["Inbound"] == maxIn_InboundBytes, "Week"].max()
    maxIn_OutboundBytes = df_groups_in["Outbound"].max()
    maxIn_OutboundWeek = df_groups_in.loc[df_groups_in["Outbound"] == maxIn_OutboundBytes, "Week"].max()

    fig_groups_in_inout.add_annotation(text='<b>' + str(byte_format(maxIn_InboundBytes)) + '</b>', textangle=-90,
                                       x=week_number(maxIn_InboundWeek) - 0.2,
                                       y=math.log10(maxIn_InboundBytes) - 0.8, showarrow=False,
                                       font_size=18, font_color='black'
                                       )
    fig_groups_in_inout.add_annotation(text='<b>' + str(byte_format(maxIn_OutboundBytes)) + '</b>',
                                       x=week_number(maxIn_OutboundWeek) + 0.2,
                                       y=math.log10(maxIn_OutboundBytes) - 0.8, showarrow=False, textangle=-90,
                                       font_size=18, font_color='black'
                                       )

    # ------------------------------------------------------------------------------------------------------------------

    fig_groups_in_asym = go.Figure()
    fig_groups_in_asym.add_trace(
        go.Bar(x=df_groups_in["Week"], y=(df_groups_in["Inbound"] - df_groups_in["Outbound"]), name='In > Out',
               offsetgroup=0, marker_color='rgb(104,187,227)'))
    fig_groups_in_asym.add_trace(
        go.Bar(x=df_groups_in["Week"], y=(df_groups_in["Outbound"] - df_groups_in["Inbound"]), name='Out > In',
               offsetgroup=0))
    fig_groups_in_asym.update_layout(height=600, margin=dict(l=0, r=0, t=60, b=80, pad=0))
    fig_groups_in_asym.update_xaxes(title="Week")
    fig_groups_in_asym.update_yaxes(title="Difference in Asymmetry", type="log")
    # endregion

    # ==================================================================================================================

    # region Section_Orgs_Out

    if DEBUG: print("=================== top 10 orgs graphs - outgoing ===================")
    if DEBUG: print("<type_graph_orgs_out>: ", type_graph_orgs_out)

    if type_graph_orgs_out == "WiFi":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_wifi.csv")

    elif type_graph_orgs_out == "WLAN":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_wlan.csv")

    elif type_graph_orgs_out == "Services":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_services.csv")

    elif type_graph_orgs_out == "VPN":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_vpn.csv")

    elif type_graph_orgs_out == "Science":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_science.csv")

    elif type_graph_orgs_out == "Schulich":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_schulich.csv")

    elif type_graph_orgs_out == "Medical":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_medical.csv")

    elif type_graph_orgs_out == "Arts":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_arts.csv")

    elif type_graph_orgs_out == "CPSC":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_cpsc.csv")

    elif type_graph_orgs_out == "PHAS":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_phas.csv")

    elif type_graph_orgs_out == "Reznet":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_reznet.csv")

    elif type_graph_orgs_out == "Admin":
        df_orgs_out = pd.read_csv("input_type_7/orgs_outgoing_admin.csv")

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_out_conns = px.line(df_orgs_out, x='Week', y='Connections', log_y=True, color='TargetOrgs',
                                 color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                     'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc', 'GOOGLE': '#109618',
                                                     'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                     'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                     'VALVE-CORPORATION': '#bcbd22'},
                                 markers=True, line_dash='TargetOrgs', symbol='TargetOrgs', height=600)
    fig_orgs_out_conns.update_layout(plot_bgcolor='white', showlegend=False)
    fig_orgs_out_conns.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_conns.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_conns.update_traces(line_width=4, marker_size=12)

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_out_bytes = px.line(df_orgs_out, x='Week', y='TotalBytes', log_y=True, color='TargetOrgs',
                                 color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                     'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc', 'GOOGLE': '#109618',
                                                     'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                     'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                     'VALVE-CORPORATION': '#bcbd22'},
                                 markers=True, line_dash='TargetOrgs', symbol='TargetOrgs', height=600)
    fig_orgs_out_bytes.update_layout(plot_bgcolor='white')
    fig_orgs_out_bytes.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_bytes.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_bytes.update_traces(line_width=4, marker_size=12)

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_out_src_ips = px.line(df_orgs_out, x='Week', y='SourceIPs', color='TargetOrgs',
                                   color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                       'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc', 'GOOGLE': '#109618',
                                                       'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                       'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                       'VALVE-CORPORATION': '#bcbd22'},
                                   markers=True, line_dash='TargetOrgs', symbol='TargetOrgs', height=600)
    fig_orgs_out_src_ips.update_layout(plot_bgcolor='white', showlegend=False)
    fig_orgs_out_src_ips.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_src_ips.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_src_ips.update_traces(line_width=4, marker_size=12)

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_out_trg_ips = px.line(df_orgs_out, x='Week', y='TargetIPs', color='TargetOrgs',
                                   color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                       'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc', 'GOOGLE': '#109618',
                                                       'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                       'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                       'VALVE-CORPORATION': '#bcbd22'},
                                   markers=True, line_dash='TargetOrgs', symbol='TargetOrgs', height=600)
    fig_orgs_out_trg_ips.update_layout(plot_bgcolor='white')
    fig_orgs_out_trg_ips.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_trg_ips.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_trg_ips.update_traces(line_width=4, marker_size=12)

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_out_src_ports = px.line(df_orgs_out, x='Week', y='SourcePorts', color='TargetOrgs',
                                     color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                         'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc',
                                                         'GOOGLE': '#109618',
                                                         'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                         'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                         'VALVE-CORPORATION': '#bcbd22'},
                                     markers=True, line_dash='TargetOrgs', symbol='TargetOrgs', height=600)
    fig_orgs_out_src_ports.update_layout(plot_bgcolor='white', showlegend=False)
    fig_orgs_out_src_ports.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_src_ports.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_src_ports.update_traces(line_width=4, marker_size=12)

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_out_trg_ports = px.line(df_orgs_out, x='Week', y='TargetPorts', color='TargetOrgs',
                                     color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                         'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc',
                                                         'GOOGLE': '#109618',
                                                         'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                         'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                         'VALVE-CORPORATION': '#bcbd22'},
                                     markers=True, line_dash='TargetOrgs', symbol='TargetOrgs', height=600)
    fig_orgs_out_trg_ports.update_layout(plot_bgcolor='white')
    fig_orgs_out_trg_ports.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_trg_ports.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_out_trg_ports.update_traces(line_width=4, marker_size=12)
    # endregion

    # ==================================================================================================================

    # region Section_Orgs_In

    if DEBUG: print("=================== top 10 orgs graphs - incoming ===================")
    if DEBUG: print("<type_graph_orgs_in>: ", type_graph_orgs_in)

    if type_graph_orgs_in == "WiFi":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_wifi.csv")

    elif type_graph_orgs_in == "WLAN":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_wlan.csv")

    elif type_graph_orgs_in == "Services":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_services.csv")

    elif type_graph_orgs_in == "VPN":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_vpn.csv")

    elif type_graph_orgs_in == "Science":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_science.csv")

    elif type_graph_orgs_in == "Schulich":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_schulich.csv")

    elif type_graph_orgs_in == "Medical":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_medical.csv")

    elif type_graph_orgs_in == "Arts":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_arts.csv")

    elif type_graph_orgs_in == "CPSC":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_cpsc.csv")

    elif type_graph_orgs_in == "PHAS":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_phas.csv")

    elif type_graph_orgs_in == "Reznet":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_reznet.csv")

    elif type_graph_orgs_in == "Admin":
        df_orgs_in = pd.read_csv("input_type_8/orgs_incoming_admin.csv")

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_in_conns = px.line(df_orgs_in, x='Week', y='Connections', log_y=True, color='SourceOrgs',
                                color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                    'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc', 'GOOGLE': '#109618',
                                                    'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                    'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                    'VALVE-CORPORATION': '#bcbd22', 'TELUS': '#db1f48',
                                                    'SHAW': '#613659', 'BACOM': '#01949a', 'ROGERS': '#81b622',
                                                    'Chinanet': '#d3b1c2', 'AHS': '#eeb5eb', 'YANDEXLLC': '#fad02c',
                                                    'NLM-GW': '#055c9d', 'JiscServicesLimited': '#870a30',
                                                    'BROADINSTITUTE-AS': '#e57f84', 'OoredooQ.S.C.': '#90adc6',
                                                    'RelianceJioInfocommLimited': '#a16ae8', 'O-NET': '#ffa384',
                                                    'Vetenskapsradet/SUNET': '#74bdcb', 'VELOCITYNET-01': '#3d5b59',
                                                    'CHINAUNICOMChina169Backbone': '#ff4500', 'CIPHERKEY': '#b7ac44',
                                                    'TEKSAVVY': '#52688f', 'BARR-XPLR-ASN': '#d4f1f4',
                                                    'PRIMUS-AS6407': '#b9b7bd', 'CIKTELECOM-CABLE': '#fb4570',
                                                    'TWC-11426-CAROLINAS': '#7cf3a0', 'PEGTECHINC': '#f9eac2',
                                                    'UniversityofQueensland': '#bfd7ed'},
                                markers=True, line_dash='SourceOrgs', symbol='SourceOrgs', height=600)
    fig_orgs_in_conns.update_layout(plot_bgcolor='white', showlegend=False)
    fig_orgs_in_conns.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_conns.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_conns.update_traces(line_width=4, marker_size=12)

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_in_bytes = px.line(df_orgs_in, x='Week', y='TotalBytes', log_y=True, color='SourceOrgs',
                                color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                    'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc', 'GOOGLE': '#109618',
                                                    'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                    'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                    'VALVE-CORPORATION': '#bcbd22', 'TELUS': '#db1f48',
                                                    'SHAW': '#613659', 'BACOM': '#01949a', 'ROGERS': '#81b622',
                                                    'Chinanet': '#d3b1c2', 'AHS': '#eeb5eb', 'YANDEXLLC': '#fad02c',
                                                    'NLM-GW': '#055c9d', 'JiscServicesLimited': '#870a30',
                                                    'BROADINSTITUTE-AS': '#e57f84', 'OoredooQ.S.C.': '#90adc6',
                                                    'RelianceJioInfocommLimited': '#a16ae8', 'O-NET': '#ffa384',
                                                    'Vetenskapsradet/SUNET': '#74bdcb', 'VELOCITYNET-01': '#3d5b59',
                                                    'CHINAUNICOMChina169Backbone': '#ff4500', 'CIPHERKEY': '#b7ac44',
                                                    'TEKSAVVY': '#52688f', 'BARR-XPLR-ASN': '#d4f1f4',
                                                    'PRIMUS-AS6407': '#b9b7bd', 'CIKTELECOM-CABLE': '#fb4570',
                                                    'TWC-11426-CAROLINAS': '#7cf3a0', 'PEGTECHINC': '#f9eac2',
                                                    'UniversityofQueensland': '#bfd7ed'},
                                markers=True, line_dash='SourceOrgs', symbol='SourceOrgs', height=600)
    fig_orgs_in_bytes.update_layout(plot_bgcolor='white'),
    fig_orgs_in_bytes.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_bytes.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_bytes.update_traces(line_width=4, marker_size=12)

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_in_src_ips = px.line(df_orgs_in, x='Week', y='SourceIPs', color='SourceOrgs',
                                  color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                      'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc', 'GOOGLE': '#109618',
                                                      'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                      'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                      'VALVE-CORPORATION': '#bcbd22', 'TELUS': '#db1f48',
                                                      'SHAW': '#613659', 'BACOM': '#01949a', 'ROGERS': '#81b622',
                                                      'Chinanet': '#d3b1c2', 'AHS': '#eeb5eb', 'YANDEXLLC': '#fad02c',
                                                      'NLM-GW': '#055c9d', 'JiscServicesLimited': '#870a30',
                                                      'BROADINSTITUTE-AS': '#e57f84', 'OoredooQ.S.C.': '#90adc6',
                                                      'RelianceJioInfocommLimited': '#a16ae8', 'O-NET': '#ffa384',
                                                      'Vetenskapsradet/SUNET': '#74bdcb', 'VELOCITYNET-01': '#3d5b59',
                                                      'CHINAUNICOMChina169Backbone': '#ff4500', 'CIPHERKEY': '#b7ac44',
                                                      'TEKSAVVY': '#52688f', 'BARR-XPLR-ASN': '#d4f1f4',
                                                      'PRIMUS-AS6407': '#b9b7bd', 'CIKTELECOM-CABLE': '#fb4570',
                                                      'TWC-11426-CAROLINAS': '#7cf3a0', 'PEGTECHINC': '#f9eac2',
                                                      'UniversityofQueensland': '#bfd7ed'},
                                  markers=True, line_dash='SourceOrgs', symbol='SourceOrgs', height=600)
    fig_orgs_in_src_ips.update_layout(plot_bgcolor='white', showlegend=False)
    fig_orgs_in_src_ips.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_src_ips.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_src_ips.update_traces(line_width=4, marker_size=12)

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_in_trg_ips = px.line(df_orgs_in, x='Week', y='TargetIPs', color='SourceOrgs',
                                  color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                      'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc', 'GOOGLE': '#109618',
                                                      'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                      'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                      'VALVE-CORPORATION': '#bcbd22', 'TELUS': '#db1f48',
                                                      'SHAW': '#613659', 'BACOM': '#01949a', 'ROGERS': '#81b622',
                                                      'Chinanet': '#d3b1c2', 'AHS': '#eeb5eb', 'YANDEXLLC': '#fad02c',
                                                      'NLM-GW': '#055c9d', 'JiscServicesLimited': '#870a30',
                                                      'BROADINSTITUTE-AS': '#e57f84', 'OoredooQ.S.C.': '#90adc6',
                                                      'RelianceJioInfocommLimited': '#a16ae8', 'O-NET': '#ffa384',
                                                      'Vetenskapsradet/SUNET': '#74bdcb', 'VELOCITYNET-01': '#3d5b59',
                                                      'CHINAUNICOMChina169Backbone': '#ff4500', 'CIPHERKEY': '#b7ac44',
                                                      'TEKSAVVY': '#52688f', 'BARR-XPLR-ASN': '#d4f1f4',
                                                      'PRIMUS-AS6407': '#b9b7bd', 'CIKTELECOM-CABLE': '#fb4570',
                                                      'TWC-11426-CAROLINAS': '#7cf3a0', 'PEGTECHINC': '#f9eac2',
                                                      'UniversityofQueensland': '#bfd7ed'},
                                  markers=True, line_dash='SourceOrgs', symbol='SourceOrgs', height=600)
    fig_orgs_in_trg_ips.update_layout(plot_bgcolor='white'),
    fig_orgs_in_trg_ips.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_trg_ips.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_trg_ips.update_traces(line_width=4, marker_size=12)

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_in_src_ports = px.line(df_orgs_in, x='Week', y='SourcePorts', color='SourceOrgs',
                                    color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                        'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc',
                                                        'GOOGLE': '#109618',
                                                        'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                        'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                        'VALVE-CORPORATION': '#bcbd22', 'TELUS': '#db1f48',
                                                        'SHAW': '#613659', 'BACOM': '#01949a', 'ROGERS': '#81b622',
                                                        'Chinanet': '#d3b1c2', 'AHS': '#eeb5eb', 'YANDEXLLC': '#fad02c',
                                                        'NLM-GW': '#055c9d', 'JiscServicesLimited': '#870a30',
                                                        'BROADINSTITUTE-AS': '#e57f84', 'OoredooQ.S.C.': '#90adc6',
                                                        'RelianceJioInfocommLimited': '#a16ae8', 'O-NET': '#ffa384',
                                                        'Vetenskapsradet/SUNET': '#74bdcb', 'VELOCITYNET-01': '#3d5b59',
                                                        'CHINAUNICOMChina169Backbone': '#ff4500',
                                                        'CIPHERKEY': '#b7ac44',
                                                        'TEKSAVVY': '#52688f', 'BARR-XPLR-ASN': '#d4f1f4',
                                                        'PRIMUS-AS6407': '#b9b7bd', 'CIKTELECOM-CABLE': '#fb4570',
                                                        'TWC-11426-CAROLINAS': '#7cf3a0', 'PEGTECHINC': '#f9eac2',
                                                        'UniversityofQueensland': '#bfd7ed'},
                                    markers=True, line_dash='SourceOrgs', symbol='SourceOrgs', height=600)
    fig_orgs_in_src_ports.update_layout(plot_bgcolor='white', showlegend=False)
    fig_orgs_in_src_ports.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_src_ports.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_src_ports.update_traces(line_width=4, marker_size=12)

    # ------------------------------------------------------------------------------------------------------------------

    fig_orgs_in_trg_ports = px.line(df_orgs_in, x='Week', y='TargetPorts', color='SourceOrgs',
                                    color_discrete_map={'APPLE': '#7f7f7f', 'NETFLIX': '#dc3912', 'AKAMAI': '#ff9900',
                                                        'CANARIE': '#fb00d1', 'FACEBOOK': '#3366cc',
                                                        'GOOGLE': '#109618',
                                                        'AMAZON': '#212E3C', 'FASTLY': '#8c564b', 'LEVEL3': '#17becf',
                                                        'MICROSOFT': '#990099', 'EDGECAST': '#316395',
                                                        'VALVE-CORPORATION': '#bcbd22', 'TELUS': '#db1f48',
                                                        'SHAW': '#613659', 'BACOM': '#01949a', 'ROGERS': '#81b622',
                                                        'Chinanet': '#d3b1c2', 'AHS': '#eeb5eb', 'YANDEXLLC': '#fad02c',
                                                        'NLM-GW': '#055c9d', 'JiscServicesLimited': '#870a30',
                                                        'BROADINSTITUTE-AS': '#e57f84', 'OoredooQ.S.C.': '#90adc6',
                                                        'RelianceJioInfocommLimited': '#a16ae8', 'O-NET': '#ffa384',
                                                        'Vetenskapsradet/SUNET': '#74bdcb', 'VELOCITYNET-01': '#3d5b59',
                                                        'CHINAUNICOMChina169Backbone': '#ff4500',
                                                        'CIPHERKEY': '#b7ac44',
                                                        'TEKSAVVY': '#52688f', 'BARR-XPLR-ASN': '#d4f1f4',
                                                        'PRIMUS-AS6407': '#b9b7bd', 'CIKTELECOM-CABLE': '#fb4570',
                                                        'TWC-11426-CAROLINAS': '#7cf3a0', 'PEGTECHINC': '#f9eac2',
                                                        'UniversityofQueensland': '#bfd7ed'},
                                    markers=True, line_dash='SourceOrgs', symbol='SourceOrgs', height=600)
    fig_orgs_in_trg_ports.update_layout(plot_bgcolor='white'),
    fig_orgs_in_trg_ports.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_trg_ports.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_orgs_in_trg_ports.update_traces(line_width=4, marker_size=12)
    # endregion

    # ==================================================================================================================

    return fig_subs_out, '## Source Subnets on Outgoing Connections - ' + type_graph_subs_out, \
           fig_subs_in, '## Target Subnets on Incoming Connections - ' + type_graph_subs_in, \
           fig_groups_out_conns, fig_groups_out_bytes, fig_groups_out_inout, fig_groups_out_asym, \
           '## Outgoing Connections from Subnet Group - ' + type_graph_groups_out, \
           fig_groups_in_conns, fig_groups_in_bytes, fig_groups_in_inout, fig_groups_in_asym, \
           '## Incoming Connections to Subnet Group - ' + type_graph_groups_in, \
           fig_orgs_out_conns, fig_orgs_out_bytes, \
           fig_orgs_out_src_ips, fig_orgs_out_trg_ips, fig_orgs_out_src_ports, fig_orgs_out_trg_ports, \
           '## External Targets of the Outgoing Connections from Groups - ' + type_graph_orgs_out, \
           fig_orgs_in_conns, fig_orgs_in_bytes, \
           fig_orgs_in_src_ips, fig_orgs_in_trg_ips, fig_orgs_in_src_ports, fig_orgs_in_trg_ports, \
           '## External Sources of the Incoming Connections to Groups - ' + type_graph_orgs_in
    # returned objects are assigned to the component property of the Output


# region Section_Callbacks_2

# The callback specifies all the inputs and outputs of the function that is defined right below it. The dependent graphs
# that show the distribution of all IPs within a selected subnet are defined here. There are two dependent graphs, one
# for the selected subnet in the subnets graph of outgoing connections, and the other for the selected subnet in the
# subnets graph of incoming connections.
@app.callback(
    # Distribution of IPs - outgoing connections: graph
    Output(depGraph_subs_out, component_property='figure'),
    # Distribution of IPs - outgoing connections: title of graph
    Output(depTitle_subs_out, component_property='children'),
    # Distribution of IPs - incoming connections: graph
    Output(depGraph_subs_in, component_property='figure'),
    # Distribution of IPs - incoming connections: title of graph
    Output(depTitle_subs_in, component_property='children'),
    # Distribution of IPs - outgoing connections: selected subnet
    Input(graph_subs_out, component_property='clickData'),
    # Distribution of IPs - outgoing connections: type of graph
    Input(dropdown_subs_out, component_property='value'),
    # Distribution of IPs - incoming connections: selected subnet
    Input(graph_subs_in, component_property='clickData'),
    # Distribution of IPs - incoming connections: type of graph
    Input(dropdown_subs_in, component_property='value'),
)
# endregion
def update_dependent_graph(click_data_subs_out, type_graph_dep_out, click_data_subs_in, type_graph_dep_in):

    # ==================================================================================================================
    # region Section_Dependent_Graph_Subs_Out
    # Initializing the selected subnet in the outgoing subnet graph.
    selected_subnet_out = None

    if DEBUG: print("=================== Dependent graphs - outgoing ===================")
    if DEBUG: print('<type_graph_dep_out>: ', type_graph_dep_out)
    if DEBUG: print('<click_data_subs_out>: ', click_data_subs_out)

    # Getting the subnet number that the user clicked on.
    if click_data_subs_out is not None:
        selected_subnet_out = click_data_subs_out['points'][0]['text']

    if DEBUG: print('<selected_subnet_out>: ', selected_subnet_out)

    # Initializing a new DataFrame that only contains data for the selected subnet.
    new_df_subs_out_dep = df_subs_out_dep.loc[(df_subs_out_dep["SourceSubnet"] == selected_subnet_out)]  # &

    if DEBUG: print('<new_df_subs_out_dep dataframe>: ')
    if DEBUG: print(new_df_subs_out_dep)
    if DEBUG: print("count of new_df_subs_out_dep: ", len(new_df_subs_out_dep.index))

    # Cleaning the graph type name.
    graph_out_type_cleaned = str(type_graph_dep_out).replace(" ", "")
    if DEBUG: print('<graph_type>: ', str(graph_out_type_cleaned))

    # Plotting the dependent graph is similar for all types, except for two: SourceIPs and Difference.

    # SourceIPs subnet graph does not have a corresponding graph in the dependent graph. The dependent graph can plot
    # a specific value for each IP within the selected subnet, and "the number of IPs" does not make sense in this case.
    # So if SourceIPs is selected for the graph type, the TotalBytes for each IP is shown here in the dependent graph.
    if graph_out_type_cleaned == 'SourceIPs':
        max_yaxis = df_subs_out_dep.loc[df_subs_out_dep["SourceSubnet"] == selected_subnet_out, 'TotalBytes'].max()
        min_yaxis = df_subs_out_dep.loc[df_subs_out_dep["SourceSubnet"] == selected_subnet_out, 'TotalBytes'].min()

        fig_dep_subs_out = px.bar(data_frame=new_df_subs_out_dep, x="SourceIP", y='TotalBytes', range_x=[0, 255],
                                  range_y=[min_yaxis, max_yaxis], height=400, log_y=True, animation_frame='Week',
                                  color_discrete_sequence=['#0a7029'])
        fig_dep_subs_out.update_traces(width=1)
        fig_dep_subs_out.update_xaxes(title="Source IPs")
        fig_dep_subs_out.update_yaxes(title=graph_type_yaxis("TotalBytes"))

    # For the graph type "Difference" the coloring is different from other types.
    elif graph_out_type_cleaned == 'Difference':
        max_yaxis = df_subs_out_dep.loc[df_subs_out_dep["SourceSubnet"] == selected_subnet_out, 'Difference'].max()
        min_yaxis = df_subs_out_dep.loc[df_subs_out_dep["SourceSubnet"] == selected_subnet_out, 'Difference'].min()

        fig_dep_subs_out = px.bar(data_frame=new_df_subs_out_dep, x="SourceIP", animation_frame='Week',
                                  y=graph_out_type_cleaned, range_x=[0, 255], range_y=[min_yaxis, max_yaxis],
                                  color='Color', color_discrete_map={"In > Out": "blue", "Out > In": "red"}, height=400,
                                  log_y=True)
        fig_dep_subs_out.update_traces(width=1)
        fig_dep_subs_out.update_xaxes(title="Source IPs")
        fig_dep_subs_out.update_yaxes(title=graph_type_yaxis(graph_out_type_cleaned))

    # The rest of the graph types can be plotted accordingly.
    else:
        max_yaxis = df_subs_out_dep.loc[
            df_subs_out_dep["SourceSubnet"] == selected_subnet_out, graph_out_type_cleaned].max()
        min_yaxis = df_subs_out_dep.loc[
            df_subs_out_dep["SourceSubnet"] == selected_subnet_out, graph_out_type_cleaned].min()

        fig_dep_subs_out = px.bar(data_frame=new_df_subs_out_dep, x="SourceIP", animation_frame="Week",
                                  y=graph_out_type_cleaned, range_x=[0, 255], range_y=[min_yaxis, max_yaxis],
                                  height=400, log_y=True, color_discrete_sequence=['#0a7029'])
        fig_dep_subs_out.update_traces(width=1)
        fig_dep_subs_out.update_xaxes(title="Source IPs")
        fig_dep_subs_out.update_yaxes(title=graph_type_yaxis(graph_out_type_cleaned))

    # If the selected subnet was only active during one of the time points, no transition slide and buttons can be
    # added to the graph. This if-condition checks the DataFrame to make sure there are more than one points.
    if len(new_df_subs_out_dep.index) > 1:
        fig_dep_subs_out.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 800
        fig_dep_subs_out.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500

    # If the selected subnet was active at one point in time, a red message appears below the graph.
    elif len(new_df_subs_out_dep.index) == 1:
        thisWeek_out = selected_subnet_out = click_data_subs_out['points'][0]['customdata'][0]
        fig_dep_subs_out.add_annotation(dict(font=dict(color='red', size=18), x=0, y=-0.2, showarrow=False,
                                             text="This subnet was only active in " + thisWeek_out, textangle=0,
                                             xanchor='left',
                                             xref="paper", yref="paper"))
        if DEBUG: print("Only 1 data point is available in the selected subnet in outgoing connections.")
    # endregion

    # ==================================================================================================================

    # region Section_Dependent_Graph_Subs_In
    # Initializing the selected subnet in the outgoing subnet graph.
    selected_subnet_in = None

    if DEBUG: print("=================== Dependent graphs - incoming ===================")
    if DEBUG: print('<type_graph_dep_in>: ', type_graph_dep_in)
    if DEBUG: print('<click_data_subs_in>: ', click_data_subs_in)

    # Getting the subnet number that the user clicked on.
    if click_data_subs_in is not None:
        selected_subnet_in = click_data_subs_in['points'][0]['text']

    if DEBUG: print('<selected_subnet_in>: ', selected_subnet_in)

    # Initializing a new DataFrame that only contains data for the selected subnet.
    new_df_subs_in_dep = df_subs_in_dep.loc[(df_subs_in_dep["TargetSubnet"] == selected_subnet_in)]  # &

    if DEBUG: print('<new_df_subs_in_dep dataframe>: ')
    if DEBUG: print(new_df_subs_in_dep)
    if DEBUG: print("count of new_df_subs_in_dep: ", len(new_df_subs_in_dep.index))

    # Cleaning the graph type name.
    graph_in_type_cleaned = str(type_graph_dep_in).replace(" ", "")
    if DEBUG: print('<graph_type>: ', str(graph_out_type_cleaned))

    # Plotting the dependent graph is similar for all types, except for two: TargetIPs and Difference.

    # TargetIPs subnet graph does not have a corresponding graph in the dependent graph. The dependent graph can plot
    # a specific value for each IP within the selected subnet, and "the number of IPs" does not make sense in this case.
    # So if TargetIPs is selected for the graph type, the TotalBytes for each IP is shown here in the dependent graph.
    if str(type_graph_dep_in).replace(" ", "") == 'TargetIPs':
        max_yaxis = new_df_subs_in_dep.loc[new_df_subs_in_dep["TargetSubnet"] == selected_subnet_in, 'TotalBytes'].max()
        min_yaxis = new_df_subs_in_dep.loc[new_df_subs_in_dep["TargetSubnet"] == selected_subnet_in, 'TotalBytes'].min()

        fig_dep_subs_in = px.bar(data_frame=new_df_subs_in_dep, x="TargetIP", y='TotalBytes', range_x=[0, 255],
                                 range_y=[min_yaxis, max_yaxis], height=400, log_y=True, animation_frame='Week',
                                 color_discrete_sequence=['#0a7029'])
        fig_dep_subs_in.update_traces(width=1)
        fig_dep_subs_in.update_xaxes(title="Target IPs")
        fig_dep_subs_in.update_yaxes(title=graph_type_yaxis("TotalBytes"))

    # For the graph type "Difference" the coloring is different from other types.
    elif graph_in_type_cleaned == 'Difference':
        max_yaxis = df_subs_in_dep.loc[df_subs_in_dep["TargetSubnet"] == selected_subnet_in, 'Difference'].max()
        min_yaxis = df_subs_in_dep.loc[df_subs_in_dep["TargetSubnet"] == selected_subnet_in, 'Difference'].min()

        fig_dep_subs_in = px.bar(data_frame=new_df_subs_in_dep, x="TargetIP", y=graph_in_type_cleaned, color='Color',
                                 range_x=[0, 255], range_y=[min_yaxis, max_yaxis], animation_frame='Week',
                                 color_discrete_map={"In > Out": "blue", "Out > In": "red"}, height=400, log_y=True)
        fig_dep_subs_in.update_traces(width=1)
        fig_dep_subs_in.update_xaxes(title="Target IPs")
        fig_dep_subs_in.update_yaxes(title=graph_type_yaxis(graph_in_type_cleaned))

    # The rest of the graph types can be plotted accordingly.
    else:
        max_yaxis = df_subs_in_dep.loc[
            df_subs_in_dep["TargetSubnet"] == selected_subnet_in, graph_in_type_cleaned].max()
        min_yaxis = df_subs_in_dep.loc[
            df_subs_in_dep["TargetSubnet"] == selected_subnet_in, graph_in_type_cleaned].min()

        fig_dep_subs_in = px.bar(data_frame=new_df_subs_in_dep, x="TargetIP", y=graph_in_type_cleaned, log_y=True,
                                 range_x=[0, 255], range_y=[min_yaxis, max_yaxis], height=400, animation_frame='Week',
                                 color_discrete_sequence=['#0a7029'])
        fig_dep_subs_in.update_traces(width=1)
        fig_dep_subs_in.update_xaxes(title="Target IPs")
        fig_dep_subs_in.update_yaxes(title=graph_type_yaxis(graph_in_type_cleaned))

    # If the selected subnet was only active during one of the time points, no transition slide and buttons can be
    # added to the graph. This if-condition checks the DataFrame to make sure there are more than one points.
    if len(new_df_subs_in_dep.index) > 1:
        fig_dep_subs_in.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 800
        fig_dep_subs_in.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500

    # If the selected subnet was active at one point in time, a red message appears below the graph.
    elif len(new_df_subs_in_dep.index) == 1:
        thisWeek_in = selected_subnet_out = click_data_subs_in['points'][0]['customdata'][0]
        fig_dep_subs_in.add_annotation(dict(font=dict(color='red', size=18), x=0, y=-0.2, showarrow=False,
                                            text="This subnet was only active in " + thisWeek_in, textangle=0,
                                            xanchor='left',
                                            xref="paper", yref="paper"))
        if DEBUG: print("Only 1 data point is available in the selected subnet in incoming connections.")
    # endregion

    return fig_dep_subs_out, '### Distribution of the Selected Subnet in Outgoing Connections - ' + \
           str(selected_subnet_out), fig_dep_subs_in, \
           '### Distribution of the Selected Subnet in Incoming Connections - ' + str(selected_subnet_in)


# region Functions

def byte_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1024.0
    # add more suffixes if you need them
    return '%.1f%s' % (num, ['', ' KB', ' MB', ' GB', ' TB', ' PB'][magnitude])


def conn_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.1f%s' % (num, ['', ' K', ' M', ' B', ' T'][magnitude])


def week_number(week_string):
    return {
        'Feb 2020': 0,
        'Apr 2020': 1,
        'Sept 2020': 2,
        'Sept 2021': 3,
    }[week_string]


def rank_field(rank_string):
    return {
        'Total Bytes': 'Rank_Bytes',
        'Inbound': 'Rank_In',
        'Outbound': 'Rank_Out',
        'Connections': 'Rank_Conns',
        'Source IPs': 'Rank_Sources',
        'Target IPs': 'Rank_Targets',
        'Source Ports': 'Rank_SrcPorts',
        'Target Ports': 'Rank_TrgPorts',
        'Source Subnets': 'SourceSubnet',
        'Target Subnets': 'TargetSubnet'
    }[rank_string]


def rank_title(rank_string):
    return {
        'Total Bytes': 'Rank of Subnets Based on Total Bytes',
        'Inbound': 'Rank of Subnets Based on Inbound Bytes',
        'Outbound': 'Rank of Subnets Based on Outbound Bytes',
        'Connections': 'Rank of Subnets Based on Connections',
        'Source IPs': 'Rank of Subnets Based on Number of Distinct Source IPs',
        'Target IPs': 'Rank of Subnets Based on Number of Distinct Target IPs',
        'Source Ports': 'Rank of Subnets Based on Number of Distinct Source Ports',
        'Target Ports': 'Rank of Subnets Based on Number of Distinct Target Ports',
        'Source Subnets': 'Third Octets of the Subnets',
        'Target Subnets': 'Third Octets of the Subnets'
    }[rank_string]


def graph_type_yaxis(type_string):
    return {
        'TotalBytes': 'Total Bytes',
        'Inbound': 'Inbound Bytes',
        'Outbound': 'Outbound Bytes',
        'Difference': 'Difference Between Inbound and Outbound',
        'Connections': 'Connections',
        'SourceIPs': 'Number of Distinct Source IPs',
        'TargetIPs': 'Number of Distinct Target IPs',
        'SourcePorts': 'Number of Distinct Source Ports',
        'TargetPorts': 'Number of Distinct Target Ports'
    }[type_string]
# endregion


# Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8054)

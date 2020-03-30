import pandas as pd # for dataframe

import random as rand #for scrambling

import numpy as np

#app imports
import dash
import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
 

def show_app(app,  
         #If the port number is busy, change it here! 
             width=700,
             height=350,
             offline=True,
             style=True,
             **dash_flask_kwargs):

    if offline:
        app.css.config.serve_locally = False
        app.scripts.config.serve_locally = False

    return app.run_server(debug=False,  # needs to be false in Jupyter
                          **dash_flask_kwargs)
#Define colum names
column_list = ['B','I','N','G','O']
#Define function to create list of the statements, scramble it and turn into dataframe
def phrases():
    phrases_list = ["hi, who just joined",
               'Can you email that to everyone?',
               'X, are you still there',
                '''Uf, X, you're still sharing''',
               'Guys, I have to jump to another call',
               '(sound of someone typing)... ...possibly with a hammer',
               '(Loud painful echo)',
               '(Child noises)',
               'HI, can you hear me',
                '''No, it's still loading''',
                'Next slide, please',
                'Can everyone go on mute please',
                'Sorry, I was talking on mute',
                'Sorry, go ahead',
                'Sorry, my dog is really excited about this call',
                'So (fades out) I can (cuts out) by (unintelligble), ok?',
                'Sorry, I am double booked',
                'X, your screen just blacked out',
                'Sorry, you cut out there',
                'Can we take this offline',
                '''I'll have to get back to you on that''',
                'Can everyone see my screen',
                'Sorry, I was having connection issues',
                '''sorry, I think there's a lag''',
                'Sorry, the other call ran over',
               ]
    return phrases_list
    

def update_table():
    phrases_list = phrases()
    rand.shuffle(phrases_list)
    phrases_list_1 =  phrases_list[0:5]
    phrases_list_2 = phrases_list[5:10]
    phrases_list_3 = phrases_list[10:15]
    phrases_list_4 = phrases_list[15:20]
    phrases_list_5 = phrases_list[20:]
    df = pd.DataFrame({'B':phrases_list_1,'I':phrases_list_2,'N':phrases_list_3,'G':phrases_list_4,'O':phrases_list_5 })
    data = df.to_dict('records')
    return data


#define app and applayout
app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([
        html.H1('Bingo'), #headline
    ]),
       html.Div([  #instructions
        html.H6('1. When you hear one of the phrases, find it in the table, select it and then type x'),
        html.H6('2. when you get 5 x:es in a row yell BINGO!'),
    ]),
    
    html.Button('Scramble', id='scramble'), #Button to scramble

    
    
    dash_table.DataTable(
        id='datatable',
        columns=[
            {'name': i, 'id': i,} for i in column_list
        ],
        data = update_table(),
        editable=True, #setting editable to true allows the user to replace the text with x
    ),
    
    html.H6('Removed objects in table below'),
    
    dash_table.DataTable(
        id='removed',
        columns=[{'name':'Removed', 'id':'Removed'}],
        data = [{'Removed':'Nothing yet'}, {'Removed':'still nothing'}],
        editable=False, #setting editable to true allows the user to replace the text with x
        style_cell={
        'height': 'auto',
        # all three widths are needed
        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
        'whiteSpace': 'normal'}
    ),
    
])

# callback for scrambling data. a callback needs and input and an output. n-clicks is the input, when button is clicked nclicks change and code runs
# the code changes the data, i.e. data is the output. 

#decorator
@app.callback(
    [Output('datatable', 'data'),
    ]
,
    [Input('scramble','n_clicks'),
    ]
)
#function
def update_table_callback(n):
    data = update_table() 
    return [data]

#callback for keeping track of what was removed
@app.callback(
    [Output('removed', 'data'),
    ]
,
    [Input('datatable','data'),
    ]
)

def compare(data):
    current_list=[]
    current_list=[]
    for di in data:
        for stringtext in di.values():
            current_list.append(stringtext)
    current_list = np.array(current_list)
    allvalues = np.array(phrases())
    non_match = allvalues[np.invert(np.isin(allvalues, current_list))]
    non_match.tolist()
    data_removed = []
    for textstring in non_match:
        data_removed.append({'Removed':textstring})
    return [data_removed]


#start app by using our showapp-function. if fails change the port in the show_app-function
show_app(app, host='0.0.0.0')

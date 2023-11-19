import json
from google.cloud import storage, firestore
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import random
import datetime

# Create a Dash application
app = Dash(__name__, suppress_callback_exceptions=True)

# Create a GCS client
storage_client = storage.Client()

# Create a Firestore client
firestore_client = firestore.Client()

# Update the Firestore collection name
collection_name = 'mi-ejercicio-gcp'

today = datetime.date.today().strftime('%Y-%m-d')

# Function to get data from Firestore
def get_firestore_data():
    docs = firestore_client.collection(collection_name).stream()
    items = [doc.to_dict() for doc in docs]
    return items

# Define the overall layout of the application
app.layout = html.Div([
    html.H1('Navigation Menu'),  # Page title

    # Navigation menu
    dcc.Link('User Form', href='/form'),  # Link to the user form
    html.Br(),  # Line break
    dcc.Link('User Table', href='/user_table'),  # Link to the user table
    html.Br(),  # Line break

    # The content of the pages will be displayed here
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback to load the content of the pages
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/form':
        # If the user navigates to the form, display the form content
        return html.Div([
            html.H1('User Form'),
            dcc.Input(id='name', type='text', placeholder='Name', value=''),
            dcc.Input(id='email', type='email', placeholder='Email', value=''),
            html.Button('Submit', id='submit-button', n_clicks=0),
            html.Div(id='output-container-button', children='Hit the button to update.')
        ])
    elif pathname == '/user_table':
        # If the user navigates to the user table, display the content of the table
        data = get_firestore_data()
        return html.Div([
            html.H1('User Table'),
            dash_table.DataTable(
                columns=[{'name': key, 'id': key} for key in data[0].keys()],
                data=data
            )
        ])

# Route to handle form data submission
@app.callback(
    Output('output-container-button', 'children'),
    [Input('submit-button', 'n_clicks'),
    State('name', 'value'),
    State('email', 'value')]
)
def submit_form(n_clicks, name, email):
    if n_clicks > 0:  # Check if the "Submit" button has been clicked
        # Get data from the form
        user = {
            'ID': random.randint(100000, 999999),
            'Name': name,
            'Email': email,
            'Registration Date': today
        }
        # Save the data in Firestore
        firestore_client.collection(collection_name).add(user)
        return f'Data saved in Firestore: {user}'  # Provide a confirmation
    else:
        return 'Submit button has not been clicked yet'

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
    
    
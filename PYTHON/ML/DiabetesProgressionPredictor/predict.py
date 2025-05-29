# """
# Script for making predictions using a saved model - Jupyter Notebook compatible version
# """

# import joblib
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.datasets import load_diabetes
# import ipywidgets as widgets
# from IPython.display import display, clear_output


# def load_model_and_preprocessors(model_path='output/models/random_forest_tuned.pkl',
#                                 rfe_path='output/models/rfe_selector.pkl',
#                                 scaler_path='output/models/scaler.pkl'):
#     """
#     Load the saved model and preprocessors
    
#     Returns:
#     --------
#     model: estimator
#         The trained model
#     rfe: RFE
#         The RFE feature selector
#     scaler: StandardScaler
#         The scaler for features
#     """
#     try:
#         model = joblib.load(model_path)
#         rfe = joblib.load(rfe_path)
#         scaler = joblib.load(scaler_path)
#         return model, rfe, scaler
#     except FileNotFoundError as e:
#         print(f"Error loading model or preprocessors: {str(e)}")
#         print("Make sure you've run advanced.py first to train and save the models.")
#         return None, None, None


# def predict_progression(features, model, rfe, scaler):
#     """
#     Make a prediction for a single patient
    
#     Parameters:
#     -----------
#     features: array-like
#         The patient features
#     model: estimator
#         The trained model
#     rfe: RFE
#         The RFE feature selector
#     scaler: StandardScaler
#         The scaler for features
        
#     Returns:
#     --------
#     prediction: float
#         The predicted disease progression
#     """
#     # Apply feature selection
#     features_rfe = rfe.transform(features)
    
#     # Apply scaling
#     features_scaled = scaler.transform(features_rfe)
    
#     # Make prediction
#     prediction = model.predict(features_scaled)
    
#     return prediction[0]


# # Function for Jupyter interactive prediction
# def create_prediction_widgets():
#     """
#     Create interactive widgets for entering patient data in Jupyter
#     """
#     # Get feature names from the diabetes dataset
#     diabetes = load_diabetes()
#     feature_names = diabetes.feature_names
    
#     # Create sliders for each feature with appropriate ranges
#     feature_ranges = {
#         'age': (-0.1, 0.2, 0.01),      # Normalized age 
#         'sex': (-0.05, 0.05, 0.001),   # Gender
#         'bmi': (-0.1, 0.15, 0.01),     # Body mass index
#         'bp': (-0.1, 0.15, 0.01),      # Blood pressure
#         's1': (-0.1, 0.15, 0.01),      # Total serum cholesterol
#         's2': (-0.1, 0.15, 0.01),      # Low-density lipoproteins
#         's3': (-0.1, 0.15, 0.01),      # High-density lipoproteins
#         's4': (-0.1, 0.15, 0.01),      # Total cholesterol / HDL
#         's5': (-0.1, 0.15, 0.01),      # Log of serum triglycerides level
#         's6': (-0.1, 0.15, 0.01),      # Blood sugar level
#     }
    
#     widgets_dict = {}
#     for name in feature_names:
#         min_val, max_val, step = feature_ranges[name]
#         widgets_dict[name] = widgets.FloatSlider(
#             value=0,
#             min=min_val,
#             max=max_val,
#             step=step,
#             description=name,
#             disabled=False,
#             continuous_update=False,
#             orientation='horizontal',
#             readout=True,
#             readout_format='.3f',
#             layout=widgets.Layout(width='500px')
#         )
    
#     # Create predict button
#     predict_button = widgets.Button(
#         description='Predict',
#         disabled=False,
#         button_style='success',
#         tooltip='Click to predict',
#         icon='check'
#     )
    
#     # Create output widget for displaying results
#     output = widgets.Output()
    
#     return widgets_dict, predict_button, output


# def run_jupyter_prediction():
#     """
#     Run the prediction tool in Jupyter Notebook
#     """
#     # Load model and preprocessors
#     print("Loading model and preprocessors...")
#     model, rfe, scaler = load_model_and_preprocessors()
    
#     if model is None:
#         return
    
#     print("Model loaded successfully!")
    
#     # Create widgets
#     feature_widgets, predict_button, output = create_prediction_widgets()
    
#     # Display widgets
#     print("Enter patient information using the sliders below:")
#     for widget in feature_widgets.values():
#         display(widget)
#     display(predict_button)
#     display(output)
    
#     # Define button click handler
#     def on_button_clicked(b):
#         # Get values from widgets
#         features = {name: widget.value for name, widget in feature_widgets.items()}
        
#         # Convert to DataFrame
#         patient_data = pd.DataFrame([features])
        
#         # Make prediction
#         progression = predict_progression(patient_data, model, rfe, scaler)
        
#         # Clear previous output and display result
#         with output:
#             clear_output()
#             print("\n=== Prediction ===")
#             print(f"Predicted disease progression: {progression:.2f}")
#             print("Note: Higher values indicate more severe disease progression.")
    
#     # Connect button to handler
#     predict_button.on_click(on_button_clicked)


# # Function to create a basic version without ipywidgets (fallback)
# def simple_jupyter_prediction():
#     """
#     Simple prediction function for Jupyter that doesn't rely on ipywidgets
#     """
#     # Load model and preprocessors
#     print("Loading model and preprocessors...")
#     model, rfe, scaler = load_model_and_preprocessors()
    
#     if model is None:
#         return
        
#     print("Model loaded successfully!")
    
#     # Get feature names
#     diabetes = load_diabetes()
#     feature_names = diabetes.feature_names
    
#     # Create a dictionary with default values
#     default_values = {name: 0.0 for name in feature_names}
    
#     # Display information
#     print("\n===== Diabetes Progression Predictor =====")
#     print("Default feature values (these are normalized values):")
#     for name, value in default_values.items():
#         print(f"{name}: {value}")
    
#     print("\nTo make a prediction, modify the feature values in this cell:")
#     print("features = {")
#     for name in feature_names:
#         print(f"    '{name}': 0.0,  # Replace with your value")
#     print("}")
    
#     # Provide example code for making prediction
#     print("\nThen run:")
#     print("patient_data = pd.DataFrame([features])")
#     print("progression = predict_progression(patient_data, model, rfe, scaler)")
#     print("print(f'Predicted disease progression: {progression:.2f}')")


# # Determine if ipywidgets is available
# def check_ipywidgets():
#     try:
#         import ipywidgets
#         return True
#     except ImportError:
#         return False


# # Main function to choose appropriate version
# def main_jupyter():
#     """
#     Main function for Jupyter notebook
#     """
#     if check_ipywidgets():
#         run_jupyter_prediction()
#     else:
#         print("ipywidgets not available. Using simple mode.")
#         simple_jupyter_prediction()


# # This will execute when the cell is run in Jupyter
# main_jupyter()


"""
Diabetes Prediction with Linear Regression - Jupyter Notebook version
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML

# Function to load and prepare data
def prepare_data():
    # Load the diabetes dataset
    diabetes = load_diabetes()
    X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
    y = pd.Series(diabetes.target, name="target")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=45)
    
    # Apply RFE for feature selection
    model = LinearRegression()
    rfe = RFE(estimator=model, n_features_to_select=6)
    rfe.fit(X_train, y_train)
    X_train_rfe = rfe.transform(X_train)
    
    # Apply scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_rfe)
    
    # Train the model
    model.fit(X_train_scaled, y_train)
    
    # Get selected features
    selected_features = X.columns[rfe.support_]
    
    return model, rfe, scaler, selected_features

def predict_progression(features, model, rfe, scaler):
    """
    Make a prediction for a single patient
    
    Parameters:
    -----------
    features: array-like
        The patient features
    model: estimator
        The trained model
    rfe: RFE
        The RFE feature selector
    scaler: StandardScaler
        The scaler for features
        
    Returns:
    --------
    prediction: float
        The predicted disease progression
    """
    # Apply feature selection
    features_rfe = rfe.transform(features)
    
    # Apply scaling
    features_scaled = scaler.transform(features_rfe)
    
    # Make prediction
    prediction = model.predict(features_scaled)
    
    return prediction[0]

# Function for Jupyter interactive prediction
def create_prediction_widgets():
    """
    Create interactive widgets for entering patient data in Jupyter
    """
    # Get feature names from the diabetes dataset
    diabetes = load_diabetes()
    feature_names = diabetes.feature_names
    
    # More descriptive labels and ranges for each feature
    feature_info = {
        'age': {
            'description': 'Age',
            'long_desc': 'Patient age (normalized)',
            'min': -0.1, 'max': 0.2, 'step': 0.01
        },
        'sex': {
            'description': 'Sex',
            'long_desc': 'Patient gender (male/female)',
            'options': [('Male', 0.05), ('Female', -0.05)]  # Values based on dataset normalization
        },
        'bmi': {
            'description': 'BMI',
            'long_desc': 'Body Mass Index (weight/height²)',
            'min': -0.1, 'max': 0.15, 'step': 0.01
        },
        'bp': {
            'description': 'Blood Pressure',
            'long_desc': 'Average blood pressure',
            'min': -0.1, 'max': 0.15, 'step': 0.01
        },
        's1': {
            'description': 'Total Cholesterol',
            'long_desc': 'Total serum cholesterol',
            'min': -0.1, 'max': 0.15, 'step': 0.01
        },
        's2': {
            'description': 'LDL',
            'long_desc': 'Low-density lipoproteins',
            'min': -0.1, 'max': 0.15, 'step': 0.01
        },
        's3': {
            'description': 'HDL',
            'long_desc': 'High-density lipoproteins',
            'min': -0.1, 'max': 0.15, 'step': 0.01
        },
        's4': {
            'description': 'TCH/HDL',
            'long_desc': 'Total cholesterol / HDL',
            'min': -0.1, 'max': 0.15, 'step': 0.01
        },
        's5': {
            'description': 'Triglycerides',
            'long_desc': 'Log of serum triglycerides level',
            'min': -0.1, 'max': 0.15, 'step': 0.01
        },
        's6': {
            'description': 'Blood Sugar',
            'long_desc': 'Blood sugar level',
            'min': -0.1, 'max': 0.15, 'step': 0.01
        }
    }
    
    widgets_dict = {}
    
    # Create a container for each parameter with a label
    for name in feature_names:
        info = feature_info[name]
        
        # Create a container for the parameter
        container = widgets.VBox()
        
        # Add a label with description
        label = widgets.HTML(
            value=f"<b>{info['description']}</b><br><small>{info['long_desc']}</small>",
            layout=widgets.Layout(width='300px')
        )
        
        # For sex, create a dropdown
        if name == 'sex':
            widget = widgets.Dropdown(
                options=info['options'],
                value=info['options'][0][1],
                description='',
                disabled=False,
                layout=widgets.Layout(width='150px')
            )
        else:
            # For numeric values, create a numeric input with up/down arrows
            widget = widgets.FloatText(
                value=0.0,
                min=info['min'],
                max=info['max'],
                step=info['step'],
                description='',
                disabled=False,
                layout=widgets.Layout(width='150px')
            )
        
        # Store the widget for later access
        widgets_dict[name] = widget
        
        # Combine label and widget horizontally
        container.children = [label, widget]
        widgets_dict[f"{name}_container"] = container
    
    # Create predict button
    predict_button = widgets.Button(
        description='Predict',
        disabled=False,
        button_style='success',
        tooltip='Click to predict',
        icon='check',
        layout=widgets.Layout(width='200px', margin='20px 0 0 0')
    )
    
    # Create output widget for displaying results
    output = widgets.Output()
    
    return widgets_dict, predict_button, output

def run_jupyter_prediction(model, rfe, scaler, selected_features):
    """
    Run the prediction tool in Jupyter Notebook
    """
    # Header
    display(HTML("<h2>Diabetes Progression Predictor</h2>"))
    display(HTML("<p>Adjust the values below to predict diabetes progression. The features are normalized values from the diabetes dataset.</p>"))
    display(HTML(f"<p>Selected features by Linear Regression model: {', '.join(selected_features)}</p>"))
    
    # Create widgets
    feature_widgets, predict_button, output = create_prediction_widgets()
    
    # Create a grid layout for the features
    feature_containers = [feature_widgets[f"{name}_container"] for name in load_diabetes().feature_names]
    
    # Split into two columns
    col1 = widgets.VBox(feature_containers[:5])
    col2 = widgets.VBox(feature_containers[5:])
    
    # Create the layout
    layout = widgets.HBox([col1, col2])
    
    # Display the widgets
    display(layout)
    display(predict_button)
    display(output)
    
    # Define button click handler
    def on_button_clicked(b):
        # Get values from widgets
        features = {name: feature_widgets[name].value for name in load_diabetes().feature_names}
        
        # Convert to DataFrame
        patient_data = pd.DataFrame([features])
        
        # Make prediction
        progression = predict_progression(patient_data, model, rfe, scaler)
        
        # Determine severity level
        if progression < 100:
            severity = "Low"
            color = "green"
        elif progression < 200:
            severity = "Moderate"
            color = "orange"
        else:
            severity = "High"
            color = "red"
        
        # Clear previous output and display result
        with output:
            clear_output()
            display(HTML(f"""
                <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin: 10px 0;">
                    <h3>Prediction Result</h3>
                    <p>Predicted diabetes progression: <b>{progression:.2f}</b></p>
                    <p>Severity level: <span style="color: {color}; font-weight: bold;">{severity}</span></p>
                    <p><small>Note: Higher values indicate more severe disease progression.</small></p>
                </div>
            """))
            
            # Display feature importance info
            display(HTML(f"""
                <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin: 10px 0;">
                    <h3>Feature Importance</h3>
                    <p>The most important features for prediction (selected by RFE):</p>
                    <ul>
                        {"".join(f"<li>{feature}</li>" for feature in selected_features)}
                    </ul>
                </div>
            """))
    
    # Connect button to handler
    predict_button.on_click(on_button_clicked)

# Main function to run in Jupyter
def main_jupyter():
    """
    Main function for Jupyter notebook
    """
    print("Training Linear Regression model...")
    model, rfe, scaler, selected_features = prepare_data()
    print("Model training complete.")
    print(f"Selected features: {selected_features}")
    
    try:
        import ipywidgets
        run_jupyter_prediction(model, rfe, scaler, selected_features)
    except ImportError:
        print("ipywidgets not available. Can't create interactive interface.")

# This will execute when the cell is run in Jupyter
main_jupyter()
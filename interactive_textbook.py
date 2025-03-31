import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import io
from contextlib import redirect_stdout
import sys
import traceback

def app():
    st.title("Interactive Coding Laboratory")
    
    st.markdown("""
    ## Learn by Coding: Physical Pharmacy Concepts
    
    This interactive coding laboratory allows you to modify and execute Python code directly in your browser. 
    Each section focuses on a key concept from the laboratory course, with examples you can modify and execute 
    to deepen your understanding.
    
    Choose a topic below to get started:
    """)
    
    # Topic selection
    topic = st.selectbox(
        "Select a topic:",
        ["Standard Curve Generation", 
         "Higuchi Model Implementation",
         "Diffusion Coefficient Calculation",
         "Sink Condition Analysis"]
    )
    
    # Display the selected topic content
    if topic == "Standard Curve Generation":
        standard_curve_lesson()
    elif topic == "Higuchi Model Implementation":
        higuchi_model_lesson()
    elif topic == "Diffusion Coefficient Calculation":
        diffusion_coefficient_lesson()
    elif topic == "Sink Condition Analysis":
        sink_condition_lesson()

def execute_code(code_string):
    """
    Safely execute the provided code string and capture its output
    """
    # Create string buffer to capture print statements
    buffer = io.StringIO()
    
    # Dictionary to store variables that will be returned for plotting or further use
    output_vars = {}
    
    try:
        # Execute the code with stdout redirected to our buffer
        with redirect_stdout(buffer):
            # Create a local environment with necessary imports
            exec_globals = {
                'np': np,
                'pd': pd,
                'plt': plt,
                'px': px,
                'go': go,
                'stats': stats,
                'output_vars': output_vars
            }
            
            # Execute the code
            exec(code_string, exec_globals)
            
            # Save any variables the user assigned to output_vars dictionary
            output_vars = exec_globals['output_vars']
        
        # Get the printed output
        output = buffer.getvalue()
        
        return True, output, output_vars
    
    except Exception as e:
        # Return the error message
        error_msg = traceback.format_exc()
        return False, error_msg, {}
    
    finally:
        buffer.close()

def standard_curve_lesson():
    st.header("Standard Curve Generation and Analysis")
    
    st.markdown("""
    A standard curve is a critical component of quantitative analysis in pharmacy. It allows you to:
    
    1. Convert measured absorbance values to concentrations
    2. Ensure the linearity of your detection method
    3. Calculate unknown concentrations from measured signals
    
    ### The Beer-Lambert Law
    
    The Beer-Lambert law states that absorbance is directly proportional to concentration:
    
    $$A = \\varepsilon \\cdot c \\cdot l$$
    
    Where:
    - $A$ is the absorbance (no units)
    - $\\varepsilon$ is the molar absorptivity (L·mol⁻¹·cm⁻¹)
    - $c$ is the concentration (mol·L⁻¹)
    - $l$ is the path length (cm)
    
    In practice, we often express this as:
    
    $$A = m \\cdot c + b$$
    
    Where $m$ is the slope and $b$ is the y-intercept of our standard curve.
    """)
    
    # Initial code example
    initial_code = """# Creating a standard curve for Lidocaine HCl
# STEP 1: Import required libraries
import numpy as np # numerical operations
import pandas as pd # data manipulation
import plotly.express as px # interactive plotting
from scipy import stats # statistical functions

# STEP 2: Define standard concentrations for the calibration curve
concentrations = np.array([20, 100, 200, 300, 500])

# STEP 3: Create simulated absorbance values based on Beer-Lambert law
np.random.seed(42)  # For reproducibility
absorbance = 0.0018 * concentrations + 0.01 + np.random.normal(0, 0.01, len(concentrations)) # A = ε·c + b (where ε is approximately 0.0018 and b is 0.01)

# STEP 4: Organize data into a structured DataFrame
data = pd.DataFrame({
    'Concentration (μg/ml)': concentrations,
    'Absorbance': absorbance
})

# STEP 5: Perform linear regression to create the standard curve
slope, intercept, r_value, p_value, std_err = stats.linregress(concentrations, absorbance)
r_squared = r_value ** 2

# Print results
print(f"Regression equation: Absorbance = {slope:.6f} × Concentration + {intercept:.6f}")
print(f"R² value: {r_squared:.6f}")

# STEP 6: Create visualization of the standard curve
fig = px.scatter(data, x='Concentration (μg/ml)', y='Absorbance',
                title='Standard Curve for Lidocaine HCl')

# STEP 7: Add the regression line to the plot
x_range = np.linspace(0, max(concentrations) * 1.1, 100)
y_pred = intercept + slope * x_range

fig.add_scatter(x=x_range, y=y_pred, mode='lines', name='Linear Regression',
               line=dict(color='red'))

# STEP 8: Add the equation and R² to the plot
fig.add_annotation(
    x=max(concentrations) * 0.6,
    y=max(absorbance) * 0.2,
    text=f"y = {slope:.6f}x + {intercept:.6f}<br>R² = {r_squared:.6f}",
    showarrow=False,
    font=dict(size=12)
)

# Store the figure in output_vars for display
output_vars['fig'] = fig

# STEP 9: Calculate an unknown concentration from a measured absorbance
unknown_absorbance = 0.45
unknown_concentration = (unknown_absorbance - intercept) / slope
print(f"\\nFor an absorbance of {unknown_absorbance}, the calculated concentration is {unknown_concentration:.2f} μg/ml")
"""

    # Create an editable text area with the initial code
    user_code = st.text_area("Modify the code and hit Execute to see the results:", 
                            value=initial_code, height=400)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Execute button
        execute_button = st.button("Execute Code")
    
    with col2:
        # Add hints and challenges
        with st.expander("Ideas to try!"):
            st.markdown("""
            **Try modifying:**
            - Change the concentrations to those used for Salicylic Acid (5-30 μg/ml)
            - Increase or decrease the noise level (change 0.01 to another value)
            - Test how outliers affect the R² value (modify one absorbance value significantly)
            
            **Challenges:**
            1. Add error bars to the plot (standard deviation of triplicate measurements)
            2. Calculate and print the limit of detection (LOD = 3.3 × σ/slope)
            3. Determine if an unknown sample with absorbance 1.2 is within the linear range
            """)
    
    if execute_button:
        # Execute the code and display results
        success, output, output_vars = execute_code(user_code)
        
        if success:
            # Display any printed output
            if output:
                st.subheader("Output:")
                st.text(output)
            
            # Display any figures generated
            if 'fig' in output_vars:
                st.plotly_chart(output_vars['fig'], use_container_width=True)
        else:
            # Display error message
            st.error("Error in your code:")
            st.code(output)
    
    # Include a discussion section
    st.subheader("Discussion")
    st.markdown("""
    ### Key Concepts to Understand:
    
    1. **Linearity**: A good standard curve should be linear within your working range. This is 
       quantified by R², which should be ≥ 0.99 for analytical methods.
    
    2. **Sensitivity**: The slope of the line indicates how much change in signal (absorbance) 
       you get for a change in concentration. Higher sensitivity means better detection of small
       concentration differences.
    
    3. **Range**: The standard curve is only valid within the range of concentrations used to create it.
       Extrapolating beyond this range can lead to significant errors.
    
    4. **Precision**: The scatter of points around the regression line indicates the precision of your method.
       Lower scatter means better precision.
    
    ### Why This Matters in Pharmacy:
    
    Understanding standard curves is essential for:
    - Quality control of pharmaceutical products
    - Bioanalytical method validation
    - Drug release studies from formulations
    - Pharmacokinetic studies
    """)

def higuchi_model_lesson():
    st.header("Higuchi Model Implementation")
    
    st.markdown("""
    ### The Higuchi Model for Drug Release
    
    The Higuchi model is one of the most widely used mathematical models to describe drug release from 
    matrix systems, including semi-solid formulations. It describes drug release as a diffusion process 
    based on Fick's first law.
    
    The simplified Higuchi equation states:
    
    $$Q = k_H \\sqrt{t}$$
    
    Where:
    - $Q$ is the cumulative amount of drug released per unit area (mg/cm²)
    - $k_H$ is the Higuchi dissolution constant
    - $t$ is time
    
    For matrix systems, the Higuchi constant can be expanded to:
    
    $$k_H = \\sqrt{D \\cdot C_s \\cdot (2C_0 - C_s)}$$
    
    Where:
    - $D$ is the diffusion coefficient of the drug in the matrix
    - $C_s$ is the solubility of the drug in the matrix
    - $C_0$ is the initial drug concentration in the matrix
    
    ### Implementing the Higuchi Model
    """)
    
    # Initial code example
    initial_code = """# Implementing the Higuchi model for drug release
# STEP 1: Import packages as before 
import numpy as np
import pandas as pd
import plotly.express as px
from scipy import stats

# STEP 2: Set up time points for simulation (0-120 min, as in lab protocol)
time_points = np.linspace(0, 120, 50)  # Time in minutes
sqrt_time = np.sqrt(time_points) # Square root of time for Higuchi model

# STEP 3: Define Higuchi constant (k_H) - key parameter that determines release rate
k_H = 0.05  # Higuchi constant (units: fraction released per √min)

# STEP 4: Apply Higuchi equation: Q = k_H * sqrt(t), a mathematical model for diffusion-controlled release
# Q = k_H * sqrt(t)
release_fraction = k_H * sqrt_time

# STEP 5: Add some experimental noise (to simulate real data)
np.random.seed(42)
noise = np.random.normal(0, 0.02, len(time_points))
experimental_release = release_fraction + noise
experimental_release = np.maximum(0, np.minimum(experimental_release, 1.0))  # Constrain between 0 and 1

# STEP 6: Organize all data into a structured dataframe
data = pd.DataFrame({
    'Time (min)': time_points,
    'Square Root of Time': sqrt_time,
    'Theoretical Release (fraction)': release_fraction,
    'Experimental Release (fraction)': experimental_release,
    'Experimental Release (%)': experimental_release * 100
})

# Print a sample of the data
print(data.head())

# STEP 7: Calculate the R² value for how well experimental data fits the Higuchi model
# We'll use the relationship between experimental release and square root of time
slope, intercept, r_value, p_value, std_err = stats.linregress(
    data['Square Root of Time'], 
    data['Experimental Release (fraction)']
)
r_squared = r_value ** 2

print(f"\\nLinear regression on experimental data:")
print(f"Higuchi constant (from slope): {slope:.6f}")
print(f"R² value: {r_squared:.6f}")

# STEP 8: Create plots
# 1. Standard time plot (shows curved release profile)
fig1 = px.line(data, x='Time (min)', y=['Theoretical Release (fraction)', 'Experimental Release (fraction)'],
              title='Drug Release vs Time')

# 2. Higuchi plot (should show linear relationship if model fits)
fig2 = px.scatter(data, x='Square Root of Time', y='Experimental Release (fraction)',
                 title='Higuchi Plot (Release vs √Time)')

# 3. Add regression line to Higuchi plot
x_range = np.linspace(0, max(data['Square Root of Time']), 100)
y_pred = intercept + slope * x_range

fig2.add_scatter(x=x_range, y=y_pred, mode='lines', name='Linear Regression',
                line=dict(color='red'))

# 4. Display equation and R² on the Higuchi plot
fig2.add_annotation(
    x=max(data['Square Root of Time']) * 0.6,
    y=max(data['Experimental Release (fraction)']) * 0.2,
    text=f"y = {slope:.6f}x + {intercept:.6f}<br>R² = {r_squared:.6f}",
    showarrow=False,
    font=dict(size=12)
)

# Store figures for display
output_vars['fig1'] = fig1
output_vars['fig2'] = fig2
"""

    # Create an editable text area with the initial code
    user_code = st.text_area("Modify the code and hit Execute to see the results:", 
                            value=initial_code, height=400)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Execute button
        execute_button = st.button("Execute Code")
    
    with col2:
        # Add hints and challenges
        with st.expander("Ideas to try!"):
            st.markdown("""
            **Try modifying:**
            - Change the Higuchi constant (k_H) to model faster or slower drug release
            - Modify the noise level to simulate different experimental conditions
            - Add a second formulation with a different release rate for comparison
            
            **Challenges:**
            1. Calculate the time required to reach 50% drug release (t₅₀)
            2. Implement the full Higuchi equation with diffusion coefficient (D), solubility (Cs), and initial concentration (C0)
            3. Compare both zero-order and Higuchi models to determine which better fits the data
            """)
    
    if execute_button:
        # Execute the code and display results
        success, output, output_vars = execute_code(user_code)
        
        if success:
            # Display any printed output
            if output:
                st.subheader("Output:")
                st.text(output)
            
            # Display any figures generated
            if 'fig1' in output_vars:
                st.plotly_chart(output_vars['fig1'], use_container_width=True)
            
            if 'fig2' in output_vars:
                st.plotly_chart(output_vars['fig2'], use_container_width=True)
        else:
            # Display error message
            st.error("Error in your code:")
            st.code(output)
    
    # Include a discussion section
    st.subheader("Discussion")
    st.markdown("""
    ### Understanding the Higuchi Model in Practice:
    
    1. **Square Root Time Dependence**: The Higuchi model predicts that drug release is proportional to the square root of time, 
       not time itself. This distinguishes it from zero-order (linear with time) or first-order (logarithmic with time) kinetics.
    
    2. **Physical Meaning**: The model describes a process where the drug must diffuse through an increasingly thick layer 
       of depleted matrix, which explains the decreasing release rate over time.
    
    3. **Assumptions**: The Higuchi model assumes:
       - The initial drug concentration is much higher than drug solubility (C₀ >> Cs)
       - Drug diffusion is the rate-limiting step
       - Perfect sink conditions are maintained
       - The matrix does not swell or dissolve
    
    4. **Limitations**: The model typically applies to the first 60% of drug release. Beyond this point, 
       other factors may become significant.
    
    ### Applications in Pharmacy:
    
    - Characterization of topical formulations (creams, ointments, gels)
    - Development of controlled-release matrix tablets
    - Quality control of transdermal delivery systems
    - Comparison of different formulation strategies
    """)

def diffusion_coefficient_lesson():
    st.header("Diffusion Coefficient Calculation")
    
    st.markdown("""
    ### Diffusion in Pharmaceutical Systems
    
    Diffusion is a fundamental process in drug delivery that governs how drug molecules move through different media.
    The diffusion coefficient (D) is a measure of how quickly molecules can move in a specific environment.
    
    ### Fick's First Law of Diffusion
    
    Fick's first law states that the flux of material is proportional to the concentration gradient:
    
    $$J = -D \\frac{dC}{dx}$$
    
    Where:
    - $J$ is the diffusion flux (amount of substance per unit area per unit time)
    - $D$ is the diffusion coefficient
    - $\\frac{dC}{dx}$ is the concentration gradient
    
    ### Calculating Diffusion Coefficient from Experimental Data
    
    For a slab geometry (like in the Freiburger Schnecke), the diffusion coefficient can be calculated using:
    
    $$D = \\frac{k_H^2 \\pi h^2}{2C_0^2}$$
    
    Where:
    - $k_H$ is the Higuchi constant
    - $h$ is the thickness of the formulation
    - $C_0$ is the initial drug concentration
    """)
    
    # Initial code example
    initial_code = """# Calculating diffusion coefficients from drug release data
# Step 1: Import required libraries for calculations and visualization
import numpy as np
import pandas as pd
import plotly.express as px
from scipy import stats

# Step 2: Set up experimental parameters matching lab conditions
formulation_thickness = 0.2  # cm
initial_drug_conc = 20     # mg/cm³ (assuming 2% w/v)

# Step 3: Define time points and calculate square roots (for Higuchi analysis)
time_points = np.array([15, 30, 60, 90, 120])
sqrt_time = np.sqrt(time_points)

# Step 4: Input release data for different formulations (as fractions of total)
release_formulation1 = np.array([0.12, 0.18, 0.25, 0.31, 0.35])  # Base II (Hydrogel)
release_formulation2 = np.array([0.05, 0.08, 0.12, 0.15, 0.17])  # Base III (Oleogel)

# Step 5: Calculate Higuchi constants by linear regression (slope of release vs. √time)
slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(sqrt_time, release_formulation1)
slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(sqrt_time, release_formulation2)

# Step 6: Define function to convert Higuchi constants to diffusion coefficients
def calculate_diffusion_coeff(k_H, thickness, initial_conc):
    # Convert units: k_H from fraction/√min to mg/(cm²·√min)
    k_H_converted = k_H * initial_conc * thickness
    
    # D = (k_H² * π * h²) / (2 * C₀²)
    D = (k_H_converted**2 * np.pi * thickness**2) / (2 * initial_conc**2)
    
    # Convert to cm²/s (from cm²/min)
    D = D / 60
    
    return D

# Step 7: Calculate diffusion coefficients for both formulations
D1 = calculate_diffusion_coeff(slope1, formulation_thickness, initial_drug_conc)
D2 = calculate_diffusion_coeff(slope2, formulation_thickness, initial_drug_conc)

# Step 8: Display results and compare formulations
print(f"Formulation 1 (Hydrogel):")
print(f"  Higuchi constant: {slope1:.4f} fraction/√min")
print(f"  R² value: {r_value1**2:.4f}")
print(f"  Diffusion coefficient: {D1:.3e} cm²/s")

print(f"\\nFormulation 2 (Oleogel):")
print(f"  Higuchi constant: {slope2:.4f} fraction/√min")
print(f"  R² value: {r_value2**2:.4f}")
print(f"  Diffusion coefficient: {D2:.3e} cm²/s")

print(f"\\nRatio of diffusion coefficients (D1/D2): {D1/D2:.2f}")

# Step 9: Create Higuchi plot comparing both formulations
data = pd.DataFrame({
    'Square Root of Time': np.concatenate([sqrt_time, sqrt_time]),
    'Release Fraction': np.concatenate([release_formulation1, release_formulation2]),
    'Formulation': ['Hydrogel']*len(time_points) + ['Oleogel']*len(time_points)
})

fig = px.scatter(data, x='Square Root of Time', y='Release Fraction', color='Formulation',
                title='Higuchi Plot for Different Formulations')

# Step 10: Add regression lines to visualize different release rates
x_range = np.linspace(0, max(sqrt_time), 100)

fig.add_scatter(x=x_range, y=intercept1 + slope1 * x_range,
               mode='lines', name='Hydrogel Regression',
               line=dict(color='blue', dash='dash'))

fig.add_scatter(x=x_range, y=intercept2 + slope2 * x_range,
               mode='lines', name='Oleogel Regression',
               line=dict(color='red', dash='dash'))

# Step 11: Prepare Higuchi plot for display
output_vars['fig'] = fig

# Step 12: Create bar chart to visually compare diffusion coefficients
diff_data = pd.DataFrame({
    'Formulation': ['Hydrogel', 'Oleogel'],
    'Diffusion Coefficient (cm²/s)': [D1, D2]
})

fig2 = px.bar(diff_data, x='Formulation', y='Diffusion Coefficient (cm²/s)', 
             title='Comparison of Diffusion Coefficients',
             log_y=True)  # Log scale due to potentially large differences

output_vars['fig2'] = fig2
"""

    # Create an editable text area with the initial code
    user_code = st.text_area("Modify the code and hit Execute to see the results:", 
                            value=initial_code, height=400)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Execute button
        execute_button = st.button("Execute Code")
    
    with col2:
        # Add hints and challenges
        with st.expander("Ideas to try!"):
            st.markdown("""
            **Try modifying:**
            - Change the release data to simulate different formulations
            - Modify the formulation thickness to see how it affects diffusion
            - Change the initial drug concentration
            
            **Challenges:**
            1. Add a third formulation (e.g., emulsion cream) for comparison
            2. Calculate the time required for 50% release for each formulation
            3. Implement a full calculation that accounts for drug solubility in the vehicle
            """)
    
    if execute_button:
        # Execute the code and display results
        success, output, output_vars = execute_code(user_code)
        
        if success:
            # Display any printed output
            if output:
                st.subheader("Output:")
                st.text(output)
            
            # Display any figures generated
            if 'fig' in output_vars:
                st.plotly_chart(output_vars['fig'], use_container_width=True)
            
            if 'fig2' in output_vars:
                st.plotly_chart(output_vars['fig2'], use_container_width=True)
        else:
            # Display error message
            st.error("Error in your code:")
            st.code(output)
    
    # Include a discussion section
    st.subheader("Discussion")
    st.markdown("""
    ### Understanding Diffusion Coefficients:
    
    1. **Orders of Magnitude**: Typical diffusion coefficients in pharmaceutical systems:
       - In water: 10⁻⁵ to 10⁻⁶ cm²/s
       - In hydrogels: 10⁻⁶ to 10⁻⁷ cm²/s
       - In lipid matrices: 10⁻⁸ to 10⁻¹⁰ cm²/s
    
    2. **Factors Affecting Diffusion**:
       - **Temperature**: Higher temperatures increase diffusion (Arrhenius relationship)
       - **Molecular Size**: Larger molecules diffuse more slowly
       - **Medium Viscosity**: Higher viscosity decreases diffusion rate
       - **Interactions**: Chemical interactions between drug and matrix can slow diffusion
    
    3. **Stokes-Einstein Equation**: Relates diffusion to molecular size and medium viscosity:
    
       $$D = \\frac{k_B T}{6 \\pi \\eta r}$$
       
       Where:
       - $k_B$ is Boltzmann's constant
       - $T$ is temperature
       - $\\eta$ is viscosity
       - $r$ is the hydrodynamic radius of the diffusing molecule
    
    ### Pharmaceutical Implications:
    
    - **Formulation Design**: Use diffusion coefficients to predict drug release rates
    - **Bioavailability**: Faster diffusion generally leads to higher bioavailability for topical products
    - **Stability**: Understanding diffusion helps predict drug stability in formulations
    - **Quality Control**: Measure diffusion coefficients to ensure batch-to-batch consistency
    """)

def sink_condition_lesson():
    st.header("Sink Condition Analysis")
    
    st.markdown("""
    ### Understanding Sink Conditions
    
    Sink conditions are an important concept in drug dissolution and release testing. They refer to 
    maintaining a low concentration of drug in the release medium to ensure maximum dissolution rate.
    
    ### Definition of Sink Conditions
    
    Sink conditions are generally maintained when:
    
    $$C_m \\leq \\frac{C_s}{3} \\ \\text{to} \\ \\frac{C_s}{10}$$
    
    Where:
    - $C_m$ is the maximum concentration of drug in the release medium
    - $C_s$ is the saturation solubility of the drug in the release medium
    
    ### Why Sink Conditions Matter
    
    1. **Driving Force**: The concentration gradient is the driving force for diffusion-controlled release
    2. **Reliable Data**: Ensures that release rate is not artificially limited by solubility
    3. **In Vivo Relevance**: Better mimics physiological conditions where drug is constantly removed
    
    ### Analyzing Sink Conditions in a Release Study
    """)
    
    # Initial code example
    initial_code = """# Analyzing sink conditions in a drug release study
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Experimental parameters
medium_volume = 150  # ml
formulation_weight = 1.0  # g
drug_concentration = 2.0  # % w/w
drug_solubility = 680  # μg/ml (for Lidocaine HCl in buffer)

# Calculate total drug amount in the formulation
total_drug_mg = formulation_weight * drug_concentration * 10  # convert % to mg
print(f"Total drug in formulation: {total_drug_mg:.2f} mg")

# Example release data (time in minutes, cumulative release in μg/ml)
time_points = np.array([15, 30, 60, 90, 120])
concentration_data = np.array([20.5, 35.8, 62.4, 85.9, 102.3])  # μg/ml

# Calculate the percentage of solubility at each time point
solubility_percentage = (concentration_data / drug_solubility) * 100

# Calculate cumulative drug release
drug_released_mg = concentration_data * medium_volume / 1000  # convert μg to mg
release_percentage = (drug_released_mg / total_drug_mg) * 100

# Create a dataframe with all calculations
data = pd.DataFrame({
    'Time (min)': time_points,
    'Concentration (μg/ml)': concentration_data,
    'Drug Released (mg)': drug_released_mg,
    'Release (%)': release_percentage,
    'Percent of Solubility (%)': solubility_percentage,
    'Sink Conditions': ['Maintained' if p <= 30 else 'Not Maintained' for p in solubility_percentage]
})

# Print the data
print("\\nRelease data analysis:")
print(data)

# Evaluate overall sink conditions
max_conc = max(concentration_data)
max_percent_solubility = max(solubility_percentage)

print(f"\\nMaximum concentration: {max_conc:.2f} μg/ml")
print(f"Maximum percentage of solubility: {max_percent_solubility:.2f}%")

if max_percent_solubility <= 10:
    print("Strict sink conditions (≤ 10% of solubility) were maintained throughout the experiment.")
elif max_percent_solubility <= 30:
    print("Acceptable sink conditions (≤ 30% of solubility) were maintained throughout the experiment.")
else:
    print("Sink conditions were not maintained. This may affect the reliability of release data.")
    print("Consider using a larger volume of medium or more frequent sampling.")

# Create dual-axis plot showing both concentration and % of solubility
fig = go.Figure()

# First y-axis - concentration
fig.add_trace(go.Scatter(
    x=time_points,
    y=concentration_data,
    name="Drug Concentration",
    mode="lines+markers",
    line=dict(color="blue")
))

# Add second y-axis - percentage of solubility
fig.add_trace(go.Scatter(
    x=time_points,
    y=solubility_percentage,
    name="% of Solubility",
    mode="lines+markers",
    line=dict(color="red"),
    yaxis="y2"
))

# Add horizontal lines for sink condition thresholds
fig.add_trace(go.Scatter(
    x=[min(time_points), max(time_points)],
    y=[10, 10],
    mode="lines",
    line=dict(color="green", dash="dash", width=1),
    name="Strict Sink Limit (10%)",
    yaxis="y2"
))

fig.add_trace(go.Scatter(
    x=[min(time_points), max(time_points)],
    y=[30, 30],
    mode="lines",
    line=dict(color="orange", dash="dash", width=1),
    name="Acceptable Sink Limit (30%)",
    yaxis="y2"
))

# Update layout with second y-axis
fig.update_layout(
    title="Drug Concentration and Sink Condition Analysis",
    xaxis=dict(title="Time (min)"),
    yaxis=dict(title="Concentration (μg/ml)", side="left", showgrid=False),
    yaxis2=dict(title="Percentage of Solubility (%)", side="right", overlaying="y", showgrid=False),
    legend=dict(x=0.01, y=0.99, bordercolor="Black", borderwidth=1)
)

# Store figure for display
output_vars['fig'] = fig

# Create a bar chart for % released vs time
fig2 = px.bar(data, x='Time (min)', y='Release (%)',
             title='Cumulative Drug Release Percentage')

output_vars['fig2'] = fig2
"""

    # Create an editable text area with the initial code
    user_code = st.text_area("Modify the code and hit Execute to see the results:", 
                            value=initial_code, height=400)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Execute button
        execute_button = st.button("Execute Code")
    
    with col2:
        # Add hints and challenges
        with st.expander("Ideas to try!"):
            st.markdown("""
            **Try annotating this code:**
            - Add comments to define the different steps and explain the purpose of each calculation 
                     
            **Try modifying:**
            - Change the drug solubility (e.g., 4 mg/ml for Lidocaine, 2 mg/ml for Salicylic Acid)
            - Modify the volume of release medium to see how it affects sink conditions
            - Change the concentration data to simulate faster or slower release
            
            **Challenges:**
            1. Calculate and plot the concentration gradient (Cs - C) over time
            2. Simulate the effect of replacing a fixed volume of medium at each sampling point
            3. Calculate the minimum volume needed to maintain sink conditions throughout the experiment
            """)
    
    if execute_button:
        # Execute the code and display results
        success, output, output_vars = execute_code(user_code)
        
        if success:
            # Display any printed output
            if output:
                st.subheader("Output:")
                st.text(output)
            
            # Display any figures generated
            if 'fig' in output_vars:
                st.plotly_chart(output_vars['fig'], use_container_width=True)
            
            if 'fig2' in output_vars:
                st.plotly_chart(output_vars['fig2'], use_container_width=True)
        else:
            # Display error message
            st.error("Error in your code:")
            st.code(output)
    
    # Include a discussion section
    st.subheader("Discussion")
    st.markdown("""
    ### Practical Considerations for Sink Conditions:
    
    1. **Volume Selection**: When designing a release study, select a volume that will maintain sink conditions:
    
       $$V_{min} = \\frac{3 \\times M_{dose}}{C_s}$$
       
       Where:
       - $V_{min}$ is the minimum volume needed
       - $M_{dose}$ is the total amount of drug
       - $C_s$ is the saturation solubility
    
    2. **Common Methods to Maintain Sink Conditions**:
       - Increase the volume of release medium
       - Add solubilizing agents to the medium
       - Use continuous flow systems
       - Replace a portion of the medium during sampling
    
    3. **Effect of Non-Sink Conditions**:
       - Slower apparent release rate
       - Plateau in the release profile below 100%
       - Poor correlation with in vivo performance
       - Reduced discrimination between formulations
    
    ### Regulatory Perspective:
    
    - USP and FDA guidelines recommend maintaining sink conditions in dissolution testing
    - When sink conditions cannot be maintained, results should be interpreted with caution
    - Alternative methodologies may be justified for poorly soluble drugs
    """)

if __name__ == "__main__":
    app()

import streamlit as st
import sys
import os
import base64
import pandas as pd
import streamlit as st
import requests
import json
from datetime import datetime

# Main app file
def main():
    st.set_page_config(
        page_title="FAR-2402 Laboratory Visualization Tool",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add CSS fixes for table stability
    st.markdown("""
    <style>
    /* Force tables to stay fixed width with no reflow */
    [data-testid="stDataFrame"] > div {
        width: 680px !important;
        max-width: 680px !important;
        min-width: 680px !important;
        overflow-x: auto !important;
        margin: 0 auto;
        transform: translateZ(0);
    }

    /* Force container widths to be consistent */
    .element-container {
        width: 100% !important;
    }

    /* Prevent layout shifts */
    .block-container {
        padding-bottom: 1rem;
        padding-top: 1rem;
    }

    /* Stabilize tables */
    .stDataFrame {
        will-change: transform;
        transform: translateZ(0);
    }
    
    /* Table container styles */
    .fixed-table-container {
        width: 680px;
        margin: 0 auto;
        overflow-x: auto;
        border: 1px solid #e6e9ef;
        border-radius: 5px;
        padding: 0;
        margin-bottom: 15px;
        transform: translateZ(0);
    }
    .small-table-container {
        width: 680px;
        margin: 0 auto;
        overflow-x: auto;
        border: 1px solid #e6e9ef;
        border-radius: 5px;
        padding: 0;
        margin-bottom: 15px;
        transform: translateZ(0);
    }
    
    /* Static HTML table styles */
    .static-table {
        width: 680px;
        margin: 0 auto;
        border-collapse: collapse;
        font-size: 14px;
    }
    .static-table th {
        background-color: #f5f5f5;
        padding: 8px;
        text-align: left;
        border-bottom: 2px solid #ddd;
    }
    .static-table td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Set up sidebar navigation
    st.sidebar.title("FAR-2402 Lab Tool")
    st.sidebar.image("https://en.uit.no/ressurs/uit/2020web/gfx/logo/UiT_Logo_Eng_Sort.svg", width=200)       
    # Initialize session state for navigation
    if 'app_mode' not in st.session_state:
        st.session_state.app_mode = "Home"

    # Convert the image to a base64 string
    def image_to_base64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    # Load your image from a local path
    image_path = ("cartoon.JPG")
    # Get the base64 string of the image
    image_base64 = image_to_base64(image_path)

    # Display your image and name in the top right corner
    st.markdown(
        f"""
        <style>
        .header {{
            position: absolute;  /* Fix the position */
            top: -20px;  /* Adjust as needed */
            right: -40px;  /* Align to the right */
            display: flex;
            justify-content: flex-end;
            align-items: center;
            padding: 10px;
            flex-direction: column; /* Stack items vertically */
            text-align: center; /* Ensures text is centrally aligned */
        }}
        .header img {{
            border-radius: 50%;
            width: 50px;
            height: 50px;
            margin-bottom: 5px; /* Space between image and text */
        }}
        .header-text {{
            font-size: 12px;
            font-weight: normal; /* Regular weight for text */
            text-align: center;
        }}
        </style>
        <div class="header">
            <img src="data:image/jpeg;base64,{image_base64}" alt="Mohsen Askar">
            <div class="header-text">Developed by: Mohsen Askar</div>
        </div>
        """,
        unsafe_allow_html=True
    )

   
    # Navigation options
    app_mode = st.sidebar.selectbox(
        "Select a Section:",
        ["Home",
         "Laboratory Protocol",
         "Drug & Base Properties", 
         "Standard Curve Generator",
         "Freiburger Schnecke Simulation",
         "Data Analysis Tool",
         "Interactive Coding Laboratory"
         ],
        index=["Home", 
               "Laboratory Protocol",
               "Drug & Base Properties", 
               "Standard Curve Generator",
               "Freiburger Schnecke Simulation",
               "Data Analysis Tool",
               "Interactive Coding Laboratory",
               ].index(st.session_state.app_mode)
    )
    
    # Update session state when selectbox changes
    st.session_state.app_mode = app_mode
    
    # Display content based on selection
    if app_mode == "Home":
        show_home()
    elif app_mode == "Drug & Base Properties":
        show_properties()
    elif app_mode == "Standard Curve Generator":
        show_standard_curve()
    elif app_mode == "Freiburger Schnecke Simulation":
        show_simulation()
    elif app_mode == "Data Analysis Tool":
        show_data_analysis()
    elif app_mode == "Interactive Coding Laboratory":
        import interactive_textbook
        interactive_textbook.app()
    elif app_mode == "Laboratory Protocol":
        show_protocol()
    st.markdown("---")  # Add a divider line

    # Function to get and update the visitor count using a cloud database
    def track_visitor():
        # Option 1: Using a simple cloud database like Firebase (requires setup)
        # Replace with your Firebase project details if using this option
        if 'firebase_option' == True:
            import firebase_admin
            from firebase_admin import credentials, db
            
            # Initialize Firebase (do this only once)
            if 'firebase_initialized' not in st.session_state:
                try:
                    cred = credentials.Certificate("your-firebase-credentials.json")
                    firebase_admin.initialize_app(cred, {
                        'databaseURL': 'https://your-project.firebaseio.com/'
                    })
                    st.session_state.firebase_initialized = True
                except Exception as e:
                    st.error(f"Error initializing Firebase: {e}")
                    return 0
            
            # Increment the counter
            try:
                ref = db.reference('visitor_counter')
                current_count = ref.get() or 0
                new_count = current_count + 1
                ref.set(new_count)
                return new_count
            except Exception as e:
                st.error(f"Error updating counter: {e}")
                return 0
        
        # Option 2: Using KV store from Streamlit Cloud (if deployed there)
        elif 'streamlit_cloud_option' == True:
            if 'count' not in st.session_state:
                # This works only on Streamlit Cloud with secrets management
                try:
                    # Get current count
                    response = requests.get(
                        "https://kvdb.io/YOUR_BUCKET_ID/visitor_count",
                        headers={"Content-Type": "application/json"}
                    )
                    current_count = int(response.text) if response.text else 0
                    
                    # Update count
                    new_count = current_count + 1
                    requests.post(
                        "https://kvdb.io/YOUR_BUCKET_ID/visitor_count",
                        data=str(new_count),
                        headers={"Content-Type": "text/plain"}
                    )
                    st.session_state.count = new_count
                    return new_count
                except Exception as e:
                    st.error(f"Error with KV store: {e}")
                    return 0
            return st.session_state.count
        
        # Option 3: Using local file storage (simplest but may not work in all deployments)
        else:
            if 'count' not in st.session_state:
                try:
                    with open('visitor_count.txt', 'r') as f:
                        current_count = int(f.read().strip())
                except FileNotFoundError:
                    current_count = 0
                
                new_count = current_count + 1
                
                try:
                    with open('visitor_count.txt', 'w') as f:
                        f.write(str(new_count))
                    st.session_state.count = new_count
                except Exception as e:
                    st.error(f"Error saving count: {e}")
                    st.session_state.count = current_count + 1
                    
            return st.session_state.count

    # Only increment the counter once per session
    if 'visitor_counted' not in st.session_state:
        count = track_visitor()
        st.session_state.visitor_counted = True
    else:
        count = st.session_state.get('count', 0)

    # Display the counter with nice styling
    st.markdown(
        f"""
        <div style="text-align: center; padding: 10px; margin-top: 30px; 
            border-top: 1px solid #f0f0f0; color: #888;">
            <span style="font-size: 14px;">👥 Total Visitors: {count}</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # You can also add today's date next to the counter
    today = datetime.now().strftime("%B %d, %Y")
    st.markdown(
        f"""
        <div style="text-align: center; color: #888; font-size: 12px; margin-top: 5px;">
            {today}
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to create static HTML tables for better stability
def create_html_table(df, highlight_cells=None):
    """
    Create a static HTML table from a pandas DataFrame
    highlight_cells: Optional dictionary mapping (row, col) tuples to CSS styles
    """
    if highlight_cells is None:
        highlight_cells = {}
    
    table_html = '<div class="fixed-table-container">'
    table_html += '<table class="static-table">'
    
    # Add header
    table_html += '<thead><tr>'
    for col in df.columns:
        table_html += f'<th>{col}</th>'
    table_html += '</tr></thead>'
    
    # Add body
    table_html += '<tbody>'
    for i, (_, row) in enumerate(df.iterrows()):
        table_html += '<tr>'
        for j, val in enumerate(row):
            # Check if this cell needs special styling
            cell_style = ''
            if (i, j) in highlight_cells:
                cell_style = f' style="{highlight_cells[(i, j)]}"'
            
            table_html += f'<td{cell_style}>{val}</td>'
        table_html += '</tr>'
    table_html += '</tbody></table></div>'
    
    return table_html
# Define page content functions
def show_home():
    st.title("FAR-2402: Drug Formulation and Release Visualization Tool")
    
    st.markdown("""
    ## Welcome to the Laboratory Visualization Tool
    
    This interactive application will help you visualize and understand the concepts involved in the 
    FAR-2402 laboratory course on pharmaceutical formulation and drug release from semi-solid bases.
    
    ### Key Features:
    
    - **Drug & Base Properties**: Interactive database of drug and excipient properties
    - **Standard Curve Generator**: Create and visualize standard curves for UV analysis
    - **Freiburger Schnecke Simulation**: Simulate drug release from different formulations
    - **Data Analysis Tool**: Analyze your lab data and compare formulations
    - **Laboratory Protocol**: Reference for the laboratory procedures
    
    ### How to Use This Tool:
    
    1. Use the sidebar to navigate between different sections
    2. Each section provides interactive visualizations and simulations
    3. You can input your own data or use the provided examples
    4. Use this tool before, during, and after your laboratory session
    
    This tool is designed to complement the laboratory manual and enhance your understanding of 
    the physical pharmacy concepts covered in this course.
    """)
    
    # Create columns for the main sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pre-Lab Preparation")
        st.markdown("""
        Before your laboratory session:
        
        - Review drug and excipient properties
        - Understand the Freiburger Schnecke apparatus
        - Simulate expected drug release profiles
        - Prepare your data collection sheets
        """)
        
        col1a, col1b = st.columns(2)
        with col1a:
            if st.button("Go to Properties Database"):
                st.session_state.app_mode = "Drug & Base Properties"
                st.rerun()
        with col1b:
            if st.button("Try a bit Coding"):
                st.session_state.app_mode = "Interactive Coding Laboratory"
                st.rerun()
    
    with col2:
        st.subheader("Post-Lab Analysis")
        st.markdown("""
        After your laboratory session:
        
        - Upload your experimental data
        - Generate standard curves from your measurements
        - Analyze drug release profiles
        - Compare different formulations
        - Prepare your lab report
        """)
        
        if st.button("Go to Data Analysis"):
            st.session_state.app_mode = "Data Analysis Tool"
            st.rerun()

def show_properties():
    st.title("Drug and Excipient Properties Database")
    
    st.markdown("""
    ## Interactive Properties Quiz
    
    Fill in the properties of the pharmaceutical ingredients used in this lab course. 
    Enter your answers in the table below and click "Check Answers" to see how well you did!
    """)
    
    tab1, tab2, tab3 = st.tabs(["Active Ingredients", "Base Components", "Formulations"])
    
    with tab1:
        st.subheader("Active Pharmaceutical Ingredients")
        
        # Initialize session state for storing user answers if not already present
        if 'drug_answers' not in st.session_state:
            st.session_state.drug_answers = None
            st.session_state.drug_score = 0
            st.session_state.drug_checked = False
        
        # Define correct answers
        correct_answers = {
            'Property': ['Latin Name', 'Molecular Weight (g/mol)', 'Appearance', 'Topical Function', 
                       'Water Solubility (mg/mL)', 'Melting Point (°C)', 'pKa', 'logP', 'UV max (λmax) (nm)'],
            'Lidocaine': ['Lidocainum', '234.34', 'White crystalline powder', 'Local anesthetic',
                        '4', '68-69', '7.9', '2.26', '262'],
            'Lidocaine HCl': ['Lidocaini hydrochloridum monohydricum', '288.81', 
                            'White crystalline powder', 'Local anesthetic',
                            '680', '74-79', '7.9', '1.15', '262'],
            'Salicylic Acid': ['Acidum salicylicum', '138.12', 'White crystalline powder', 
                             'Keratolytic, antiseptic', '2', '158-161', 
                             '3.0', '2.26', '303']
        }
        
        # Create empty DataFrame for student answers
        import pandas as pd
        
        if st.session_state.drug_answers is None:
            # First time - create empty dataframe structure
            empty_df = pd.DataFrame({
                'Property': correct_answers['Property'],
                'Lidocaine': ['' for _ in range(len(correct_answers['Property']))],
                'Lidocaine HCl': ['' for _ in range(len(correct_answers['Property']))],
                'Salicylic Acid': ['' for _ in range(len(correct_answers['Property']))]
            })
            st.session_state.drug_answers = empty_df
       
        # Wrap in container to isolate and prevent layout shifts
        with st.container():
            # Display editable dataframe with fixed width
            edited_df = st.data_editor(
                st.session_state.drug_answers,
                disabled=["Property"],
                hide_index=True,
                key="drug_properties_editor",
                use_container_width=False,
                width=680,  # Reduced from 900px to 680px
                height=300  # Fixed height to prevent resizing
            )
        
        # Update session state with edited values
        st.session_state.drug_answers = edited_df
        
        # Check answers button
        if st.button("Check Answers"):
            st.session_state.drug_checked = True
            
            # Create styled DataFrame
            styled_df = st.session_state.drug_answers.copy()
            
            # Make a copy for style application
            style_df = pd.DataFrame('', index=styled_df.index, columns=styled_df.columns)
            
            # Count correct answers
            total_cells = 0
            correct_cells = 0
            
            # Check each cell against correct answers
            highlight_cells = {}  # For HTML table styling
            
            for col in ['Lidocaine', 'Lidocaine HCl', 'Salicylic Acid']:
                col_idx = list(styled_df.columns).index(col)
                
                for i, prop in enumerate(correct_answers['Property']):
                    if styled_df.loc[i, col] == '':
                        # Empty cell - no styling
                        continue
                    
                    total_cells += 1
                    
                    # Get student answer and correct answer
                    student_answer = str(styled_df.loc[i, col]).strip().lower()
                    correct_answer = str(correct_answers[col][i]).strip().lower()
                    
                    # Special case for ranges (like melting points)
                    if '-' in correct_answer:
                        # Check if within range
                        try:
                            min_val, max_val = map(float, correct_answer.split('-'))
                            try:
                                student_val = float(student_answer)
                                if min_val <= student_val <= max_val:
                                    style_df.loc[i, col] = 'background-color: #c6efce'  # Light green
                                    highlight_cells[(i, col_idx)] = 'background-color: #c6efce'
                                    correct_cells += 1
                                else:
                                    style_df.loc[i, col] = 'background-color: #ffc7ce'  # Light red
                                    highlight_cells[(i, col_idx)] = 'background-color: #ffc7ce'
                            except:
                                style_df.loc[i, col] = 'background-color: #ffc7ce'  # Light red
                                highlight_cells[(i, col_idx)] = 'background-color: #ffc7ce'
                        except:
                            # Fall back to exact comparison if range parsing fails
                            if student_answer == correct_answer:
                                style_df.loc[i, col] = 'background-color: #c6efce'  # Light green
                                highlight_cells[(i, col_idx)] = 'background-color: #c6efce'
                                correct_cells += 1
                            else:
                                style_df.loc[i, col] = 'background-color: #ffc7ce'  # Light red
                                highlight_cells[(i, col_idx)] = 'background-color: #ffc7ce'
                    
                    # Check approximate matches for numeric values
                    elif correct_answer.replace('.', '', 1).isdigit() and student_answer.replace('.', '', 1).isdigit():
                        try:
                            correct_val = float(correct_answer)
                            student_val = float(student_answer)
                            
                            # Allow 5% tolerance for numeric values
                            if abs(correct_val - student_val) / correct_val <= 0.05:
                                style_df.loc[i, col] = 'background-color: #c6efce'  # Light green
                                highlight_cells[(i, col_idx)] = 'background-color: #c6efce'
                                correct_cells += 1
                            else:
                                style_df.loc[i, col] = 'background-color: #ffc7ce'  # Light red
                                highlight_cells[(i, col_idx)] = 'background-color: #ffc7ce'
                        except:
                            # Fall back to exact comparison if float conversion fails
                            if student_answer == correct_answer:
                                style_df.loc[i, col] = 'background-color: #c6efce'  # Light green
                                highlight_cells[(i, col_idx)] = 'background-color: #c6efce'
                                correct_cells += 1
                            else:
                                style_df.loc[i, col] = 'background-color: #ffc7ce'  # Light red
                                highlight_cells[(i, col_idx)] = 'background-color: #ffc7ce'
                    
                    # Exact match for text values
                    elif student_answer == correct_answer:
                        style_df.loc[i, col] = 'background-color: #c6efce'  # Light green
                        highlight_cells[(i, col_idx)] = 'background-color: #c6efce'
                        correct_cells += 1
                    else:
                        style_df.loc[i, col] = 'background-color: #ffc7ce'  # Light red
                        highlight_cells[(i, col_idx)] = 'background-color: #ffc7ce'
            
            # Calculate score if any answers were provided
            if total_cells > 0:
                score = (correct_cells / total_cells) * 100
                st.session_state.drug_score = score
            else:
                st.session_state.drug_score = 0
            
            # Use static HTML table for more stability instead of dataframe styling
            html_table = create_html_table(styled_df, highlight_cells)
            st.markdown(html_table, unsafe_allow_html=True)
            
            # Display score
            if total_cells > 0:
                if score >= 90:
                    st.success(f"🎉 Great job! Your score: {score:.1f}% ({correct_cells}/{total_cells} correct)")
                elif score >= 70:
                    st.info(f"👍 Good work! Your score: {score:.1f}% ({correct_cells}/{total_cells} correct)")
                elif score >= 50:
                    st.warning(f"🤔 Keep studying! Your score: {score:.1f}% ({correct_cells}/{total_cells} correct)")
                else:
                    st.error(f"📚 More review needed! Your score: {score:.1f}% ({correct_cells}/{total_cells} correct)")
            else:
                st.warning("Please fill in some answers before checking")
        
        # If answers were previously checked, show the last result
        elif st.session_state.drug_checked and hasattr(st.session_state, 'drug_score'):
            st.info(f"Previous score: {st.session_state.drug_score:.1f}%")
            st.write("Edit your answers and click 'Check Answers' again to update your score.")
        
        # Display chemical structures
        st.subheader("Chemical Structures")
        drug = st.selectbox("Select a drug to view its structure:", 
                          ["Lidocaine", "Lidocaine HCl", "Salicylic Acid"])
        
        structure_urls = {
            "Lidocaine": "https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?cid=3676&t=l",
            "Lidocaine HCl": "https://file.medchemexpress.com/product_pic/hy-b0185a.gif",
            "Salicylic Acid": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcShHzWn1SOtPSyg9JxGDz3lutqoqwM44cDbHA&s"
        }
        
        st.image(structure_urls[drug], width=300, caption=f"Structure of {drug}")   
        
    with tab2:
        st.subheader("Base Components")
        
        # Create tabs for different component types
        base_tab1, base_tab2 = st.tabs(["Hydrophilic Components", "Lipophilic Components"])
        
        with base_tab1:
            st.markdown("""
            ### Hydrophilic Components
            
            **Carmellose Sodium 2000**
            - Latin: Carmellosum natricum 2000
            - Function: Gelling agent, viscosity enhancer
            - Appearance: White powder
            - Solubility: Swells in water, forms gel
            
            **Glycerol 85%**
            - Latin: Glycerolum 85 per centum
            - Function: Humectant, solvent
            - Appearance: Clear viscous liquid
            - Solubility: Miscible with water
            """)
            
        with base_tab2:
            st.markdown("""
            ### Lipophilic Components
            
            **Liquid Paraffin**
            - Latin: Paraffinum liquidum
            - Function: Emollient, occlusive agent
            - Appearance: Clear colorless oil
            - Solubility: Insoluble in water
            
            **Aerosil R972**
            - Latin: Silica hydrophobica colloidalis
            - Function: Thickening agent
            - Appearance: White fine powder
            - Properties: Hydrophobic fumed silica
            
            **Medium Chain Triglycerides**
            - Latin: Triglycerida media
            - Function: Emollient, carrier oil
            - Appearance: Clear colorless oil
            - Solubility: Insoluble in water
            """)
            
    with tab3:
        st.subheader("Formulation Compositions")
        
        # Display formulation compositions using static HTML table
        import pandas as pd
        import numpy as np
        import plotly.express as px
        
        bases_df = pd.DataFrame({
            'Component': ['Carmellose sodium 2000', 'Glycerol 85%', 'Purified water', 
                         'Aerosil R972', 'Liquid paraffin', 'Cetyl alcohol', 'Almond oil',
                         'Polysorbate', 'Medium chain triglycerides'],
            'Base II (%)': [4, 15, 81, 0, 0, 0, 0, 0, 0],
            'Base III (%)': [0, 0, 0, 15, 85, 0, 0, 0, 0],
            'Base IV (%)': [0, 0, 55, 0, 0, 20, 20, 5, 0],
            'Base VI (%)': [0, 0, 0, 15, 0, 0, 0, 0, 85]
        })
        
        # Use static HTML table instead of dataframe
        html_table = create_html_table(bases_df)
        st.markdown(html_table, unsafe_allow_html=True)
        
        # Show bar chart of compositions
        st.subheader("Composition Visualization")
        
        # For a real chart, you would need to reshape the data appropriately
        formulation_types = pd.DataFrame({
            'Base': ['Base II', 'Base III', 'Base IV', 'Base VI'],
            'Type': ['Hydrogel', 'Oleogel', 'O/W cream/emulsion', 'Oleogel'],
            'Primary Phase': ['Aqueous', 'Oil', 'Aqueous', 'Oil'],
            'Water Content (%)': [81, 0, 55, 0]
        })
        
        fig = px.bar(formulation_types, x='Base', y='Water Content (%)', 
                    color='Primary Phase', title='Water Content in Different Bases')
        st.plotly_chart(fig, use_container_width=True)

def show_standard_curve():
    st.title("Standard Curve Generator")
    
    # Add theoretical background
    with st.expander("📚 Theory: The Beer-Lambert Law", expanded=False):
        st.markdown("""
        ### Beer-Lambert Law
        
        The Beer-Lambert Law states that absorbance (A) is directly proportional to concentration (c):
        
        **A = ε × c × l**
        
        Where:
        - A is the absorbance (no units)
        - ε is the molar absorptivity (L·mol⁻¹·cm⁻¹)
        - c is the concentration (mol·L⁻¹)
        - l is the path length (cm)
        
        This relationship allows us to create a **standard curve** (calibration curve) by measuring the absorbance of known concentrations and then use it to determine unknown concentrations.
        """)
    
    # Create a simplified version of the standard curve generator
    import numpy as np
    import pandas as pd
    import plotly.express as px
    from scipy import stats
    
    drug = st.selectbox(
        "Select active pharmaceutical ingredient:",
        ["Lidocaine", "Lidocaine HCl", "Salicylic Acid"]
    )
    
    # Set default concentration ranges based on drug
    if drug == "Salicylic Acid":
        default_concentrations = [5.0, 10.0, 15.0, 20.0, 30.0]
    else:  # Lidocaine or Lidocaine HCl
        default_concentrations = [20.0, 100.0, 200.0, 300.0, 500.0]
    
    st.subheader("Enter Standard Curve Data")
    
    # Create a form for entering concentration and absorbance data
    with st.form("standard_curve_data"):
        st.write("Enter concentration and absorbance values:")
        
        # Create 5 columns for the 5 standard points
        cols = st.columns(5)
        concentrations = []
        absorbances = []
        
        for i, col in enumerate(cols):
            with col:
                conc = st.number_input(f"Conc. {i+1} (μg/ml)", 
                                      value=default_concentrations[i],
                                      step=0.1,
                                      format="%.1f")
                
                # Calculate a reasonable default absorbance based on the concentration
                default_abs = 0.0
                if drug == "Salicylic Acid":
                    default_abs = conc * 0.033 + 0.02
                else:
                    default_abs = conc * 0.0018 + 0.01
                
                abs_val = st.number_input(f"Abs. {i+1}", 
                                         value=float(default_abs), 
                                         format="%.2f")
                
                concentrations.append(conc)
                absorbances.append(abs_val)
        
        submitted = st.form_submit_button("Generate Standard Curve")
    
    if submitted or 'concentrations' in locals():
        # Create dataframe
        data = pd.DataFrame({
            'Concentration (μg/ml)': concentrations,
            'Absorbance': absorbances
        })
        
        # Display the data
        st.subheader("Standard Curve Data")
        st.dataframe(data, use_container_width=True)
        
        # Create linear regression
        x = np.array(concentrations)
        y = np.array(absorbances)
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Create equation text
        equation = f"y = {slope:.5f}x + {intercept:.5f}"
        r_squared = r_value ** 2
        
        # Display statistics
        st.subheader("Regression Analysis")
        
        # Add explanation of the parameters
        with st.expander("📚 What do these values mean?", expanded=True):
            st.markdown("""
            - **Slope (m)**: Represents the change in absorbance per unit change in concentration. Higher values indicate greater sensitivity.
            - **Y-intercept (b)**: The absorbance value when concentration is zero. Ideally should be close to zero.
            - **R² value**: Coefficient of determination, measures how well the data fits the linear model. Values ≥ 0.95 indicate a good fit.
            """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Slope", f"{slope:.5f}")
            st.metric("Y-intercept", f"{intercept:.5f}")
        
        with col2:
            st.metric("R² value", f"{r_squared:.5f}")
            if r_squared >= 0.95:
                st.success("✓ Standard curve is valid")
            else:
                st.error("✗ R² must be ≥ 0.95")
        
        # Plot the standard curve
        st.subheader("Standard Curve Plot")
        
        # Create figure
        fig = px.scatter(data, x='Concentration (μg/ml)', y='Absorbance',
                        title=f'Standard Curve for {drug}')
        
        # Add regression line
        x_range = np.linspace(0, max(concentrations) * 1.1, 100)
        y_pred = intercept + slope * x_range
        
        fig.add_scatter(x=x_range, y=y_pred, mode='lines', name='Linear Regression',
                      line=dict(color='red'))
        
        # Add equation and R² to the plot
        fig.add_annotation(
            x=max(concentrations) * 0.6,
            y=max(absorbances) * 0.2,
            text=f"{equation}<br>R² = {r_squared:.5f}",
            showarrow=False,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculator for unknown concentrations
        st.subheader("Calculate Concentration from Absorbance")
        
        # Add explanation of how concentration is calculated
        with st.expander("📚 How is concentration calculated?", expanded=True):
            st.markdown("""
            ### Calculating Concentration from Absorbance
            
            Rearranging the linear equation **A = m·c + b** to solve for concentration (c):
            
            **c = (A - b) / m**
            
            Where:
            - A is the measured absorbance
            - b is the y-intercept
            - m is the slope
            
            This formula allows us to determine the concentration of an unknown sample based on its absorbance.
            
            **Note:** For accurate results, the absorbance should fall within the range of the standard curve.
            """)
        
        unknown_abs = st.number_input("Enter measured absorbance:", 
                                     min_value=0.0, 
                                     value=0.5, 
                                     format="%.3f")
        
        # Calculate concentration
        if unknown_abs < intercept:
            st.warning("Absorbance is lower than the y-intercept - results may be inaccurate.")
            calc_conc = 0.0
        else:
            calc_conc = (unknown_abs - intercept) / slope
        
        st.metric("Calculated Concentration", f"{calc_conc:.2f} μg/ml")
        
def show_simulation():
    st.title("Freiburger Schnecke Drug Release Simulation")
    
    # Create a simplified version of the Freiburger Schnecke simulation
    import numpy as np
    import pandas as pd
    import plotly.express as px
    
    st.markdown("""
    This simulation helps you visualize how drug release occurs in the Freiburger Schnecke apparatus 
    and how different formulations affect the release profile.\n
    Get back to Laboratory Protocol section --> Step 3: Release study to see the instructions.
    """)
    
    # Add schematic of the apparatus
    st.subheader("Apparatus simple diagram")
    
    # Create columns for the layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
                # Create a basic diagram mockup
        diagram = """
        digraph G {
            rankdir=circo;
            graph [size="12,10"];
            node [shape=box, style=rounded, color=lightblue, fontname="Helvetica", fontsize=14];
            Schnecke [label="Freiburger\nSchnecke"];
            Flask [label="Release Medium\nFlask"];
            Pump [label="Pump"];
            
            Schnecke -> Flask -> Pump -> Schnecke;
        }
        """
        
        st.graphviz_chart(diagram,use_container_width=True) 
    
    with col2:
        st.markdown("""
        ### Components of the Apparatus:
        
        1. **Donor Chamber**: Contains the semi-solid formulation
        2. **Membrane**: Separates donor and acceptor chambers
        3. **Acceptor Chamber**: Flow path for release medium
        4. **Pump**: Circulates release medium (buffer)
        5. **Collection Flask**: For sampling released drug
        
        ### Release Process:
        
        * Drug diffuses from the formulation through the membrane
        * Released drug is carried away by flowing buffer
        * Samples are collected at fixed time intervals
        * Drug concentration is measured by UV spectrophotometry
        """)
    
    # Simulation parameters
    st.subheader("Simulation Parameters")
    
    # Create two columns for parameter input
    col1, col2 = st.columns(2)
    
    with col1:
        drug = st.selectbox(
            "Select drug:",
            ["Lidocaine", "Lidocaine HCl", "Salicylic Acid"]
        )
        
        base = st.selectbox(
            "Select base formulation:",
            ["Base II: Hydrogel", "Base III: Oleogel", 
             "Base IV: O/W Cream", "Base VI: Oleogel MCT"]
        )
    
    with col2:
        simulation_time = st.slider(
            "Simulation time (minutes):",
            15, 240, 120
        )
        
        flow_rate = st.slider(
            "Flow rate (rpm):",
            50, 150, 100
        )
    
    # Run simulation based on parameters
    # For the actual simulation, you would have more complex logic
    # This is a simplified version
    
    # Create formulation-specific parameters
    base_diffusion = {
        "Base II: Hydrogel": 0.8,
        "Base III: Oleogel": 0.3,
        "Base IV: O/W Cream": 0.6,
        "Base VI: Oleogel MCT": 0.4
    }
    
    drug_properties = {
        "Lidocaine": {"water_solubility": 0.2, "oil_solubility": 0.8, "diffusivity": 0.7},
        "Lidocaine HCl": {"water_solubility": 0.9, "oil_solubility": 0.1, "diffusivity": 0.8},
        "Salicylic Acid": {"water_solubility": 0.4, "oil_solubility": 0.6, "diffusivity": 0.5}
    }
    
    # Create a simplified model for drug release
    # In reality, this would be based on diffusion equations
    
    # Calculate compatibility between drug and base
    base_type = base.split(":")[1].strip()
    base_hydrophilicity = 0.8 if "Hydrogel" in base_type else 0.2 if "Cream" in base_type else 0.1
    drug_hydrophilicity = drug_properties[drug]["water_solubility"]
    compatibility = 1 - abs(base_hydrophilicity - drug_hydrophilicity)
    
    # Release coefficient
    k_h = base_diffusion[base] * drug_properties[drug]["diffusivity"] * compatibility * (flow_rate/100) * 0.15
    
    # Generate time points and release data
    t = np.linspace(0, simulation_time, 50)
    t_sqrt = np.sqrt(t)
    
    # Higuchi model: Q = k_h * sqrt(t)
    release = k_h * t_sqrt + np.random.normal(0, 0.02 * k_h, len(t))
    release = np.maximum(0, np.minimum(release, 1.0))  # Constrain between 0 and 1
    
    # Create dataframe for plotting
    release_data = pd.DataFrame({
        'Time (min)': t,
        'Cumulative Release (fraction)': release,
        'Cumulative Release (%)': release * 100,
        'Square Root of Time': t_sqrt
    })
    
    # Plot the release profile
    st.subheader("Simulated Drug Release Profile")
    
    fig = px.line(release_data, x='Time (min)', y='Cumulative Release (%)', 
                 title=f'Drug Release Profile: {drug} from {base}')
    
    # Add specific time points that correspond to lab protocol
    lab_times = [15, 30, 60, 90, 120]
    lab_times = [time for time in lab_times if time <= simulation_time]
    
    lab_releases = [k_h * np.sqrt(time) * 100 for time in lab_times]
    
    fig.add_scatter(x=lab_times, y=lab_releases, mode='markers', 
                   name='Sampling Points', marker=dict(size=10))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add Higuchi plot
    st.subheader("Higuchi Plot (√Time)")
    
    fig = px.scatter(release_data, x='Square Root of Time', y='Cumulative Release (%)',
                    title=f'Higuchi Plot: {drug} from {base}')
    
    # Add regression line
    x_higuchi = release_data['Square Root of Time']
    y_higuchi = release_data['Cumulative Release (%)']
    
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_higuchi, y_higuchi)
    
    fig.add_scatter(x=x_higuchi, y=intercept + slope * x_higuchi,
                   mode='lines', name='Linear Regression',
                   line=dict(color='red'))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display release parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Higuchi Constant (kH)", f"{slope:.3f} %/√min")
    
    with col2:
        st.metric("R² for Higuchi Model", f"{r_value**2:.5f}")
    
    # Comparison option
    if st.checkbox("Compare with another formulation"):
        other_base = st.selectbox(
            "Select another base to compare:",
            [b for b in base_diffusion.keys() if b != base]
        )
        
        # Calculate new parameters for second formulation
        other_base_type = other_base.split(":")[1].strip()
        other_hydrophilicity = 0.8 if "Hydrogel" in other_base_type else 0.2 if "Cream" in other_base_type else 0.1
        other_compatibility = 1 - abs(other_hydrophilicity - drug_hydrophilicity)
        other_k_h = base_diffusion[other_base] * drug_properties[drug]["diffusivity"] * other_compatibility * (flow_rate/100) * 0.15
        
        # Generate release data for second formulation
        other_release = other_k_h * t_sqrt + np.random.normal(0, 0.02 * other_k_h, len(t))
        other_release = np.maximum(0, np.minimum(other_release, 1.0))
        
        # Create comparison dataframe
        compare_data = pd.DataFrame({
            'Time (min)': np.concatenate([t, t]),
            'Cumulative Release (%)': np.concatenate([release * 100, other_release * 100]),
            'Formulation': np.concatenate([[base] * len(t), [other_base] * len(t)])
        })
        
        # Plot comparison
        fig = px.line(compare_data, x='Time (min)', y='Cumulative Release (%)', 
                     color='Formulation', title=f'Comparison of Drug Release Profiles for {drug}')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show relative release rates
        if k_h > other_k_h:
            st.info(f"{base} releases {k_h/other_k_h:.1f}× faster than {other_base}")
        else:
            st.info(f"{other_base} releases {other_k_h/k_h:.1f}× faster than {base}")
        
        st.markdown(f"""
        ### Factors affecting the difference in release rates:
        
        - **Base properties**: {base} is {"more hydrophilic" if "Hydrogel" in base or "Cream" in base else "more lipophilic"} than {other_base}
        - **Drug-base compatibility**: {drug} is {"more compatible with hydrophilic bases" if drug_hydrophilicity > 0.5 else "more compatible with lipophilic bases"}
        - **Viscosity effects**: Higher viscosity generally leads to slower release
        - **Water content**: Higher water content facilitates release of hydrophilic drugs
        """)

def show_data_analysis():
    # Import necessary libraries
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
    from scipy import stats
    
    st.title("Drug Release Data Analysis Tool")
    
    # Initialize session state for calculated data if not already present
    if 'calculated_data' not in st.session_state:
        st.session_state.calculated_data = None
    
    # Data source selection
    data_source = st.radio(
        "Select data source:",
        ["Enter Data Manually", "Upload Your Lab Data", "Use Example Data"]
    )
    
    if data_source == "Enter Data Manually":
        st.subheader("Enter Your Release Data")
        
        # Let user select drug and formulations first
        drug = st.selectbox(
            "Select drug used in your experiment:",
            ["Lidocaine", "Lidocaine HCl", "Salicylic Acid"]
        )
        
        # Option to compare multiple formulations
        num_formulations = st.number_input("How many formulations do you want to analyze?", 
                                         min_value=1, max_value=4, value=1, step=1)
        
        # Get formulation names if multiple formulations
        formulation_names = []
        if num_formulations > 1:
            for i in range(num_formulations):
                form_name = st.text_input(f"Name for formulation {i+1}:", value=f"Base {i+1}")
                formulation_names.append(form_name)
        else:
            formulation_names = ["Formulation 1"]
        
        # Create a suggested number of rows per formulation
        suggested_rows_per_formulation = 8
        
        # Create empty dataframes for each formulation
        all_dataframes = []
        
        for form_idx, form_name in enumerate(formulation_names):
            # Start with standard time points plus empty rows
            standard_times = [15, 30, 60, 90, 120]
            additional_times = [None] * (suggested_rows_per_formulation - len(standard_times))
            
            form_df = pd.DataFrame({
                "Time (min)": standard_times + additional_times,
                "Concentration (μg/ml)": [None] * suggested_rows_per_formulation
            })
            
            if num_formulations > 1:
                form_df["Formulation"] = form_name
            
            all_dataframes.append(form_df)
        
        # Combine all formulation dataframes
        if all_dataframes:
            initial_df = pd.concat(all_dataframes, ignore_index=True)
        else:
            initial_df = pd.DataFrame({"Time (min)": [], "Concentration (μg/ml)": []})
        
        # Make the dataframe fully editable - wrap in container for stability
        st.subheader(f"Enter your data (you can add/modify time points as needed)")
        
        with st.container():
            edited_df = st.data_editor(
                initial_df,
                num_rows="dynamic",
                key="manual_data_editor",
                column_config={
                    "Time (min)": st.column_config.NumberColumn(
                        "Time (min)",
                        help="Sampling time in minutes",
                        format="%.1f"
                    ),
                    "Concentration (μg/ml)": st.column_config.NumberColumn(
                        "Concentration (μg/ml)",
                        help="Measured concentration from standard curve",
                        min_value=0.0,
                        format="%.2f"
                    )
                },
                use_container_width=False,
                width=680,  # Fixed width
                height=300  # Fixed height for data editor
            )
        
        # Remove rows with empty time values before calculations
        if not edited_df.empty:
            edited_df = edited_df.dropna(subset=["Time (min)"])
        
        # Add experimental parameters BEFORE the calculate button
        st.subheader("Experiment Parameters for Calculations")
        
        col1, col2 = st.columns(2)
        with col1:
            medium_volume = st.number_input("Volume of release medium (ml):", 
                                          min_value=50.0, max_value=500.0, value=150.0)
            
        with col2:
            formulation_weight = st.number_input("Weight of formulation (g):", 
                                               min_value=0.1, max_value=10.0, value=1.0)
            drug_conc = st.number_input("Drug concentration in formulation (%):", 
                                      min_value=0.1, max_value=10.0, value=2.0)
        
        # Calculate button
        calculate_btn = st.button("Calculate Release Parameters")
        
        if calculate_btn and not edited_df.empty:
            # Calculate total drug amount in the formulation
            total_drug_mg = formulation_weight * drug_conc * 10  # convert % to mg
            
            # Convert string or object columns to numeric types
            edited_df['Time (min)'] = pd.to_numeric(edited_df['Time (min)'], errors='coerce')
            edited_df['Concentration (μg/ml)'] = pd.to_numeric(edited_df['Concentration (μg/ml)'], errors='coerce')
            
            # Drop rows with missing values in critical columns
            edited_df = edited_df.dropna(subset=['Time (min)', 'Concentration (μg/ml)'])
            
            # Only proceed if we still have data points
            if len(edited_df) > 0:
                # Calculate release percentage
                edited_df['Square Root of Time'] = np.sqrt(edited_df['Time (min)'])
                edited_df['Cumulative Release (mg)'] = edited_df['Concentration (μg/ml)'] * medium_volume / 1000  # convert to mg
                edited_df['Cumulative Release (%)'] = (edited_df['Cumulative Release (mg)'] / total_drug_mg) * 100
                
                # Store calculated data in session state
                st.session_state.calculated_data = edited_df
                
                # Use static HTML table for more stable display
                html_table = create_html_table(edited_df)
                st.subheader("Calculated Data")
                st.markdown(html_table, unsafe_allow_html=True)
            else:
                st.warning("No valid data points after processing. Please check your data entry.")
    
    elif data_source == "Upload Your Lab Data":
        st.subheader("Upload Your Data")
        
        # Add imports at the top of your function
        import pandas as pd
        from io import BytesIO
        
        uploaded_file = st.file_uploader("Upload your data file", type=["csv", "xlsx", "xls"])
        # Add clear instructions about required column format
        st.caption("ℹ️ File format: Your spreadsheet should have columns named 'Time' and 'Concentration'. For multiple formulations, include a 'Formulation' column.")
            
        if uploaded_file is not None:
            try:
                # Get file extension
                file_extension = uploaded_file.name.split(".")[-1].lower()
                
                # Handle different file types
                if file_extension == "csv":
                    # CSV handling
                    data = pd.read_csv(uploaded_file)
                elif file_extension in ["xlsx", "xls"]:
                    # Excel handling
                    data = pd.read_excel(uploaded_file, engine='openpyxl')
                else:
                    st.error(f"Unsupported file format: {file_extension}")
                    data = None
                    
                # Check for required columns (with more flexible column name matching)
                if data is not None:
                    # Define possible column name variations
                    time_columns = ['Time', 'Time (min)', 'time', 'TIME', 'Time(min)', 'time(min)']
                    conc_columns = ['Concentration', 'Concentration (μg/ml)', 'conc', 'CONCENTRATION', 'Conc (μg/ml)', 'concentration']
                    form_columns = ['Formulation', 'formulation', 'FORMULATION', 'Form', 'form', 'Base', 'base', 'Formula']
                    
                    # Try to find matching columns
                    time_col = next((col for col in data.columns if col in time_columns), None)
                    conc_col = next((col for col in data.columns if col in conc_columns), None)
                    form_col = next((col for col in data.columns if col in form_columns), None)
                    
                    missing_columns = []
                    if not time_col:
                        missing_columns.append('Time')
                    if not conc_col:
                        missing_columns.append('Concentration')
                    
                if missing_columns:
                    st.error(f"Missing required columns in file: {', '.join(missing_columns)}")
                    st.info("Your file should include at minimum columns for Time and Concentration")
                    data = None
                else:
                    # Rename columns to standard format for consistency in the app
                    column_mapping = {}
                    if time_col:
                        column_mapping[time_col] = 'Time (min)'
                    if conc_col:
                        column_mapping[conc_col] = 'Concentration (μg/ml)'
                    if form_col:
                        column_mapping[form_col] = 'Formulation'
                    
                    # Apply renaming
                    data = data.rename(columns=column_mapping)
                    
                    # Store in session state
                    st.session_state.calculated_data = data
                    st.success("Data loaded successfully!")
                    
                    # Use static HTML table for stability
                    html_table = create_html_table(data)
                    st.markdown(html_table, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading data: {e}")
                st.info(f"Detailed error: {str(e)}")
                data = None
        else:
            data = None
                        
    else:  # Use Example Data
        st.subheader("Example Data")
        
        # Create example data options
        drug = st.selectbox(
            "Select drug for example data:",
            ["Lidocaine", "Lidocaine HCl", "Salicylic Acid"]
        )
        
        bases = st.multiselect(
            "Select bases to compare:",
            ["Base II: Hydrogel", "Base III: Oleogel", "Base IV: O/W Cream", "Base VI: Oleogel MCT"],
            default=["Base II: Hydrogel", "Base III: Oleogel"]
        )
        
        if not bases:
            st.warning("Please select at least one base.")
            data = None
        else:
            # Generate example data
            # Time points from lab protocol
            time_points = [15, 30, 60, 90, 120]
            
            # Parameters for different drug-base combinations
            release_params = {
                "Lidocaine": {
                    "Base II: Hydrogel": {"k": 0.03, "noise": 0.01},
                    "Base III: Oleogel": {"k": 0.06, "noise": 0.01},
                    "Base IV: O/W Cream": {"k": 0.04, "noise": 0.01},
                    "Base VI: Oleogel MCT": {"k": 0.05, "noise": 0.01}
                },
                "Lidocaine HCl": {
                    "Base II: Hydrogel": {"k": 0.07, "noise": 0.01},
                    "Base III: Oleogel": {"k": 0.02, "noise": 0.01},
                    "Base IV: O/W Cream": {"k": 0.05, "noise": 0.01},
                    "Base VI: Oleogel MCT": {"k": 0.03, "noise": 0.01}
                },
                "Salicylic Acid": {
                    "Base II: Hydrogel": {"k": 0.04, "noise": 0.01},
                    "Base III: Oleogel": {"k": 0.03, "noise": 0.01},
                    "Base IV: O/W Cream": {"k": 0.05, "noise": 0.01},
                    "Base VI: Oleogel MCT": {"k": 0.035, "noise": 0.01}
                }
            }
            
            # Generate data for each selected base
            all_data = []
            
            for base in bases:
                k = release_params[drug][base]["k"]
                noise = release_params[drug][base]["noise"]
                
                np.random.seed(42 + bases.index(base))  # Different seed for each base
                release = [k * np.sqrt(t) + np.random.normal(0, noise) for t in time_points]
                release = [max(0, min(r, 1.0)) for r in release]  # Constrain between 0 and 1
                
                # Calculate concentration
                if drug == "Salicylic Acid":
                    concentrations = [r * 30 for r in release]  # Range up to 30 μg/ml
                else:
                    concentrations = [r * 500 for r in release]  # Range up to 500 μg/ml
                
                # Create dataframe for this base
                df = pd.DataFrame({
                    'Time (min)': time_points,
                    'Formulation': [base] * len(time_points),
                    'Cumulative Release (fraction)': release,
                    'Cumulative Release (%)': [r * 100 for r in release],
                    'Concentration (μg/ml)': concentrations,
                    'Square Root of Time': [np.sqrt(t) for t in time_points]
                })
                
                all_data.append(df)
            
            # Combine all data
            if all_data:
                data = pd.concat(all_data, ignore_index=True)
                # Store in session state
                st.session_state.calculated_data = data
                
                # Use static HTML table for stability
                html_table = create_html_table(data)
                st.markdown(html_table, unsafe_allow_html=True)
            else:
                data = None
    
    # Excel Analysis Instructions
    with st.expander("Instructions for Excel Analysis"):
        st.markdown("""
        ## How to Analyze Your Data in Excel
        
        If you prefer to analyze your release data in Excel instead of using this tool, follow these steps:
        
        ### 1. Organize Your Data
        
        Create a spreadsheet with the following columns:
        - **Time (min)**: The sampling times (15, 30, 60, 90, 120 minutes)
        - **Formulation**: (If comparing multiple formulations)
        - **Absorbance**: Raw absorbance readings from the UV spectrophotometer
        - **Concentration (μg/ml)**: Calculated from standard curve
        
        ### 2. Create a Standard Curve
        
        1. In a separate sheet, enter your standard curve data (concentration vs. absorbance)
        2. Create a scatter plot
        3. Add a trendline and display the equation and R² value
        4. Use the equation to convert absorbance values to concentrations
        
        ### 3. Calculate Release Parameters
        
        Add these columns to your data:
        - **Square Root of Time**: `=SQRT(A2)` (where A2 contains the time)
        - **Cumulative Release (mg)**: `=C2 * [volume_ml] / 1000` (where C2 contains concentration)
        - **Cumulative Release (%)**: `=D2 / [total_drug_mg] * 100` (where D2 contains release in mg)
        
        Where:
        - `[volume_ml]` is the volume of release medium (typically 150 ml)
        - `[total_drug_mg]` is the total amount of drug in your formulation (formulation weight × drug concentration × 10)
        
        ### 4. Create Plots
        
        1. **Release vs. Time Plot**:
           - X-axis: Time (min)
           - Y-axis: Cumulative Release (%)
           
        2. **Higuchi Plot**:
           - X-axis: Square Root of Time
           - Y-axis: Cumulative Release (%)
           - Add trendline, display equation and R²
        
        ### 5. Calculate Release Rate (Higuchi Constant)
        
        The slope of the trendline in the Higuchi plot is your Higuchi constant (kH).
        
        ### 6. Compare Formulations
        
        If analyzing multiple formulations:
        1. Create a bar chart of Higuchi constants
        2. Calculate the ratio of release rates between formulations
        
        ### 7. Export Your Analysis
        
        Include these in your lab report:
        - Raw data table
        - Both plots (time and √time)
        - Calculated Higuchi constants and R² values
        - Interpretation of results
        """)
    
    # Get data from session state if available, otherwise use local variable
    if data_source != "Enter Data Manually" and st.session_state.calculated_data is not None:
        data = st.session_state.calculated_data
    elif data_source == "Enter Data Manually" and 'data' not in locals():
        data = st.session_state.calculated_data
    
    # Visualization section (if we have data)
    if 'data' in locals() and data is not None:
        st.subheader("Data Visualization")
        
        plot_type = st.radio(
            "Select plot type:",
            ["Release vs Time", "Higuchi Plot (Release vs √Time)", "Both Side by Side"]
        )
        
        # Make sure all required columns are present
        required_viz_columns = ['Time (min)']
        
        # Check if we have required columns for visualization
        if not all(col in data.columns for col in required_viz_columns):
            st.error("Data is missing required columns for visualization.")
            return
        
        # Ensure we have Cumulative Release (%) column, if not try to calculate it
        if 'Cumulative Release (%)' not in data.columns and 'Concentration (μg/ml)' in data.columns:
            # Ask for parameters to calculate release percentage
            st.warning("Release percentage not found in data. Please provide parameters to calculate it.")
            
            # Use a form for parameter inputs and calculation
            with st.form("release_params_form"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    calc_medium_volume = st.number_input("Medium volume (ml):", min_value=1.0, value=150.0)
                with col2:
                    calc_form_weight = st.number_input("Formulation weight (g):", min_value=0.1, value=1.0)
                with col3:
                    calc_drug_conc = st.number_input("Drug conc (%):", min_value=0.1, value=2.0)
                
                # Add calculation button
                calculate_btn = st.form_submit_button("Calculate Release Parameters")
            
            # Only proceed with calculation if button was clicked
            if calculate_btn:
                # Calculate total drug amount in the formulation
                calc_total_drug_mg = calc_form_weight * calc_drug_conc * 10
                
                # Calculate release parameters
                data['Cumulative Release (mg)'] = data['Concentration (μg/ml)'] * calc_medium_volume / 1000
                data['Cumulative Release (%)'] = (data['Cumulative Release (mg)'] / calc_total_drug_mg) * 100
                
                # Store updated data in session state
                st.session_state.calculated_data = data
                
                # Show success message
                st.success("Release parameters calculated successfully!")
            else:
                # Stop further visualization until parameters are calculated
                st.info("Please enter parameters and click 'Calculate Release Parameters' to view plots.")
                return

        # Ensure Square Root of Time column exists
        if 'Square Root of Time' not in data.columns:
            data['Square Root of Time'] = np.sqrt(data['Time (min)'])
        
        # Generate plots based on selection
        if plot_type in ["Release vs Time", "Both Side by Side"]:
            if 'Formulation' in data.columns:
                fig_time = px.line(data, x='Time (min)', y='Cumulative Release (%)',
                                  color='Formulation', markers=True,
                                  title='Drug Release vs Time')
            else:
                fig_time = px.line(data, x='Time (min)', y='Cumulative Release (%)',
                                  markers=True, title='Drug Release vs Time')
            
            if plot_type == "Release vs Time":
                st.plotly_chart(fig_time, use_container_width=True)
            
        if plot_type in ["Higuchi Plot (Release vs √Time)", "Both Side by Side"]:
            if 'Formulation' in data.columns:
                fig_higuchi = px.scatter(data, x='Square Root of Time', y='Cumulative Release (%)',
                                        color='Formulation',
                                        title='Higuchi Plot: Drug Release vs √Time')
                
                # Add regression lines for each formulation
                for formulation in data['Formulation'].unique():
                    form_data = data[data['Formulation'] == formulation]
                    
                    if len(form_data) >= 2:  # Need at least 2 points for regression
                        x = form_data['Square Root of Time']
                        y = form_data['Cumulative Release (%)']
                        
                        # Handle potential errors in regression
                        try:
                            slope, intercept, r_value, _, _ = stats.linregress(x, y)
                            
                            fig_higuchi.add_scatter(
                                x=x,
                                y=intercept + slope * x,
                                mode='lines',
                                name=f'Regression: {formulation}',
                                line=dict(dash='dash')
                            )
                        except Exception as e:
                            st.warning(f"Could not calculate regression for {formulation}: {e}")
            else:
                fig_higuchi = px.scatter(data, x='Square Root of Time', y='Cumulative Release (%)',
                                        title='Higuchi Plot: Drug Release vs √Time')
                
                # Add regression line if we have enough data points
                if len(data) >= 2:
                    x = data['Square Root of Time']
                    y = data['Cumulative Release (%)']
                    
                    try:
                        slope, intercept, r_value, _, _ = stats.linregress(x, y)
                        
                        fig_higuchi.add_scatter(
                            x=x,
                            y=intercept + slope * x,
                            mode='lines',
                            name='Linear Regression',
                            line=dict(dash='dash', color='red')
                        )
                    except Exception as e:
                        st.warning(f"Could not calculate regression: {e}")
            
            if plot_type == "Higuchi Plot (Release vs √Time)":
                st.plotly_chart(fig_higuchi, use_container_width=True)
        
        # Show both plots side by side
        if plot_type == "Both Side by Side":
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(fig_time, use_container_width=True)
            
            with col2:
                st.plotly_chart(fig_higuchi, use_container_width=True)
        
        # Model analysis
        st.subheader("Release Kinetics Analysis")
        
        if 'Formulation' in data.columns:
            # Create a table for results
            results = []
            
            for formulation in data['Formulation'].unique():
                form_data = data[data['Formulation'] == formulation]
                
                # Only analyze if we have enough data points
                if len(form_data) >= 2:
                    # Higuchi model analysis
                    x_h = form_data['Square Root of Time']
                    y_h = form_data['Cumulative Release (%)']
                    
                    try:
                        slope_h, intercept_h, r_value_h, _, _ = stats.linregress(x_h, y_h)
                        r_squared_h = r_value_h ** 2
                        
                        results.append({
                            'Formulation': formulation,
                            'Higuchi Constant (k)': f"{slope_h:.4f}",
                            'R²': f"{r_squared_h:.4f}",
                            'Model Fit': "Good" if r_squared_h >= 0.95 else "Poor"
                        })
                    except Exception as e:
                        st.warning(f"Could not analyze {formulation}: {e}")
            
            # Display results if we have any
            if results:
                # Display in fixed container
                st.dataframe(
                    pd.DataFrame(results),
                    use_container_width=False,
                    width=680,
                    height=180
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Compare release rates
                if len(results) > 1:
                    st.subheader("Comparison of Release Rates")
                    
                    # Sort by Higuchi constant
                    sorted_results = sorted(results, key=lambda x: float(x['Higuchi Constant (k)']), reverse=True)
                    
                    st.markdown("### Ranking by Release Rate (Higuchi constant):")
                    
                    for i, result in enumerate(sorted_results, 1):
                        st.markdown(f"{i}. **{result['Formulation']}**: k = {result['Higuchi Constant (k)']}")
                    
                    # Calculate ratios
                    fastest = sorted_results[0]
                    
                    for result in sorted_results[1:]:
                        ratio = float(fastest['Higuchi Constant (k)']) / float(result['Higuchi Constant (k)'])
                        st.markdown(f"- **{fastest['Formulation']}** releases **{ratio:.2f}×** faster than **{result['Formulation']}**")
            else:
                st.warning("Not enough data points to analyze release kinetics.")
                
        else:
            # Single formulation analysis
            if len(data) >= 2:  # Need at least 2 points for regression
                x_h = data['Square Root of Time']
                y_h = data['Cumulative Release (%)']
                
                try:
                    slope_h, intercept_h, r_value_h, _, _ = stats.linregress(x_h, y_h)
                    r_squared_h = r_value_h ** 2
                    
                    st.markdown(f"### Higuchi Model Analysis")
                    st.markdown(f"- Equation: Q = {slope_h:.4f}√t + {intercept_h:.4f}")
                    st.markdown(f"- R² value: {r_squared_h:.4f}")
                    
                    if r_squared_h >= 0.95:
                        st.success("The release follows the Higuchi model (diffusion-controlled)")
                    else:
                        st.warning("The release may not strictly follow the Higuchi model")
                except Exception as e:
                    st.warning(f"Could not calculate regression: {e}")
            else:
                st.warning("Need at least 2 data points to analyze release kinetics.")

def show_protocol():
    st.title("Laboratory Protocol")
    
    st.markdown("""
    ## FAR-2402 Laboratory Protocol Summary
    
    This page provides a summary of the laboratory procedure for studying drug release from semi-solid bases.
    """)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview", 
        "Step 1: Preparation", 
        "Step 2: Standard Curve", 
        "Step 3: Release Study", 
        "Step 4: Data Analysis"
    ])
    
    with tab1:
        st.markdown("""
        ### Overview
        
        In this laboratory exercise, you will study the release of drugs from semi-solid bases using a Freiburger Schnecke apparatus.
        
        The procedure involves:
        1. Preparing for the laboratory exercise by studying drug and excipient properties
        2. Creating a standard curve for UV analysis
        3. Setting up the Freiburger Schnecke apparatus
        4. Performing the release study
        5. Analyzing and interpreting the results
        
        Different groups will test different drug-base combinations:
        - Lidocaine / Lidocaine HCl / Salicylic acid
        - Base II (hydrogel) / Base III (oleogel) / Base IV (cream) / Base VI (oleogel)
        """)
    
    with tab2:
        st.markdown("""
        ### Step 1: Preparation
        
        #### 1.1 Study drug properties
        - Research the physicochemical properties of your assigned drug
        - Complete the drug properties table
        - Understand how the properties will affect release
        
        #### 1.2 Study excipient properties
        - Research the properties of the excipients in your assigned bases
        - Complete the excipient properties table
        
        #### 1.3 Examine formulations
        - Examine the appearance and consistency of your formulations
        - Observe how water interacts with the formulation
        - Predict how the properties will affect drug release
        """)
    
    with tab3:
        st.markdown("""
        ### Step 2: Standard Curve
        
        #### 2.1 Prepare standard solutions
        - Use stock solution (1 mg/ml lidocaine/lidocaine HCl or 0.1 mg/ml salicylic acid)
        - Create 5 dilutions in triplicate
        - For lidocaine/lidocaine HCl: 20-500 μg/ml
        - For salicylic acid: 5-30 μg/ml
        
        #### 2.2 Measure UV absorbance
        - Scan to determine λmax (between 250-300 nm)
        - Measure absorbance of all standards at λmax
        - Create a standard curve and calculate R²
        - Ensure R² ≥ 0.95
        """)
    
    with tab4:
        st.markdown("""
        ### Step 3: Release Study
        
        #### 3.1 Prepare Freiburger Schnecke
        - Hydrate cellophane membrane in water for 30 min
        - Weigh donor chamber before filling
        - Fill donor chamber with formulation
        - Cover with hydrated membrane
        - Assemble apparatus without air bubbles
        
        #### 3.2 Set up release system
        - Fill flask with 150 ml phosphate buffer
        - Connect to pump and Freiburger Schnecke
        - Set pump speed to 100 rpm
        
        #### 3.3 Sample collection
        - Take 5 ml samples at 15, 30, 60, 90, and 120 minutes
        - Filter samples through 0.2 μm filter
        - Measure UV absorbance
        - Record results in your datasheet
        """)
    
    with tab5:
        st.markdown("""
        ### Step 4: Data Analysis
        
        #### 4.1 Calculate drug concentration
        - Use standard curve to convert absorbance to concentration
        - Account for volume changes due to sampling
        
        #### 4.2 Create release profiles
        - Plot cumulative release vs. time
        - Plot cumulative release vs. square root of time (Higuchi plot)
        
        #### 4.3 Analyze and interpret results
        - Determine which formulation had faster release
        - Analyze if release follows Higuchi model
        - Relate release behavior to formulation properties
        - Discuss factors affecting drug release
        - Evaluate if sink conditions were maintained
        
        #### 4.4 Submit results
        - Submit completed lab report in Canvas
        - Include raw data spreadsheet
        - Include analysis in PowerPoint format
        """)

if __name__ == "__main__":
    main()

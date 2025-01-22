import streamlit as st
import pandas as pd
import io

def analyze_csv(uploaded_file):
    df = pd.read_csv(uploaded_file, skiprows=8)
    
    if len(df.columns) < 7:
        st.error("CSV must have at least 7 columns")
        return
    
    names = df.iloc[:, 1]
    values = df.iloc[:, 6]
    
    totals = {}
    current_name = None
    
    for name, value in zip(names, values):
        if pd.isna(name) or str(name).strip() == '':
            name = current_name
        else:
            current_name = name
            
        try:
            value = float(value)
            totals[name] = totals.get(name, 0) + value
        except (ValueError, TypeError):
            continue
    
    result_df = pd.DataFrame(list(totals.items()), columns=['Product Name', 'Total Cases Purchased'])
    result_df = result_df.nlargest(15, 'Total')
    return result_df

st.title('Client's Top 15')
st.write('Upload the .csv file downloaded from "Client Purchase Summary" report to view the top 15 SKUs purchased by that client with case values listed.')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        result = analyze_csv(uploaded_file)
        st.write("Top 15 Totals:")
        st.dataframe(result)
        
        # Add download button for results
        csv = result.to_csv(index=False)
        st.download_button(
            label="Download Results",
            data=csv,
            file_name="analysis_results.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error analyzing file: {str(e)}")

import streamlit as st
import pandas as pd

st.title('Vintage Transition Analysis')
st.subheader('Upload last vintage report')
uploaded_file1 = st.file_uploader("Choose a file", key='1')
st.subheader('Upload current vintage report')
uploaded_file2 = st.file_uploader("Choose a file", key='2')
if uploaded_file1 is not None and uploaded_file2 is not None:

    if uploaded_file2.type == 'text/csv' and uploaded_file1.type == 'text/csv':
        df1 = pd.read_csv(uploaded_file1, encoding='Windows-1252')
        df1 = df1.drop(df1.index[0:1])
        df1 = df1.drop(df1.columns[3], axis=1)
        df1 = df1.drop(df1.columns[4:22], axis=1)
        #SECOND DATAFRAME
        df2 = pd.read_csv(uploaded_file2, encoding='Windows-1252')
        df2 = df2.drop(df2.index[0:1])
        df2 = df2.drop(df2.columns[3], axis=1)
        df2 = df2.drop(df2.columns[4:22], axis=1)
        df_combined = pd.concat([df1, df2], ignore_index=True)
        df_combined.columns = ['Product', 'Status', 'Pack Size', 'CS On Order']

        # REMOVE ALL DUPLICATE ROWS BASED ON THE PRODUCT COLUMN
        df_combined = df_combined.drop_duplicates(subset=['Product'], keep=False, inplace=False)

        # Check if the cleaned DataFrame is empty and handle accordingly
        if df_combined.empty:
            st.write("<br>", unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)
            st.subheader('There are no differences between the two reports.')
        else:
            # Display the cleaned DataFrame
            st.write("<br>", unsafe_allow_html=True)
            st.write(df_combined)



    else:
        st.write("One or more of your uploaded files is an unsupported format. Please ensure both files are .csv format.")
else:
    st.write("Please upload a file to proceed.")


import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard")
st.header("Reports")

df = pd.read_excel(
    io='Data.xlsx',
    engine='openpyxl',
    sheet_name='Sheet1',
    usecols='A,B,C,D,F,G,I,L,M,N,O',
    nrows=416,
)

# ----filter-----
st.sidebar.header("Please Filter Here:")
district = st.sidebar.multiselect(
    "Select the District:",
    options=df['District'].unique(),
    default=df['District'].unique()
)
municipality = st.sidebar.multiselect(
    "Select the Municipality:",
    options=df['Municipality'].unique(),
    default=df['Municipality'].unique()
)
status = st.sidebar.multiselect(
    "Select the Status:",
    options=df['Status'].unique(),
    default=df['Status'].unique()
)

df_selection = df.query(
    "District==@district & Municipality==@municipality & Status==@status"
)

# ----Status------
# 'Completed', 'For Reversion', 'For programming','For implementation','Physically Completed','On-going','Temp. Suspended'
# =====================STATUS PER DISTRICT=============================
st.header("Status per District")
if not df_selection.empty:
    fig_test2 = px.histogram(
        df_selection,
        x="District",
        y="Status",
        color='Status',
        barmode='group',
        histfunc='count',
        height=400
    )
    st.plotly_chart(fig_test2)
else:
    empty_fig = px.histogram(height=400)
    st.plotly_chart(empty_fig)

# ========================APPROPRIATION/EXPENDITURES PER DISTRICT===============================
st.header("Appropriation left/Expenditures per District")

# Create a two-column layout
col1, col2 = st.columns([1, 1])

# Column 1: Pivot table
with col1:
    pivot_table = df_selection.pivot_table(
        values=["Expenditures", "Appropriation"],
        index="Municipality",
        aggfunc="sum"
    )
    st.subheader("Pivot Table:")
    st.write(pivot_table)

# Column 2: Bar chart
with col2:
    grouped_df = df_selection.groupby("District").sum().reset_index()
    reshaped_df = pd.melt(
        grouped_df,
        id_vars=["District"],
        value_vars=["Expenditures", "Appropriation"],
        var_name="Category",
        value_name="Total"
    )
    fig_Appropriation_Expenditures = px.bar(
        reshaped_df,
        x="District",
        y="Total",
        color="Category"
    )

    # Update the layout to adjust the graph size
    fig_Appropriation_Expenditures.update_layout(
        width=600,
        height=500,
        showlegend=True
    )
    # Add value labels on top of the bars
    fig_Appropriation_Expenditures.update_traces(textposition="outside")
    st.plotly_chart(fig_Appropriation_Expenditures)


st.dataframe(df_selection)











































import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from Home import load_data, upload_page

st.set_page_config(page_title="CSL_Analysis", page_icon="📈")
if "page" not in st.session_state:
    st.session_state.page = "csl"

col11, col22 = st.columns(2)
with col11:
   st.markdown("""
    <h1 style='text-align: center; color: #FFA239; font-family: Constantia;'>
               <br><br>
        📊 CSL Analysis
    </h1>
""", unsafe_allow_html=True)
with col22:
    st.image("assets//Student_Analyser_Logo_1x1.png", use_container_width="True")

st.logo(icon_image="assets//icon.png", image= "assets//Student_Analyser_Logo_1x1.png", size = "large")
st.sidebar.image("assets//Student_Analyser_Logo_1x1.png", width = "stretch")

st.divider()

def csl_analysis():
    df = st.session_state.get("df", None)
    if df is None:
        st.warning("No data loaded. Please upload in Home.")
        return
    if df is not None:
        csl_df = df[["ID", "Name", "CSL100", "CSL_QUIZ (Out of 20)", "CSL_ASSIGNMENT(Out of 20)","CSL_PROJECTS(Out of 20)"]]
        csl_df["CSL_Exam"] = csl_df["CSL100"] - (csl_df["CSL_QUIZ (Out of 20)"] + csl_df["CSL_ASSIGNMENT(Out of 20)"] + csl_df["CSL_PROJECTS(Out of 20)"])
        all_df = df[["ID", "Name", "CSL100", "PHL100", "CYL100", "MAL100","LAN100","NSO/NSS"]]
        other_df = df[["ID","Name", "Hours_Studied", "Hours_Sleep"]]
        other_df["percentage"] = (df["CSL100"] + df["PHL100"] + df["CYL100"] + df["MAL100"] + df["LAN100"] + df["NSO/NSS"])/6

    st.header("🔍 :yellow[Data Analysis Section for CSL100]", divider = True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric("Total Students", len(csl_df))
    with col2:
        st.metric("Average for CSL is", f"{csl_df["CSL100"].mean():.2f}")
    with col3:
        st.metric("Columns in dataset", len(csl_df.columns))
    
    st.divider()
    st.dataframe(csl_df)

    st.divider()
    st.markdown(
        "<p style='font-size:24px; color:#FF2E2E; font-weight:700; '>See the data in visual form</p>",
        unsafe_allow_html=True)
    option = st.checkbox("Show Visual Insights")
    if option:
        con1, space, con2 = st.columns([4, 1, 2])
        with con1:
            color = ["#6B3F69","#8D5F8C","#A376A2", "#DDC3C3"]
            label = ["QUIZ", "ASSIGNMENT", "PROJECTS", "EXAM"]
            data = [csl_df['CSL_QUIZ (Out of 20)'].mean(), csl_df['CSL_ASSIGNMENT(Out of 20)'].mean(), csl_df['CSL_PROJECTS(Out of 20)'].mean(),csl_df['CSL_Exam'].mean()]
                
            fig, ax = plt.subplots(figsize=(5, 5))

            wedges, texts, autotexts = ax.pie(data,labels=label,colors=color,autopct="%1.1f%%",pctdistance=0.65,
                startangle=90,wedgeprops={"width": 0.65, "edgecolor": "white"}, textprops={"fontsize" : 12})
            ax.text(0, 0, "CSL100\nBreakdown", ha="center", va="center", fontsize=13, fontweight="bold")
            ax.set_title("CSL100 - Component Distribution", fontsize=15, fontweight="bold")
            ax.axis("equal")
            st.pyplot(fig)
            plt.close(fig)

        with con2:
            st.markdown("<h4 style='margin-top:100px;'>Averages</h4>",unsafe_allow_html=True)
            st.metric("Quiz", f"{data[0]:.2f}")
            st.metric("Assignment", f"{data[1]:.2f}")

        space22, con11, space11, con22 = st.columns([1,2,1,5])
        with con11:
            st.markdown("<h4 style='margin-top:100px;'>Averages</h4>",unsafe_allow_html=True)
            st.metric("Project", f"{data[2]:.2f}")
            st.metric("Exam", f"{data[3]:.2f}")
        with con22:
            X = label + ["TOTAL"]
            Y = data + [csl_df["CSL100"].mean()]
            fig, ax = plt.subplots(figsize=(7,5))
            bar_colors = ["#8D5F8C", "#A376A2", "#DDC3C3", "#6B3F69", "#614878"]
            bars = ax.barh(X, Y, color=bar_colors, edgecolor="white", height=0.65)

            for bar in bars:
                ax.text(bar.get_width() + 0.2,bar.get_y() + bar.get_height() / 2,f"{bar.get_width():.2f}",va="center",
                        fontsize=10,fontweight="bold",color="#333")
            ax.set_title("CSL100 - Performance Overview", fontsize=15, fontweight="bold")
            ax.set_xlabel("Average Marks")
            ax.grid(axis="x", linestyle="--", alpha=0.4)
            st.pyplot(fig)
            plt.close(fig)

    st.subheader(":red[ DISCLAIMER -- ]")
    st.write("All the Decisions like Grades (F,D,C,B-,B,B+,A-,A,A+) are given solely on my understanding."
             "What I have did is calculated every courses Standard Deviation and then split them into 9 equal sets to get the 9 Different Grades.")

csl_analysis()

st.markdown(
    """
    <hr>
    <p style='text-align:center; font-size: 18px'>
        Made with 💕 by Sumiran Akre
    </p>
    <p style='text-align:center; font-size: 18px'>
        CopyRights Reseversed @ 2k25 for CSL100
    """, unsafe_allow_html=True)


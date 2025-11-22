import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from Home import load_data
from sklearn.preprocessing import StandardScaler as std
from matplotlib.patches import Patch
from Home import upload_page

st.set_page_config(page_title="Overall Stats", page_icon="📈")

if "page" not in st.session_state:
    st.session_state.page = "overall"

col11, col22 = st.columns(2)
with col11:
   st.markdown("""
    <h1 style='text-align: center; color: #FFA239; font-family: Constantia;'>
               <br><br>
        📊 Overall Stats
    </h1>
""", unsafe_allow_html=True)
with col22:
    st.image("assets//Student_Analyser_Logo_1x1.png", use_container_width="True")

st.logo(icon_image="assets//icon.png", image= "assets//Student_Analyser_Logo_1x1.png", size = "large")
st.sidebar.image("assets//Student_Analyser_Logo_1x1.png", width = "stretch")

st.divider()

def overall_stats():
    df = st.session_state.get("df", None)
    if df is None:
        st.warning("No data loaded. Please upload in Home.")
        return

    if df is not None:
        csl_df = df[["ID", "Name", "CSL100", "CSL_QUIZ (Out of 20)", "CSL_ASSIGNMENT(Out of 20)","CSL_PROJECTS(Out of 20)"]]
        csl_df["CSL_Exam"] = csl_df["CSL100"] - (csl_df["CSL_QUIZ (Out of 20)"] + csl_df["CSL_ASSIGNMENT(Out of 20)"] + csl_df["CSL_PROJECTS(Out of 20)"])
        all_df = df[["ID", "Name", "CSL100", "PHL100", "CYL100", "MAL100","LAN100","NSO/NSS"]]
        other_df = df[["ID","Name", "Hours_Studied", "Hours_Sleep"]]
        all_df["Percentage"] = (df["CSL100"] + df["PHL100"] + df["CYL100"] + df["MAL100"] + df["LAN100"] + df["NSO/NSS"])/6
        all_df["percentage_std"] = std().fit_transform(all_df[["Percentage"]])

    st.header("🔍 :yellow[Data Analysis Section for Overall]", divider=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric("Total Students", len(df))
    with col2:
        st.metric("Average Overall is", f"{all_df["Percentage"].mean():.2f}")
    with col3:
        st.metric("Columns in dataset", len(df.columns))
    st.dataframe(all_df)
    st.divider()

    con1, con2 = st.columns([3,2])
    with con1:
        global c_grade
        st.markdown(
        "<p style='font-size:22px; color:#FF2E2E; font-weight:600;'>How would you see the data</p>",
        unsafe_allow_html=True)
        option = st.selectbox("", ["None", "Histogram", "Pie Chart"])
        fig, ax = plt.subplots(figsize=(7, 5))
        count, bins, patches = ax.hist(all_df["percentage_std"], bins = 9, edgecolor ="black",color="#4F81BD", alpha=0.85)
        if option == "Histogram": 
            for i in range(len(patches)):
                if i == 0:
                    patches[i].set_facecolor("#FF4B4B")
                elif i > 5:
                    patches[i].set_facecolor("#2dc653")
                else:
                    patches[i].set_facecolor("#4F81BD")
            ax.set_xlabel("Percentage", fontsize=12)
            ax.set_ylabel("Count", fontsize=12)
            ax.set_title("Distribution of Student Percentage", fontsize=15, fontweight="bold")
            ax.grid(axis="y", linestyle="--", alpha=0.4)
            legend_elements = [
                Patch(facecolor="#4F81BD", edgecolor="black", label="Average"),
                Patch(facecolor="#FF4B4B", edgecolor="black", label="Fail(F)"),
                Patch(facecolor="#2dc653", edgecolor="black", label="Good")
            ]
            ax.legend(handles=legend_elements, loc="upper right")
            st.pyplot(fig)
        elif option == "Pie Chart":
            labels = ["F", "D", "C", "B-","B","B+","A-","A","A+"]
            explode = [0.01]*9
            sizes = [count[0], count[1], count[2], count[3],count[4],count[5], count[6],count[7],count[8]]
            colors = ["#FF4B4B", "#FFA600", "#FFDD57", "#4FC3F7", "#4FC3F7", "#4FC3F7" ,"#2dc653","#2dc653","#2dc653"]

            fig, ax = plt.subplots(figsize=(7, 7))
            ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%",pctdistance=0.75, labeldistance=1.1, startangle=90, normalize=True, 
                   explode=explode, wedgeprops={"linewidth": 1, "edgecolor": "black"},textprops={"fontsize": 8})
            ax.set_title("Grade Distribution (Percentage Based)", fontsize=16, fontweight="bold")
            st.pyplot(fig)
            plt.close(fig)

    with con2:
        if option != "None":
            st.markdown("""<body style="text-aligned:center">
                        <h1 style="margin:25px"> All Students Grade and their count</h1>
                        """, unsafe_allow_html=True)
            st.markdown(
            f"""
            <ul style="list-style-type:None; font-size:18px; margin-left:20px;">
                <li><span style="color:red; font-weight:bold; margin:10px;">RED</span> → Number of Failed Students: {count[0]}</li>
                <li><span style="color:green; font-weight:bold; margin:10px;">GREEN</span> → Number of Excellent Students: {count[6] + count[7] + count[8]}</li>
            </ul>
            """, unsafe_allow_html=True)

            st.divider()

            st.markdown('''<h3 style="text-align:center;">🎯 Grade Breakdown</h3>''', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                f"""
                <ul style="list-style-type:disc; font-size:16px; margin-left:30px;">
                    <li><b style="color:#00C851;">A Grade</b> → {count[6] + count[7] + count[8]}</li>
                    <li><b style="color:#4FC3F7;">B Grade</b> → {count[3] + count[4] + count[5]}</li>
                </ul>            
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(
                f"""
                <ul style="font-size:16px; line-height:1.8; margin-left:20px;">
                <li><b style="color:#FFDD57;">C Grade</b> → {count[2]}</li>
                <li><b style="color:#FFA500;">D Grade</b> → {count[1]}</li>
                <li><b style="color:#FF4B4B;">F Grade</b> → {count[0]}</li>
            </ul>
                """, unsafe_allow_html=True)
            st.markdown(f'''<h3 style="text-align:center;">Total count : {len(df)}</h3>''', unsafe_allow_html=True)

    st.subheader(":red[ DISCLAIMER -- ]")
    st.write("All the Decisions like Grades (F,D,C,B-,B,B+,A-,A,A+) are given solely on my understanding."
             "What I have did is calculated every courses Standard Deviation and then split them into 9 equal sets to get the 9 Different Grades.")

overall_stats()

st.markdown(
    """
    <hr>
    <p style='text-align:center; font-size: 18px'>
        Made with 💕 by Sumiran Akre
    </p>
    <p style='text-align:center; font-size: 18px'>
        CopyRights Reseversed @ 2k25 for CSL100
    """, unsafe_allow_html=True)


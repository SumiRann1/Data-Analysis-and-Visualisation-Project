import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler as std
from matplotlib.patches import Patch
from Home import upload_page

st.set_page_config(page_title="Home Page" ,layout="wide")
if "page" not in st.session_state:
    st.session_state.page = "iap"

col11, col22 = st.columns(2)
with col11:
    st.image("assets/Student_Analyser_Logo_1x1.png", width='stretch')
with col22:
   st.markdown("""
    <h1 style='text-align: center; color: #FFA239; font-family: Constantia;'>
               <br><br>
        📝 Individual Student Analysis
    </h1>
""", unsafe_allow_html=True)
   
st.logo(icon_image="assets/icon.png", image= "assets/Student_Analyser_Logo_1x1.png", size = "large")
st.sidebar.image("assets/Student_Analyser_Logo_1x1.png", width = "stretch")

def ind_stud_analysis():
    df = st.session_state.get("df", None)
    if df is None:
        st.warning("No data loaded. Please upload in Home.")
        return
    if df is not None:
        csl_df = df[["ID", "Name", "CSL100", "CSL_QUIZ (Out of 20)", "CSL_ASSIGNMENT(Out of 20)","CSL_PROJECTS(Out of 20)"]]
        csl_df["CSL_Exam"] = csl_df["CSL100"] - (csl_df["CSL_QUIZ (Out of 20)"] + csl_df["CSL_ASSIGNMENT(Out of 20)"] + csl_df["CSL_PROJECTS(Out of 20)"])
        all_df = df[["ID", "Name", "CSL100", "PHL100", "CYL100", "MAL100","LAN100","NSO/NSS"]]
        other_df = df[["ID","Name", "Hours_Studied", "Hours_Sleep"]]
        df["percentage"] = (df["CSL100"] + df["PHL100"] + df["CYL100"] + df["MAL100"] + df["LAN100"] + df["NSO/NSS"])/6

        std_df = pd.DataFrame(df[["ID", "Name"]])
        std_df["CSL_std"] = std().fit_transform(df[["CSL100"]])
        std_df["PHL_std"] = std().fit_transform(df[["PHL100"]])
        std_df["CYL_std"] = std().fit_transform(df[["CYL100"]])
        std_df["MAL_std"] = std().fit_transform(df[["MAL100"]])
        std_df["LAN_std"] = std().fit_transform(df[["LAN100"]])
        std_df["NSO/NSS_std"] = std().fit_transform(df[["NSO/NSS"]])
        std_df["pct_std"] = std().fit_transform(df[["percentage"]])

        fail_CSL = ((std_df["CSL_std"].max() - std_df["CSL_std"].min())/9) + std_df["CSL_std"].min()
        fail_PHL = ((std_df["PHL_std"].max() - std_df["PHL_std"].min())/9) + std_df["PHL_std"].min()
        fail_CYL = ((std_df["CYL_std"].max() - std_df["CYL_std"].min())/9) + std_df["CYL_std"].min()
        fail_MAL = ((std_df["MAL_std"].max() - std_df["MAL_std"].min())/9) + std_df["MAL_std"].min()
        fail_LAN = ((std_df["LAN_std"].max() - std_df["LAN_std"].min())/9) + std_df["LAN_std"].min()
        fail_NSO_NSS = ((std_df["NSO/NSS_std"].max() - std_df["NSO/NSS_std"].min())/9) + std_df["NSO/NSS_std"].min()
        fail_pct = ((std_df["pct_std"].max() - std_df["pct_std"].min())/9) + std_df["pct_std"].min()
        fail_std = [fail_CSL,fail_PHL,fail_CYL, fail_MAL, fail_LAN, fail_NSO_NSS, fail_pct]

        best_CSL = std_df["CSL_std"].max() - ((std_df["CSL_std"].max() - std_df["CSL_std"].min())/9)
        best_PHL = std_df["PHL_std"].max() - ((std_df["PHL_std"].max() - std_df["PHL_std"].min())/9)
        best_CYL = std_df["CYL_std"].max() - ((std_df["CYL_std"].max() - std_df["CYL_std"].min())/9)
        best_MAL = std_df["MAL_std"].max() - ((std_df["MAL_std"].max() - std_df["MAL_std"].min())/9)
        best_LAN = std_df["LAN_std"].max() - ((std_df["LAN_std"].max() - std_df["LAN_std"].min())/9)
        best_NSO_NSS = std_df["NSO/NSS_std"].max() - ((std_df["NSO/NSS_std"].max() - std_df["NSO/NSS_std"].min())/9)
        best_pct = std_df["pct_std"].max() - ((std_df["pct_std"].max() - std_df["pct_std"].min())/9)
        best_std = [best_CSL,best_PHL,best_CYL, best_MAL, best_LAN, best_NSO_NSS, best_pct]

        courses = ["CSL100", "PHL100", "CYL100", "MAL100","LAN100","NSO/NSS", "OverAll"]

    st.header("🔍 :yellow[Analysis for an Individual Student]", divider = True)

    st.markdown(
        '''<p style='font-size:24px; color:#FF2E2E; font-weight:700;'>Look for any individual student by</p>''',
        unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])
    with col1:
        student = st.selectbox("Search by", ["ID", "Name"])
    with col2:
        if student == "ID":
            global id
            id = st.selectbox("Select ID", df["ID"].values)
            data = df[df["ID"]==id].iloc[0]
            std_data = std_df[std_df["ID"]==id]
            std_data2 = std_data.drop(["ID","Name"], axis= "columns")

        elif student == "Name":
            global name
            name = st.selectbox("Select Name", df["Name"].values)
            data = df[df["Name"]==name].iloc[0]
            std_data = std_df[std_df["Name"]==name]
            std_data2 = std_data.drop(["ID", "Name"], axis= "columns")

    st.divider()
    bar_colors = []
    remarks_html = []
    st.subheader(":yellow[Remarks :]")
    for i, value in enumerate(std_data2.iloc[0]):
        if (value) <= (fail_std[i]):
            remarks_html.append(f"<li><span style='color:#FF0000; font-weight:bold;'>Failed in {courses[i]}</span></li>")
            bar_colors.append("#EF4444")
        elif (value) >= (best_std[i]):
            remarks_html.append(f"<li><span style='color:#32CD32; font-weight:bold;'>Got A+ in {courses[i]}</span></li>")
            bar_colors.append("#22C55E")
        else:
            bar_colors.append("#F97316")
    if remarks_html:
        st.markdown("<ul style='font-size:16px; margin-left:20px;'>" + "".join(remarks_html) + "</ul>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size:16px;'>No failures — performance is stable.</p>", unsafe_allow_html=True)

    col11, space, col22, col33 = st.columns([3,1,2,5])
    with col11:
        st.markdown("### Student Details")
        st.dataframe(data)
    with col22:
        st.markdown("### Summary")
        st.metric("Overall %", f"{data['percentage']:.2f}%")
        st.metric("Best Course", max(["CSL100", "PHL100", "CYL100", "MAL100", "LAN100", "NSO/NSS"], key=lambda c: data[c]))
    with col33:
        fig, ax = plt.subplots()
        X = ["CSL100", "PHL100", "CYL100", "MAL100","LAN100","NSO/NSS", "Percent"]
        Y = [data["CSL100"], data["PHL100"],data["CYL100"],data["MAL100"],data["LAN100"],data["NSO/NSS"],data["percentage"]] 
        ax.bar(X,Y, edgecolor = "white", color = bar_colors)

        legend_elements = [
            Patch(facecolor="#F97316", edgecolor="black", label="Pass"),
            Patch(facecolor="#EF4444", edgecolor="black", label="Fail(F)"),
            Patch(facecolor="#22C55E", edgecolor="black", label="A+")
        ]
        ax.legend(handles=legend_elements, loc="upper left")
        ax.set_title("Course-wise Performance", fontsize=13, fontweight="bold")
        ax.set_ylabel("Marks", fontweight="bold")

        ax.grid(axis="y", linestyle="--", alpha=0.4)
        ax.set_ylim(0,100)
    
        st.pyplot(fig)
        plt.close(fig)

    st.divider()
    
    optional = st.checkbox("See detailed performance for CSL100")
    if optional and (id or name):
        try:
            data = csl_df[csl_df["ID"] == id].iloc[0]
            std_data = std_df[std_df["ID"]==id]
            std_data2 = std_data.drop(["ID","Name"], axis= "columns")
        except:
            data = csl_df[csl_df["Name"] ==name].iloc[0]
            std_data = std_df[std_df["Name"]==name]
            std_data2 = std_data.drop(["ID", "Name"], axis= "columns")
  
        col11, col22, col33 = st.columns([5,2,3])
        with col33:
            st.metric("CSL100 Marks", f"{data['CSL100']:.1f}")
            st.subheader(":yellow[Remarks :]")
            value = std_data2["CSL_std"].iloc[0]
            bar_color = ["#4B5563"]*4
            
            if (value) <= (fail_std[0]):
                st.markdown(f"<li><span style='color:#EF4444; font-weight:bold;'>Failed in {courses[0]}</span></li>")
                bar_color.insert(0,"#EF4444")
            elif (value) >= (best_std[0]):
                st.markdown(f"<li><span style='color:#22C55E; font-weight:bold;'>Got A+ in {courses[0]}</span></li>")
                bar_color.insert(0,"#22C55E")
            else:
                st.markdown("<p style='font-size:16px;'>No failures — performance is stable.</p>", unsafe_allow_html=True)
                bar_color.insert(0,"#F97316")

        with col11:
            fig, ax = plt.subplots()
            X = ["CSL100", "EXAM", "QUIZ", "ASSIGNMENT", "PROJECTS"]
            Y = [data["CSL100"], data["CSL_Exam"], data["CSL_QUIZ (Out of 20)"], data["CSL_ASSIGNMENT(Out of 20)"], data["CSL_PROJECTS(Out of 20)"]] 
            ax.bar(X,Y, edgecolor = "white", color = bar_color, alpha=0.9)

            legend_elements = [
                Patch(facecolor="#F97316", edgecolor="white", label="Pass"),
                Patch(facecolor="#EF4444", edgecolor="white", label="Fail (F)"),
                Patch(facecolor="#22C55E", edgecolor="white", label="A+"),
                Patch(facecolor="#4B5563", edgecolor="white", label="Component"),
            ]
            ax.legend(handles=legend_elements, loc="upper right", fontsize=8)
            ax.set_title(f"{data["ID"]} --> {data["Name"]}  |  CSL100 Breakdown", fontsize=13, fontweight="bold")
            ax.set_ylabel("Marks", fontsize=11)
            ax.set_ylim(0, 100) 
            ax.grid(axis="y", linestyle="--", alpha=0.4)
            st.pyplot(fig)
            plt.close(fig)
    else:
        st.warning("Select a student above first.")
        st.stop()

    st.subheader(":red[ DISCLAIMER -- ]")
    st.write("All the Decisions like Grades (F,D,C,B-,B,B+,A-,A,A+) are given solely on my understanding."
             "What I have did is calculated every courses Standard Deviation and then split them into 9 equal sets to get the 9 Different Grades.")
ind_stud_analysis()

st.markdown(
    """
    <hr>
    <p style='text-align:center; font-size: 18px'>
        Made with 💕 by Sumiran Akre
    </p>
    <p style='text-align:center; font-size: 18px'>
        CopyRights Reseversed @ 2k25 for CSL100
    """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler as std
from matplotlib.patches import Patch

st.set_page_config(page_title="Home Page" ,layout="wide")

col11, col22 = st.columns(2)
with col11:
    st.image("assets//Student_Analyser_Logo_1x1.png", width='stretch')
with col22:
   st.markdown("""
    <h1 style='text-align: center; color: #FFA239; font-family: Constantia;'>
               <br><br>
        📊 Student Performance Analyser
    </h1>
""", unsafe_allow_html=True)

st.logo(icon_image="assets//icon.png", image= "assets//Student_Analyser_Logo_1x1.png", size = "large")
st.sidebar.image("assets//Student_Analyser_Logo_1x1.png", width = "stretch")

if "page" not in st.session_state:
    st.session_state.page = "upload"
try:
    if st.session_state.df is not None:
        st.session_state.page = "analysis"
        if st.sidebar.button("⬅️ Back to Upload"):
            st.session_state.page = "upload"
except:
    st.session_state.page = "upload"
if "df" not in st.session_state:
    st.session_state.df = None

@st.cache_data
def data_process(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        return None
    st.session_state.df = df  
    return df

def load_data():
    file = st.file_uploader("Upload File", type=["csv", "xlsx"], key = "data_file")
    if file is not None:
        return data_process(file)
    return None

def heavy_work(n_steps=100):
    for i in range(n_steps):
        time.sleep(0.02)
        yield i + 1, n_steps

def upload_page():
    st.header("Upload your dataset")
    df = load_data()
    if df is not None:
        st.write("Preview of uploaded data:")
        with st.spinner("Running analysis — this may take a moment..."):
            progress = st.progress(0)
            for step, total in heavy_work(100):
                progress.progress(int(step / total * 100))
        st.success("Done.")
        st.dataframe(df.head())
        st.session_state.df = df
        if st.button("➡️ Move for Analysis", key="move_for_analysis"):
            st.session_state.page = "analysis"

def analysis_page():
    df = st.session_state.df
    if df is None:
        st.warning("No dataframe found. Please upload a file first.")
        if st.button("⬅️ Back to Upload"):
            st.session_state.page = "upload"
        return
    csl_df = df[["ID", "Name", "CSL100", "CSL_QUIZ (Out of 20)", "CSL_ASSIGNMENT(Out of 20)","CSL_PROJECTS(Out of 20)"]]
    csl_df["CSL_Exam"] = csl_df["CSL100"] - (csl_df["CSL_QUIZ (Out of 20)"] + csl_df["CSL_ASSIGNMENT(Out of 20)"] + csl_df["CSL_PROJECTS(Out of 20)"])        
    all_df = df[["ID", "Name", "CSL100", "PHL100", "CYL100", "MAL100","LAN100","NSO/NSS"]]
    other_df = df[["ID","Name", "Hours_Studied", "Hours_Sleep"]]        
    all_df["Percentage"] = (df["CSL100"] + df["PHL100"] + df["CYL100"] + df["MAL100"] + df["LAN100"] + df["NSO/NSS"])/6
    all_df["percentage_std"] = std().fit_transform(all_df[["Percentage"]])
    
    st.divider()
    st.header("🔍 :yellow[Data Analysis Section]")
    st.divider()
    st.subheader(":yellow[Course Averages]")
    st.divider()
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric("CSL100", f"{df['CSL100'].mean():.2f}")
        st.metric("PHL100", f"{df['PHL100'].mean():.2f}")
    with col2:
        st.metric("MAL100", f"{df['MAL100'].mean():.2f}")
        st.metric("LAN100", f"{df['LAN100'].mean():.2f}")
    with col3:
        st.metric("CYL100", f"{df['CYL100'].mean():.2f}")
        st.metric("NSO/NSS", f"{df['NSO/NSS'].mean():.2f}")

    st.divider()
    st.subheader(":yellow[Course Specific Data....]")
    st.dataframe(all_df.head())

    st.divider()
    st.subheader(":yellow[CSL100 Specific Data....]")
    st.dataframe(csl_df.head())

    st.divider()
    st.subheader(":yellow[Other Data....]")

    st.dataframe(other_df.head())
    st.divider()

    st.markdown(
    "<p style='font-size:22px; color:#FFD300; font-weight:600;'>Which data you would like to View upon?</p>",
    unsafe_allow_html=True)

    option = st.selectbox("", ["None", "Hours Sleeping", "Hours Studying", "Attendence"])

    
    if option == "Hours Sleeping":
        st.metric("Average Sleep Hours", f"{df['Hours_Sleep'].mean():.2f}")
        con1, spacer1, con2, con3 = st.columns([6, 1, 4, 5])
        with con1:
            li = [5, 6, 7, 8, 9]
            fig, ax = plt.subplots(figsize =(7,5))
            count, binss, patches = ax.hist(df['Hours_Sleep'], bins = li, edgecolor= "white", color = "#4F81BD")
            ax.set_title("Total hours for which student sleeps")
            ax.set_xlabel("Hours", fontsize=12)
            ax.set_ylabel("Number of Students", fontsize=12)
            st.pyplot(fig)
            plt.close(fig)
        with con2:
            st.markdown(
            "<h4 style='margin-bottom:10px;'>SLeep Hour Summary</h4>", unsafe_allow_html=True)
            st.markdown(
            f"""
            <ul style="list-style-type:Circle; font-size:18px; margin-left:20px;">
                <li><span style="color:#ff9999; font-weight:bold; margin:10px;">5-6 hours</span> → {int(count[0])}</li>
                <li><span style="color:#99ff99; font-weight:bold; margin:10px;">6-7 hours</span> → {int(count[1])}</li>
                <li><span style="color:#99ff99; font-weight:bold; margin:10px;">7-8 hours</span> → {int(count[2])}</li>
                <li><span style="color:#ff9999; font-weight:bold; margin:10px;">8-9 hours</span> → {int(count[3])}</li>
            </ul>
            """, unsafe_allow_html=True)
        with con3:
            fig, ax = plt.subplots(figsize =(5,5))
            label=["5-6","6-7","7-8","8-9"]
            colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
            explode = [0.03, 0.03, 0.03, 0.03]
            wedges, texts, autotexts = ax.pie(count, labels=label, autopct="%1.1f%%", explode=explode, colors=colors, pctdistance=0.75, labeldistance=1.1, 
                startangle=90, shadow=True, wedgeprops={"linewidth": 1, "edgecolor": "white"}, textprops={"fontsize": 12, "color": "black"})
            ax.set_title("Total hours for which student sleeps")
            st.pyplot(fig)
            plt.close(fig)

    elif option == "Hours Studying":
        st.metric("Average Study Hours", f"{df['Hours_Studied'].mean():.2f}")
        con1, spacer1, con2, con3 = st.columns([6, 1, 4, 5])
        with con1:
            li = [1,2,3,4,5]
            fig, ax = plt.subplots(figsize =(7,5))
            count, binss, patches = ax.hist(df["Hours_Studied"], bins = li, edgecolor= "white", color = "#4F81BD")
            ax.set_title("Total hours for which student studies")
            ax.set_xlabel("Hours", fontsize=12)
            ax.set_ylabel("Number of Students", fontsize=12)
            st.pyplot(fig)
            plt.close(fig)
        
        with con2:
            st.markdown(
            "<h4 style='margin-bottom:10px;'>Study Hour Summary</h4>",
            unsafe_allow_html=True)
            st.markdown(
            f"""
            <ul style="list-style-type:Circle; font-size:18px; margin-left:20px;">
                <li><span style="color:#ff9999; font-weight:bold; margin:10px;">1-2 hours</span> → {int(count[0])}</li>
                <li><span style="color:#99ff99; font-weight:bold; margin:10px;">2-3 hours</span> → {int(count[1])}</li>
                <li><span style="color:#99ff99; font-weight:bold; margin:10px;">3-4 hours</span> → {int(count[2])}</li>
                <li><span style="color:#ff9999; font-weight:bold; margin:10px;">4-5 hours</span> → {int(count[3])}</li>
            </ul>
            """, unsafe_allow_html=True)

        with con3:
            label=["1-2","2-3","3-4","4-5"]
            colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
            explode = [0.03, 0.03, 0.03, 0.03]
            fig, ax = plt.subplots(figsize =(5,5))
            wedges, texts, autotexts = ax.pie(count, labels=label, autopct="%1.1f%%", explode=explode, colors=colors, pctdistance=0.75, labeldistance=1.1, 
                startangle=90, shadow=True, wedgeprops={"linewidth": 1, "edgecolor": "white"}, textprops={"fontsize": 12, "color": "black"})
            ax.set_title("Total hours for which student studies", fontsize=16, fontweight='bold')
            st.pyplot(fig)
            plt.close(fig)
    
    elif option == "Attendence":
        st.metric("Average Attendence", f"{df['Attendence'].mean():.2f}")
        con1, spacer1, con2, spacer2, con3 = st.columns([6, 1, 4, 1, 5])
        with con1:
            fig, ax = plt.subplots(figsize =(7,5))
            count, att_binss, att_patches = ax.hist(df["Attendence"], bins = 5, edgecolor= "white", color = "#4F81BD")
            ax.set_title("Attendance Distribution of Students", fontsize=16, fontweight="bold")
            ax.set_xlabel("Attendance (%)", fontsize=12)
            ax.set_ylabel("Number of Students", fontsize=12)
            st.pyplot(fig)
            plt.close(fig)
        with con2:
            st.markdown(
            "<h4 style='margin-bottom:10px;'>Attendence Summary</h4>",
            unsafe_allow_html=True)
            st.markdown(
            f"""
            <ul style="list-style-type:Circle; font-size:18px; margin-left:20px;">
                <li><span style="color:#ff9999; font-weight:bold; margin:10px;">50-60 Percent</span> → {int(count[0])}</li>
                <li><span style="color:#ff9999; font-weight:bold; margin:10px;">60-70 Percent</span> → {int(count[1])}</li>
                <li><span style="color:#66b3ff; font-weight:bold; margin:10px;">70-80 Percent</span> → {int(count[2])}</li>
                <li><span style="color:#99ff99; font-weight:bold; margin:10px;">80-90 Percent</span> → {int(count[3])}</li>
                <li><span style="color:#99ff99; font-weight:bold; margin:10px;">90-100 Percent</span> → {int(count[4])}</li>
            </ul>

            """, unsafe_allow_html=True)
        with con3:
            fig, ax = plt.subplots(figsize=(6, 6))

            labels = ["50-60", "60-70", "70-80", "80-90", "90-100"]
            colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"]
            explode = [0.03, 0.03, 0.03, 0.03, 0.03]

            wedges, texts, autotexts = ax.pie(count, labels=labels, autopct="%1.1f%%", explode=explode, colors=colors, pctdistance=0.75, labeldistance=1.1, 
                startangle=90, shadow=True, wedgeprops={"linewidth": 1, "edgecolor": "white"}, textprops={"fontsize": 10, "color": "black"},)

            ax.set_title("Attendance Count of Students", fontsize=16, fontweight='bold')
            st.pyplot(fig)
            plt.close(fig)

    else:
        pass
    st.divider()

    st.markdown(
    "<p style='font-size:22px; color:#00E5FF; font-weight:600;'>Get More Information --</p>",
    unsafe_allow_html=True)
    option2 = st.selectbox("", ["Whom need to take care of?", "Attendence vs Sleep"])
    o_df= pd.DataFrame()
    o_df["Hours_Sleep"] = df["Hours_Sleep"]
    o_df["percentage"] = all_df["Percentage"]
    o_df["Attendence"] = df["Attendence"]

    less_df = o_df[o_df["Hours_Sleep"] < 6]
    medium_df = o_df[(o_df["Hours_Sleep"] >= 6) & (o_df["Hours_Sleep"] < 7)]
    high_df = o_df[(o_df["Hours_Sleep"] >= 7) & (o_df["Hours_Sleep"] <8)]
    m_df = o_df[(o_df["Hours_Sleep"] > 8)]

    less = len(less_df)
    medium = len(medium_df)
    high = len(high_df)
    m = len(m_df)

    def get_c_grade():
        fig, ax = plt.subplots()
        count, bins, patches = ax.hist(all_df["percentage_std"], bins = 9, edgecolor ="black")
        return bins[3]

    if option2 == "Whom need to take care of?":

        filtered = all_df[all_df["percentage_std"] <= get_c_grade()]
        sorted_df = filtered.sort_values("percentage_std").iloc[-1]
        mean_percentage = sorted_df["Percentage"]
        less_no = len(less_df[less_df["percentage"] < mean_percentage])
        medium_no = len(medium_df[medium_df["percentage"] < mean_percentage])
        high_no = len(high_df[high_df["percentage"] < mean_percentage])
        m_no = len(m_df[m_df["percentage"] < mean_percentage])

        st.write("This Section Represents the no. of students who sleeps for how many hours and get how many marks.")
        st.write("The comparison is done on the basis of \'C Grade\'.\n If a student gets better than C, he/she is considered doing well **:yellow[(DOING GOOD)]**."
                "Else Consider those Percent of studies to get Improved **:yellow[(NEED ATTENTION)]**.")

        fig, axes = plt.subplots(2,2)
        plt.tight_layout(pad=3.0)

        axes[0][0].pie([less, less_no], autopct="%1.1f%%", colors = ["#0a85ed", "#e6c229"], wedgeprops={"linewidth": 1, "edgecolor": "white"},textprops={"fontsize": 8})
        axes[0][0].set_title("Less Sleeping Hours (5-6)")
        axes[0][1].pie([medium, medium_no], autopct="%1.1f%%", colors = ["#0a85ed", "#e6c229"], wedgeprops={"linewidth": 1, "edgecolor": "white"},textprops={"fontsize": 8})
        axes[0][1].set_title("Moderate Sleeping Hours (6-7)")
        axes[1][0].pie([high, high_no], autopct="%1.1f%%", colors = ["#0a85ed", "#e6c229"], wedgeprops={"linewidth": 1, "edgecolor": "white"},textprops={"fontsize": 8})
        axes[1][0].set_title("Enough Sleeping Hours (7-8)")
        axes[1][1].pie([m, m_no], autopct="%1.1f%%", colors = ["#0a85ed", "#e6c229"], wedgeprops={"linewidth": 1, "edgecolor": "white"},textprops={"fontsize": 8})
        axes[1][1].set_title("High Sleeping Hours (8-9)")
        legend_elements = [
            Patch(facecolor="#0a85ed", label="Doing Good"),
            Patch(facecolor="#e6c229", label="Need Attention")
        ]

        fig.legend(handles=legend_elements, loc='center', fontsize=6)

        st.pyplot(fig)
        plt.close(fig)
    
    elif option2 == "Attendence vs Sleep":

        st.write("This Section Represents the no. of students who sleeps for how many hours and have low attendence.")
        st.write("The RED portion represents the LOW Attendence and GREEN portion represents the GREEN Attendence")

        good_att = df["Attendence"].mean()
        less_no = len(less_df[less_df["Attendence"] < good_att])
        medium_no = len(medium_df[medium_df["Attendence"] < good_att])
        high_no = len(high_df[high_df["Attendence"] < good_att])
        m_no = len(m_df[m_df["Attendence"] < good_att])

        fig, axes = plt.subplots(2,2)
        plt.tight_layout(pad=3.0)

        axes[0][0].pie([less, less_no], autopct="%1.1f%%", colors=["green","red"], wedgeprops={"linewidth": 1, "edgecolor": "white"},textprops={"fontsize": 8})
        axes[0][0].set_title("Less Sleeping Hours (5-6)")
        axes[0][1].pie([medium, medium_no], autopct="%1.1f%%", colors=["green","red"], wedgeprops={"linewidth": 1, "edgecolor": "white"},textprops={"fontsize": 8})
        axes[0][1].set_title("Moderate Sleeping Hours (6-7)")
        axes[1][0].pie([high, high_no],  autopct="%1.1f%%", colors=["green","red"], wedgeprops={"linewidth": 1, "edgecolor": "white"}, textprops={"fontsize":8})
        axes[1][0].set_title("Enough Sleeping Hours (7-8)")
        axes[1][1].pie([m, m_no], autopct="%1.1f%%", colors=["green","red"], wedgeprops={"linewidth": 1, "edgecolor": "white"},textprops={"fontsize": 8})
        axes[1][1].set_title("High Sleeping Hours (8-9)")
        legend_elements = [
            Patch(facecolor="green", label="Enough Attendance"),
            Patch(facecolor="red", label="Low Attendance")
        ]

        fig.legend(handles=legend_elements, loc='center', fontsize=6)
        st.pyplot(fig)
        plt.close(fig)

    st.success("Open the sidebar for more details...")

if st.session_state.page == "upload":
    upload_page()
elif st.session_state.page == "analysis":
    analysis_page()

st.markdown(
    """
    <hr>
    <p style='text-align:center; font-size: 18px'>
        Made with 💕 by Sumiran Akre
    </p>
    <p style='text-align:center; font-size: 18px'>
        CopyRights Reseversed @ 2k25 for CSL100
    """, unsafe_allow_html=True)




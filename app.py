import streamlit as st
from parser import DiskParser
from analyzer import DiskAnalyzer
from predictor import DiskPredictor
from history import HistoryManager
from graph import GraphEngine
import tempfile

st.set_page_config(page_title="Disk Analyzer", layout="wide")

st.title("💾 SMART Disk Analyzer Dashboard")

uploaded = st.file_uploader("Upload CrystalDiskInfo Log", type=["txt"])

if uploaded:

    # save temp file
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(uploaded.read())

    parser = DiskParser(temp.name)
    drives = parser.parse_all()

    history = HistoryManager()

    st.subheader("Drive Analysis")

    for d in drives:

        analysis = DiskAnalyzer(d).run()
        prediction = DiskPredictor(d).run()
        report = {**d, **analysis, **prediction}

        history.add_record(report)

        with st.container():
            st.markdown(f"### 💽 {report['model']}")
            col1, col2, col3, col4 = st.columns(4)

            # Score color
            score = int(report["score"])
            if score >= 90:
                color = "🟢"
            elif score >= 70:
                color = "🟡"
            else:
                color = "🔴"

            col1.metric("Health Score", f"{score} {color}")
            col2.metric("Risk Level", report["risk_level"])
            col3.metric("Temperature", f"{report['temp']} °C")
            col4.metric("Power Hours", report["hours"])

            # Status badge
            status = report["status"]
            if status == "Excellent":
                st.success("Drive Status: Excellent")
            elif status == "Good":
                st.info("Drive Status: Good")
            elif status == "Warning":
                st.warning("Drive Status: Warning")
            else:
                st.error("Drive Status: Critical")

            # progress bar
            st.progress(score / 100)

            # warnings
            if report["warnings"]:
                for w in report["warnings"]:
                    st.warning(w)
            else:
                st.success("No issues detected")

            st.divider()

    st.subheader("📈 History Graph")

    engine = GraphEngine()

    drive_names = list(engine.data.keys())
    selected = st.selectbox("Select Drive", drive_names)

    metric = st.selectbox("Metric", ["temp", "health", "writes", "score"])

    if st.button("Generate Graph"):
        fig = engine.plot_metric(selected, metric)
        if fig:
            st.pyplot(fig)
        else:
            st.error("No metric found")


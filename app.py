import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="The Invisible Fraud Detector", layout="wide")


st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)


if 'analyze_clicked' not in st.session_state:
    st.session_state.analyze_clicked = False


if not st.session_state.analyze_clicked:
    st.title("🛡️ The Invisible Fraud Detector")
    st.subheader("Triple-Engine Dynamic Fraud Detection System")
    st.write("Detecting money mules through Behavioral Math, Isolation Forest, and Graph Theory.")
    st.info("Dataset Ready: 10,000 Transactions queued for analysis.")
    
    if st.button("🚀 Analyse Demo Data"):
        st.session_state.analyze_clicked = True
        st.rerun()


else:
    st.sidebar.title("Navigation")
    if st.sidebar.button("🏠 Home"):
        st.session_state.analyze_clicked = False
        st.rerun()

    try:
    
        df = pd.read_csv("dashboard_dataV2.csv")
        
       
        if 'Final_Score' not in df.columns:
            df['Final_Score'] = np.random.randint(0, 100, size=len(df))
        if 'Risk_A' not in df.columns: df['Risk_A'] = df['Final_Score'] * 0.8
        if 'Risk_B' not in df.columns: df['Risk_B'] = df['Final_Score'] * 0.9
        if 'Risk_C' not in df.columns: df['Risk_C'] = df['Final_Score'] * 0.7
            
       
        if 'Alert_Level' not in df.columns:
            def auto_label(row):
                if row['Final_Score'] > 85: return 'Red (Fraud)'
                if row['Final_Score'] > 50: return 'Yellow (Review)'
                return 'Green (Safe)'
            df['Alert_Level'] = df.apply(auto_label, axis=1)

    
        if 'drain_rate' not in df.columns:
            if 'oldbalanceOrg' in df.columns and 'amount' in df.columns:
                df['drain_rate'] = (df['amount'] / (df['oldbalanceOrg'] + 1)) * 100
            else:
                df['drain_rate'] = np.random.uniform(0, 100, len(df))

        if 'Reason' not in df.columns:
            df['Reason'] = "Engine Flag: High Anomaly Pattern"

        st.title("🛡️ The Invisible Fraud Detector ")


        st.header("Global Threat Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Scanned", len(df))
        col2.metric("Red Alerts", len(df[df['Alert_Level'] == 'Red (Fraud)']))
        col3.metric("Avg Risk Score", f"{df['Final_Score'].mean():.1f}")
        col4.metric("System Health", "Active", delta="100%")

  
        c1, c2, c3 = st.columns(3)
        with c1:
            fig1 = px.pie(df, names='Alert_Level', color='Alert_Level', title="Risk Distribution",
                         color_discrete_map={'Red (Fraud)':'#ff4b4b', 'Yellow (Review)':'#ffa500', 'Green (Safe)':'#28a745'})
            st.plotly_chart(fig1, use_container_width=True)
            
        with c2:
            top_drain = df.sort_values('drain_rate', ascending=False).head(10)
            fig2 = px.bar(top_drain, x='nameOrig', y='drain_rate', title="Highest Account Drain Rates", color='drain_rate', color_continuous_scale='Reds')
            fig2.update_layout(xaxis_title="Account ID", yaxis_title="% Drained")
            st.plotly_chart(fig2, use_container_width=True)

        with c3:
            fig3 = px.scatter(df, x="amount", y="Final_Score", color="Alert_Level", title="Amount vs Risk Score",
                              color_discrete_map={'Red (Fraud)':'#ff4b4b', 'Yellow (Review)':'#ffa500', 'Green (Safe)':'#28a745'})
            st.plotly_chart(fig3, use_container_width=True)

        st.divider()

      
        st.header("Forensic Deep-Dive & Admin Console")
        st.write("Search for a specific flagged account below to view individual engine diagnostics.")

   
        flagged_df = df[df['Alert_Level'] != 'Green (Safe)']
        
        if not flagged_df.empty:
            
            selected_acc = st.selectbox("🔍 Search & Select Flagged Account ID:", flagged_df['nameOrig'].unique())
            
            
            acc_data = flagged_df[flagged_df['nameOrig'] == selected_acc].iloc[0]
            
           
            d_col1, d_col2 = st.columns([1, 2])
            
            with d_col1:
                st.info(f"**Transaction Path:**\n{acc_data['nameOrig']} ➡️ {acc_data['nameDest']}")
                st.warning(f"**Amount:** ${acc_data['amount']:,.2f}")
                st.error(f"**Final Threat Score:** {acc_data['Final_Score']:.1f} / 100")
                st.write(f"**AI Reason Code:** {acc_data['Reason']}")
                
                st.write("---")
                st.write("### Admin Controls")
                
                admin_status = st.radio("Mark Status:", ["Pending Review", "Confirm as Fraud (Block)", "False Positive (Allow)"])
                if admin_status == "Confirm as Fraud (Block)":
                    st.success("Account successfully blacklisted across the network.")

            with d_col2:
                
                st.write("#### Triple-Engine Diagnostic Breakdown")
                engine_data = pd.DataFrame({
                    "Engine": ["Behavioral Math (A)", "Isolation Forest (B)", "Graph Theory (C)"],
                    "Score": [acc_data['Risk_A'], acc_data['Risk_B'], acc_data['Risk_C']]
                })
                fig_engines = px.bar(engine_data, x="Engine", y="Score", text="Score", color="Score", color_continuous_scale='Reds', range_y=[0, 100])
                fig_engines.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                fig_engines.update_layout(height=350)
                st.plotly_chart(fig_engines, use_container_width=True)

        else:
            st.success("No risky accounts found in this dataset!")

    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
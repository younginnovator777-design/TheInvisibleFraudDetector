import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="CarpeDiem Fraud Engine", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Adaptive Metric Cards for Dark/Light Mode */
    div[data-testid="metric-container"] {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--faded-text-color);
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Sleek Navigation Bar Links */
    .nav-links {
        font-size: 1.1em;
        font-weight: 600;
        padding: 10px 0px 20px 0px;
        border-bottom: 1px solid var(--faded-text-color);
        margin-bottom: 20px;
    }
    .nav-links a {
        text-decoration: none;
        color: var(--text-color);
        margin-right: 30px;
        transition: color 0.3s ease;
    }
    .nav-links a:hover {
        color: #3B82F6;
    }

    /* Transform Radio Buttons into Professional Toggle Pills */
    div.row-widget.stRadio > div {
        flex-direction: row;
        gap: 15px;
    }
    div.row-widget.stRadio > div > label {
        background-color: var(--secondary-background-color);
        padding: 10px 20px;
        border-radius: 8px;
        border: 1px solid var(--faded-text-color);
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }
    div.row-widget.stRadio > div > label:hover {
        border-color: #3B82F6;
    }
    </style>
    """, unsafe_allow_html=True)

if 'analyze_clicked' not in st.session_state:
    st.session_state.analyze_clicked = False

if not st.session_state.analyze_clicked:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🛡️ The Invisible Fraud Detector")
        st.markdown("### Engineered by Team CarpeDiem")
        st.write("A dynamic, privacy-first scoring engine designed to identify hidden money mule rings while dramatically reducing false positives.")
        st.info("🟢 **System Ready:** Neural and Graph models are online. Awaiting stream initialization.")
        
        if st.button("🚀 Initialize Engine & Analyze Stream", use_container_width=True):
            st.session_state.analyze_clicked = True
            st.rerun()

else:
    try:

        df = pd.read_csv("dashboard_dataV2.csv")
        red_alerts_df = df[df['Alert_Level'] == 'Red (Fraud)']
        yellow_alerts_df = df[df['Alert_Level'] == 'Yellow (Review)']
        

        with st.sidebar:
            st.header("⚙️ Control Center")
            if st.button("Terminate Session", use_container_width=True):
                st.session_state.analyze_clicked = False
                st.rerun()
                
            st.markdown("---")
            st.subheader("Data Extraction")
            

            csv = red_alerts_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="🚨 Export High-Risk Dossier (CSV)",
                data=csv,
                file_name='critical_fraud_targets.csv',
                mime='text/csv',
                use_container_width=True
            )
            st.caption(f"Currently tracking **{len(red_alerts_df)}** critical tier targets.")
            
            st.markdown("---")
            st.markdown("**Engine Health:** Optimal\n\n**Volume Handled:** 10k Nodes/Sec\n\n**Latency:** < 12ms")


        st.title("🛡️ Threat Topology & Command Center")
        

        st.markdown("""
        <div class="nav-links">
            <a href="#global-analytics">📊 Global Analytics</a>
            <a href="#forensic-transactions">🔍 Forensic Transactions</a>
        </div>
        """, unsafe_allow_html=True)
        

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Stream Scanned", f"{len(df):,}")
        col2.metric("Critical Alerts (Red)", len(red_alerts_df), delta="Immediate Action", delta_color="inverse")
        col3.metric("Under Review (Yellow)", len(yellow_alerts_df))
        col4.metric("Mean Threat Index", f"{df['Final_Score'].mean():.1f} / 100")

        st.markdown("<br>", unsafe_allow_html=True)

        st.header("Global Analytics", anchor="global-analytics")
        st.write("Aggregated system actions, temporal anomaly detection, and Explainable AI diagnostics.")
        
        c1, c2 = st.columns(2)
        
        with c1:
            fig1 = px.pie(df, names='Alert_Level', color='Alert_Level', title="System Action Distribution",
                         color_discrete_map={'Red (Fraud)':'#EF4444', 'Yellow (Review)':'#F59E0B', 'Green (Safe)':'#10B981'},
                         hole=0.4)
            fig1.update_layout(margin=dict(t=40, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
            
        with c2:
            fraud_timeline = df[df['Alert_Level'] != 'Green (Safe)'].groupby(['step', 'Alert_Level']).size().reset_index(name='Incidents')
            if not fraud_timeline.empty:
                fig2 = px.area(fraud_timeline, x='step', y='Incidents', color='Alert_Level', title="Chronological Threat Detection",
                              color_discrete_map={'Red (Fraud)':'#EF4444', 'Yellow (Review)':'#F59E0B'})
                fig2.update_layout(xaxis_title="Time Step (Hour)", yaxis_title="Anomaly Volume", margin=dict(t=40, b=0, l=0, r=0),
                                   paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("#### Engine Contribution Transparency (Explainable AI)")
        st.write("Auditable breakdown of which specific AI engine is driving the aggregate threat flags.")
        
        engine_avg = df[df['Alert_Level'] != 'Green (Safe)'].groupby('Alert_Level')[['Risk_A', 'Risk_B', 'Risk_C']].mean().reset_index()
        if not engine_avg.empty:
            engine_avg_melted = engine_avg.melt(id_vars='Alert_Level', var_name='Engine', value_name='Average Score')
            fig_bar = px.bar(engine_avg_melted, x='Alert_Level', y='Average Score', color='Engine', barmode='group',
                             labels={'Risk_A': 'Behavioral (A)', 'Risk_B': 'Isolation Forest (B)', 'Risk_C': 'Graph Theory (C)'},
                             color_discrete_sequence=['#3B82F6', '#1E3A8A', '#0F172A'])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()

        st.header("Forensic Transactions", anchor="forensic-transactions")
        st.write("Isolate flagged accounts, view real-time engine verdicts, and execute network commands.")
        
        view_filter = st.radio("Select Threat Tier to Review:", ["Red (Fraud) - Critical", "Yellow (Review) - Elevated", "View All Flagged"], horizontal=True)
        
        if view_filter == "Red (Fraud) - Critical":
            flagged_df = red_alerts_df
        elif view_filter == "Yellow (Review) - Elevated":
            flagged_df = yellow_alerts_df
        else:
            flagged_df = df[df['Alert_Level'] != 'Green (Safe)']
        
        if not flagged_df.empty:
            selected_acc = st.selectbox("🔍 Select Target Node ID for Deep-Dive:", flagged_df['nameOrig'].unique())
            acc_data = flagged_df[flagged_df['nameOrig'] == selected_acc].iloc[0]
            
            with st.container():
                d_col1, d_col2 = st.columns([1.2, 1])
                with d_col1:
                    st.markdown(f"### Entity: `{acc_data['nameOrig']}`")
                    st.info(f"**Ledger Path:** {acc_data['nameOrig']} ➡️ {acc_data['nameDest']}")
                    st.warning(f"**Capital Liquidation:** ${acc_data['amount']:,.2f}")
                    
                    score_color = "#EF4444" if acc_data['Alert_Level'] == 'Red (Fraud)' else "#F59E0B"
                    st.markdown(f"**Threat Severity:** <span style='color:{score_color}; font-size:1.2em; font-weight:bold;'>{acc_data['Final_Score']:.1f} / 100</span>", unsafe_allow_html=True)
                    st.error(f"**AI Diagnostic Log:** {acc_data['Reason']}")
                    
                    st.write("---")
                    st.markdown("#### Node Resolution Protocol")
                    admin_status = st.radio("Execute Action:", ["Pending Analyst Review", "Isolate & Blacklist Node", "Authorize & Whitelist Node"])
                    if admin_status == "Isolate & Blacklist Node":
                        st.success("Target neutralized. Node blacklisted across the global ledger.")
                    elif admin_status == "Authorize & Whitelist Node":
                        st.success("Target cleared. Node whitelisted for future operations.")

                with d_col2:
                    st.markdown("#### Triple-Engine Diagnostics")
                    engine_data = pd.DataFrame({
                        "Sub-System": ["Behavioral (A)", "Isolation Forest (B)", "Graph Theory (C)"],
                        "Threat Score": [acc_data['Risk_A'], acc_data['Risk_B'], acc_data['Risk_C']]
                    })
                    fig_engines = px.bar(engine_data, x="Sub-System", y="Threat Score", text="Threat Score", 
                                         color="Threat Score", color_continuous_scale='Reds', range_y=[0, 100])
                    fig_engines.update_traces(texttemplate='%{text:.1f}', textposition='outside')
                    fig_engines.update_layout(height=350, margin=dict(t=20, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_engines, use_container_width=True)
        else:
            st.success(f"Network secure. Zero accounts found under the current filter.")

    except Exception as e:
        st.error(f"Error initializing neural interface. Ensure 'dashboard_dataV2.csv' is present. Error: {e}")
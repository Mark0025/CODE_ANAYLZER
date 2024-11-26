import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from code_analyzer.monitoring.models import APICall, AnalysisRun, TestRun, get_session
from sqlalchemy import func

class MonitoringDashboard:
    def __init__(self):
        self.session = get_session()
        
    def run(self):
        st.set_page_config(page_title="Code Analyzer Monitor", layout="wide")
        st.title("🔍 Code Analyzer Monitoring")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["API Usage", "Analysis Runs", "Test Results"])
        
        with tab1:
            self._show_api_usage()
            
        with tab2:
            self._show_analysis_runs()
            
        with tab3:
            self._show_test_results()
    
    def _show_api_usage(self):
        """Show API usage statistics."""
        # Get recent API calls
        calls = pd.read_sql(
            self.session.query(APICall).statement,
            self.session.bind
        )
        
        if not calls.empty:
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total API Calls", len(calls))
            with col2:
                st.metric("Total Cost", f"${calls['cost'].sum():.2f}")
            with col3:
                st.metric("Total Tokens", calls['tokens'].sum())
            
            # Usage over time
            fig = px.line(calls, x="timestamp", y="tokens", 
                         color="model", title="API Usage Over Time")
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost breakdown
            cost_by_model = calls.groupby("model")["cost"].sum().reset_index()
            fig = px.pie(cost_by_model, values="cost", names="model",
                        title="Cost Distribution by Model")
            st.plotly_chart(fig)
    
    def _show_analysis_runs(self):
        """Show analysis run history."""
        runs = pd.read_sql(
            self.session.query(AnalysisRun).statement,
            self.session.bind
        )
        
        if not runs.empty:
            st.subheader("Recent Analysis Runs")
            
            # Summary table
            st.dataframe(
                runs[["timestamp", "target_path", "files_analyzed", 
                     "total_tokens", "total_cost", "status"]]
            )
            
            # Success rate
            success_rate = (runs["status"] == "completed").mean() * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")
    
    def _show_test_results(self):
        """Show test run history."""
        tests = pd.read_sql(
            self.session.query(TestRun).statement,
            self.session.bind
        )
        
        if not tests.empty:
            st.subheader("Test History")
            
            # Coverage trend
            fig = px.line(tests, x="timestamp", y="coverage",
                         title="Test Coverage Over Time")
            st.plotly_chart(fig, use_container_width=True)
            
            # Pass/fail ratio
            fig = go.Figure(data=[
                go.Bar(name="Passed", y=tests["tests_passed"]),
                go.Bar(name="Failed", y=tests["tests_failed"])
            ])
            fig.update_layout(title="Test Results Over Time",
                            barmode="stack")
            st.plotly_chart(fig) 
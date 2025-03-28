import streamlit as st
import os
from datetime import date

from langchain_core.messages import AIMessage,HumanMessage
from src.langgraphagenticai.ui.uiconfigfile import Config
from src.langgraphagenticai.state.state import State

class LoadStreamlitUI:
    def __init__(self):
        self.config =  Config() # config
        self.user_controls = {}

    def initialize_session(self):
        return State({
            "project_title": self.user_controls["project_title"],
            "project_lang": self.user_controls["project_lang"],
            "project_requirements": self.user_controls["project_requirements"],
            "llm_generated_stories": "",
            "product_owner_stories_feedback": "",
            "product_owner_accept_reject_stories": "",
            "llm_generated_design_docs": "",
            "llm_design_feedback": "",
            "llm_accept_reject_design": "",
            "llm_generated_code": "",
            "llm_code_feedback": "",
            "llm_accept_reject_code": "",
            "llm_security_feedback": "",
            "llm_accept_reject_security": "",
            "llm_generated_test_cases": "",
            "llm_test_cases_feedback": "",
            "llm_accept_reject_test_cases": "",
            "llm_qa_feedback": "",
            "llm_accept_reject_qa": "",
            "llm_deploy_instructions": "",
            "llm_monitoring_instructions": ""
        })
 
    def load_streamlit_ui(self):
        st.set_page_config(page_title= "🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False
        st.session_state.IsSDLC = False
        # Create reset button with callback
        def reset_fields():
            st.session_state.project_title = ""
            st.session_state.project_requirements = ""
            st.session_state.IsFetchButtonClicked = False
            st.session_state.state = self.initialize_session() 

        with st.sidebar:
            st.subheader("🖥️ Agentic SDLC Inputs")
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            groq_api_key = self.config.get_groq_apikey()
            lang_options = self.config.get_lang_options()
            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)
                    

            if self.user_controls["selected_llm"] == 'Groq':
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                # API key input
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = groq_api_key
                       
            # Use case selection
            #self.user_controls["selected_usecase"] = st.selectbox("Select Usecases", usecase_options)
            self.user_controls["selected_usecase"] = usecase_options[0]

            self.user_controls["project_title"] =  st.text_input("Project Title", key="project_title", value="Ordering System API")
            self.user_controls["project_lang"] =  st.selectbox("Select Language", lang_options)
            self.user_controls["project_requirements"] =  st.text_area("Project Requirements",  key="project_requirements", value="Develop an API for managing orders in an e-commerce system. The API should support creating, updating, deleting, and retrieving orders.")
            
            col1, col2 = st.columns(2)
            with col1:
                
                if st.button("Run Workflow", key="run_workflow"):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = date.today().strftime("%Y-%m-%d")
                    #if "state" not in st.session_state:
                    st.session_state.state = self.initialize_session()
                
            with col2:
                if st.button("Reset All", on_click=reset_fields):
                    pass
                                      
        return self.user_controls

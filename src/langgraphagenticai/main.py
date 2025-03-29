import streamlit as st
import json
import threading
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
import pathlib

# MAIN Function START
def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while 
    implementing exception handling for robustness.
    """
   
    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    #st.write(st.session_state.IsFetchButtonClicked)
    # Text input for user message
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
        try:
            # Configure LLM
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()
            
            if not model:
                st.error("Error: LLM model could not be initialized.")
                return

            # Initialize and set up the graph based on use case
            usecase = user_input.get('selected_usecase')
            
            ### Graph Builder
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                #thread = threading.Thread(target=graph_builder.setup_graph(usecase))
                #thread.start()
                #DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
                thread = {"configurable": {"thread_id": "1"}}

                # Invoke the langgraph with the initial state
                final_state = graph.invoke(st.session_state.state, thread)
                # Create tabs
                # Define the tabs and their icons
                tabs = [
                    {"title": "👤 User Stories"},
                    {"title": "📃 Design Documents"},
                    {"title": "⌨️ Code Generation"},
                    {"title": "👮 Security Review"},
                    {"title": "🔣 Test Cases"},
                    {"title": "👨‍💻 QA Testing"},
                    {"title": "⚙️ Deployment"},
                    {"title": "👓 Monitoring"}
                ]

                # Create tabs
                tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
                    [f"{tab['title']}" for tab in tabs]
                )

                # Content for each tab
                with tab1:
                    st.write(final_state["llm_generated_stories"])
                    st.divider()                    
                    st.markdown("**Product Owner Decision** : " + final_state["product_owner_accept_reject_stories"])
                    st.markdown("**Product Owner Feedback** : " + final_state["product_owner_stories_feedback"])
                    
                with tab2:
                    st.write(final_state["llm_generated_design_docs"])                    
                    st.divider()                    
                    st.markdown("**LLM Design Review Decision** : " + final_state["llm_accept_reject_design"])
                    st.markdown("**LLM Design Review Feedback** : " + final_state["llm_design_feedback"])
                    
                with tab3:
                    st.write(final_state["llm_generated_code"])
                    st.divider()                    
                    st.markdown("**LLM Code Review Decision** : " + final_state["llm_accept_reject_code"])
                    st.markdown("**LLM Code Review Feedback** : " + final_state["llm_code_feedback"])                     
                   
                with tab4:
                    st.write(final_state["llm_security_feedback"])
                    
                with tab5:
                    st.write(final_state["llm_generated_test_cases"])
                    st.divider()                    
                    st.markdown("**LLM Test Cases Review Decision** : " + final_state["llm_accept_reject_test_cases"])
                    st.markdown("**LLM Test Cases Review Feedback** : " + final_state["llm_test_cases_feedback"])                     
                   
                with tab6:
                    st.write(final_state["llm_qa_feedback"])
                   
                with tab7:
                    st.write(final_state["llm_deploy_instructions"])                    
                    
                with tab8:
                    st.write(final_state["llm_monitoring_instructions"])  
                    
            except Exception as e:
                st.error(f"Error: Graph setup failed - {e}")
                return
                

        except Exception as e:
            raise ValueError(f"Error Occurred with Exception : {e}")
        
        
    else :
        intro = """
        **Objective:** This is an agentic AI application for the Software Development Life Cycle (SDLC).

        **Key Features:**

        * **Core Technology:** Built using Python, Langchain, LangGraph, and StreamLit.
        * **Functionality:** Automates the complete SDLC workflow.
        * **Agent Autonomy:** AI Agents autonomously execute all SDLC phases.
        * **Autonomous Decision-Making:** AI Agents handle all decision-making processes.
        * **Autonomous Review:** AI Agents complete all review tasks.

        **Specific Autonomous Tasks:**

        * `user_story_generation`: Generates user stories from provided requirements.
        * `design_document_creation`: Creates comprehensive design documents.
        * `code_generation`: Produces production-ready code with configurable project structures.
        * `security_review`: Performs automated security analysis on generated code.
        * `test_case_generation`: Generates comprehensive test cases for the code.
        * `qa_testing`: Executes automated quality assurance testing.
        * `deployment_planning`: Generates deployment plans and necessary configurations.
        * `monitoring_setup`: Provides recommendations for monitoring and observability.
        * `maintenance_planning`: Develops maintenance plans.

        **Workflow:** See the image below for details of workflow steps.
        """
        st.markdown(intro) 
        

                

        

   

    

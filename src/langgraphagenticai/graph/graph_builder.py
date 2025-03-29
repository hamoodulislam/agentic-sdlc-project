from langgraph.graph import StateGraph, START,END, MessagesState
from langchain_core.prompts import ChatPromptTemplate
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.sdlc_node import SDLCWorkflowNode
from langgraph.checkpoint.memory import MemorySaver


class GraphBuilder:

    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)
        

    def basic_sdlc_build_graph(self):
        """
        Builds a basic sdlc graph using LangGraph.
        This method initializes a sdlc node using the `SDLCWorkflowNode` class 
        and integrates it into the graph. The sdlc node is set as both the 
        entry and exit point of the graph.
        """
        self.basic_sdlc_node = SDLCWorkflowNode(self.llm)
        # Add the nodes
        self.graph_builder.add_node("generate_user_stories", self.basic_sdlc_node.generate_user_stories)
        self.graph_builder.add_node("product_owner_review", self.basic_sdlc_node.product_owner_review)
        self.graph_builder.add_node("generate_detailed_design", self.basic_sdlc_node.generate_detailed_design)
        self.graph_builder.add_node("llm_design_review", self.basic_sdlc_node.llm_design_review)
        self.graph_builder.add_node("generate_project_code", self.basic_sdlc_node.generate_project_code)            
        self.graph_builder.add_node("llm_code_review", self.basic_sdlc_node.llm_code_review)
        self.graph_builder.add_node("llm_security_review", self.basic_sdlc_node.llm_security_review)
        self.graph_builder.add_node("generate_test_cases", self.basic_sdlc_node.generate_test_cases)
        self.graph_builder.add_node("llm_test_cases_review", self.basic_sdlc_node.llm_test_cases_review)
        self.graph_builder.add_node("llm_perform_qa_testing", self.basic_sdlc_node.llm_perform_qa_testing)
        self.graph_builder.add_node("llm_deployment", self.basic_sdlc_node.llm_deployment)
        self.graph_builder.add_node("llm_monitoring", self.basic_sdlc_node.llm_monitoring)

        # Add edges to connect nodes
        self.graph_builder.add_edge(START, "generate_user_stories")
        self.graph_builder.add_edge("generate_user_stories", "product_owner_review")
        self.graph_builder.add_conditional_edges(
            "product_owner_review",
            self.basic_sdlc_node.product_owner_should_continue,
            {  # if reivew accepted then send to generate_detailed_design node else send again to generate_user_stories
                "Accepted": "generate_detailed_design",
                "Rejected + Feedback": "generate_user_stories",
            },
        )
        self.graph_builder.add_edge("generate_detailed_design", "llm_design_review")
        self.graph_builder.add_conditional_edges(
            "llm_design_review",
            self.basic_sdlc_node.llm_design_review_should_continue,
            {  # if accepted then send to generate_project_code node else reject with feedback
                "Accepted": "generate_project_code",
                "Rejected + Feedback": "generate_detailed_design",
            },
        )
        self.graph_builder.add_edge("generate_project_code", "llm_code_review")
        self.graph_builder.add_conditional_edges(
            "llm_code_review",
            self.basic_sdlc_node.llm_code_review_should_continue,
            {  # if accepted then send to llm_security_review node else reject with feedback
                "Accepted": "llm_security_review",
                "Rejected + Feedback": "generate_project_code",
            },
        )
        #self.graph_builder.add_edge("llm_security_review", "generate_test_cases")
        self.graph_builder.add_conditional_edges(
            "llm_security_review",
            self.basic_sdlc_node.llm_security_review_should_continue,
            {  # if accepted then send to generate_test_cases node else reject with feedback
                "Accepted": "generate_test_cases",
                "Rejected + Feedback": END,
            },
        )
        self.graph_builder.add_edge("generate_test_cases", "llm_test_cases_review")
        self.graph_builder.add_conditional_edges(
            "llm_test_cases_review",
            self.basic_sdlc_node.llm_test_cases_review_should_continue,
            {  # if accepted then send to perform_qa_testing node else reject with feedback
                "Accepted": "llm_perform_qa_testing",
                "Rejected + Feedback": "generate_test_cases",
            },
        )
        self.graph_builder.add_edge("llm_perform_qa_testing", "llm_deployment")
        self.graph_builder.add_edge("llm_deployment", "llm_monitoring")
        self.graph_builder.add_edge("llm_monitoring", END)
        
    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        # Compile the workflow
        memory = MemorySaver()
        print("usecase=",usecase)
        if usecase == "SDLC Project":
            self.basic_sdlc_build_graph()
        return self.graph_builder.compile()



    


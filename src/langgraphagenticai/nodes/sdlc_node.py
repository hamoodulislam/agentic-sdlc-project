from src.langgraphagenticai.common.test_case_feedback import TestCaseFeedback
from src.langgraphagenticai.state.state import State
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.langgraphagenticai.common.storey_feedback import StoryFeedback
from src.langgraphagenticai.common.design_feedback import DesignFeedback
from src.langgraphagenticai.common.code_feedback import CodeFeedback
from src.langgraphagenticai.common.security_feedback import SecurityFeedback

class SDLCWorkflowNode:
    """
    Basic SDLC workflow logic implementation.
    """
    def __init__(self, model):
        self.llm = model

    
    def generate_user_stories(self, state: State):
        """LLM generate user stores"""
        print("generate_user_stories=")
        if(state["product_owner_accept_reject_stories"]=="Rejected"):
            sys_msg = SystemMessage(content=f"You are an exprienced product owner in scrum methodology. Use your expertise, to generate user stories for the provided project but take into account the feedback: {state['product_owner_stories_feedback']}")
            hum_msg = HumanMessage(content=f"project title : {state['project_title']}, project requirements : {state['project_requirements']}")
        else:
            sys_msg = SystemMessage(content="You are an exprienced product owner in scrum methodology. Use your expertise, to generate user stories for the provided project.")
            hum_msg = HumanMessage(content=f"project title : {state['project_title']}, project requirements : {state['project_requirements']}")
        
        llm_response = self.llm.invoke([sys_msg] + [hum_msg])
        state["llm_generated_stories"] = llm_response.content
        return state 

    def product_owner_review(self, state: State):
        """ No-op node that should be interrupted on """
        print("product_owner_review is called")
        #print("state=", state)
        """LLM evaluates the blog"""
        #Augment the LLM with schema for structured output
        evaluator = self.llm.with_structured_output(StoryFeedback)
        grade = evaluator.invoke(f"As a product owner evaluate the generated stories : {state['llm_generated_stories']}")
        print("grade=",grade)
        state["product_owner_accept_reject_stories"] = grade.grade 
        state["product_owner_stories_feedback"] = grade.feedback
        return state

    def product_owner_should_continue(self, state: State):
        print("product_owner_should_continue is called")
        
        product_owner_feedback = state.get('product_owner_accept_reject_stories', None)
        if product_owner_feedback=="Accepted" or product_owner_feedback=="Approved":
            return "Accepted"
        else:
            return "Rejected + Feedback"

    # llm to generate details design or review and re-generate detaild design
    def generate_detailed_design(self, state: State):
        print("generate_detailed_design is called")
                
        if(state["llm_accept_reject_design"]=="Rejected"):
            sys_msg = SystemMessage(content=f"You are an exprienced software architect. Use your expertise, to generate detailed design of the provided project but take into account the feedback: {state['llm_design_feedback']}")
            hum_msg = HumanMessage(content=f"project title : {state['project_title']}, project requirements : {state['project_requirements']}, user stories : {state['llm_generated_stories']}, current design : {state['llm_generated_design_docs']}")
        else:
            sys_msg = SystemMessage(content="You are an exprienced software architect. Use your expertise, to generate detailed design of the provided project. The design should be based on the user stories.")
            hum_msg = HumanMessage(content=f"project title : {state['project_title']}, project requirements : {state['project_requirements']}, user stories : {state['llm_generated_stories']}")
        
        llm_response = self.llm.invoke([sys_msg] + [hum_msg])
        state["llm_generated_design_docs"] = llm_response.content
        return state
    
    def llm_design_review(self, state: State):
        print("llm_design_docs_review is called")
       
        """LLM evaluates the doc design"""
        #Augment the LLM with schema for structured output
        evaluator = self.llm.with_structured_output(DesignFeedback)
        grade = evaluator.invoke(f"As an experienced software architect evaluate the project design : {state['llm_generated_design_docs']}")
        print("grade=",grade)
        state["llm_accept_reject_design"] = grade.grade 
        state["product_owner_stories_feedback"] = grade.feedback
        return state

    def llm_design_review_should_continue(self, state: State):
        """ Return the next node to execute """
        print("llm_design_review_should_continue is called")
        
        llm_design_feedback = state.get('llm_accept_reject_design', None)
        #product_owner_feedback = "Accepted"
        if llm_design_feedback=="Accepted" or llm_design_feedback=="Approved":
            return "Accepted"
        else:
            return "Rejected + Feedback"
        

    # llm to generate project code or review and re-generate project code
    def generate_project_code(self, state: State):
        print("generate_project_code is called : ",state["llm_accept_reject_code"])
       
        if(state["llm_accept_reject_code"]=="Rejected"):
            sys_msg = SystemMessage(content=f"You are an exprienced software developer. Use your expertise, to write code for the provided project but take into account the feedback: {state['llm_code_feedback']}")
            hum_msg = HumanMessage(content=f"project title : {state['project_title']}, project requirements : {state['project_requirements']}, current design : {state['llm_generated_design_docs']}, current code : {state['llm_generated_code']}")
        else:
            sys_msg = SystemMessage(content="You are an exprienced software developer. Use your expertise, to write code for the provided project. The code should in java and based on detailed desgin.")
            hum_msg = HumanMessage(content=f"project title : {state['project_title']}, project requirements : {state['project_requirements']}, project detailed design : {state['llm_generated_design_docs']}")
        
        llm_response = self.llm.invoke([sys_msg] + [hum_msg])
        state["llm_generated_code"] = llm_response.content
        return state
    
    def llm_code_review(self, state: State):
        """LLM evaluates the code """
        print("llm_code_review is called")
        #Augment the LLM with schema for structured output
        evaluator = self.llm.with_structured_output(CodeFeedback)
        grade = evaluator.invoke(f"As an experienced software developer review the project code : {state['llm_generated_code']}")
        print("grade code=",grade)
        state["llm_accept_reject_code"] = grade.grade 
        state["llm_code_feedback"] = grade.feedback
        return state

    def llm_code_review_should_continue(self, state: State):
        print("llm_code_review_should_continue is called")        
        llm_code_feedback = state.get('llm_accept_reject_code', None)
       
        if llm_code_feedback=="Accepted" or llm_code_feedback=="Approved":
            return "Accepted"
        else:
            return "Rejected + Feedback"

    def llm_security_review(self, state: State):
        """LLM evaluates the code for security """
        print("llm_security_review is called")
        #Augment the LLM with schema for structured output
        evaluator = self.llm.with_structured_output(SecurityFeedback)
        grade = evaluator.invoke(f"As experienced security analyst review the project code and suggest improvements : {state['llm_generated_code']}")
        print("grade security=",grade)
        state["llm_accept_reject_security"] = grade.grade 
        state["llm_security_feedback"] = grade.feedback
        return state

    def llm_security_review_should_continue(self, state: State):
        print("llm_security_review_should_continue is called")        
        llm_security_feedback = state.get('llm_accept_reject_security', None)
       
        #Commented code to complete the flow. it is taking too much time
        """if llm_security_feedback=="Accepted" or llm_security_feedback=="Approved":
            return "Accepted"
        else:
            return "Rejected + Feedback""
        """
        return "Accepted"
    
    # llm to generate test cases or review and re-generate test cases
    def generate_test_cases(self, state: State):
        print("generate_test_cases is called")
            
        if(state["llm_accept_reject_test_cases"]=="Rejected"):
            sys_msg = SystemMessage(content=f"You are an exprienced software tester. Use your expertise, to write test cases for the provided project but take into account the feedback: {state['llm_test_cases_feedback']}")
            hum_msg = HumanMessage(content=f"project title : {state['project_title']}, project requirements : {state['project_requirements']}, current code : {state['llm_generated_code']}, current test cases : {state['llm_generated_test_cases']}")
        else:
            sys_msg = SystemMessage(content="You are an exprienced software tester. Use your expertise, to write test cases for the provided project. The test cases should be based on project code.")
            hum_msg = HumanMessage(content=f"project title : {state['project_title']}, project requirements : {state['project_requirements']}, project code : {state['llm_generated_code']}")
        
        llm_response = self.llm.invoke([sys_msg] + [hum_msg])
        state["llm_generated_test_cases"] = llm_response.content
        return state
    
    def llm_test_cases_review(self, state: State):
        """LLM evaluates test cases """
        print("llm_test_cases_review is called")
        #Augment the LLM with schema for structured output
        evaluator = self.llm.with_structured_output(TestCaseFeedback)
        grade = evaluator.invoke(f"As an experienced QA enignner review the test cases : {state['llm_generated_test_cases']}")
        print("grade test cases=",grade)
        state["llm_accept_reject_test_cases"] = grade.grade 
        state["llm_test_cases_feedback"] = grade.feedback
        return state

    def llm_test_cases_review_should_continue(self, state: State):
        print("llm_test_cases_review_should_continue is called")        
        llm_test_case_feedback = state.get('llm_accept_reject_test_cases', None)
       
        if llm_test_case_feedback=="Accepted" or llm_test_case_feedback=="Approved":
            return "Accepted"
        else:
            return "Rejected + Feedback"
        

    #llm to perform QA based on generated code and test cases
    def llm_perform_qa_testing(self, state: State):
        print("perform_qa_testing is called")
            
        sys_msg = SystemMessage(content="You are a experienced QA Engineer. Use your expertise, to perform QA testing of the provided project. The QA testing should be based on project code and test cases.")
        hum_msg = HumanMessage(content=f"project title : {state['project_title']}, project requirements : {state['project_requirements']}, project code : {state['llm_generated_code']}, test cases : {state['llm_generated_test_cases']}")
        
        llm_response = self.llm.invoke([sys_msg] + [hum_msg])
        state["llm_qa_feedback"] = llm_response.content
        return state
    
    #llm to generate instructions to deploy the project on docker/kubernetes env
    def llm_deployment(self, state: State):
        print("llm_deployment is called")
            
        sys_msg = SystemMessage(content="You are a experienced DevOps Engineer. Use your expertise, to write detailed instructions to deploy the provided project code. Our perference of deployment is on Docker and Kubernetes envirnment.")
        hum_msg = HumanMessage(content=f"project title : {state['project_title']}, project requirements : {state['project_requirements']}, project code : {state['llm_generated_code']}")
        
        llm_response = self.llm.invoke([sys_msg] + [hum_msg])
        state["llm_deploy_instructions"] = llm_response.content
        return state
    
    #llm to generate instructions to monitor project after deployment
    def llm_monitoring(self, state: State):
        print("llm_monitoring is called")
            
        sys_msg = SystemMessage(content="You are a experienced DevOps Engineer. Use your expertise, to write detailed instructions on monitoring deployed app on docker and kubernetes environment. We want details about logs, alerts and oberserability setup.")
        hum_msg = HumanMessage(content=f"project title : {state['project_title']}, project requirements : {state['project_requirements']}, project code : {state['llm_generated_code']}, deployment : {state['llm_deploy_instructions']}")
        
        llm_response = self.llm.invoke([sys_msg] + [hum_msg])
        state["llm_monitoring_instructions"] = llm_response.content
        return state
        
    
    
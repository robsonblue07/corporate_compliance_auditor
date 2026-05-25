from langgraph.graph import StateGraph, END
from src.state import AuditorState
from src.nodes.extractor_node import document_extractor
from src.nodes.auditor_node import compliance_auditor

def route_audit_outcome(state: AuditorState) -> str:
    """
    Conditional edge function to determine the next step based on audit status.
    Routes to END if human review is needed, allowing the external system to pause.
    """
    status = state.get("audit_status")
    
    if status == "NEEDS_REVIEW":
        print("--- ROUTING: HUMAN REVIEW REQUIRED ---")
        return "human_review_required"
    
    print("--- ROUTING: AUDIT COMPLETE ---")
    return "audit_complete"

def build_auditor_graph():
    """
    Compiles the multi-agent graph workflow for document auditing.
    """
    # 1. Initialize the graph with the defined state
    workflow = StateGraph(AuditorState)
    
    # 2. Add the nodes
    workflow.add_node("extractor", document_extractor)
    workflow.add_node("auditor", compliance_auditor)
    
    # 3. Define the standard edges (the linear flow)
    workflow.set_entry_point("extractor")
    workflow.add_edge("extractor", "auditor")
    
    # 4. Define the conditional edges for routing
    workflow.add_conditional_edges(
        "auditor",
        route_audit_outcome,
        {
            "human_review_required": END,
            "audit_complete": END
        }
    )
    
    # 5. Compile the graph
    app = workflow.compile()
    
    return app

# Example usage for testing the compiled graph locally
if __name__ == "__main__":
    app = build_auditor_graph()
    
    initial_state = {
        "document_id": "doc-789",
        "raw_text": (
            "SERVICE AGREEMENT\n"
            "This agreement is made between Global Tech Solutions and Acme Corp. "
            "Acme Corp agrees to pay Global Tech Solutions the sum of $150,000 for cloud infrastructure services. "
            "Both parties agree to the terms outlined in this document. Confidentiality is strictly maintained."
        ),
        "extracted_entities": {},
        "compliance_issues": [],
        "audit_status": "PENDING",
        "human_feedback": None
    }
    
    print("Starting Audit Workflow...\n")
    
    # Run the graph and print the state updates
    for output in app.stream(initial_state):
        for key, value in output.items():
            print(f"Node '{key}' completed.")
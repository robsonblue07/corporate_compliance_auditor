import operator
from typing import TypedDict, Annotated, List, Dict, Any, Optional

class ComplianceIssue(TypedDict):
    """Represents a single compliance violation found in the document."""
    rule_id: str
    description: str
    severity: str  # e.g., "LOW", "MEDIUM", "HIGH", "CRITICAL"
    context_snippet: str

class AuditorState(TypedDict):
    """
    Defines the state of the document auditing graph.
    Uses Annotated with operator.add for lists to append items across nodes.
    """
    document_id: str
    raw_text: str
    extracted_entities: Dict[str, Any]
    
    # The issues list will be updated continuously by the nodes
    compliance_issues: Annotated[List[ComplianceIssue], operator.add]
    
    # Status can be "PENDING", "APPROVED", "REJECTED", or "NEEDS_REVIEW"
    audit_status: str
    
    # To store human feedback if the process is paused
    human_feedback: Optional[str]
from src.state import AuditorState, ComplianceIssue

def compliance_auditor(state: AuditorState) -> AuditorState:
    """
    Node responsible for validating the extracted entities against corporate policies.
    """
    print("--- AUDITING COMPLIANCE RULES ---")
    entities = state.get("extracted_entities", {})
    issues = []
    status = "APPROVED"
    
    # Mocking a compliance rule check: High value + missing governing law
    if entities.get("contract_value", 0) > 100000 and entities.get("governing_law") == "Undefined":
        issues.append(
            ComplianceIssue(
                rule_id="COMP-001",
                description="High value contracts must specify a governing law.",
                severity="HIGH",
                context_snippet="Governing law clause is missing."
            )
        )
        status = "NEEDS_REVIEW" # Triggers Human-in-the-loop

    return {
        "compliance_issues": issues,
        "audit_status": status
    }
from src.state import AuditorState

def document_extractor(state: AuditorState) -> AuditorState:
    """
    Node responsible for extracting structured entities from the raw text.
    In a real scenario, this would call an LLM with structured output parsing.
    """
    print("--- EXTRACTING DOCUMENT ENTITIES ---")
    
    # Mocking entity extraction for the portfolio stub
    extracted_data = {
        "company_name": "Acme Corp",
        "contract_value": 500000,
        "governing_law": "Undefined"
    }
    
    return {"extracted_entities": extracted_data}
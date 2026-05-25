import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from src.state import AuditorState

# Load environment variables from the .env file
load_dotenv()

class ContractEntities(BaseModel):
    """
    Pydantic model to enforce structured output from the LLM.
    This guarantees the AI returns exactly these keys with the correct data types.
    """
    company_name: str = Field(description="The name of the company involved in the contract. Return 'Unknown' if not found.")
    contract_value: float = Field(description="The total financial value of the contract. Return 0 if not found.")
    governing_law: str = Field(description="The state or country law governing the contract. Return 'Undefined' if missing.")

def document_extractor(state: AuditorState) -> AuditorState:
    """
    Node responsible for extracting structured entities from the raw text using an LLM.
    """
    print("--- EXTRACTING DOCUMENT ENTITIES WITH LLM ---")
    
    raw_text = state.get("raw_text", "")
    
    # Initialize the LLM (using gpt-4o-mini for cost-efficiency and speed)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Bind the LLM to output exactly our Pydantic schema
    structured_llm = llm.with_structured_output(ContractEntities)
    
    # Define the extraction prompt
    prompt = PromptTemplate.from_template(
        "You are an expert corporate lawyer. Extract the requested entities from the following document.\n\n"
        "Document Text:\n{text}"
    )
    
    # Create the LCEL (LangChain Expression Language) chain and execute
    chain = prompt | structured_llm
    
    try:
        # Invoke the LLM
        extracted_data = chain.invoke({"text": raw_text})
        # Convert Pydantic model back to a dictionary to update the graph state
        entities_dict = extracted_data.model_dump()
        print(f"Extraction Successful: {entities_dict}")
    except Exception as e:
        print(f"Error during extraction: {e}")
        entities_dict = {}

    return {"extracted_entities": entities_dict}
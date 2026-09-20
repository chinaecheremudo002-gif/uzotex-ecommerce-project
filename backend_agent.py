import os   
from dotenv import load_dotenv
from openai import OpenAI
from agents import Agent, Runner, function_tool
from pypdf import PdfReader
def main():
    load_dotenv(override=True)  # Load environment variables from .env file

    com_reader = PdfReader(
    "company overview/ecommerce_company_overview.pdf")
    
    for page in com_reader.pages:
        text_page=page.extract_text()
        text+=f"{text_page} \n\n" 
        
    print(text)
        
    system_prompt = f"""
    You are a helpful and professional customer support agent for an e-commerce
    building materials company.

    Use the following company document as your primary source of information:

    --- COMPANY KNOWLEDGE BASE ---
    {text}
    --- END COMPANY KNOWLEDGE BASE ---

    Answer the customer's questions using the information provided in the
    company knowledge base.

    Rules:
    1. Do not invent information that is not contained in the knowledge base.
    2. Do not make up product prices, stock availability, delivery fees,
    payment status, order status, or rider information.
    3. If the answer cannot be found in the knowledge base, politely tell the
    customer that you do not have that information.
    4. Keep your answers clear, concise, friendly, and professional.
    5. If the customer asks about an existing order, ask for the order reference
    when necessary.
    6. Never claim that you performed an action unless a tool or system has
    actually confirmed that the action was completed.
    7. Use simple language that customers can easily understand.

    Your goal is to provide accurate and helpful customer support based on the
    company knowledge base.
    """



    #print("OpenAI API Key:", open_ai_key[:4])  # Print the API key to verify it's loaded correctly

    os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_BASE_URL"]="https://openrouter.ai/api/v1"
    model = "gpt-4o-mini"
    ecommerce_agent = Agent(
        name='ecommerce_agent',
        model=model,
        instructions=system_prompt
    )
    
    return ecommerce_agent


  

    

    if __name__ == "__main__":
        main()
    
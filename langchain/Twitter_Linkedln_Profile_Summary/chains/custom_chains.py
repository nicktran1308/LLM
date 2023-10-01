# ------------------------------- Import Libraries -------------------------------
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from output_parsers import summary_parser, ice_breaker_parser, topics_of_interest_parser

# ------------------------------- Model Initializations -------------------------------
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
llm_creative = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")

# ------------------------------- Summary Chain -------------------------------
def get_summary_chain() -> LLMChain:
    # Prompt template for generating summary and notable facts
    summary_template = """
         Using LinkedIn data {information} and Twitter posts {twitter_posts}, create:
         1. A brief summary.
         2. Two notable facts.
         \n{format_instructions}
     """
    
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    return LLMChain(llm=llm, prompt=summary_prompt_template)

# ------------------------------- Interests Chain -------------------------------
def get_interests_chain() -> LLMChain:
    # Prompt template for identifying potential topics of interest
    facts_template = """
         Using LinkedIn data {information} and Twitter posts {twitter_posts}, determine:
         3 potential topics of interest.
         \n{format_instructions}
     """
    
    facts_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=facts_template,
        partial_variables={"format_instructions": topics_of_interest_parser.get_format_instructions()}
    )

    return LLMChain(llm=llm, prompt=facts_prompt_template)

# ------------------------------- Ice Breaker Chain -------------------------------
def get_ice_breaker_chain() -> LLMChain:
    # Prompt template for generating creative icebreakers based on recent activity
    ice_template = """
         Using LinkedIn data {information} and Twitter posts {twitter_posts}, devise:
         2 creative icebreakers, ideally from recent tweets.
         \n{format_instructions}
     """
    
    ice_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=ice_template,
        partial_variables={"format_instructions": ice_breaker_parser.get_format_instructions()}
    )

    return LLMChain(llm=llm_creative, prompt=ice_prompt_template)


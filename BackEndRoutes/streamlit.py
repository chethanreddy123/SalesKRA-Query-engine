# agent.py
from langchain import OpenAI
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd
from langchain.llms import GooglePalm


def create_agent(filename: str):
    """
    Create an agent that can access and use a large language model (LLM).

    Args:
        filename: The path to the CSV file that contains the data.

    Returns:
        An agent that can access and use the LLM.
    """

    # Create an OpenAI object.
    llm = GooglePalm(
        model='models/text-bison-001',
        temperature=0,
        max_output_tokens=80000,
        google_api_key='AIzaSyA1fu-ob27CzsJozdr6pHd96t5ziaD87wM'
    )


    # Read the CSV file into a Pandas DataFrame.
    df = pd.read_csv(filename)

    # Create a Pandas DataFrame agent.
    return create_pandas_dataframe_agent(llm, df, verbose=False)

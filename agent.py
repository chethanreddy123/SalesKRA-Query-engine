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
        # The maximum length of the response
        max_output_tokens=80000,
        google_api_key='AIzaSyA1fu-ob27CzsJozdr6pHd96t5ziaD87wM'
    )

    # Read the CSV file into a Pandas DataFrame.
    df = pd.read_csv(filename)

    # Create a Pandas DataFrame agent.
    return create_pandas_dataframe_agent(llm, df, verbose=False)


def query_agent(agent, query, df):
    """
    Query an agent and return the response as a pure python code only.

    Args:
        agent: The agent to query.
        query: The query to ask the agent.

    Returns:
        The response from the agent as a string.
    """

    prompt = (
        """Act like expert data analyst, Give below is sample csv file, and query related to it.
        write a python code to generate a graph of the data in the csv file based on the query and 
        store it in png file named graph.png. On return the python code as output
        Sample Structure of CSV file: {df}
        Query: {query}
        """
    )

    # Run the prompt through the agent.
    response = agent.run(prompt)

    # Convert the response to a string.
    return response.__str__()
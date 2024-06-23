import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Ensure the OpenAI API key is set
if not openai_api_key:
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

app = FastAPI()


class TravelQuery(BaseModel):
    query: str
    travel_date: date
    destination: str
    query_type: str  # Add query_type to distinguish between different requests


# Function to generate prompt for different query types
def generate_prompt(query: TravelQuery):
    if query.query_type == "hotels":
        return f"List some popular hotels in {query.destination}."
    elif query.query_type == "places":
        return f"List some popular places to visit in {query.destination}."
    elif query.query_type == "attractions":
        return f"List some popular attractions in {query.destination}."
    else:
        return f"User is planning a trip. Query: {query.query}, Date: {query.travel_date}, Destination: {query.destination}."


@app.post("/process_query/")
async def process_query(query: TravelQuery):
    llm = ChatOpenAI(
        model='gpt-4',
        openai_api_key=openai_api_key,
        temperature=0.7
    )

    prompt = generate_prompt(query)
    prompt_template = ChatPromptTemplate.from_template(prompt)

    chain = LLMChain(llm=llm, prompt=prompt_template)

    try:
        # Generate the response using LangChain
        gpt_response = chain.run(
            {"query": query.query, "travel_date": str(query.travel_date), "destination": query.destination}
        )

        # Log token usage if available
        if 'usage' in gpt_response:
            token_usage = gpt_response['usage']
            print(
                f"Prompt tokens: {token_usage['prompt_tokens']}, Completion tokens: {token_usage['completion_tokens']}, Total tokens: {token_usage['total_tokens']}")

        data = gpt_response

        return {"response": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    # example_query_general = TravelQuery(query="Where to travel?", travel_date=date(2024, 6, 23), destination="India",
    #                                     query_type="general")
    # example_query_hotels = TravelQuery(query="Find hotels", travel_date=date(2024, 6, 23), destination="India",
    #                                    query_type="hotels")
    # example_query_places = TravelQuery(query="What are some places to visit?", travel_date=date(2024, 6, 23),
    #                                    destination="India", query_type="places")
    # example_query_attractions = TravelQuery(query="What attractions are there?", travel_date=date(2024, 6, 23),
    #                                         destination="India", query_type="attractions")
    #
    # # Test general query
    # response_general = process_query(example_query_general)
    # print(response_general)
    #
    # # Test hotels query
    # response_hotels = process_query(example_query_hotels)
    # print(response_hotels)
    #
    # # Test places to visit query
    # response_places = process_query(example_query_places)
    # print(response_places)
    #
    # # Test attractions query
    # response_attractions = process_query(example_query_attractions)
    # print(response_attractions)

    # Uncomment the line below to run the FastAPI server
    uvicorn.run("dem:app", host="127.0.0.1", port=8000, reload=True)

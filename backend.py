import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import
import os

# openai.api_key = ""

app = FastAPI()


class TravelQuery(BaseModel):
    query: str
    travel_date: date
    destination: str


@app.post("/process_query")
async def process_query(query: TravelQuery):
    prompt = f"User is planning a trip. Query: {query.query}, Date: {query.travel_date}, Destination: {query.destination}."

    response = openai.Completion.create(
        engine="gpt-4o",
        prompt=prompt,
        max_tokens=500
    )

    get_response = response.choices[0].text.strip()

    return {"response": get_response}


if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8080)
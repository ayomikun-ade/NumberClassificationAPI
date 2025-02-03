# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import math
from typing import List, Dict, Union
from pydantic import BaseModel

app = FastAPI(title="Number Classification API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ErrorResponse(BaseModel):
    number: str
    error: bool = True


class NumberResponse(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: List[str]
    digit_sum: int
    fun_fact: str


def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def is_perfect(n: int) -> bool:
    """Check if a number is perfect."""
    if n < 1:
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)
    return sum_factors == n


def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    num_str = str(n)
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == n


def get_digit_sum(n: int) -> int:
    """Calculate the sum of digits."""
    return sum(int(digit) for digit in str(n))


def get_number_properties(n: int) -> List[str]:
    """Get all properties of a number."""
    properties = []

    if is_armstrong(n):
        properties.append("armstrong")
        
    # Check basic properties
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    

    # Add more properties as needed
    return properties


def get_fun_fact(n: int) -> str:
    """Get a fun fact about the number from Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        if response.status_code == 200:
            return response.text
        return f"{n} is an Armstrong number because {'^3 + '.join(str(n))}^3 = {n}" if is_armstrong(n) else f"The digit sum of {n} is {get_digit_sum(n)}"
    except:
        return f"The digit sum of {n} is {get_digit_sum(n)}"


@app.get("/api/classify-number", response_model=Union[NumberResponse, ErrorResponse])
async def classify_number(number: str):
    """
    Classify a number and return its properties.

    Args:
        number: The number to classify

    Returns:
        JSON object containing number properties
    """
    try:
        num = int(number)
        if num < 0:
            raise HTTPException(
                status_code=400, detail="Negative numbers are not supported")

        return NumberResponse(
            number=num,
            is_prime=is_prime(num),
            is_perfect=is_perfect(num),
            properties=get_number_properties(num),
            digit_sum=get_digit_sum(num),
            fun_fact=get_fun_fact(num)
        )
    except ValueError:
        return ErrorResponse(number=number)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import math
from typing import List, Union
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
    message: str
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
    if n <= 1:
        return False
    sum_divisors = 1  # 1 is always a divisor
    sqrt_n = int(math.sqrt(n))
    for i in range(2, sqrt_n + 1):
        if n % i == 0:
            sum_divisors += i
            other = n // i
            if other != i:
                sum_divisors += other
    return sum_divisors == n
def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    if n < 0:
        return False
    digits = str(n)
    power = len(digits)
    return sum(int(digit) ** power for digit in digits) == n
def get_digit_sum(n: int) -> int:
    """Calculate the sum of digits."""
    return sum(int(digit) for digit in str(n))
def get_fun_fact(n: int) -> str:
    """Get a fun fact about the number from Numbers API."""
    url = f"http://numbersapi.com/{n}/math"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200 and response.text.strip():
            return response.text.strip()
        else:
            return f"The digit sum of {n} is {get_digit_sum(n)}"
    except Exception:
        return f"The digit sum of {n} is {get_digit_sum(n)}"
@app.get("/api/classify-number", response_model=Union[NumberResponse, ErrorResponse])
async def classify_number(number: str):
    """
    Classify a number and return its properties.
    Query Parameters:
        number: The number to classify
    Returns:
        JSON object containing number properties or an error response.
    """
    number = number.strip()
    if not number:
        return ErrorResponse(
            number="",
            message="Invalid input. Please provide an integer."
        )
    try:
        num = int(number)
    except ValueError:
        return ErrorResponse(
            number=number,
            message="Invalid input. Please provide an integer."
        )
    if num < 0:
        raise HTTPException(status_code=400, detail="Negative numbers are not supported")
    prime_status = is_prime(num)
    perfect_status = is_perfect(num)
    armstrong_status = is_armstrong(num)
    properties = []
    if prime_status:
        properties.append("prime")
    if perfect_status:
        properties.append("perfect")
    if armstrong_status:
        properties.append("armstrong")
    properties.append("even" if num % 2 == 0 else "odd")
    return NumberResponse(
        number=num,
        is_prime=prime_status,
        is_perfect=perfect_status,
        properties=properties,
        digit_sum=get_digit_sum(num),
        fun_fact=get_fun_fact(num)
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 
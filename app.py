import secrets
import threading

from fastapi import FastAPI
from api.models import (
    CreateOrderRequest,
    CreateOrderResponse,
    GetOrderResponse,
    ServiceUnavailableResponse,
    BadRequestResponse,
    InternalServerErrorResponse,
)

from api.core import ewh_pipeline
from api.data_helpers import get_user_metadata


app = FastAPI(
    title="Electric Water Heater Flexibility API",
    description="""
OpenAPI specifications for **INESC TEC Enershare Electric Water Heater Flexibility API**.  

Welcome to our OpenAPI documentation for the INESC TEC Enershare Electric Water Heater Flexibility API. 

This REST API provides endpoints for initiating a request for Electric Water Heater (EWH) load optimization, and for
retrieving the result, respectively.


**This documentation will guide you through:**

1. **Request EWH Simulations**:  Initiates a request for load optimization for a specific Electric Water Heater. 
Users can provide the EWH specifications (power, maximum allowed water temperature, capacity), desired hot water
comfort temperature, and a time schedule during which the optimization should occur.

2. **Retrieve EWH Simulations Result**: Retrieves the result of a previously initiated Electric Water Heater load
optimization request based on the provided request ID.


**Developers // Contacts:**
- José Paulos (jose.paulos@inesctec.pt)
""",
)

error_responses = {
    400: {"description": "Bad request", "model": BadRequestResponse},
    500: {"description": "Service Unavailable", "model": InternalServerErrorResponse},
    503: {"description": "Service Unavailable", "model": ServiceUnavailableResponse}
}


@app.post("/api/ewh/request",
          response_model=CreateOrderResponse,
          status_code=201,
          responses=error_responses,
          tags=["api"],
          description="Endpoint to Get EWH Simulation Results")
def create_order(ewh_request: CreateOrderRequest):
    # Access the data using EWHRequest model
    user_id = ewh_request.user
    start_datetime = ewh_request.datetime_start
    end_datetime = ewh_request.datetime_end
    ewh_specs = ewh_request.ewh_specs

    # Check if minimum conditions to run model are met
    # -- right now we are just checking if user is registered in DS
    # Check if user exists in dataspace:
    metadata = get_user_metadata(identifier=user_id)

    if not metadata["data_available"]:
        response = {
            "order_status": "failed",
            "message": "Failed to fetch user metadata/data (unavailable)."
        }
        return response
    else:
        # Create new order id
        order_id = secrets.token_urlsafe(45)

        # Run ewh pipeline in separate thread and continue with response
        t = threading.Thread(target=ewh_pipeline,
                             args=(
                                 order_id,
                                 user_id,
                                 start_datetime,
                                 end_datetime,
                                 ewh_specs
                             ))
        t.start()  # Detatch

        response = {
            "order_id": order_id,
            "order_status": "placed"
        }
        return response


@app.get("/api/ewh/result", response_model=GetOrderResponse,
         status_code=200,
         responses=error_responses,
         tags=["api"],
         description="Endpoint to Get EWH Simulation Results")
def get_order(order_id: str):
    # Query database for Order ID status. If "complete", return result
    return {}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080)


from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from fastapi import Query


###########################################################
#     Input payloads (query parameters / JSON payloads)   #
###########################################################


class EWHSpecs(BaseModel):
    # Aux Model -> EWH Specs JSON to be used in EWHRequest
    ewh_capacity: int = Field(description="EWH capacity (l)")
    ewh_power: int = Field(description="EWH heating power (W)")
    ewh_max_temp: int = Field(description="EWH maximum allowed water temperature")
    user_comf_temp: int = Field(description="Hot-Water Usage Comfort Temperature (minimum user-defined temperature - °C)")
    tariff: int = Field(description='Tariff selection between simple (1) or dual (2)')
    price_simple: float = Field(description='Simple pricing value per kWh')
    price_dual_day: float = Field(description='Dual day pricing value per kWh ')
    price_dual_night: float = Field(description='Dual night pricing value per kWh')
    tariff_simple: float = Field(description='Fixed daily simple tariff pricing')
    tariff_dual: float = Field(description='Fixed daily dual tariff pricing')



class CreateOrderRequest(BaseModel):
    user: str = Field(description="User Identification")
    datetime_start: datetime = Field(description="Start date of the period to be optimized")
    datetime_end: datetime = Field(description="End date of the period to be optimized")
    ewh_specs: Optional[EWHSpecs] = Field(description="EWH Specifications")


class GetOrderRequest(BaseModel):
    order_id: str = Field(Query(description="Initiates a request for Electric Water Heater (EWH) load optimization"))


############################################################
#     Output payloads (query parameters / JSON payloads)   #
############################################################

class ServiceUnavailableResponse(BaseModel):
    error_message: str = Field(description="Status code for service unavailability")


class BadRequestResponse(BaseModel):
    error_message: str = Field(description="Status code for bad request (missing or wrong inputs)")


class InternalServerErrorResponse(BaseModel):
    error_message: str = Field(description="Status code for internal server error")


class CreateOrderResponse(BaseModel):
    order_id: str = Field(description="Automatically created token that identifies the requested order")
    order_status: str = Field(description="Current order status")
    message: str = Field(description="Current order status message")


class CalendarField(BaseModel):
    timestamp: datetime
    hot_water_usage: float


class RefUsageProfileField(BaseModel):
    timestamp: datetime
    ewh_on: float


class SimulationPeriodField(BaseModel):
    start: datetime
    end: datetime
    days_in_simulation: int


class ValueUnitsField(BaseModel):
    value: float
    unit: str


class GetOrderResponse(BaseModel):
    user: str = Field(description="User Identification")
    simulation_period: SimulationPeriodField = Field(description="Simulated/Optimized Period (minutes)")
    original_energy: ValueUnitsField = Field(description="Total accumulated energy in kWh for the real measurement profile")
    optimized_energy: ValueUnitsField = Field(description="Total accumulated energy in kWh for the optimized measurement profile")
    original_price: ValueUnitsField = Field(description="Total cost in € for the real measurement profile")
    optimized_price: ValueUnitsField = Field(description="Total cost in € for the optimized measurement profile")
    avg_daily_energy: ValueUnitsField = Field(description="Average Daily Energy Consumption for the optimized scenario")
    total_flexibility: ValueUnitsField = Field(description="Flexibility availability for the optimized period (minutes)")
    perc_flexibility: ValueUnitsField = Field(description="Percentage of the total simulated period that can provide flexibility")
    avg_daily_flexibility: ValueUnitsField = Field(description="Average flexibility availability for the optimized scenario")
    savings_cost: ValueUnitsField = Field(description="Pricing savings between real and optimized scenarios")
    savings_energy: ValueUnitsField = Field(description="Energy savings between real and optimized scenarios")
    original_usage_profile: List[RefUsageProfileField] = Field(description="Estimated hot-water usage profile based on EWH's real load diagram")
    optimized_calendar: List[CalendarField] = Field(description="Optimized EWH functioning calendarization")


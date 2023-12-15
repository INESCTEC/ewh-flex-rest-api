from .data_helpers import (
    get_electricity_tariffs,
    get_user_measurements,
    save_ewh_results,
    update_order_id
)

from .defaults import default_ewh_specs


def ewh_pipeline(order_id, identifier, start_datetime, end_datetime, ewh_specs):

    # Fetch necessary data from external providers
    measurements = get_user_measurements(identifier)
    tariffs = get_electricity_tariffs(identifier)

    # if ewh_specs do not exist -> try to fetch from dataspace / default
    ewh_specs = default_ewh_specs()

    # Update "order_id" status to "running" or "failed" depending on
    # the data availability above (add IF statement below)
    update_order_id(order_id=order_id, status="running")

    # Compute:
    results = run_ewh(measurements, tariffs, ewh_specs)

    # Save results to db (with order ID assigned to it):
    save_ewh_results(order_id=order_id, results=results)

    # if it computes + saves results successfully, update order ID to complete
    update_order_id(order_id=order_id, status="complete")

    return


def run_ewh(measurements, tariffs, ewh_specs):
    # Executes ewh simulations
    results = {}

    return results



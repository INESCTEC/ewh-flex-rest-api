
def get_user_metadata(identifier):
    # query metadata broker
    broker_response = {
        "identifier": identifier,
        "data_available": True
    }
    return broker_response


def get_user_measurements(identifier):
    # query metadata broker
    measurements = {

    }
    return measurements


def get_electricity_tariffs(identifier):
    # query metadata broker
    tariffs = {

    }
    return tariffs


def save_ewh_results(order_id, results):
    # save results to DB
    return True  # if success


def update_order_id(order_id, status):
    # update order ID in database (INSERT / UPSERT)
    return True

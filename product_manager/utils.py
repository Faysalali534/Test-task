def create_json_response(status, message, data=[]):
    response_data = [data] if data else []

    response = {
        "status": status,
        "message": str(message),
        "data": response_data
    }
    return response

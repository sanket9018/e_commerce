from rest_framework.response import Response


def get_response(code_status, payload, msg):
    return Response(
        {
            "code": code_status,
            "data": payload,
            "message": msg,
        }
    )


def get_status_msg(key):
    status_msg = {
        "CREATED": "Date created successfully",
        "UPDATED": "Date updated successfully",
        "DELETED": "Data deleted",
        "RETRIEVE": "Data retrieve",
        "ERROR_400": "Bad request",
        "DATA_NOT_FOUND": "Data not found",
    }
    return status_msg.get(key)


def Generate_Order_Number(latest_order):
    if latest_order and latest_order.order_number:
        order_number = int(latest_order.order_number[3:]) + 1
    else:
        order_number = 1
    return f"ORD{order_number:05d}"

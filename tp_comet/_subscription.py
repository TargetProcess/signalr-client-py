import uuid


def create_subscription(id_=str(uuid.uuid1()), client_id=None, parameters=None, log_notifications=None):
    return {
        'id': id_,
        'clientId': client_id,
        'parameters': parameters,
        'logNotifications': log_notifications
    }

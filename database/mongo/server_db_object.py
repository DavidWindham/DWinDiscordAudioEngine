def get_mongo_server_object(server_id, queue_message_id=None):
    return {
        'server_id': server_id,
        'queue_message_id': queue_message_id,
        'history': [

        ],
    }

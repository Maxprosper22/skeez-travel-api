async def create_trip_success(**context):
    """
        Signal dispatched when a new trip is created successfully
        Arguments (context):
            ws: type-Websocket; desc - Websocket connection;
            trip_id: type-UUID; desc - ID of newly created trip
            app: Sanic app context
    """
    print(context)

    ws.send()

async def create_trip_failure(**context):
    """
        Signal dispatched when trip creation fails
        Arguments (context):
            ws: type-Websocket; desc - Websocket connection;
            message: type-str; desc - Error message;
    """
    print(context)

async def trip_status_update(**context):
    """
        Signals a changes to the status field of a trip
        Arguments (context):
            ws: type - Websocket; desc - Websocket connection;
            data: type - dict; 
                desc - 
                values - {
                    type: update,
                    trip: type - str; desc - Affected trip's id, 
                    fields: type - []; desc - Array of fields to be updated,
                    values: type - []; desc - Values to be inserted,
                }
    """
    print(context)

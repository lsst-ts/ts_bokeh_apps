
def on_server_loaded(server_context):
    # If present, this function executes when the server starts.
    print("Server load")

def on_server_unloaded(server_context):
    # If present, this function executes when the server shuts down.
    print("Server unload")

def on_session_created(session_context):
    # If present, this function executes when the server creates a session.
    print("Server created")

def on_session_destroyed(session_context):
    # If present, this function executes when the server closes a session.
    print("Server destroyed")
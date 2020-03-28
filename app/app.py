# Core imports
import os
from chalice import Chalice

# App level imports
from chalicelib.utils.response import custom_response
from chalicelib.utils.config import get_config_env
from chalicelib.utils.exceptions import ExceptionNotFound
from chalicelib.utils.exceptions import ExceptionHandler
from chalicelib.utils.cors import cors_config

from chalicelib.resources.message import MessageResource

# Main
app = Chalice(app_name='chaski-services-email')
app.debug = eval(os.getenv('DEBUG'))

@app.route('/messages', methods=['POST'], cors=cors_config)
def messages():
    try:
        request = app.current_request
        resource = MessageResource(get_config_env(), app)
        resource_method = getattr(resource, 
            'on_{}'.format(request.method.lower())
        )
        response = resource_method(request)

    except (ExceptionHandler, ExceptionNotFound) as e:
        response = custom_response(409, str(e))

    return response

from rest_framework.views import exception_handler


def app_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['success'] = False
        full_messages = []
        response.data['errors'] = {}
        if hasattr(exc.detail, 'values'):
            for value in list(exc.detail.items()):
                if type(value) == str:
                    full_messages.append(value)
                elif type(value) == tuple:
                    if value[0] == 'errors' or value[0] == 'success':
                        continue
                    response.data['errors'][value[0]] = str(value[1][0])
                    full_messages.append('%s -> %s' % (value[0], str(value[1][0])))
            response.data['full_messages'] = full_messages
        else:
            response.data['full_messages']=['somethign went wrong']
            response.data['errors'] = exc.detail

    return response

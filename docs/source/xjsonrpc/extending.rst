.. _extending:

Extending
=========

``xjsonrpc`` can be easily extended without writing a lot of boilerplate code. The following example illustrate
an JSON-RPC server implementation based on :py:mod:`http.server` standard python library module:

.. code-block:: python

    import uuid
    import http.server
    import socketserver

    import xjsonrpc
    import xjsonrpc.server


    class JsonRpcHandler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            content_type = self.headers.get('Content-Type')
            if content_type not in xjsonrpc.common.JSONRPC_REQUEST_CONTENT_TYPES:
                self.send_response(http.HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
                return

            try:
                content_length = int(self.headers.get('Content-Length', -1))
                request_text = self.rfile.read(content_length).decode()
            except UnicodeDecodeError:
                self.send_response(http.HTTPStatus.BAD_REQUEST)
                return

            response_text = self.server.dispatcher.dispatch(request_text, context=self)
            if response_text is None:
                self.send_response(http.HTTPStatus.OK)
            else:
                self.send_response(http.HTTPStatus.OK)
                self.send_header("Content-type", xjsonrpc.common.DEFAULT_CONTENT_TYPE)
                self.end_headers()

                self.wfile.write(response_text.encode())


    class JsonRpcServer(http.server.HTTPServer):
        def __init__(self, server_address, RequestHandlerClass=JsonRpcHandler, bind_and_activate=True, **kwargs):
            super().__init__(server_address, RequestHandlerClass, bind_and_activate)
            self._dispatcher = xjsonrpc.server.Dispatcher(**kwargs)

        @property
        def dispatcher(self):
            return self._dispatcher


    methods = xjsonrpc.server.MethodRegistry()


    @methods.add(context='request')
    def add_user(request: http.server.BaseHTTPRequestHandler, user: dict):
        user_id = uuid.uuid4().hex
        request.server.users[user_id] = user

        return {'id': user_id, **user}


    class ThreadingJsonRpcServer(socketserver.ThreadingMixIn, JsonRpcServer):
        users = {}


    with ThreadingJsonRpcServer(("localhost", 8080)) as server:
        server.dispatcher.add_methods(methods)

        server.serve_forever()

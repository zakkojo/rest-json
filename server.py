import tornado.ioloop
import tornado.web
import json

# elaborate a request payload and return a valid response
# NOTE: to JSON serialization dict key must be strings (don't know why)
def foo(payload):
    print '***** foo',payload
    return {
        'foo': 'happy',
        'periodo': payload['periodo']*2
    }

class JsonHandler(tornado.web.RequestHandler):
    """Request handler where requests and responses speak JSON."""

    def prepare(self):
        """ Parse JSON body/payload and save on `self.request.arguments` for convenience"""

        print('***** prepare')
        if self.request.body:
            try:
                print '****** inside try, body: \n', self.request.body
                # try to parse json from the POST body.
                # POST body is also called payload.
                payload = self.request.body
                json_data = json.loads(payload)
                self.request.arguments.update(json_data)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message) # Bad Request

    def set_default_headers(self):
        # default shim
        self.set_header('Content-Type', 'application/json')
        self.set_header('Accept', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405: kwargs['message'] = 'Invalid HTTP method.'
            else: kwargs['message'] = 'Unknown error.'
        self.response = kwargs
        self.write_json()

    def write_json(self):
        print('\n\n\n\n***** write_json')

        # TODO: this json.dumps should be inside a try...
        self.response = json.dumps( self.response )

        output = json.dumps(
            self.response,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )
        self.write(output)


class MyHandler(JsonHandler):

    def post(self):
        # here is the POST handler. make a response from the payload.
        # NOTE: payload is already jsonized and saved on self.request.arguments
        print '***** post'
        self.response = foo(self.request.arguments)
        self.write_json()

def make_app():
    return tornado.web.Application([
        (r"/", MyHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

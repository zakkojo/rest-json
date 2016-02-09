import tornado.ioloop
import tornado.web
import json

class JsonHandler(tornado.web.RequestHandler):
    """Request handler where requests and responses speak JSON."""
    def prepare(self):
        # Incorporate request JSON into arguments dictionary.
        if self.request.body:
            try:
		json_data = json.loads(self.request.body)		
		print(self.request.body)
                self.request.arguments.update(json_data)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message) # Bad Request

        # Set up response dictionary.
        self.response = dict()

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')
	self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')

    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'

        self.response = kwargs
        self.write_json()

    def write_json(self):
        output = json.dumps(self.response, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
        self.write(output)



class MyHandler(JsonHandler):
    
    def post(self):
        # Access JSON request body through a dict.

        # Do something with arguments...

        # Set JSON response body through a dict.
	self.response['input'] = json.dumps(self.request)
        # Required at end of method (similar to self.write).
	self.write_json()

def make_app():
    return tornado.web.Application([
        (r"/", MyHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

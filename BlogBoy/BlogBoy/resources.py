from flask_restful import Resource


class BaseResource(Resource):
    def json_response(self, success=True, error_code=0, error_message=None,
            data=None):
        return {
                'success': success,
                'error_code': error_code,
                'error_message': error_message,
                'data': data
                }


class Ping(Resource):
    def get(self):
        return {"success": True}



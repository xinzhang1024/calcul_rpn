
from flask import Flask
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

from apis.stack import StackAPI, StackIdAPI
from apis.operand import AllOperandsAPI, ApplyOperandAPI

app = Flask(__name__)
api = Api(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='RPN API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # API Doc URL
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # UI of API Doc URL
})
docs = FlaskApiSpec(app)
api.add_resource(StackIdAPI, '/rpn/stack/<string:stack_id>')
api.add_resource(StackAPI, '/rpn/stack')
api.add_resource(AllOperandsAPI, '/rpn/op')
api.add_resource(ApplyOperandAPI, '/rpn/op/<string:op>/stack/<string:stack_id>')
docs.register(StackAPI)
docs.register(StackIdAPI)
docs.register(AllOperandsAPI)
docs.register(ApplyOperandAPI)


if __name__ == '__main__':
    app.run(debug=True)

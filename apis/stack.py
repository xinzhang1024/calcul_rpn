
import uuid

from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs

from models.stack import StackRequest, StackResponse, AllStacksResponse
from database import mock_db


class StackAPI(MethodResource, Resource):
    @doc(description='List the available stacks', tags=['stack'])
    @marshal_with(AllStacksResponse)
    def get(self):
        """
        Get all stacks
        """
        all_stacks = mock_db.get_all_stacks()
        res = {
            'data': all_stacks
        }
        return AllStacksResponse().dump(res)

    @doc(description='Create a new stack', tags=['stack'])
    @use_kwargs(StackRequest, location='json')
    @marshal_with(StackResponse)
    def post(self, **request_dict):
        """
        Create a new stack
        """
        new_value = request_dict['value']
        new_id = str(uuid.uuid4())
        new_data = {
            'stack_id': new_id,
            'values': [new_value],
            'operands': []
        }
        mock_db.create_new_stack(new_data)
        return StackResponse().dump(new_data)


class StackIdAPI(MethodResource, Resource):

    @doc(description='Get a stack', tags=['stack'])
    @marshal_with(StackResponse)
    def get(self, stack_id):
        """
        Get a stack
        """
        all_stacks = mock_db.get_all_stacks()
        res = {}

        for stack in all_stacks:
            if stack['stack_id'] == stack_id:
                res = stack
        if res:
            return StackResponse().dump(res)
        else:
            return abort(404)

    @doc(description='Push a new value to stack', tags=['stack'])
    @use_kwargs(StackRequest, location='json')
    @marshal_with(StackResponse)
    def post(self, stack_id, **request_dict):
        """
        Push a new value to stack
        """
        all_stacks = mock_db.get_all_stacks()
        new_stack = {}

        for stack in all_stacks:
            if stack['stack_id'] == stack_id:
                new_stack = stack
                new_value = request_dict['value']
                # add new value
                values = stack['values']
                values.append(new_value)
                # update stacks
                new_stack.update({'values': values})
                all_stacks.remove(stack)
                all_stacks.append(new_stack)

        if new_stack:
            mock_db.update_all_stacks(all_stacks)
            return StackResponse().dump(new_stack)
        else:
            return abort(404)

    @doc(description='Delete a stack', tags=['stack'])
    def delete(self, stack_id):
        """
        Delete a stack
        """
        all_stacks = mock_db.get_all_stacks()
        res = {}

        for stack in all_stacks:
            if stack['stack_id'] == stack_id:
                res = stack
                all_stacks.remove(stack)
        if res:
            mock_db.update_all_stacks(all_stacks)
            return 200
        else:
            return abort(404)

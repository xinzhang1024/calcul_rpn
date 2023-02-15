
from flask_restful import Resource, abort
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc

from models.operand import AllOperandsResponse
from models.stack import StackResponse
from database import mock_db
from utils.operator_helper import opt


class AllOperandsAPI(MethodResource, Resource):
    @doc(description='List all the operands', tags=['operand'])
    @marshal_with(AllOperandsResponse)
    def get(self):
        """
        Get all operands
        """
        all_stacks = mock_db.get_all_stacks()

        all_operands = []

        for one in all_stacks:
            all_operands.append({
                'stack_id': one['stack_id'],
                'operands': one['operands']
            })
        res = {
            'data': all_operands
        }
        return AllOperandsResponse().dump(res)


class ApplyOperandAPI(MethodResource, Resource):

    @doc(description='Apply an operand to a stack', tags=['operand'])
    @marshal_with(StackResponse)
    def post(self, op, stack_id):
        """
        Apply an operand to a stack
        """
        all_stacks = mock_db.get_all_stacks()
        new_stack = {}

        for stack in all_stacks:
            if stack['stack_id'] == stack_id and op in opt.keys():
                new_stack = stack
                # add new op
                operands = stack['operands']
                operands.append(op)
                # get values and apply op
                values = stack['values']

                if len(values) >= 2:
                    item1 = values[-2]
                    item2 = values[-1]
                    new_item = opt[op](item1, item2)
                    # remove and add value
                    del values[-2]
                    del values[-1]
                    values.append(new_item)
                    # update stacks
                    new_stack.update({
                        'values': values,
                        'operands': operands
                    })
                    all_stacks.remove(stack)
                    all_stacks.append(new_stack)
                else:
                    return abort(400)

        if new_stack:
            mock_db.update_all_stacks(all_stacks)
            return StackResponse().dump(new_stack)
        else:
            return abort(404)

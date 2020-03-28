import boto3
from .response import validate_response_metadata

dynamodb = boto3.resource('dynamodb')

def prepare_update_expression(data):
    update_expression = 'SET '
    for k in sorted(data):
        update_expression += '#{} = :new_{},'.format(k, k)
    return update_expression[:-1]

def prepare_expression_attribute_values(data):
    expression_attribute_values = {}
    for k in sorted(data):
        expression_attribute_values.update({ ':new_{}'.format(k): data[k]})
    return expression_attribute_values

def prepare_expression_attribute_names(data):
    expression_attribute_names = {}
    for k in sorted(data):
        expression_attribute_names.update({ '#{}'.format(k): k})
    return expression_attribute_names

def update_item(table_name, key, data):
    table = dynamodb.Table(table_name)
    response = table.update_item(
        Key=key,
        UpdateExpression=prepare_update_expression(data),
        ExpressionAttributeValues=prepare_expression_attribute_values(data),
        ExpressionAttributeNames=prepare_expression_attribute_names(data)
    )
    validate_response_metadata(response)

def put_item(table_name, data):
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=data)
    validate_response_metadata(response)

def get_item(table_name, key):
    table = dynamodb.Table(table_name)
    response = table.get_item(Key=key)
    validate_response_metadata(response)
    return response.get('Item', None)



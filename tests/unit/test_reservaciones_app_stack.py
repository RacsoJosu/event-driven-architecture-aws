import aws_cdk as core
import aws_cdk.assertions as assertions

from reservaciones_app.reservaciones_app_stack import ReservacionesAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in reservaciones_app/reservaciones_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ReservacionesAppStack(app, "reservaciones-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

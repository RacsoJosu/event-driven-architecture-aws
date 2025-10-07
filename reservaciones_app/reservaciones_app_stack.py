from aws_cdk import Stack, CfnOutput
from constructs import Construct
from .api_gateway import ReservacionesAppApiGateway
from aws_cdk import aws_events as events


class ReservacionesAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "ReservacionesAppQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        event_bus = events.EventBus(
            self, "ReservacionesEventBus", event_bus_name="ReservacionesEventBus"
        )
        CfnOutput(self, "EventBusArn", value=event_bus.event_bus_arn)
        gateway = ReservacionesAppApiGateway(self, "ReservacionesGateway")
        reserva_lambda = gateway.reserva_fn

        reserva_lambda.add_environment("EVENT_BUS_NAME", event_bus.event_bus_name)
        event_bus.grant_put_events_to(reserva_lambda)

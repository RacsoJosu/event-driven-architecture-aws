from aws_cdk import aws_apigateway as apigw, aws_lambda as _lambda, CfnOutput
from aws_cdk.aws_lambda_nodejs import NodejsFunction
from constructs import Construct
from pathlib import Path


class ReservacionesAppApiGateway:
    def __init__(self, scope: Construct, construct_id: str):
        self.scope = scope
        self.construct_id = construct_id
        self.reserva_fn = self.create_lambda()
        self.create_api_gateway(self.reserva_fn)

    def create_lambda(self) -> NodejsFunction:
        lambda_path = (
            Path(__file__).parent.parent / "services" / "reservas" / "src" / "index.ts"
        )
        root_lockfile = (
            Path(__file__).parent.parent / "services" / "reservas" / "pnpm-lock.yaml"
        )

        reserva_fn = NodejsFunction(
            self.scope,
            "ReservacionService",
            entry=str(lambda_path.resolve()),
            handler="handler",
            runtime=_lambda.Runtime.NODEJS_22_X,
            deps_lock_file_path=str(root_lockfile.resolve()),
        )

        reserva_fn_url = reserva_fn.add_function_url(
            auth_type=_lambda.FunctionUrlAuthType.NONE
        )
        CfnOutput(self.scope, "LambdaFunctionUrl", value=reserva_fn_url.url)

        return reserva_fn

    def create_api_gateway(self, reserva_fn: NodejsFunction):
        reservas_api = apigw.LambdaRestApi(
            self.scope,
            "ReservasApi",
            handler=reserva_fn,
            proxy=False,
            rest_api_name="ReservacionesServiceAPI",
        )

        reservas_resource = reservas_api.root.add_resource("reservas")
        reservas_resource.add_method("POST")

        CfnOutput(self.scope, "ReservasApiUrl", value=reservas_api.url)

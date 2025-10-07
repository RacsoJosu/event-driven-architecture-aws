#!/usr/bin/env python3
from dotenv import load_dotenv
import os

import aws_cdk as cdk

from reservaciones_app.reservaciones_app_stack import ReservacionesAppStack

load_dotenv()

# Obtener variables de entorno
CDK_ACCOUNT = os.getenv("CDK_ACCOUNT")
CDK_REGION = os.getenv("CDK_REGION")


app = cdk.App()
ReservacionesAppStack(
    app,
    "ReservacionesAppStack",
    env=cdk.Environment(account=CDK_ACCOUNT, region=CDK_REGION),
)

app.synth()

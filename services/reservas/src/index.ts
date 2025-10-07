import { EventBridgeClient, PutEventsCommand } from "@aws-sdk/client-eventbridge";
import { Context, APIGatewayProxyResult, APIGatewayEvent } from "aws-lambda";

const eventBridge = new EventBridgeClient({});
export const handler = async (event: APIGatewayEvent, context: Context): Promise<APIGatewayProxyResult> => {
    console.log(`Event: ${JSON.stringify(event, null, 2)}`);
    const reservaId = Math.floor(Math.random() * 10000).toString();
    const usuarioId = event.body ? JSON.parse(event.body).usuarioId : "anon";


    await eventBridge.send(new PutEventsCommand({
        Entries: [
            {
                EventBusName: process.env.EVENT_BUS_NAME!,
                Source: "reservaciones.service",
                DetailType: "ReservaCreada",
                Detail: JSON.stringify({ reservaId, usuarioId }),
            }
        ]
    }));

    return {
        statusCode: 200,
        body: JSON.stringify({
            message: "Reserva creada correctamente",
            reservaId,
        }),
    };
};

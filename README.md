
# 🏗️ Arquitectura Basada en Eventos (EDA) con AWS CDK

Este proyecto es una **aplicación serverless de aprendizaje** que implementa una **arquitectura basada en eventos (EDA)** sobre **AWS** utilizando **CDK (Cloud Development Kit)** en **Python**.

El objetivo es aprender a diseñar, desplegar y conectar múltiples microservicios mediante **eventos asíncronos** usando servicios como **Amazon EventBridge**, **AWS Lambda**, y **API Gateway**.

---

## 📘 Descripción del Proyecto

El sistema simula una **plataforma de reservas** que dispara eventos hacia otros microservicios especializados cuando se crea una nueva reserva.

Cada microservicio se implementa como una **función Lambda** independiente, escrita potencialmente en diferentes lenguajes (Python, TypeScript, Go, etc.), para demostrar interoperabilidad entre servicios.

---

## 🧩 Arquitectura General

```mermaid
config:
  look: handDrawn
  theme: neutral
---
flowchart LR
    A["🟦 Servicio de Reservas (API Gateway + Lambda)"]
    B["🟪 Event Broker (Amazon EventBridge)"]
    C["🟩 Servicio de Notificaciones (Lambda)"]
    D["🟩 Servicio de Facturación (Lambda)"]
    E["🟩 Servicio de Analítica (Lambda)"]

    EV1["📦 Publica evento: ReservaCreada"]
    EV2["📦 Propaga evento: ReservaCreada"]

    A --> EV1 --> B --> EV2 --> C
    EV2 --> D
    EV2 --> E
```

---

## 🧱 Componentes Principales

| Componente | Descripción | Tecnología |
|-------------|--------------|-------------|
| **Servicio de Reservas** | Expone una API REST para crear reservas y publicar eventos `ReservaCreada`. | AWS Lambda + API Gateway |
| **Event Broker** | Canal de eventos que enruta los mensajes entre servicios. | Amazon EventBridge |
| **Servicio de Notificaciones** | Escucha eventos de reservas y envía notificaciones al usuario. | AWS Lambda |
| **Servicio de Facturación** | Procesa pagos o genera facturas al recibir eventos de reservas. | AWS Lambda |
| **Servicio de Analítica** | Registra métricas o estadísticas de uso. | AWS Lambda |

---

## ⚙️ Estructura de Carpetas

```text
cdk-app/
├── .venv/                 # Entorno virtual Python
├── cdk.out/               # Archivos generados por CDK
├── reservaciones_app/     # Código de la app CDK (stacks, app.py)
├── services/              # Código fuente de los microservicios
│   ├── reservas/
│   ├── notificaciones/
│   ├── facturacion/
│   ├── analitica/
├── tests/                 # Pruebas unitarias
├── .env                   # Variables de entorno
├── .env.example           # Ejemplo de archivo de variables de entorno
├── .gitignore
├── app.py                 # Entrada principal del CDK
├── cdk.json               # Configuración CDK
├── README.md              # Este archivo
├── requirements-dev.txt   # Dependencias de desarrollo
├── requirements.txt       # Dependencias de producción
└── source.bat             # Script de entorno (Windows)
```

---

## 🚀 Despliegue con AWS CDK

### 1️⃣ Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / Mac
.venv\Scripts\activate.bat # Windows
```

### 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3️⃣ Comandos útiles de CDK

| Comando | Descripción |
|----------|--------------|
| `cdk ls` | Lista los stacks del proyecto |
| `cdk synth` | Genera la plantilla de CloudFormation |
| `cdk deploy` | Despliega los recursos en AWS |
| `cdk diff` | Compara cambios entre la versión local y desplegada |
| `cdk destroy` | Elimina los recursos del stack |

---


## 🧠 Conceptos Clave Aprendidos

- Arquitecturas desacopladas mediante eventos.
- AWS CDK en Python para IaC.
- Lambdas multi-lenguaje.
- Comunicación entre servicios con EventBridge.
- Uso de API Gateway como punto de entrada.
- Simulación de AWS con LocalStack.
- Automatización con CloudFormation.
- Añadir persistencia (DynamoDB).
- Autenticación en API Gateway.
- Analítica avanzada (Kinesis / Athena).
- CI/CD para despliegue automatizado.

---

## 🧑‍💻 Autor

**Oscar Vallecillo**
Proyecto educativo de arquitectura basada en eventos.
Tecnologías: AWS, CDK, Lambda, EventBridge, API Gateway, Python, Node.js.

## 🧪 Pruebas Locales

### 🔹 Ejecutar Lambdas localmente

```bash
# Desde el directorio del servicio
python lambda_function.py
```

O usando **AWS SAM CLI**:

```bash
sam local invoke
```

### 🔹 Simular AWS Localmente con LocalStack

LocalStack permite emular servicios de AWS como Lambda, API Gateway y EventBridge **sin costo**.

#### Instalación

```bash
pip install localstack
localstack --version
```

#### Levantar LocalStack

```bash
# Levanta todos los servicios simulados
localstack start
```

O con Docker:

```bash
docker run --rm -it -p 4566:4566 -p 4571:4571 localstack/localstack
```

#### Configurar CDK para LocalStack

```python
import aws_cdk.aws_lambda as lambda_
from aws_cdk import aws_apigateway as apigw, Stack, Environment

class ApiStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)

        func = lambda_.Function(
            self, "ReservasLambda",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="lambda_function.handler",
            code=lambda_.Code.from_asset("services/reservas")
        )

        apigw.LambdaRestApi(self, "ReservasApi", handler=func)

app = App()
ApiStack(app, "ApiStack", env=Environment(
    account="000000000000",  # Dummy para LocalStack
    region="us-east-1"
))
```

Invocar la API localmente con **curl**:

```bash
curl -X POST http://localhost:4566/restapis/<API_ID>/reservas
```

### 🔹 Ejecutar pruebas unitarias

```bash
cd tests/
pytest
```

---

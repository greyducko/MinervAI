import os
from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    CfnOutput,
    aws_lambda as lambda_,
)
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from aws_cdk.aws_apigatewayv2 import HttpApi
from dotenv import load_dotenv

load_dotenv()


class MinervAiAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_function = lambda_.DockerImageFunction(
            self,
            "MinervAiAppFunction",
            code=lambda_.DockerImageCode.from_image_asset("app/"),
            timeout=Duration.seconds(30),
            environment={
                "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
                "FLASK_SECRET_KEY": os.getenv("FLASK_SECRET_KEY"),
            },
            memory_size=256,
        )

        api_gateway = HttpApi(
            self,
            "FlaskHttpApi",
            default_integration=HttpLambdaIntegration(
                "FlaskIntegration", lambda_function
            ),
        )

        CfnOutput(
            self,
            "FlaskApi",
            description="API Gateway endpoint URL",
            value=api_gateway.url or "",
        )

        CfnOutput(
            self,
            "FlaskFunctionArn",
            description="Flask Lambda Function ARN",
            value=lambda_function.function_arn,
        )

        CfnOutput(
            self,
            "FlaskIamRole",
            description="Implicit IAM Role created for Flask function",
            value=lambda_function.role.role_arn,
        )

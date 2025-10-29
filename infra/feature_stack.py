import os
from aws_cdk import (
    Stack, RemovalPolicy, CfnOutput,
    aws_dynamodb as ddb,
)
from constructs import Construct

class FeatureRequestsStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        table = ddb.Table(
            self, "FeatureRequests",
            table_name="FeatureRequestsService",
            partition_key=ddb.Attribute(name="requestId", type=ddb.AttributeType.STRING),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,  # dev only; switch to RETAIN in prod
        )

        # Per-client "top" view
        table.add_global_secondary_index(
            index_name="GSI_TopByLikes",
            partition_key=ddb.Attribute(name="clientId", type=ddb.AttributeType.STRING),
            sort_key=ddb.Attribute(name="likesCount", type=ddb.AttributeType.NUMBER),
            projection_type=ddb.ProjectionType.ALL,
        )

        # Per-client "newest" view
        table.add_global_secondary_index(
            index_name="GSI_Newest",
            partition_key=ddb.Attribute(name="clientId", type=ddb.AttributeType.STRING),
            sort_key=ddb.Attribute(name="createdAt", type=ddb.AttributeType.STRING),
            projection_type=ddb.ProjectionType.ALL,
        )

        CfnOutput(self, "TableName", value=table.table_name)
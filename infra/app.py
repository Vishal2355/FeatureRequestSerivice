#!/usr/bin/env python3
import os
import aws_cdk as cdk
from feature_stack import FeatureRequestsStack

app = cdk.App()
FeatureRequestsStack(
    app, "FeatureRequestsStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION") or "us-east-1",
    ),
)
app.synth()
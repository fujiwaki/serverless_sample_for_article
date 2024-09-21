"""AWS Resources for Chat App."""

import aws_cdk as cdk
from stacks.root_stack import RootStack

app = cdk.App()

RootStack(app, "SampleApp")

app.synth()

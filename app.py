# #!/usr/bin/env python3

import aws_cdk as cdk

from app.minervai_app_stack import MinervAiAppStack


app = cdk.App()
MinervAiAppStack(app, "MinervAiAppStack")

app.synth()

#!/usr/bin/env python3
import os
import aws_cdk as cdk
from wildfire_risk_analytics.wildfire_risk_analytics_stack import WildfireRiskAnalyticsStack


app = cdk.App()
WildfireRiskAnalyticsStack(app, "WildfireRiskAnalyticsStack")
app.synth()

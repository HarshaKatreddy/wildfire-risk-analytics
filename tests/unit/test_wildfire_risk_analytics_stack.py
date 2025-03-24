import aws_cdk as core
import aws_cdk.assertions as assertions

from wildfire_risk_analytics.wildfire_risk_analytics_stack import WildfireRiskAnalyticsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in wildfire_risk_analytics/wildfire_risk_analytics_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = WildfireRiskAnalyticsStack(app, "wildfire-risk-analytics")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

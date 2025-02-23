from aws_cdk import (
    Stack,
    aws_cloudwatch as cloudwatch,
)
from constructs import Construct

class MonitoringStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create dashboard
        dashboard = cloudwatch.Dashboard(
            self, "CremeBruleeDashboard",
            dashboard_name="CremeBrulee-Metrics"
        )

        # Add widgets
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="API Response Times",
                left=[
                    cloudwatch.Metric(
                        namespace="CremeBruleeChatbot",
                        metric_name="ResponseTime",
                        statistic="avg",
                        period=300
                    )
                ]
            ),
            
            cloudwatch.GraphWidget(
                title="Request Count by Endpoint",
                left=[
                    cloudwatch.Metric(
                        namespace="CremeBruleeChatbot",
                        metric_name="RequestCount",
                        statistic="sum",
                        period=300
                    )
                ]
            ),
            
            cloudwatch.GraphWidget(
                title="Chat Processing Times by Platform",
                left=[
                    cloudwatch.Metric(
                        namespace="CremeBruleeChatbot",
                        metric_name="ChatProcessingTime",
                        statistic="avg",
                        period=300,
                        dimensions={"Platform": platform}
                    ) for platform in ["discord", "web", "instagram"]
                ]
            )
        )

        # Create alarms
        cloudwatch.Alarm(
            self, "HighLatencyAlarm",
            metric=cloudwatch.Metric(
                namespace="CremeBruleeChatbot",
                metric_name="ResponseTime",
                statistic="avg",
                period=300
            ),
            threshold=1000,  # 1 second
            evaluation_periods=2,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD
        ) 
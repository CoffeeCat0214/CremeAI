import boto3
from datetime import datetime
import time
from typing import Dict, Any
from ..config import get_settings

settings = get_settings()

class MonitoringService:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.namespace = 'CremeBruleeChatbot'

    async def log_api_metrics(
        self,
        endpoint: str,
        response_time: float,
        status_code: int,
        user_id: str
    ):
        metrics = [
            {
                'MetricName': 'ResponseTime',
                'Value': response_time,
                'Unit': 'Milliseconds',
                'Dimensions': [
                    {'Name': 'Endpoint', 'Value': endpoint},
                    {'Name': 'StatusCode', 'Value': str(status_code)}
                ]
            },
            {
                'MetricName': 'RequestCount',
                'Value': 1.0,
                'Unit': 'Count',
                'Dimensions': [
                    {'Name': 'Endpoint', 'Value': endpoint},
                    {'Name': 'StatusCode', 'Value': str(status_code)}
                ]
            }
        ]
        
        self.cloudwatch.put_metric_data(
            Namespace=self.namespace,
            MetricData=metrics
        )

    async def log_chat_metrics(
        self,
        user_id: str,
        platform: str,
        response_length: int,
        processing_time: float
    ):
        metrics = [
            {
                'MetricName': 'ChatResponseLength',
                'Value': float(response_length),
                'Unit': 'Count',
                'Dimensions': [
                    {'Name': 'Platform', 'Value': platform}
                ]
            },
            {
                'MetricName': 'ChatProcessingTime',
                'Value': processing_time,
                'Unit': 'Milliseconds',
                'Dimensions': [
                    {'Name': 'Platform', 'Value': platform}
                ]
            }
        ]
        
        self.cloudwatch.put_metric_data(
            Namespace=self.namespace,
            MetricData=metrics
        ) 
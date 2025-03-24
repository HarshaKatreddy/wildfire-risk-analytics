from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_glue as glue,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    CfnOutput,
    RemovalPolicy,
    Duration
)
from constructs import Construct

class WildfireRiskAnalyticsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account

        raw_bucket_name = f"wildfire-raw-data-{account}"
        processed_bucket_name = f"wildfire-processed-data-{account}"
        fpa_fod_db_name = "wildfire_fpa_fod_db"
        nclimdiv_db_name = "wildfire_nclimdiv_db"
        wrc_db_name = "wildfire_wrc_db"

        # 🔹 S3 Buckets
        self.raw_bucket = s3.Bucket(
            self, "RawDataBucket",
            bucket_name=raw_bucket_name,
            versioned=True,
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.processed_bucket = s3.Bucket(
            self, "ProcessedDataBucket",
            bucket_name=processed_bucket_name,
            versioned=True,
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # 🔹 Glue Role
        self.glue_role = iam.Role(
            self, "GlueServiceRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            ],
            role_name="GlueServiceRoleDefault",
        )

        # 🔹 Lambda Execution Role
        lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
            ]
        )

        # 🔹 Lambda 1: Download nclmdiv .dat files
        self.download_lambda = _lambda.Function(
            self, "DownloadNclimdivData",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("infra/lambdas/download_nclimdiv_data"),
            role=lambda_role,
            timeout=Duration.minutes(10),
            environment={
                "RAW_BUCKET": raw_bucket_name
            }
        )

        # 🔹 Lambda 2: Convert to CSV
        self.convert_lambda = _lambda.Function(
            self, "ConvertNclimdivToCsv",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function_csv.lambda_handler",
            code=_lambda.Code.from_asset("infra/lambdas/nclimdiv_convert_csv"),
            layers=[
                _lambda.LayerVersion.from_layer_version_arn(
                    self, "PandasLayer",
                    layer_version_arn="arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python39:2"
                )
            ],
            role=lambda_role,
            memory_size=512,
            timeout=Duration.minutes(10),
            environment={
                "RAW_BUCKET": raw_bucket_name,
                "PROCESSED_BUCKET": processed_bucket_name
            }
        )

        # 🔹 Monthly Schedule Trigger for Download Lambda
        monthly_schedule = events.Rule(
            self, "MonthlyNOAADownloadTrigger",
            schedule=events.Schedule.cron(minute="0", hour="0", day="10", month="*", year="*")
        )
        monthly_schedule.add_target(targets.LambdaFunction(self.download_lambda))

        # 🔹 EventBridge Trigger: Convert Lambda after Download
        convert_trigger = events.Rule(
            self, "TriggerConvertAfterDownload",
            event_pattern=events.EventPattern(
                source=["aws.lambda"],
                detail_type=["Lambda Function Invocation Result"],
                detail={"requestContext": {"functionArn": [self.download_lambda.function_arn]}}
            )
        )
        convert_trigger.add_target(targets.LambdaFunction(self.convert_lambda))

        # 🔹 Glue Database - FPA FOD
        self.fpa_fod_db = glue.CfnDatabase(
            self, "FpaFodDB",
            catalog_id=account,
            database_input={"Name": fpa_fod_db_name}
        )

        self.fpa_fod_crawler = glue.CfnCrawler(
            self, "FpaFodCrawler",
            name="fpa_fod_crawler",
            role=self.glue_role.role_arn,
            database_name=self.fpa_fod_db.ref,
            targets={"s3Targets": [{"path": f"s3://{raw_bucket_name}/fpa-fod/"}]},
            table_prefix="fpa_",
            schema_change_policy={
                "UpdateBehavior": "UPDATE_IN_DATABASE",
                "DeleteBehavior": "DEPRECATE_IN_DATABASE"
            }
        )

        # 🔹 Glue Database - WRC
        self.wrc_db = glue.CfnDatabase(
            self, "WrcDB",
            catalog_id=account,
            database_input={"Name": wrc_db_name}
        )

        self.wrc_crawler = glue.CfnCrawler(
            self, "WrcCrawler",
            name="wrc_crawler",
            role=self.glue_role.role_arn,
            database_name=self.wrc_db.ref,
            targets={"s3Targets": [{"path": f"s3://{raw_bucket_name}/wrc-v2/"}]},
            table_prefix="wrc_",
            schema_change_policy={
                "UpdateBehavior": "UPDATE_IN_DATABASE",
                "DeleteBehavior": "DEPRECATE_IN_DATABASE"
            }
        )

        # 🔹 Glue Database - nCLIMDIV
        self.nclimdiv_db = glue.CfnDatabase(
            self, "NclimdivDB",
            catalog_id=account,
            database_input={"Name": nclimdiv_db_name}
        )

        self.nclimdiv_crawler = glue.CfnCrawler(
            self, "NclimdivCrawler",
            name="nclimdiv_crawler",
            role=self.glue_role.role_arn,
            database_name=self.nclimdiv_db.ref,
            targets={"s3Targets": [{"path": f"s3://{processed_bucket_name}/nclimdiv/"}]},
            table_prefix="nclimdiv_",
            schema_change_policy={
                "UpdateBehavior": "UPDATE_IN_DATABASE",
                "DeleteBehavior": "DEPRECATE_IN_DATABASE"
            }
        )


        # 🔹 Glue Database - Cleaned Data
        self.clean_db_name = "wildfire_clean_db"
        self.clean_db = glue.CfnDatabase(
            self, "CleanedDB",
            catalog_id=account,
            database_input={"Name": self.clean_db_name}
        )

        # 🔹 CDK Outputs
        CfnOutput(self, "RawBucketName", value=raw_bucket_name)
        CfnOutput(self, "ProcessedBucketName", value=processed_bucket_name)
        CfnOutput(self, "GlueRoleArn", value=self.glue_role.role_arn)
        CfnOutput(self, "FpaFodDatabaseName", value=fpa_fod_db_name)
        CfnOutput(self, "FpaFodCrawlerName", value=self.fpa_fod_crawler.name)
        CfnOutput(self, "WrcDatabaseName", value=wrc_db_name)
        CfnOutput(self, "WrcCrawlerName", value=self.wrc_crawler.name)
        CfnOutput(self, "NclimdivDatabaseName", value=nclimdiv_db_name)
        CfnOutput(self, "NclimdivCrawlerName", value=self.nclimdiv_crawler.name)
        CfnOutput(self, "DownloadLambdaName", value=self.download_lambda.function_name)
        CfnOutput(self, "ConvertLambdaName", value=self.convert_lambda.function_name)

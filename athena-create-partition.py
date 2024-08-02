import boto3
import datetime
import logging
import time

# setup simple logging for INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# boto3 init
athena = boto3.client('athena','ap-northeast-2')

# setup variables
account_id = "YOUR ACCOUNT"
athena_workgroup = "WORKGROUP"
catalog_name = "CATALOG NAME"
database_name = "DATABASE NAME"
athena_result_bucket = "YOUR S3 BUCKET ARN"
bucket_kms_key = "YOUR KMS KEY FOR BUCKET ENCRYPTION" #KMS for S3 Bucket Encryption

# VPC, Flowlog 에따라 버킷 및 테이블 변수 추가
flowlog_bucket_1= "FLOWLOG S3 BUCKET NAME"
flowlog_bucket_2= "FLOWLOG S3 BUCKET NAME"

flowlog_table_1 = "ATHENA TABLE NAME"
flowlog_table_2 = "ATHENA TABLE NAME"

# time setup
today = datetime.datetime.utcnow()
logger.info('Today: {}'.format(today))
year = today.strftime("%Y")
month = today.strftime("%m")
day  = today.strftime("%d")

# 쿼리 실행
def start_query_partition(flowlog_table, flowlog_bucket):
    query = """
                ALTER TABLE {}
                ADD PARTITION (`date`='{}-{}-{}')
                LOCATION 's3://{}/AWSLogs/{}/vpcflowlogs/ap-northeast-2/{}/{}/{}'
            """.format(flowlog_table, year, month, day, flowlog_bucket, account_id, year, month, day)
    logger.info("Query: {}".format(query))
    # 쿼리 실행
    response = athena.start_query_execution( QueryString=query,
                                             QueryExecutionContext={
                                                 'Catalog': catalog_name,
                                                 'Database': database_name
                                             },
                                             WorkGroup=athena_workgroup,
                                             ResultConfiguration={
                                                 'OutputLocation': athena_result_bucket,
                                                 'EncryptionConfiguration': {
                                                     'EncryptionOption': 'SSE_KMS',
                                                     'KmsKey': bucket_kms_key
                                                 }
                                              }
                                        )
    query_execution_id = response['QueryExecutionId']
    logger.info('Query Execution ID: {}'.format(query_execution_id))
    print(query_execution_id)    

############################################################################
#  VPC Flow Log Catalog 테이블 파티션 갱신
############################################################################

def lambda_handler(event, context):
    try: 
        start_query_execution(flowlog_table_1, flowlog_bucket_1)
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1)

    try:
        start_query_execution(flowlog_table_2, flowlog_bucket_2)
    except Exception as e:
        print(f"Error: {e}")
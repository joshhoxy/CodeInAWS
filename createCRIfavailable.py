import boto3
import json
import time
import os
from datetime import datetime, timedelta, timezone

# boto3 init
region = 'ap-northeast-2'
ec2 = boto3.client('ec2', region_name=region)

# 인스턴스 타입 지정
type_1 = 'g5.2xlarge'
type_2 = 'g5.4xlarge'
type_3 = None

# 인스턴스 타입별 희망 가용영역 지정
az_1 = 'ap-northeast-2d'
az_2 = 'ap-northeast-2a'
az_3 = None

# 용량예약 수량 지정
num_1 = 1
num_2 = 2
num_3 = None
    
# 용량예약 생성 시도할 인스턴스 리스트
ec2_list = [] 
ec2_list.append(type_1)
ec2_list.append(type_2)
ec2_list.append(type_3)
ec2_list = [item for item in ec2_list if item is not None] #None 값 정리
print(ec2_list)

# SNS 관련 변수
# topicArn = os.environ['SNS_Topic_ARN']


# 용량예약 생성 함수 정의
def create_capacity(type, az, num):
    ec2.create_capacity_reservation(
        InstanceType=type,
        InstancePlatform='Linux/UNIX',
        AvailabilityZone=az,
        Tenancy='default',
        InstanceCount=num,
        EbsOptimized=True,
        EndDateType='unlimited',
        InstanceMatchCriteria='open',
        DryRun=True #실제적용시 False
    )

# 생성 성공시 SNS 보내기
def sendSnsNotification(topicArn, subject, message):
    sns_client = boto3.client('sns')

    sns_client.publish(
        TopicArn = topicArn,
        Subject = subject,
        Message = message
    )
    print(f"[INFO] Send to SNS with an exception instanceID")


# 인스턴스별 생성 가능한 가용영역 조회
response = ec2.describe_instance_type_offerings(
    DryRun=False,
    LocationType='availability-zone',
    Filters=[
        {
            'Name': 'instance-type',
            'Values': ec2_list
        },
    ],
)
offerings = response.get('InstanceTypeOfferings') # response값 정리

# 희망조건에 따라 용량예약 생성
for offer in offerings:
    print(f"Available: {offer}")
    if (offer.get('InstanceType')==type_1 and offer.get('Location')==az_1):
        try:
            print(f"Attempt to create Capacity Reservation: {type_1} in {az_1} instance")
            create_capacity(type_1,az_1,num_1)
            # sendSnsNotification(topicArn, "Capacity Reservation creation succeeded", "instance: " + type_1 + " in " +az_1)
        except Exception as e:
            print(f"Error: {e}")
    
    if (offer.get('InstanceType')==type_2 and offer.get('Location')==az_2):
        try:
            print(f"Attempt to create Capacity Reservation: {type_2} in {az_2} instance")
            create_capacity(type_2,az_2,num_2)
            # sendSnsNotification(topicArn, "Capacity Reservation creation succeeded", "instance: " + type_2 + " in " +az_2)
        except Exception as e:
            print(f"Error: {e}")
    if (offer.get('InstanceType')==type_3 and offer.get('Location')==az_3):
        try:
            print(f"Attempt to create Capacity Reservation: {type_3} in {az_3} instance")
            create_capacity(type_3,az_3,num_3)
            # sendSnsNotification(topicArn, "Capacity Reservation creation succeeded", "instance: " + type_3 + " in " +az_3)
        except Exception as e:
            print(f"Error: {e}") 

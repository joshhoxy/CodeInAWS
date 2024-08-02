import boto3
import os
import time

# 인스턴스 명세
type_1 = 't2.nano'
type_2 = 't2.micro'

type_1_az = 'ap-northeast-2a'
type_2_az = 'ap-northeast-2a'

# 목표 CR 개수
tgNum_type_1=2
tgNum_type_2=2

# 현재 CR 개수 초기화
currentNum_type_1=0
currentNum_type_2=0

def check_current_cr(type):
    num_totalInstance = 0
    response = ec2.describe_capacity_reservations(
        MaxResults=500,
        Filters = [
            {
                'Name': 'state',
                'Values': [
                    'active'
                ]
            },
            {
                'Name': 'instance-type',
                'Values': [
                    type
                ]
            }
        ],
        DryRun=False
    )
    cr_all = response['CapacityReservations']
    for cr in cr_all:
        num_totalInstance += cr['TotalInstanceCount']
    return num_totalInstance

def create_capacity(type, az, num):
    ec2.create_capacity_reservation(
        InstanceType=type,
        InstancePlatform='Linux/UNIX',
        AvailabilityZone=az,
        Tenancy='default',
        InstanceCount=num,
        EndDateType='unlimited',
        InstanceMatchCriteria='open',
        DryRun=False
    )

# CR 생성 성공시 SNS 보내기
def sendSnsNotification(topicArn, subject, message):
    sns_client = boto3.client('sns')

    sns_client.publish(
        TopicArn = topicArn,
        Subject = subject,
        Message = message
    )
    print(f"[INFO] Send to SNS with an exception instanceID")

#######################################################################################################################

# boto3 init
region = 'ap-northeast-2'
ec2 = boto3.client('ec2', region_name=region)

currentNum_type_1=check_current_cr(type_1)
currentNum_type_2=check_current_cr(type_2)
print(f"Current {type_1} InstanceCount is: {currentNum_type_1}, desirable InstanceCount is: {tgNum_type_1}")
print(f"Current {type_2} InstanceCount is: {currentNum_type_2}, desirable InstanceCount is: {tgNum_type_2}")

# type_1에 대한 CR 생성
if currentNum_type_1 < tgNum_type_1:
    for i in range(tgNum_type_1 - currentNum_type_1):
        try:
            print(f"Attempt to create Capacity Reservation: {type_1} in {type_1_az} instance")
            create_capacity(type_1, type_1_az, 1)
            print("Creation Capacity Reservation Succeeded.")
            # sendSnsNotification(topicArn, "Capacity Reservation creation succeeded", "instance: " + type_1 + " in " +type_1_az)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)

# type_2에 대한 CR 생성
if currentNum_type_2 < tgNum_type_2:
    for i in range(tgNum_type_2 - currentNum_type_2):
        try:
            print(f"Attempt to create Capacity Reservation: {type_2} in {type_2_az} instance")
            create_capacity(type_2, type_2_az, 1)
            print("Creation Capacity Reservation Succeeded.")
            # sendSnsNotification(topicArn, "Capacity Reservation creation succeeded", "instance: " + type_2 + " in " +type_2_az)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)

print('Programme terminated.')
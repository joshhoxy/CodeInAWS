# delete eks clusters
import boto3
# import time
# from datetime import datetime, timedelta, timezone

# Get clusters' names
eks_client = boto3.client('eks')
response = eks_client.list_clusters()
eks_list = response.get('clusters')

# print(eks_list)

# Make Clusters class list 
clusters = []
for cluster in eks_list:
    # print(cluster)
    # print(type(cluster))
    response = eks_client.describe_cluster(name=cluster)
    clusters.append(response['cluster'])

# Delete Cluster meets condition
for cluster in clusters:
    tag_user = cluster['tags']['User']
    if 'josh' in tag_user:
        try:
            eks_client.delete_cluster(name=cluster['name'])
            print(f"Deleted EKS Cluster : {cluster['name']}")
        except Exception as e:
            print(f"Error: {e}")

print("Lambda Execution finished.")

# print(clusters)
# print(response)

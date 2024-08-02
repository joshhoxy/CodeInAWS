CREATE EXTERNAL TABLE `test_table_vpclogs`(
  `version` int, 
  `account_id` string, 
  `interface_id` string, 
  `srcaddr` string, 
  `dstaddr` string, 
  `srcport` int, 
  `dstport` int, 
  `protocol` bigint, 
  `packets` bigint, 
  `bytes` bigint, 
  `start` bigint, 
  `end` bigint, 
  `action` string, 
  `log_status` string, 
  `vpc_id` string, 
  `subnet_id` string, 
  `instance_id` string, 
  `tcp_flags` int, 
  `type` string, 
  `pkt_srcaddr` string, 
  `pkt_dstaddr` string, 
  `az_id` string, 
  `sublocation_type` string, 
  `sublocation_id` string, 
  `pkt_src_aws_service` string, 
  `pkt_dst_aws_service` string, 
  `flow_direction` string, 
  `traffic_path` int)
PARTITIONED BY ( 
  `region` string, 
  `day` string)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY ' ' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://YOURBUCKET_NAME/AWSLogs/YOURACCOUNT/vpcflowlogs'
TBLPROPERTIES (
  'projection.day.format'='yyyy/MM/dd', 
  'projection.day.range'='2024/02/01,NOW', 
  'projection.day.type'='date', 
  'projection.enabled'='true', 
  'projection.region.type'='enum', 
  'projection.region.values'='ap-northeast-2', 
  'skip.header.line.count'='1', 
  'storage.location.template'='s3://YOURBUCKET_NAME/AWSLogs/YOURACCOUNT/vpcflowlogs/${region}/${day}'
  )
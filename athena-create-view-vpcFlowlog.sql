CREATE OR REPLACE VIEW test_table_vpclogs_utc9 AS 
SELECT
  "version"
, "account_id"
, "interface_id"
, "srcaddr"
, "dstaddr"
, "pkt_srcaddr"
, "pkt_dstaddr"
, "srcport"
, "dstport"
, "protocol"
, "tcp_flags"
, "packets"
, "bytes"
, ("from_unixtime"("start") + INTERVAL  '9' HOUR) "start"
, ("from_unixtime"("end") + INTERVAL  '9' HOUR) "end"
, "action"
, "log_status"
, "day"
FROM
  test_table_vpclogs
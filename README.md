# DDBMS
Distributed Database Management System for THUACP2023

## When running a large script in mysql workbence
### SET GLOBAL max_allowed_packet=1000000

```
SELECT * FROM dmbs1.user 
WHERE find_in_set(uid, (SELECT readUidList FROM dmbs1.be_read  WHERE aid=9));
```
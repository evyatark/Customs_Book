
### MySQL in Docker

```
docker start mysql_server_custom_book
```

## Query DB

```sql
select ID,Parent_CustomsItemID,FullClassification from CustomsItem
                    where FullClassification=8903313000 and CustomsBookTypeID=1;
-- 31244,31242,8903313000
select ID,Parent_CustomsItemID,FullClassification from CustomsItem where ID=31242;
-- 31242,31241,8903310000
select ID,Parent_CustomsItemID,FullClassification from CustomsItem where ID=31241;
-- 31241,2936,8903300000
select ID,Parent_CustomsItemID,FullClassification from CustomsItem where ID=2936;
-- 2936,23166,8903000000
select ID,Parent_CustomsItemID,FullClassification from CustomsItem where ID=23166;
-- 23166,8847,8900000000

select ci.FullClassification as 'נובע מפרק', CustomsItemID as id, AuthorityID as 'גורם מאשר',ConfirmationTypeID as 'סוג אישור' ,TextualCondition as 'תיאור תנאים',TrNumber as 'מספר תקן',InterConditionsRelationshipID as 'יחס תנאים' ,StartDate,EndDate,InceptionCodeID,RegularityPublicationCodeID,RegularityInceptionID,RegularityRequirementID,InterConditionsRelationshipID,IsPersonalImportIncluded,rr.ID,RequirementGoodsDescription
        from RegularityRequirement rr, RegularityRequiredCertificate, RegularityInception, CustomsItem ci
        where rr.CustomsItemID in (31244,31242,31241,2936,23166)
          and EndDate > '2022-11-01'
          and RegularityInception.ID=RegularityRequiredCertificate.RegularityInceptionID
          and RegularityInception.RegularityRequirementID=rr.ID
          and rr.CustomsItemID=ci.ID;
```


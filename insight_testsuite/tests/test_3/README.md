Test the case where a person prescribes a drug multiple times, she should only be counted once towards the number of unique prescribers; each prescription should still contribute to the total cost though. For example, the input

```
id,prescriber_last_name,prescriber_first_name,drug_name,drug_cost
1000000007,Rodriguez,Maria,BENZTROPINE MESYLATE,100
1000000009,Rodriguez,Maria,BENZTROPINE MESYLATE,100
```

should produce the following output

```
BENZTROPINE MESYLATE,1,200
```

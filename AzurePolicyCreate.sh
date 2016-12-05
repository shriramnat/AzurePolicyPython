python AzurePolicyCreate.py
#azure login -e AzureCloud
# RESOURCEGROUPID=$(azure group list --json | jq '.[] | select (.name | contains ("shnatarapolicy"))' | jq '.id')
RESOURCEGROUPID=""+$(azure group create shnatarapolicy09 westus --json | jq .id)
echo $RESOURCEGROUPID

POLICYID=""$(azure policy definition create --name regionPolicyDefinition1 --description "Policy to allow resource creation only in certain regions" --policy AzureStackPolicy.json --json | jq '.id')
echo $POLICYID

#azure policy assignment delete --name hellpolicy --scope "/subscriptions/d34bd6cc-8d7e-451b-ace3-cd05c69f82d0/resourceGroups/shnatarapolicy01"
azure policy assignment create --name hellopolicy --policy-definition-id $POLICYID --scope $RESOURCEGROUPID --subscription d34bd6cc-8d7e-451b-ace3-cd05c69f82d0 --verbose

POLICY=$(python AzurePolicyCreate.py)

# Login to Azure. Comment this line out if already logged in
azure login -e AzureCloud

RESOURCEGROUPID=$(azure group create shnatarapolicy31 westus --json | jq -r .id)
echo "Created Resource Group with ID " $RESOURCEGROUPID

POLICYID=$(azure policy definition create --name regionPolicyDefinition1 --description "Policy to allow resource creation only in certain regions" --policy-string "$POLICY" --json | jq -r '.id')
echo "Created Policy Definition with ID " $POLICYID

# To create policy from a file instead of a string
# POLICYID=$(azure policy definition create --name regionPolicyDefinition1 --description "Policy to allow resource creation only in certain regions" --policy AzureStackPolicy.json --json | jq -r '.id')

echo "Creating Policy Assignment on the Resource Group..."
azure policy assignment create --name hellopolicy --policy-definition-id $POLICYID --scope $RESOURCEGROUPID --verbose

# MISC helper cmds
# RESOURCEGROUPID=$(azure group list --json | jq '.[] | select (.name | contains ("shnatarapolicy"))' | jq '.id')
# azure policy assignment delete --name hellopolicy --scope "/subscriptions/d34bd6cc-8d7e-451b-ace3-cd05c69f82d0/resourceGroups/shnatarapolicy01"
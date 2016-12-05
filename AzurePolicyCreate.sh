POLICY=$(python AzurePolicyCreate.py)

# Login to Azure. Comment this line out if already logged in
azure login -e AzureCloud

# Create a Resource Group
RESOURCEGROUPID=$(azure group create shnatarapolicy32 westus --json | jq -r .id)
echo "Created Resource Group with ID " $RESOURCEGROUPID

# Create a Policy Definition
POLICYID=$(azure policy definition create --name AzureStackPolicy --description "Policy to allow only Azure Stack compatible resources to be created" --policy-string "$POLICY" --json | jq -r '.id')
echo "Created Policy Definition with ID " $POLICYID

# To create policy from a file instead of a string
# POLICYID=$(azure policy definition create --name AzureStackPolicy --description "Policy to allow only Azure Stack compatible resources to be created" --policy AzureStackPolicy.json --json | jq -r '.id')

echo "Creating Policy Assignment on the Resource Group..."
azure policy assignment create --name AzureStackPolicy --policy-definition-id $POLICYID --scope $RESOURCEGROUPID --verbose

# MISC helper cmds
# RESOURCEGROUPID=$(azure group list --json | jq '.[] | select (.name | contains ("shnatarapolicy"))' | jq '.id')
# azure policy assignment delete --name hellopolicy --scope "/subscriptions/d34bd6cc-8d7e-451b-ace3-cd05c69f82d0/resourceGroups/shnatarapolicy01"
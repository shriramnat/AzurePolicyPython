import json

def returnAllowedResources(equalsOrLike,equalsOrLikeValue):
    data = {}
    data['field'] = 'type'
    data[equalsOrLike] = equalsOrLikeValue
    return data

def main():
    #Constants
    vmSkuField = "Microsoft.Compute/virtualMachines/sku.name"
    storageSkuField = "Microsoft.Storage/storageAccounts/sku.name"

    # Read ProviderMetadata
    with open('AzureStack.Provider.Metadata.json') as data_file:
        providerMetadata = json.load(data_file)

    # Read VM SKU data
    with open('AzureStack.vmSkus.json') as data_file:
        vmSkus = json.load(data_file)

    # Read Storage SKU data
    with open('AzureStack.storageSkus.json') as data_file:
        storageSkus = json.load(data_file)
    allowResources = []

    # Form a list of allowed values from provider Metadata
    for p in providerMetadata['value']:
        for r in p['resourceTypes']:
            allowResources.append(returnAllowedResources('equals', p['namespace']+"/"+r['resourceType']))
            allowResources.append(returnAllowedResources('like', p['namespace']+"/"+r['resourceType']+"/*"))

    # Create Policy from Template with values from Metadata
    policy='{"then":{"effect":"deny"},"if":{"not":{"allOf":[{"anyOf":%s},{"not":{"anyOf":[{"allOf":[{"exists":"true","field":"%s"},{"not":{"in":%s,"field":"%s"}}]},{"allOf":[{"exists":"true","field":"%s"},{"not":{"in":%s,"field":"%s"}}]}]}}]}}}' %(json.dumps(allowResources),vmSkuField,json.dumps(vmSkus),vmSkuField,storageSkuField,json.dumps(storageSkus),storageSkuField)

    # Create a JSON file
    with open('AzureStackPolicy.json', 'w') as text_file:
        text_file.write(policy)
    
    return json.dumps(policy)

if __name__ == "__main__":
     # if you call this script from the command line (the shell) it will
 # run the 'main' function
 main()
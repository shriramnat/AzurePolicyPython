"""
This script creates an Azure Stack Policy for Azure.
"""
import json
import sys

def return_allowed_resources(equals_or_like, equals_or_like_value):
    """
    Return a dictionary of approved resources.
    """
    data = {}
    data['field'] = 'type'
    data[equals_or_like] = equals_or_like_value
    return data

def main():
    """
    Main method.
    """
    # Constants
    vm_sku_field = "Microsoft.Compute/virtualMachines/sku.name"
    storage_sku_field = "Microsoft.Storage/storageAccounts/sku.name"

    # Read ProviderMetadata
    with open('AzureStack.Provider.Metadata.json') as data_file:
        provider_metadata = json.load(data_file)

    # Read VM SKU data
    with open('AzureStack.vmSkus.json') as data_file:
        vm_skus = json.load(data_file)

    # Read Storage SKU data
    with open('AzureStack.storageSkus.json') as data_file:
        storage_skus = json.load(data_file)

    allow_resources = []

    # Form a list of allowed values from provider Metadata
    for provider in provider_metadata['value']:
        for resource_types in provider['resourceTypes']:
            allow_resources.append(return_allowed_resources('equals', provider['namespace']+"/"+resource_types['resourceType']))
            allow_resources.append(return_allowed_resources('like', provider['namespace']+"/"+resource_types['resourceType']+"/*"))

    # Create Policy from Template with values from Metadata
    policy = '{"then":{"effect":"deny"},"if":{"not":{"allOf":[{"anyOf":%s},{"not":{"anyOf":[{"allOf":[{"exists":"true","field":"%s"},{"not":{"in":%s,"field":"%s"}}]},{"allOf":[{"exists":"true","field":"%s"},{"not":{"in":%s,"field":"%s"}}]}]}}]}}}' %(json.dumps(allow_resources), vm_sku_field, json.dumps(vm_skus), vm_sku_field, storage_sku_field, json.dumps(storage_skus), storage_sku_field)

    # Create a JSON file
    # with open('AzureStackPolicy.json', 'w') as text_file:
    #     text_file.write(policy)

    print policy
    sys.exit(0)

if __name__ == "__main__":
    # if you call this script from the command line (the shell) it will
    # run the 'main' function
    main()

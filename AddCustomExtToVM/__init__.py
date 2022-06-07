import logging

import azure.functions as func
# Import the needed credential and management objects from the libraries.
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # Derived from https://docs.microsoft.com/en-us/azure/virtual-machines/extensions/custom-script-windows#using-multiple-scripts

    credentials = DefaultAzureCredential()
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

    compute_client = ComputeManagementClient(credentials, subscription_id)

    rg_name = '<resource-group>'
    vm_name = '<vm-name>'
    extenstion_name = '<vm-script-name>'
    parameters = {
        'location':'eastus',
        'publisher': 'Microsoft.Compute',
        'virtual_machine_extension_type': 'CustomScriptExtension',
        #Types found here: https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/azure-arc/servers/manage-vm-extensions.md
        'type_handler_version': '1.10',
        'auto_upgrade_minor_version': True,
        'settings':{'fileUris': ["https://xxxxxxx.blob.core.windows.net/buildServer1/1_Add_Tools.ps1"]},

    }
    #Parameters found here: https://docs.microsoft.com/en-us/python/api/azure-mgmt-compute/azure.mgmt.compute.v2018_10_01.models.virtualmachineextension?view=azure-python
    poller = compute_client.virtual_machine_extensions.begin_create_or_update(rg_name, vm_name, extenstion_name, parameters)
    #Method found here: https://docs.microsoft.com/en-us/python/api/azure-mgmt-compute/azure.mgmt.compute.v2018_10_01.operations.virtualmachineextensionsoperations?view=azure-python
    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )

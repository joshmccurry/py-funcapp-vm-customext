import logging

import azure.functions as func
# Import the needed credential and management objects from the libraries.
from azure.identity import EnvironmentCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import VirtualMachineExtension
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # Derived from https://docs.microsoft.com/en-us/azure/virtual-machines/extensions/custom-script-windows#using-multiple-scripts

    credentials = EnvironmentCredential()
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

    compute_client = ComputeManagementClient(credentials, subscription_id)

    #Exchange for hardcoded variable, received from GET Parameters/Query or POST body, or even as a Environmental variable from App Settings
    resource_group_name = os.environ["RESOURCE_GROUP"]       
    vm_name = os.environ["VM_NAME"]    
    vm_extension_name = os.environ["VM_EXT_NAME"]  

    #Parameters found here: https://docs.microsoft.com/en-us/python/api/azure-mgmt-compute/azure.mgmt.compute.v2018_10_01.models.virtualmachineextension?view=azure-python
    # VirtualMachineExtension(*, 
    #     location: str, 
    #     tags: Optional[Dict[str, str]] = None, 
    #     force_update_tag: Optional[str] = None, 
    #     publisher: Optional[str] = None, 
    #     type_properties_type: Optional[str] = None, 
    #     type_handler_version: Optional[str] = None, 
    #     auto_upgrade_minor_version: Optional[bool] = None, 
    #     settings: Optional[Any] = None, 
    #     protected_settings: Optional[Any] = None, 
    #     instance_view: Optional[azure.mgmt.compute.v2018_10_01.models._models_py3.VirtualMachineExtensionInstanceView] = None, 
    #     **kwargs)
    extension_parameters = VirtualMachineExtension(
        location="eastus",
        publisher= "Microsoft.Azure.Extensions",
        type_properties_type= "CustomScriptExtension", #Seems like a typo, but is required
        #Types found here: https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/azure-arc/servers/manage-vm-extensions.md
        type_handler_version= "2.0",
        auto_upgrade_minor_version= True,
        settings = {
            "fileUris": ["https://xxxxxxx.blob.core.windows.net/buildServer1/1_Add_Tools.ps1"]
        },
        protected_settings = {
            "commandToExecute":"powershell -ExecutionPolicy Unrestricted -File 1_Add_Tools.ps1"
        }
    ) 

    #Method found here: https://docs.microsoft.com/en-us/python/api/azure-mgmt-compute/azure.mgmt.compute.v2018_10_01.operations.virtualmachineextensionsoperations?view=azure-python#azure-mgmt-compute-v2018-10-01-operations-virtualmachineextensionsoperations-begin-create-or-update
    # begin_create_or_update(
    #     resource_group_name: str, 
    #     vm_name: str, 
    #     vm_extension_name: str, 
    #     extension_parameters: _models.VirtualMachineExtension, #See the link above for parameters
    #     **kwargs: Any) -> LROPoller[_models.VirtualMachineExtension]
    result = compute_client.virtual_machine_extensions.begin_create_or_update(resource_group_name, vm_name, vm_extension_name, extension_parameters).result()

    logging.info(f"Extension {vm_extension_name} created for {vm_name}.")
    logging.info(f"{format(result)}")

    return func.HttpResponse(
            f"This HTTP triggered function executed successfully.\n{format(result)}",
            status_code=200
    )

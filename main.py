### Import Packages
import oci
import uuid
import base64

# Setup basic variables
# Auth Config
CONFIG_PROFILE = "DEFAULT"
config = oci.config.from_file('~/.oci/config', CONFIG_PROFILE)

# Compartment where processor job will be created (required)
COMPARTMENT_ID = "ocid1.compartment.oc1..aaaaaaaa6owu3laqhrl4do5qg2dhfbdf2mune66gzhqley53dvymzpf6xvyq"  # e.g. "ocid1.compartment.oc1..aaaaaaaae5j73axsja5fnahbn23ilop3ynjkcg77mcvgryddz4pkh2t5ppaq";

def create_processor_job_callback(times_called, response):
    print("Waiting for processor lifecycle state to go into succeeded state:", response.data)

# Setup input location where document being processed is stored.
object_location = oci.ai_document.models.ObjectLocation()
object_location.namespace_name = "ax5dyyuncbga"  # e.g. "axhh9gizbq5x"
object_location.bucket_name = "bucket-20231106-1838"  # e.g "demo_examples"
object_location.object_name = "searchable_document.pdf"  # e.g "key_value_extraction_demo.jpg

aiservicedocument_client = oci.ai_document.AIServiceDocumentClientCompositeOperations(oci.ai_document.AIServiceDocumentClient(config=config))

# Document Key-Value extraction Feature
key_value_extraction_feature = oci.ai_document.models.DocumentKeyValueExtractionFeature()

# Setup the output location where processor job results will be created
output_location = oci.ai_document.models.OutputLocation()
output_location.namespace_name = "ax5dyyuncbga"  # e.g. "axk2tfhlrens"
output_location.bucket_name = "bucket-20231106-1838"  # e.g "output"
output_location.prefix = "demo"  # e.g "demo"

# Create a processor_job for invoice key_value_extraction feature. 
# Note: If you want to use another key value extraction feature, set document_type to "RECIEPT" "PASSPORT" or "DRIVER_ID". If you have a mix of document types, you can remove document_type
create_processor_job_details_key_value_extraction = oci.ai_document.models.CreateProcessorJobDetails(
                                                    display_name=str(uuid.uuid4()),
                                                    compartment_id=COMPARTMENT_ID,
                                                    input_location=oci.ai_document.models.ObjectStorageLocations(object_locations=[object_location]),
                                                    output_location=output_location,
                                                    processor_config=oci.ai_document.models.GeneralProcessorConfig(features=[key_value_extraction_feature],
                                                                                                                   document_type="INVOICE"))

print("Calling create_processor with create_processor_job_details_key_value_extraction:", create_processor_job_details_key_value_extraction)
create_processor_response = aiservicedocument_client.create_processor_job_and_wait_for_state(
    create_processor_job_details=create_processor_job_details_key_value_extraction,
    wait_for_states=[oci.ai_document.models.ProcessorJob.LIFECYCLE_STATE_SUCCEEDED],
    waiter_kwargs={"wait_callback": create_processor_job_callback})

print("processor call succeeded with status: {} and request_id: {}.".format(create_processor_response.status, create_processor_response.request_id))
processor_job: oci.ai_document.models.ProcessorJob = create_processor_response.data
print("create_processor_job_details_key_value_extraction response: ", create_processor_response.data)

print("Getting defaultObject.json from the output_location")
object_storage_client = oci.object_storage.ObjectStorageClient(config=config)
get_object_response = object_storage_client.get_object(namespace_name=output_location.namespace_name,
                                                       bucket_name=output_location.bucket_name,
                                                       object_name="{}/{}/{}_{}/results/{}.json".format(
                                                           output_location.prefix, processor_job.id,
                                                           object_location.namespace_name,
                                                           object_location.bucket_name,
                                                           object_location.object_name))
print(str(get_object_response.data.content.decode()))



#########################################################################
""" #Creating response file
print("create_processor_job_details_key_value_extraction response: ", create_processor_response.data)

# Convert the response data to a string
response_data_str = str(create_processor_response.data)

# Open a file in write mode ('w')
with open('response.txt', 'w') as f:
    # Write the response data string to the file
    f.write(response_data_str)

print("Response has been written to response.txt") """
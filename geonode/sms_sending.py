import clx.xms
import requests

client = clx.xms.Client(service_plan_id='{spid}', token='{token}')

create = clx.xms.api.MtBatchTextSmsCreate()
create.sender = '12345'
create.recipients = {'46123123123'}
create.body = 'Hello, world!'

try:
    batch = client.create_batch(create)
except (requests.exceptions.RequestException,
    clx.xms.exceptions.ApiException) as ex:
    print('Failed to communicate with XMS: %s' % str(ex))


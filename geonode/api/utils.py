
from django.conf import settings

from geonode.layers.models import Layer
from geonode.nsdi.utils import getWorkingGroupAdmins
from tasks import send_task_email


def sendMailToCommitteeMembers(resource_id, resource_type ):
    working_group_admins = getWorkingGroupAdmins()

    if resource_type == 'layer':
        layer = Layer.objects.get(id=resource_id)
        resource_link = settings.SITEURL + "layers/" + layer.typename + "/preview"
    elif resource_type == 'map':
        resource_link = settings.SITEURL + "maps/" + str(resource_id) + "/preview"
    elif resource_type == 'document':
        resource_link = settings.SITEURL + "documents/" + str(resource_id) + "/preview"

    # Send email
    subject = 'Approve or deny ' + resource_type
    from_email = settings.EMAIL_FROM
    recipient_list = [user.email for user in working_group_admins]  # str(request.user.email)
    f = open("geonode/templates/layer_map_doc_approve_mail_template.html", "r")
    html_message = f.read()
    f.close()
    html_message = html_message.format(resource_type, resource_type, resource_link)
    print html_message
    send_task_email.delay(subject, html_message, from_email, recipient_list)
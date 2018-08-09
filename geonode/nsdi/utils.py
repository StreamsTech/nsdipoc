from geonode.people.models import Profile
from geonode.groups.models import GroupProfile
from guardian.shortcuts import get_anonymous_user


def getWorkingGroupAdmins():
    """
    retuns all the members of working group say committee members
    :return:
    """
    working_group = GroupProfile.objects.get(slug='working-group')
    working_group_members = working_group.get_members().filter(is_active=True, is_working_group_admin=True)
    return working_group_members


def get_organization(user):
    """
    Returns user organization of which
    the user is a member or manager
    :return:
    """
    if user.is_authenticated() and not user.is_superuser:
        organization_set =  GroupProfile.objects.filter(groupmember__user=user).exclude(slug='working-group')
        if len(organization_set) > 0:
            return organization_set[0]
        else:
            return None
    else:
        return None
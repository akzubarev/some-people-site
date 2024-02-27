def in_team(target_user, request_user):
    children = request_user.linear_refer.get_childs(include_self=True)
    return target_user is not None and target_user.linear_refer in children

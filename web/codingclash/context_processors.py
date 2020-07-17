def base_template_name_context_processor(request):
    # Use request.user.is_authenticated() if using Django < 2.0
    if request.user.is_authenticated:
        if request.user.team == None:
            base_template_name = 'logged.html'
        else:
            base_template_name = 'logged_with_team.html'
    else:
        base_template_name = 'base.html'

    return {'base_template_name': base_template_name}

def context_var(request):
    # Use request.user.is_authenticated() if using Django < 2.0
    if request.user.is_authenticated:
        uname = request.user.username
    else:
        uname = "NONE"

    try:
        return {'thing': uname, 'secret_key': request.user.team.secret_key, 'players': str(request.user.team.players)}
    except:
        return {'thing': uname}

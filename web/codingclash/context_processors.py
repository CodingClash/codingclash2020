from django.contrib.auth import get_user_model
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
        try:
            return {'thing': uname, "secret_key": request.user.team.secret, "name": request.user.team.name}
        except:
            return {'thing': uname}
    else:
        uname = "NONE"
        return {'thing': uname}
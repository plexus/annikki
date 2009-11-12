from annikki import model

def remote_user(request):
    name = request.environ['REMOTE_USER']
    return model.meta.Session.query(model.User).filter_by(username=name).first()

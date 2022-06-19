def get_thumbnail(backend, response, user=None, *args, **kwargs):

    if backend.name == 'github':
        url = response.get('avatar_url', None)
        email = response.get('email', None)
        user.profile_image = url
        user.email = email
        user.save()

    # if url:
    #     user.profile_image = url
    #     user.email = email
    #     user.save()
    #     #print(user.thumbnail.url)
def get_thumbnail(backend, response, user=None, *args, **kwargs):
    url = None

    if backend.name == 'github':
        url = response.get('avatar_url', '')


    if url:
        user.profile_image = url
        user.save()
        #print(user.thumbnail.url)
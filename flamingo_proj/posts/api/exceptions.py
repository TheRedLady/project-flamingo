from rest_framework.exceptions import NotFound


class PostNotFoundException(NotFound):
    status_code = 404
    default_detail = 'No post with this id was found.'

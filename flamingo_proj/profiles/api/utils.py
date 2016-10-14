def get_follow_status(user, profile):
    if user.user_id == profile.user_id:
        return False
    return user in profile.followed_by.all()

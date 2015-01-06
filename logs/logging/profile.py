

class ProfileNotFound(Exception):
    pass


class ProfileManager(object):

    def change_profile_pic(self, account, image):
        account.profile_picture = image
        account.save()

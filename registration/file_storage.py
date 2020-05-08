from registration.models import User


def user_photo_storage(user: User, photo):
    user.photo.save(user.username+"/{}".format(photo), photo, save=True)

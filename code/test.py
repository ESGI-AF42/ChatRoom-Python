import user

pouet = user.User("harry", "member")
pouet.save_user()
print(pouet.get_user_nickname())
print(pouet.get_user_status())
pouet.change_status("ban")
print(pouet.get_user_status())

        
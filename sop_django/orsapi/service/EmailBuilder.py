class EmailBuilder:

    @staticmethod
    def sign_up(params):
        msg = ""
        msg += "Welcome to ORS!\n"
        msg += "Your registration was successful.\n\n"
        msg += f"Login ID: {params['loginId']}\n"
        msg += f"Password: {params['password']}\n\n"
        msg += "Log in at: https://www.raystec.com/\n"
        msg += "Please change your password after first login for security.\n"
        return msg

    @staticmethod
    def change_password(params):
        msg = ""
        msg += "Password Changed Successfully\n"
        # msg += f"Hi {params['firstName']} {params['lastName']}, your password has been updated.\n\n"
        # msg += f"Login ID: {params['loginId']}\n"
        # msg += f"New Password: {params['password']}\n"

        msg += f"Hi {params.firstName} {params.lastName}, your password has been updated.\n\n"
        msg += f"Login ID: {params.loginId}\n"
        msg += f"New Password: {params.password}\n"
        return msg

    @staticmethod
    def forget_password(params):
        msg = ""
        msg += "Password Recovery\n"
        msg += f"Hi {params.firstName} {params.lastName}, here are your login details:\n\n"
        msg += f"Login ID: {params.loginId}\n"
        msg += f"Password: {params.password}\n"
        return msg

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# User Rate Throttles
class LoginUserRateThrottle(UserRateThrottle):
    scope = "login_user"

class OtpUserRateThrottle(UserRateThrottle):
    scope = "otp_user"

class UpdateTaskUserRateThrottle(UserRateThrottle):
    scope = "update_task_user"

class UpdateProfileUserRateThrottle(UserRateThrottle):
    scope = "update_profile_user"

# Anonymous Rate Throttles
class LoginAnonRateThrottle(AnonRateThrottle):
    scope = "login_anon"

class OtpAnonRateThrottle(AnonRateThrottle):
    scope = "otp_anon"

class UpdateTaskAnonRateThrottle(AnonRateThrottle):
    scope = "update_task_anon"

class UpdateProfileAnonRateThrottle(AnonRateThrottle):
    scope = "update_profile_anon"

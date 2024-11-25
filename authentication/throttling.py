from rest_framework.throttling import UserRateThrottle

class loginThrottle(UserRateThrottle):
    scope = "1000/hour"

class otpThrottle(UserRateThrottle):
    scope = "20/min"

class updateTaskThrottle(UserRateThrottle):
    scope = "100/hour"

class updateProfileThrottle(UserRateThrottle):
    scope = "100/hour"  
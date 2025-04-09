from django.utils import timezone
from .models import AccessTokens, RefreshTokens
from rest_framework_simplejwt.tokens import RefreshToken

def checkTokenExpiry(token):
    if not AccessTokens.objects.filter(token=token).exists():
        return {"error": "Invalid Token"}
    
    accessTokenObj = AccessTokens.objects.get(token=token)
    updatedTime = accessTokenObj.updated_at
    timeDifference = (timezone.now() - updatedTime).total_seconds() / 60

    if timeDifference > 1:
        return refreshAccessTokens(token, accessTokenObj)
    return {
        "status": "valid", 
        "message": "Token is still valid",
        "existingAccessToken": token
    }

def refreshAccessTokens(token, accessTokenObj):
    if not hasattr(accessTokenObj, 'refreshToken') or not RefreshTokens.objects.filter(id=accessTokenObj.refreshToken.id).exists():
        return {"error": "No valid refresh token associated with this access token"}

    refreshTokenObj = accessTokenObj.refreshToken
    createdTimeOfRefreshToken = refreshTokenObj.created_at
    time_difference_minutes = (timezone.now() - createdTimeOfRefreshToken).total_seconds() / 60

    if time_difference_minutes > 5:
        accessTokenObj.delete()
        refreshTokenObj.delete()
        return {"error": "Refresh token has expired (older than 5 minutes)"}
    
    refreshToken = refreshTokenObj.token
    try:
        refresh = RefreshToken(refreshToken)
        newAccessToken = str(refresh.access_token)

        accessTokenObj.token = newAccessToken
        accessTokenObj.updated_at = timezone.now()
        accessTokenObj.save()

        return {
            "status": "success",
            "message": "Access token refreshed successfully",
            "newAccessToken": newAccessToken
        }
    except Exception as e:
        return {"error": f"Invalid refresh token: {str(e)}"}

def validateAndRefreshTokens(token):
    result = checkTokenExpiry(token)
    if "status" in result and result["status"] == "valid":
        return {"status": "valid", "message": "Token is still valid", "newAccessToken": token}
    elif "error" in result:
        if result["error"] == "Invalid Token":
            return {"status": "failed", "message": "Invalid access token provided", "http_status": 401}
        elif result["error"] == "Refresh token has expired (older than 5 minutes)":
            return {"status": "failed", "message": "Session expired, please log in again", "http_status": 401}
        elif "Invalid refresh token" in result["error"]:
            return {"status": "failed", "message": "Session invalid, please log in again", "http_status": 401}
        else:
            return {"status": "failed", "message": result["error"], "http_status": 401}
    else:
        return {"status": "refreshed", "message": "Token refreshed successfully", "newAccessToken": result["newAccessToken"]}
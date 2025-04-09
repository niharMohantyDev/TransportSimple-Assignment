from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt.tokens import RefreshToken

import json

from .models import User, RefreshTokens, AccessTokens, Question, Answer, InteractionLog
from .tokenHelper import *

# Create your views here.
@csrf_exempt
def register(request):
    try:
        if request.method!="POST":
            raise Exception("Method not supported")
        data = json.loads(request.body)
        username = data.get("username") if data.get("username") else ""
        password = data.get("password") if  data.get("password") else ""

        if username == "" or password == "":
            raise Exception("Please fill complete details")
        else:
            newUser = (User(username=username, password=make_password(password))).save()

            return JsonResponse({
                "Status":"Success",
                "Message":"User Registered Successfully"
            })

    except Exception as ex:
        return JsonResponse({
            "Status":"Failed",
            "Message":str(ex)
        })

@csrf_exempt
def login(request):
    try:
        if request.method!="POST":
            raise Exception("Method not supported")
        data = json.loads(request.body)
        username = data.get("username") if data.get("username") else ""
        password = data.get("password") if  data.get("password") else ""

        if username == "" or password == "":
            raise Exception("Please fill complete details")
        else:
            checkUserExists = (User.objects.filter(username=username)).exists()
            if checkUserExists == True:
                user = User.objects.get(username=username)

                if check_password(password, user.password) == True:
                    refresh = RefreshToken.for_user(user)
                    accessToken = str(refresh.access_token)
                    refreshToken = str(refresh)

                    saveRefreshToken = RefreshTokens.objects.create(
                        token=refreshToken,
                        user=user,
                        created_at=timezone.now()
                    )

                    saveAccessToken = AccessTokens.objects.create(
                        token=accessToken,
                        refreshToken=saveRefreshToken,
                        created_at=timezone.now(),
                        updated_at=timezone.now()
                    )

                    return JsonResponse({
                        "Status":"Success",
                        "Message":"User Logged in",
                        "accessToken":accessToken
                    })
                else:
                    return JsonResponse({
                        "Status":"Failed",
                        "Message":"Incorrect Password"
                    })
                
            else:
                return JsonResponse({
                        "Status":"Failed",
                        "Message":"Incorrect username supplied"
                    })


    except Exception as ex:
        return JsonResponse({
            "Status":"Failed",
            "Message":str(ex)
        })


@csrf_exempt
def logout(request):
    try:
        if request.method != "POST":
            raise Exception("Method not allowed")

        authHeader = request.headers.get("Authorization")
        if not authHeader or "Bearer " not in authHeader:
            raise Exception("Authorization header missing or malformed")
        
        accessToken = authHeader.split()[1]
        tokenResult = validateAndRefreshTokens(accessToken)

        if tokenResult["status"] == "failed":
            return JsonResponse({
                "Status": "Failed",
                "Message": tokenResult["message"]
            }, status=tokenResult["http_status"])
        
        else:
            data = json.loads(request.body)
            currentAccessToken = AccessTokens.objects.get(token=tokenResult.get("newAccessToken"))
            if data.get("logout") == True:
                refreshToken = currentAccessToken.refreshToken
                currentAccessToken.delete()
                refreshToken.delete()
                return JsonResponse({
                    "Status": "Success",
                    "Message": "Successfully logged out"
                }, status=200)
            elif data.get("logoutFromAllOtherDevices") == True:
                refreshToken = currentAccessToken.refreshToken
                AccessTokens.objects.filter(refreshToken=refreshToken).exclude(token=accessToken).delete()
                RefreshTokens.objects.exclude(id=refreshToken.id).delete()
                return JsonResponse({
                    "Status": "Success",
                    "Message": "Successfully logged out from all other devices and cleared all other tokens",
                    "accessToken": tokenResult.get("newAccessToken")
                }, status=200)
        
    except Exception as ex:
        return JsonResponse({
            "Status": "Failed",
            "Message": str(ex)
        }, status=400)
    
@csrf_exempt
def postQuestions(request):
    try:
        if request.method != "POST":
            raise Exception("Method not allowed")

        authHeader = request.headers.get("Authorization")
        if not authHeader or "Bearer " not in authHeader:
            raise Exception("Authorization header missing or malformed")
        
        accessToken = authHeader.split()[1]
        tokenResult = validateAndRefreshTokens(accessToken)

        if tokenResult["status"] == "failed":
            return JsonResponse({
                "Status": "Failed",
                "Message": tokenResult["message"]
            }, status=tokenResult["http_status"])

        data = json.loads(request.body)
        question = data.get("question", "")
        if not question:
            raise Exception("Question field is required")
        
        saveQuestion = Question.objects.create(question = question, user = ((AccessTokens.objects.get(token = tokenResult.get("newAccessToken", accessToken))).refreshToken).user, isActive =True)

        return JsonResponse({
            "Status": "Success",
            "Message": "Question posted successfully",
            "accessToken": tokenResult.get("newAccessToken", accessToken),
            "questionId": saveQuestion.id
        })

    except Exception as ex:
        return JsonResponse({
            "Status": "Failed",
            "Message": str(ex)
        }, status=400)
    

@csrf_exempt
def postAnswer(request):
    try:
        if request.method != "POST":
            raise Exception("Method not allowed")

        authHeader = request.headers.get("Authorization")
        if not authHeader or "Bearer " not in authHeader:
            raise Exception("Authorization header missing")
        
        accessToken = authHeader.split()[1]
        tokenResult = validateAndRefreshTokens(accessToken)

        if tokenResult["status"] == "failed":
            return JsonResponse({
                "Status": "Failed",
                "Message": tokenResult["message"]
            }, status=tokenResult["http_status"])

        data = json.loads(request.body)
        answer = data.get("answer", "")
        if not answer:
            raise Exception("Answer field is required")

        checkQuestionExists = Question.objects.filter(id=data.get("questionId")).exists()
        if not checkQuestionExists:
            raise Exception("Question does not exist")

        questionObj = Question.objects.get(id=data.get("questionId"))
        currentUser = ((AccessTokens.objects.get(token=tokenResult.get("newAccessToken", accessToken))).refreshToken).user

        if currentUser == questionObj.user:
            raise Exception("You cannot answer your own question")

        saveAnswer = Answer.objects.create(
            answer=answer,
            user=currentUser,
            question=questionObj,
            isActive =True
        )

        return JsonResponse({
            "Status": "Success",
            "Message": "Answer posted successfully",
            "accessToken": tokenResult.get("newAccessToken", accessToken),
            "answerId":saveAnswer.id
        })

    except Exception as ex:
        return JsonResponse({
            "Status": "Failed",
            "Message": str(ex)
        }, status=400)
    
@csrf_exempt
def likesAndDislikes(request):
    try:
        if request.method != "POST":
            raise Exception("Method not allowed")

        authHeader = request.headers.get("Authorization")
        if not authHeader or "Bearer " not in authHeader:
            raise Exception("Authorization header missing")
        
        accessToken = authHeader.split()[1]
        tokenResult = validateAndRefreshTokens(accessToken)

        if tokenResult["status"] == "failed":
            return JsonResponse({
                "Status": "Failed",
                "Message": tokenResult["message"]
            }, status=tokenResult["http_status"])
        
        user = ((AccessTokens.objects.get(token = tokenResult.get("newAccessToken", accessToken))).refreshToken).user
        
        data = json.loads(request.body)
        

        checkAnswerExists = Answer.objects.filter(id=data.get("answerId")).exists()

        if not checkAnswerExists:
            raise Exception("Answer not found")
        
        answerObj = Answer.objects.get(id=data.get("answerId"))
        
        answerObj = Answer.objects.get(id=data.get("answerId"))
        
        if data.get("like") == "True":
            existing_like = InteractionLog.objects.filter(answer=answerObj, user=user, interactionType='like').exists()
            existing_dislike = InteractionLog.objects.filter(answer=answerObj, user=user, interactionType='dislike').exists()
            
            if existing_like:
                return JsonResponse({
                    "Status": "Failed",
                    "Message": "You've already liked this answer",
                    "accessToken":tokenResult.get("newAccessToken", accessToken)
                }, status=400)
            
            if existing_dislike:
                InteractionLog.objects.filter(answer=answerObj, user=user, interactionType='dislike').delete()
            
            InteractionLog.objects.create(answer=answerObj, user=user, interactionType='like')
        else:
            existing_dislike = InteractionLog.objects.filter(answer=answerObj, user=user, interactionType='dislike').exists()
            existing_like = InteractionLog.objects.filter(answer=answerObj, user=user, interactionType='like').exists()
            
            if existing_dislike:
                return JsonResponse({
                    "Status": "Failed",
                    "Message": "You've already disliked this answer",
                    "accessToken":tokenResult.get("newAccessToken", accessToken)
                }, status=400)
            
            if existing_like:
                InteractionLog.objects.filter(answer=answerObj, user=user, interactionType='like').delete()
            
            InteractionLog.objects.create(answer=answerObj, user=user, interactionType='dislike')
        
        likes = InteractionLog.objects.filter(answer=answerObj, interactionType='like').count()
        dislikes = InteractionLog.objects.filter(answer=answerObj, interactionType='dislike').count()
        
        return JsonResponse({
            "Status": "Success",
            "likes": likes,
            "dislikes": dislikes,
            "accessToken":tokenResult.get("newAccessToken", accessToken)
        })        
    except Exception as ex:
        return JsonResponse({
            "Status": "Failed",
            "Message": str(ex)
        }, status=400)
    
@csrf_exempt
def getEveryBodyQuestions(request):
    try:
        if request.method != "GET":
            raise Exception("Method not allowed")

        authHeader = request.headers.get("Authorization")
        if not authHeader or "Bearer " not in authHeader:
            raise Exception("Authorization header missing")
        
        accessToken = authHeader.split()[1]
        tokenResult = validateAndRefreshTokens(accessToken)

        if tokenResult["status"] == "failed":
            return JsonResponse({
                "Status": "Failed",
                "Message": tokenResult["message"]
            }, status=tokenResult["http_status"])
        
        user = ((AccessTokens.objects.get(token = tokenResult.get("newAccessToken", accessToken))).refreshToken).user

        questions = Question.objects.filter(isActive=True).exclude(user=user)

        questions_data = [{
            "id": q.id,
            "question": q.question,
            "username": q.user.username,
            "isActive": q.isActive
        } for q in questions]

        return JsonResponse({
            "Status": "Success",
            "Message": "Questions retrieved successfully",
            "Data": questions_data,
            "accessToken":tokenResult.get("newAccessToken", accessToken)
        }, status=200)

    except Exception as ex:
        return JsonResponse({
            "Status": "Failed",
            "Message": str(ex)
        }, status=400)
    

@csrf_exempt
def getMyQuestions(request):
    try:
        if request.method != "GET":
            raise Exception("Method not allowed")

        authHeader = request.headers.get("Authorization")
        if not authHeader or "Bearer " not in authHeader:
            raise Exception("Authorization header missing")
        
        accessToken = authHeader.split()[1]
        tokenResult = validateAndRefreshTokens(accessToken)

        if tokenResult["status"] == "failed":
            return JsonResponse({
                "Status": "Failed",
                "Message": tokenResult["message"]
            }, status=tokenResult["http_status"])

        user = ((AccessTokens.objects.get(token = tokenResult.get("newAccessToken", accessToken))).refreshToken).user

        questions = Question.objects.filter(user=user, isActive = True)

        questions_data = [{
            "id": q.id,
            "question": q.question,
            "username": q.user.username,
            "isActive": q.isActive
        } for q in questions]

        return JsonResponse({
            "Status": "Success",
            "Message": "Your questions retrieved successfully",
            "Data": questions_data,
            "accessToken":tokenResult.get("newAccessToken", accessToken)
        }, status=200)

    except Exception as ex:
        return JsonResponse({
            "Status": "Failed",
            "Message": str(ex)
        }, status=400)
    
@csrf_exempt
def getAnswersForQuestion(request):
    try:
        if request.method != "POST":
            raise Exception("Method not allowed")

        authHeader = request.headers.get("Authorization")
        if not authHeader or "Bearer " not in authHeader:
            raise Exception("Authorization header missing")
        
        accessToken = authHeader.split()[1]
        tokenResult = validateAndRefreshTokens(accessToken)

        if tokenResult["status"] == "failed":
            return JsonResponse({
                "Status": "Failed",
                "Message": tokenResult["message"]
            }, status=tokenResult["http_status"])

        user = ((AccessTokens.objects.get(token = tokenResult.get("newAccessToken", accessToken))).refreshToken).user

        data = json.loads(request.body)
        question_id = data.get("questionId")
        
        if not question_id:
            raise Exception("questionId is required")

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise Exception("Question not found")

        answers = Answer.objects.filter(question=question, isActive=True)

        answers_data = []
        for a in answers:
            # Get like and dislike counts from InteractionLog
            likes = InteractionLog.objects.filter(answer=a, interactionType='like').count()
            dislikes = InteractionLog.objects.filter(answer=a, interactionType='dislike').count()
            
            answers_data.append({
                "id": a.id,
                "answer": a.answer,
                "username": a.user.username,
                "likes": likes,
                "dislikes": dislikes,
                "isActive": a.isActive
            })

        return JsonResponse({
            "Status": "Success",
            "Message": "Answers retrieved successfully",
            "Data": answers_data,
            "accessToken": tokenResult.get("newAccessToken", accessToken)
        }, status=200)

    except Exception as ex:
        return JsonResponse({
            "Status": "Failed",
            "Message": str(ex)
        }, status=400)

@csrf_exempt
def archiveQuestion(request):
    try:
        if request.method != "POST":
            raise Exception("Method not allowed")

        authHeader = request.headers.get("Authorization")
        if not authHeader or "Bearer " not in authHeader:
            raise Exception("Authorization header missing")
        
        accessToken = authHeader.split()[1]
        tokenResult = validateAndRefreshTokens(accessToken)

        if tokenResult["status"] == "failed":
            return JsonResponse({
                "Status": "Failed",
                "Message": tokenResult["message"]
            }, status=tokenResult["http_status"])

        user = ((AccessTokens.objects.get(token = tokenResult.get("newAccessToken", accessToken))).refreshToken).user

        data = json.loads(request.body)
        question_id = data.get("questionId")
        
        if not question_id:
            raise Exception("questionId is required")

        try:
            question = Question.objects.get(id=question_id, user=user)
        except Question.DoesNotExist:
            raise Exception("Question not found or you don't have permission to archive it")

        question.isActive = False
        question.save()

        return JsonResponse({
            "Status": "Success",
            "Message": "Question archived successfully",
            "Data": {
                "questionId": question.id,
                "isActive": question.isActive
            },
            "accessToken":tokenResult.get("newAccessToken", accessToken)        
            }, status=200)


    except Exception as ex:
        return JsonResponse({
            "Status": "Failed",
            "Message": str(ex)
        }, status=400)
    
@csrf_exempt
def archiveAnswer(request):
    try:
        if request.method != "POST":
            raise Exception("Method not allowed")

        authHeader = request.headers.get("Authorization")
        if not authHeader or "Bearer " not in authHeader:
            raise Exception("Authorization header missing")
        
        accessToken = authHeader.split()[1]
        tokenResult = validateAndRefreshTokens(accessToken)

        if tokenResult["status"] == "failed":
            return JsonResponse({
                "Status": "Failed",
                "Message": tokenResult["message"]
            }, status=tokenResult["http_status"])

        user = ((AccessTokens.objects.get(token = tokenResult.get("newAccessToken", accessToken))).refreshToken).user

        data = json.loads(request.body)
        answer_id = data.get("answerId")
        
        if not answer_id:
            raise Exception("answerId is required")

        try:
            answer = Answer.objects.get(id=answer_id, user=user)
        except Answer.DoesNotExist:
            raise Exception("Answer not found or it doesn't belong to you")

        answer.isActive = False
        answer.save()

        return JsonResponse({
            "Status": "Success",
            "Message": "Your answer archived successfully",
            "Data": {
                "answerId": answer.id,
                "isActive": answer.isActive
            },
            "accessToken":tokenResult.get("newAccessToken", accessToken)   
        }, status=200)

    except Exception as ex:
        return JsonResponse({
            "Status": "Failed",
            "Message": str(ex)
        }, status=400)


@csrf_exempt
def getAnswerLikeDislkeCount(request):
    try:
        question = Question.objects.get(id=(json.loads(request.body)).get("answerId"))
        answers = Answer.objects.filter(question=question)
        totalLikes = sum(answer.likes for answer in answers)
        totalDislikes = sum(answer.dislikes for answer in answers)

        data = {
            'answerId': (json.loads(request.body)).get("answerId"),
            'totalLikes': totalLikes,
            'totalDislikes': totalDislikes
        }

        return JsonResponse(data)
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found'})
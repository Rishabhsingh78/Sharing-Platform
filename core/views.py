from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response    
from .models import *
from .serializer import *
from rest_framework_simplejwt.tokens import RefreshToken



@api_view(['POST'])
def RegisterView(request):
    print('GOOOOGLe',request.data)
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User successfully Register'},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def LoginView(request):
    serializer = LoginSerializer(data= request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        tokens = serializer.validated_data['token']
        return Response({
            'username': user.username,
            'email': user.email,
            'refresh': tokens['refresh'],
            'access': tokens['access']
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def LogoutView(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message':'user successfully Logout'})
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET', 'POST'])
def question_list_create(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions,many = True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = QuestionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(author = request.user)
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    


@api_view(['GET','POST'])
def answer_list_create(request,question_id):
    question = Question.objects.get(id=question_id)
    if request.method == "GET":
        answers = question.answer.all()
        serializer = AnswerSerializer(answers,many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(question=question)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET'])
def AnswerList(request):
    all_answers = Answer.objects.all()
    serializer = AnswerSerializer(all_answers,many = True)
    return Response(serializer.data)

@api_view(['POST'])
def vote_answer(request,answer_id):
    answer = Answer.objects.get(id = answer_id )
    vote_type = request.data.get('vote')

    if vote_type == "UP":
        answer.votes += 1
    elif vote_type == 'DOWN' or answer.votes > 0:
        answer.votes  -= 1

    answer.save()
    return Response({'votes':answer.votes},status=200)

@api_view(['POST'])
def mark_best_answer(request,answer_id):
    answer = Answer.objects.get(id=answer_id)
    answer.votes += 20
    answer.save()

    user_profile = answer.author.userprofile
    user_profile.reputation += 50
    user_profile.save()
    return Response({'message':'Answer marked as best!'},status=200)
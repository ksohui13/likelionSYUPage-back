from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Question
from question.serializers import QuestionSerializer

@api_view(['POST'])
@permission_classes([AllowAny]) # 글쓰기 로그인 없이 가능
def question_create(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def question_list(request):
    question_list = Question.objects.all()
    paginator = PageNumberPagination()

    # 페이지 사이즈를 주면 해당 사이즈로 지정
    # 값이 없으면 기본 사이즈로 설정(기본 페이지 : settings.py안에)
    page_size = request.GET.get('size') 
    if not page_size == None:
        paginator.page_size = page_size

    result = paginator.paginate_queryset(question_list, request)
    serializers = QuestionSerializer(result, many=True)
    return paginator.get_paginated_response(serializers.data)


@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    serializer = QuestionSerializer(question)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 질문 수정 가능
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def question_update(request, pk):
    question = get_object_or_404(Question, pk=pk)
    # instance를 지정해줘야 수정될 때 해당 정보가 먼저 들어간 뒤 수정(안정적이다)
    serializer = QuestionSerializer(instance=question, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 질문 삭제 가능
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.delete()
    return Response(status=status.HTTP_200_OK)
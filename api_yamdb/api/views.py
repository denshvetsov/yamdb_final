from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenViewBase

from catalog.models import Category, Genre, Title
from users.models import User
from reviews.models import Review
from .filters import TitleFilter
from .mixins import ReviewGenreModelMixin
from .permissions import (AdminOnly, IsAdminOrReadOnly,
                          UserAndModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenerateTokenSerializer, GenreSerializer,
                          ReviewSerializer, TitleCreateSerializer,
                          TitleSerializer, UserSerializer,
                          UserSignUpSerializer)
from .utils import check_confirmation_code, make_confirmation_code


class CategoryViewSet(ReviewGenreModelMixin):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class GenreViewSet(ReviewGenreModelMixin):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [SearchFilter]
    search_fields = ['name']
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('id')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (UserAndModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями"""
    serializer_class = CommentsSerializer
    permission_classes = (UserAndModeratorOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, AdminOnly,)
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class APISignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user = User.objects.create(
            username=username, email=email
        )
        confirmation_code = make_confirmation_code()
        user.confirmation_code = confirmation_code
        user.save()
        mail_subject = 'Ваш код подтверждения для получения API токена'
        message = f'Код подтверждения - {confirmation_code}'
        send_mail(mail_subject, message, settings.EMAIL_FROM, (email, ))
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class APIGetToken(TokenViewBase):
    ''' Получение JWT-токена в обмен на username и confirmation code. '''
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GenerateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if check_confirmation_code(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': ['Код не действителен!']},
            status=status.HTTP_400_BAD_REQUEST
        )

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.posts.models import Post, Category
from utils.unittest_helpers import create_user, login_user, dump


class PostListCreateAPITest(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.user = create_user('user01')

        self.category01 = Category.objects.create(
            slug='cat01',
            name="Category 01"
        )
        self.post01 = Post.objects.create(
            author=self.user,
            title="Post 01",
            text="Text of post 01.",
            category=self.category01
        )
        self.post02 = Post.objects.create(
            author=self.user,
            title="Post 02",
            text="Text of post 02."
        )

    def test_list(self):
        login_user(self.c, self.user)

        response = self.c.get('/api/post/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {
                "id": self.post02.id,
                "author": {
                    "id": self.user.id,
                    "name": "John Doe"
                },
                "created_on": response.data[0]['created_on'],
                "title": "Post 02",
                "text": "Text of post 02.",
                "category": None
            },
            {
                "id": self.post01.id,
                "author": {
                    "id": self.user.id,
                    "name": "John Doe"
                },
                "created_on": response.data[1]['created_on'],
                "title": "Post 01",
                "text": "Text of post 01.",
                "category": {
                    "id": self.category01.id,
                    "slug": "cat01",
                    "name": "Category 01"
                }
            }
        ])

    def test_create(self):
        login_user(self.c, self.user)

        response = self.c.post(
            '/api/post/',
            data={
                'title': "Post 03",
                'text': "Text of post 03."
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            "id": response.data['id'],
            "author": {
                "id": self.user.id,
                "name": "John Doe"
            },
            "created_on": response.data['created_on'],
            "title": "Post 03",
            "text": "Text of post 03.",
            "category": None
        })

    def test_create_with_category(self):
        login_user(self.c, self.user)

        response = self.c.post(
            '/api/post/',
            data={
                'title': "Post 03",
                'text': "Text of post 03.",
                'category': {
                    'id': self.category01.id
                }
            },
            format='json'  # <= mandatory if nested JSON is in payload
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['category'], {
            "id": self.category01.id,
            "slug": "cat01",
            "name": "Category 01"
        })

    def test_list_not_authenticated(self):
        response = self.c.get('/api/post/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
            "detail": "Authentication credentials were not provided."
        })


class PostDetailsAPIView(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.user = create_user('user01')

        self.category01 = Category.objects.create(
            slug='cat01',
            name="Category 01"
        )
        self.post01 = Post.objects.create(
            author=self.user,
            title="Post 01",
            text="Text of post 01.",
            category=self.category01
        )

    def test_retrieve(self):
        login_user(self.c, self.user)

        response = self.c.get(
            '/api/post/{post_id}/'.format(
                post_id=self.post01.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": self.post01.id,
            "author": {
                "id": self.user.id,
                "name": "John Doe"
            },
            "created_on": response.data['created_on'],
            "title": "Post 01",
            "text": "Text of post 01.",
            "category": {
                "id": self.category01.id,
                "slug": "cat01",
                "name": "Category 01"
            }
        })

    def test_update(self):
        login_user(self.c, self.user)

        response = self.c.patch(
            '/api/post/{post_id}/'.format(
                post_id=self.post01.id
            ),
            data={
                'title': "Updated title"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated title")

    def test_update_category(self):
        category02 = Category.objects.create(
            slug='cat02',
            name="Category 02"
        )

        login_user(self.c, self.user)

        response = self.c.patch(
            '/api/post/{post_id}/'.format(
                post_id=self.post01.id
            ),
            data={
                'category': {
                    'id': category02.id
                }
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category'], {
            "id": category02.id,
            "slug": "cat02",
            "name": "Category 02"
        })

    def test_update_category_to_none(self):
        login_user(self.c, self.user)

        # ensure that category is set
        self.assertEqual(self.post01.category, self.category01)

        response = self.c.patch(
            '/api/post/{post_id}/'.format(
                post_id=self.post01.id
            ),
            data={
                'category': None
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category'], None)

    def test_delete(self):
        login_user(self.c, self.user)

        response = self.c.delete(
            '/api/post/{post_id}/'.format(
                post_id=self.post01.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.filter(id=self.post01.id).exists(), False)

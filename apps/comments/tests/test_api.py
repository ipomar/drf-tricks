from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.comments.models import Comment
from apps.posts.models import Post
from utils.unittest_helpers import create_user, login_user, dump


class PostCommentListCreateAPITest(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.user = create_user('user01')

        self.post01 = Post.objects.create(
            author=self.user,
            title="Post 01",
            text="Text of post 01."
        )
        self.comment01 = Comment.objects.create(
            post=self.post01,
            author=self.user,
            text="Text of comment 01."
        )
        self.comment02 = Comment.objects.create(
            post=self.post01,
            author=self.user,
            text="Text of comment 02."
        )

    def test_list(self):
        login_user(self.c, self.user)

        response = self.c.get(
            '/api/post/{post_id}/comment/'.format(
                post_id=self.post01.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {
                "id": self.comment01.id,
                "post_id": self.post01.id,
                "author": {
                    "id": self.user.id,
                    "name": "John Doe"
                },
                "created_on": response.data[0]['created_on'],
                "text": "Text of comment 01.",
                "is_banned": False
            },
            {
                "id": self.comment02.id,
                "post_id": self.post01.id,
                "author": {
                    "id": self.user.id,
                    "name": "John Doe"
                },
                "created_on": response.data[1]['created_on'],
                "text": "Text of comment 02.",
                "is_banned": False
            }
        ])

    def test_create(self):
        login_user(self.c, self.user)

        response = self.c.post(
            '/api/post/{post_id}/comment/'.format(
                post_id=self.post01.id
            ),
            data={
                'text': "Text of comment 03."
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            "id": response.data['id'],
            "post_id": self.post01.id,
            "author": {
                "id": self.user.id,
                "name": "John Doe"
            },
            "created_on": response.data['created_on'],
            "text": "Text of comment 03.",
            "is_banned": False
        })

    def test_create_banned(self):
        login_user(self.c, self.user)

        response = self.c.post(
            '/api/post/{post_id}/comment/'.format(
                post_id=self.post01.id
            ),
            data={
                'text': "Text of comment 03.",
                'is_banned': True
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['is_banned'], False)  # not saved!


class CommentDetailsAPITest(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.user = create_user('user01')

        self.post01 = Post.objects.create(
            author=self.user,
            title="Post 01",
            text="Text of post 01."
        )
        self.comment01 = Comment.objects.create(
            post=self.post01,
            author=self.user,
            text="Text of comment 01."
        )

    def test_retrieve(self):
        login_user(self.c, self.user)

        response = self.c.get(
            '/api/comment/{comment_id}/'.format(
                comment_id=self.comment01.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": self.comment01.id,
            "post_id": self.post01.id,
            "author": {
                "id": self.user.id,
                "name": "John Doe"
            },
            "created_on": response.data['created_on'],
            "text": "Text of comment 01.",
            "is_banned": False
        })

    def test_update(self):
        login_user(self.c, self.user)

        response = self.c.patch(
            '/api/comment/{comment_id}/'.format(
                comment_id=self.comment01.id
            ),
            data={
                'text': "Updated text"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], "Updated text")

    def test_update_by_not_author(self):
        other_user = create_user('other')

        login_user(self.c, other_user)

        response = self.c.patch(
            '/api/comment/{comment_id}/'.format(
                comment_id=self.comment01.id
            ),
            data={
                'text': "Updated text"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        login_user(self.c, self.user)

        response = self.c.delete(
            '/api/comment/{comment_id}/'.format(
                comment_id=self.comment01.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.filter(id=self.comment01.id).exists(), False)

    def test_delete_by_not_author(self):
        other_user = create_user('other')

        login_user(self.c, other_user)

        response = self.c.delete(
            '/api/comment/{comment_id}/'.format(
                comment_id=self.comment01.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_by_staff(self):
        staff_user = create_user('other', is_staff=True)

        login_user(self.c, staff_user)

        response = self.c.delete(
            '/api/comment/{comment_id}/'.format(
                comment_id=self.comment01.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.filter(id=self.comment01.id).exists(), False)


class CommentBannedDetailsAPITest(TestCase):

    def setUp(self):
        self.c = APIClient()
        self.user = create_user('user01')
        self.staff_user = create_user('staff01', is_staff=True)

        self.post01 = Post.objects.create(
            author=self.user,
            title="Post 01",
            text="Text of post 01."
        )
        self.comment01 = Comment.objects.create(
            post=self.post01,
            author=self.user,
            text="Text of comment 01."
        )

    def test_retrieve(self):
        login_user(self.c, self.staff_user)

        response = self.c.get(
            '/api/comment/{comment_id}/banned/'.format(
                comment_id=self.comment01.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": self.comment01.id,
            "is_banned": False,
            "banned_on": None,
            "banned_by": None
        })

    def test_update(self):
        login_user(self.c, self.staff_user)

        response = self.c.patch(
            '/api/comment/{comment_id}/banned/'.format(
                comment_id=self.comment01.id
            ),
            data={
                'is_banned': True
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": self.comment01.id,
            "is_banned": True,
            "banned_on": response.data['banned_on'],
            "banned_by": {
                "id": self.staff_user.id,
                "name": "John Doe"
            }
        })

    def test_retrieve_by_not_staff(self):
        login_user(self.c, self.user)

        response = self.c.get(
            '/api/comment/{comment_id}/banned/'.format(
                comment_id=self.comment01.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

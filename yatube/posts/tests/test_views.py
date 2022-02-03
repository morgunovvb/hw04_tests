from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

from yatube.settings import PAGINATOR_CONST

User = get_user_model()


class ViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.group = Group.objects.create(
            title='Test',
            slug='Test',
            description='Test'
        )
        cls.post = Post.objects.create(
            text='Test',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def check_context(self, response):
        self.response = response
        response_id = response.context['page_obj'][0].id
        response_text = response.context['page_obj'][0].text
        response_author = response.context['page_obj'][0].author
        response_group = response.context['page_obj'][0].group
        self.assertEqual(response_id, self.post.id)
        self.assertEqual(response_text, self.post.text)
        self.assertEqual(response_author, self.user)
        self.assertEqual(response_group, self.group)

    def test_index_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.check_context(response)

    def test_group_list_context(self):
        response = self.authorized_client.get(
            reverse('posts:group', kwargs={'slug': self.group.slug})
        )
        self.check_context(response)

    def test_profile_context(self):
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        self.check_context(response)

    def test_post_detail(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.context['posts'].author, self.user)
        self.assertEqual(response.context['posts'].text, self.post.text)

    def test_create_post(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        text_initial = response.context['form'].fields['text'].initial
        group_initial = response.context['form'].fields['group'].initial
        self.assertEqual(group_initial, None)
        self.assertEqual(text_initial, None)

    def test_edit_post(self):
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.id}
        ))
        text_initial = response.context['form'].fields['text'].initial
        group_initial = response.context['form'].fields['group'].initial
        self.assertEqual(group_initial, None)
        self.assertEqual(text_initial, None)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.group = Group.objects.create(
            title='test-title',
            slug='test-slug',
            description='test-description',
        )

    def setUp(self):
        self.a = 13
        for b in range(self.a):
            self.post = Post.objects.create(
                text='Тестовый текст %s' % b,
                author=self.user,
                group=self.group,
            )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_index_contains_ten_records(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), PAGINATOR_CONST)

    def test_second_index_contains_three_records(self):
        response = self.authorized_client.get(
            reverse('posts:index') + '?page=2'
        )
        self.assertEqual(len(
            response.context['page_obj']), (self.a - PAGINATOR_CONST)
        )

    def test_first_group_contains_ten_records(self):
        response = self.authorized_client.get(
            reverse('posts:group', kwargs={'slug': self.group.slug})
        )
        self.assertEqual(len(response.context['page_obj']), PAGINATOR_CONST)

    def test_second_group_contains_three_records(self):
        response = self.authorized_client.get(reverse(
            'posts:group', kwargs={'slug': self.group.slug}
        ) + '?page=2')
        self.assertEqual(len(
            response.context['page_obj']), (self.a - PAGINATOR_CONST)
        )

    def test_first_profile_contains_ten_records(self):
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': self.user}
        ))
        self.assertEqual(len(response.context['page_obj']), PAGINATOR_CONST)

    def test_second_profile_contains_three_records(self):
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': self.user}
        ) + '?page=2')
        self.assertEqual(len(
            response.context['page_obj']), (self.a - PAGINATOR_CONST)
        )

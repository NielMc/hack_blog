from django.test import TestCase
from blog.views import post_list
from blog.views import post_details
from models import Post
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from accounts.models import User


# Create your tests here.
class SimpleTest(TestCase):
    def test_adding_something_simple(self):
        self.assertEqual(1,1)

class PostListTest(TestCase):
    def test_blog_page_resolves(self):
        blog_page = resolve('/')
        self.assertEqual(blog_page.func, post_list)

    def test_blog_page_status_code_is_ok(self):
        blog_page = self.client.get('/')
        self.assertEqual(blog_page.status_code, 200)

    def test_check_content_is_correct(self):
        blog_page = self.client.get('/')
        self.assertTemplateUsed(blog_page, "blogposts.html")
        blog_page_template_output = render_to_response("blogposts.html", {'posts': Post.objects.all()}).content
        self.assertEqual(blog_page.content, blog_page_template_output)

class PostDetailsTest(TestCase):

    fixtures = ['posts','users']
    def test_details_page_resolves(self):
        blogdetail_page = resolve('/blog/1/')
        self.assertEqual(blogdetail_page.func, post_details)

    def test_check_content_is_correct(self):
        blogdetail_page = self.client.get('/blog/1/')
        self.assertTemplateUsed(blogdetail_page, 'postdetail.html')
        thePost = Post.objects.get(id=1)
        blogdetail_page_template_output = render_to_response('postdetail.html', {'post':
                                                                                 thePost}).content
        self.assertEqual(blogdetail_page.content, blogdetail_page_template_output)

class HomePageTest(TestCase):

    def setUp(self):
        super(HomePageTest, self).setUp()
        self.user = User.objects.create(username='testuser@example.com')
        self.user.set_password('letmein')
        self.user.save()
        self.login = self.client.login(username='testuser@example.com',password='letmein')
        self.assertEqual(self.login,True)

    def test_check_content_is_correct(self):
        home_page = self.client.get('/')
        self.assertTemplateUsed(home_page, "blogposts.html")
        home_page_template_output = render_to_response("blogposts.html", {'user':self.user}).content
        self.assertEqual(home_page.content, home_page_template_output)

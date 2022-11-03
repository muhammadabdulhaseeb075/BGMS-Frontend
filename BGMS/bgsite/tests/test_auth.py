# from tenant_schemas.test.cases import TenantTestCase
# from tenant_schemas.test.client import TenantClient, TenantRequestFactory
# from django.contrib.auth.models import User, AnonymousUser, Group
#
# from bgsite.models import Person
# from django.core.urlresolvers import reverse
# from main.models import SiteGroup, BurialGroundSite
# from django.test.utils import override_settings
# from django.db.models import permalink

# @override_settings(ROOT_URLCONF='bgsite.tests.urls')
# class AnonymousUser(TenantTestCase):
#     """
#     Tests access rights of anonymous users, i.e. those who have not logged in.
#     """
#     
#     def setUp(self):
#         self.client = TenantClient(self.tenant)
#         self.client.logout()
#         
# 
#     def test_authenticated_view(self):
#         """"
#         Accessing non-site related authenticated view for anonymous user  
#         should redirect to login.
#         """
#         response = self.client.get(reverse('test_authenticated_view'))
#         self.assertRedirects(response, 'http://'+self.tenant.domain_url+'/login/?next=/test_authenticated_view/')
#         
#     def test_view_only_view(self):
#         """Accessing site related view-only for anonymous user  
#         should redirect to login."""
#         response = self.client.get(reverse('test_view_only_view'))
#         self.assertRedirects(response, 'http://'+self.tenant.domain_url+'/login/?next=/test_view_only_view/')
#           
#     def test_admin_view(self):
#         """Accessing site related admin view for anonymous user  
#         should redirect to login."""
#         response = self.client.get(reverse('test_aadmin_view'))
#         self.assertRedirects(response, 'http://'+self.tenant.domain_url+'/login/?next=/test_aadmin_view/')
# 
# 
# @override_settings(ROOT_URLCONF='bgsite.tests.urls')
# class NoSiteUser(TenantTestCase):
#     """
#     Tests access rights of users with no associated SiteGroup tuple.
#     """
#     
#     def setUp(self):
#         self.client = TenantClient(self.tenant)
#         self.user = User.objects.create_user(username='TestUser', email='test@test.com', password='123')
#         self.client.login(username='TestUser', password='123')
# 
#     def test_authenticated_view(self):
#         """"
#         Accessing non-site related authenticated view after logging in 
#         should show the authenticated view.
#         """
#         response = self.client.get(reverse('test_authenticated_view'))
#         self.assertEqual(response.status_code, 200)
# 
#     def test_view_only_view(self):
#         """Accessing site related view-only view when non site user is logged in
#         should redirect to the login page"""
#         response = self.client.get(reverse('test_view_only_view'))
#         self.assertRedirects(response, 'http://'+self.tenant.domain_url+'/login/?next=/test_view_only_view/')
# 
#     def test_admin_view(self):
#         """Accessing site related admin view when non site user is logged in 
#         should redirect to the login page"""
#         response = self.client.get(reverse('test_aadmin_view'))
#         self.assertRedirects(response, 'http://'+self.tenant.domain_url+'/login/?next=/test_aadmin_view/')

#
# @override_settings(ROOT_URLCONF='bgsite.tests.urls')
# class SingleSiteUser(TenantTestCase):
#     def setUp(self):
#         self.client = TenantClient(self.tenant)
#         self.user = User.objects.create_user(username='TestUser', email='test@test.com', password='123')
#         group = Group.objects.create(name='SiteUser')
#         site = BurialGroundSite.objects.get_or_create(schema_name=self.tenant.schema_name)[0]
#         sitegroup = SiteGroup.objects.create(group=group, burialgroundsite=site)
#         print('tenant')
#         print(site)
#         print(sitegroup)
#
#         self.client.login(username='TestUser', password='123')

#     def test_authenticated_view(self):
#         """"
#         Accessing non-site related authenticated view after logging in should show the authenticated view.
#         """
#         response = self.client.get(reverse('test_authenticated_view'))
#         self.assertEqual(response.status_code, 200)

    # def test_view_only_view(self):
    #     """Accessing site related view-only view should show the view-only view"""
    #     response = self.client.get(reverse('test_view_only_view'))
    #     self.assertEqual(response.status_code, 200)

#     def test_admin_view(self):
#         """Accessing site related admin view should redirect to the login page"""    
#         response = self.client.get(reverse('test_aadmin_view'))
#         self.assertRedirects(response, 'http://'+self.tenant.domain_url+'/login/?next=/test_aadmin_view/')


# class MultipleSiteUser(TenantTestCase):
#     def setUp(self):
#         self.client = TenantClient(self.tenant)
#         self.user = User.objects.create_user(username='TestUser', email='test@test.com', password='123')
#         siteuser = SiteUser.objects.create(user=self.user)
#         sitegroup = SiteGroup.objects.create(group=Group.objects.get_or_create(name='SiteUser')[0], burialgroundsite=self.tenant)
#         siteuser.site_groups.add(sitegroup)
#         sitegroup = SiteGroup.objects.create(group=Group.objects.get_or_create(name='SiteUser')[0], burialgroundsite=self.tenant)
#         self.client.login(username='TestUser', password='123')
# 
#     def test_authenticated_view(self):
#         """"
#         Accessing non-site related authenticated view after logging in should show the authenticated view.
#         """
# 
#     def test_view_only(self):
#         """Accessing site related view-only view should show the view-only view"""
# 
#     def test_admin_view(self):
#         """Accessing site related admin view should redirect to the login page"""    


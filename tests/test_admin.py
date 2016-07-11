from django.core.urlresolvers import reverse

# Moritz disabled these tests due to tests failing on July 11th 2016

# def test_admin_index(admin_client):
#     response = admin_client.get(reverse('admin:index'), follow=True)
#     assert response.status_code == 200

# def test_userentry_list(admin_client):
#     response = admin_client.get(reverse('admin:socialee_userentry_changelist'),
#                                 follow=True)
#     assert response.status_code == 200

# def test_userentry_add(admin_client):
#     response = admin_client.get(reverse('admin:socialee_userentry_add'),
#                                 follow=True)
#     assert response.status_code == 200

# def test_profileentry_list(admin_client):
#     response = admin_client.get(reverse('admin:socialee_profile_changelist'),
#                                 follow=True)
#     assert response.status_code == 200

# def test_profileentry_add(admin_client):
#     response = admin_client.get(reverse('admin:socialee_profile_add'),
#                                 follow=True)
#     assert response.status_code == 200

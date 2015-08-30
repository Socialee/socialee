from django.core.urlresolvers import reverse


def test_admin_index(admin_client):
    response = admin_client.get(reverse('admin:index'), follow=True)
    assert response.status_code == 200

def test_userentry_list(admin_client, follow=True):
    response = admin_client.get(reverse('admin:socialee_userentry_changelist'))
    assert response.status_code == 200

def test_userentry_add(admin_client, follow=True):
    response = admin_client.get(reverse('admin:socialee_userentry_add'))
    assert response.status_code == 200

def test_profileentry_list(admin_client, follow=True):
    response = admin_client.get(reverse('admin:socialee_profile_changelist'))
    assert response.status_code == 200

def test_profileentry_add(admin_client, follow=True):
    response = admin_client.get(reverse('admin:socialee_profile_add'))
    assert response.status_code == 200

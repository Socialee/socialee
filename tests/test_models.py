import pytest
from allauth.account.models import EmailAddress
from socialee.models import Profile, UserEntry


@pytest.fixture
def user(db):
    user, created = UserEntry.objects.get_or_create(email="test-user@example.com")
    return user

@pytest.fixture
def profile(user):
    profile, created = Profile.objects.get_or_create(user=user)
    return profile


def test_profile_verified(profile):
    "Test the email_verified method, which goes through allauth's EmailAddress model."
    assert not profile.email_verified()

    email = EmailAddress.objects.create(email=profile.user.email, user=profile.user)
    assert not profile.email_verified()

    email.verified = True
    email.save()

    assert profile.email_verified()

import pytest
from allauth.account.models import EmailAddress
from socialee.models import Profile, User


@pytest.fixture
def user(db):
    user, created = User.objects.get_or_create(email="test-user@example.com")
    return user

@pytest.fixture
def profile(user):
    profile, created = Profile.objects.get_or_create(user=user)
    return profile


def test_profile_verified(profile):
    "Test the is_email_verified method, which goes through allauth's EmailAddress model."
    email = EmailAddress.objects.create(email=profile.user.email,
                                        user=profile.user)
    assert not profile.is_email_verified()

    email.verified = True
    email.save()

    assert profile.is_email_verified()

    email.verified = False
    email.save()
    assert not profile.is_email_verified()

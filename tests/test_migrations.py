from django.db import connection
from django.db.migrations.executor import MigrationExecutor
import pytest


@pytest.mark.slow
def test_migrate_profile_to_user(transactional_db):
    "Test that Profile fields get migrated to Users properly."

    executor = MigrationExecutor(connection)
    app = "socialee"
    migrate_from = [(app, "0007_auto_20150521_0215")]
    migrate_to = [(app, "0010_remove_profile_fields")]

    executor.migrate(migrate_from)
    old_apps = executor.loader.project_state(migrate_from).apps
    Profile = old_apps.get_model(app, "Profile")

    # Create an old Profile.
    old_profile = Profile.objects.create(email="email",
                                         firstname="firstname",
                                         lastname="lastname")
    # Migrate forwards.
    executor.loader.build_graph()  # reload.
    executor.migrate(migrate_to)
    new_apps = executor.loader.project_state(migrate_to).apps
    Profile = new_apps.get_model(app, "Profile")
    User = new_apps.get_model(app, "UserEntry")
    assert 'firstname' not in Profile._meta.get_all_field_names()

    user = User.objects.get(email='email')
    profile = Profile.objects.get(user__email='email')
    assert user.profile.pk == old_profile.pk == profile.pk
    assert profile.user.email == 'email'
    assert profile.user.first_name == 'firstname'
    assert profile.user.last_name == 'lastname'

    # Migrate to the end again.
    # executor.loader.build_graph()  # reload.
    # executor.migrate(executor.loader.graph.leaf_nodes(app))

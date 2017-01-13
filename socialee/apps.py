from django.apps import AppConfig

class SocialeeConfig(AppConfig):
    name = 'socialee'
    verbose_name = "Socialee"

    def ready(self):
        from actstream import registry
        registry.register('auth.User')
        registry.register(self.get_model('CommonGround'))
        registry.register(self.get_model('Project'))
        registry.register(self.get_model('Profile'))
        registry.register(self.get_model('Message'))

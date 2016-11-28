from config import settings


# Return TRUE if in Producion
def prod(context):
  return {'PROD': settings.PROD}

# Return TRUE if LIVE (staging and production)
def live(context):
  return {'LIVE': settings.LIVE}
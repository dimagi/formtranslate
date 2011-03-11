from django.conf import settings
import os

_DEFAULT_FORM_TRANSLATE_JAR_LOCATION = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                                                    "lib", "form_translate.jar")

FORM_TRANSLATE_JAR_LOCATION = getattr(settings, "FORM_TRANSLATE_JAR_LOCATION", 
                                      _DEFAULT_FORM_TRANSLATE_JAR_LOCATION)

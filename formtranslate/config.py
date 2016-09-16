import os


def get_form_translate_jar_location():
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "lib",
        '2.0',
        "form_translate.jar"
    )

import os


def get_form_translate_jar_location(version):
    return os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "lib",
        version,
        "form_translate.jar"
    )

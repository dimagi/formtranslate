from collections import namedtuple
import jsonobject


class RichValidatorOutputProblem(jsonobject.JsonObject):
    type = jsonobject.StringProperty(choices=[
        "error", "markup", "invalid-structure", "dangerous", "technical"])
    message = jsonobject.StringProperty()
    xml_location = jsonobject.StringProperty()
    fatal = jsonobject.BooleanProperty()
    model_location = jsonobject.StringProperty()


class RichValidatorOutput(jsonobject.JsonObject):
    validated = jsonobject.BooleanProperty()
    fatal_error = jsonobject.StringProperty()
    fatal_error_expected = jsonobject.BooleanProperty()
    problems = jsonobject.ListProperty(RichValidatorOutputProblem)


ShellResult = namedtuple('ShellResult', 'stdout stderr exit_code')

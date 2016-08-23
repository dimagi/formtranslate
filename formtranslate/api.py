from subprocess import PIPE
from dimagi.utils.subprocess_manager import subprocess_context
from formtranslate import config
import json
from formtranslate.exceptions import FormtranslateStdoutNotJSON
from formtranslate.models import RichValidatorOutput, ShellResult


class FormValidationResult(object):
    def __init__(self, problems, success, fatal_error, message):
        self.problems = problems
        self.success = success
        self.fatal_error = fatal_error
        self.message = message

    def to_json(self):
        return {
            'problems': self.problems,
            'success': self.success,
            'fatal_error': self.fatal_error,
            'message': self.message
        }


def validate(input_data, get_raw=False):
    """Validates an xform into an xsd file"""
    jar_result = form_translate(input_data, "validate")
    if jar_result.stdout:
        try:
            jar_result_json = json.loads(jar_result.stdout)
        except ValueError:
            raise FormtranslateStdoutNotJSON(jar_result.stdout)
        else:
            output = RichValidatorOutput(jar_result_json)
        result = FormValidationResult(
            problems=[problem.to_json() for problem in output.problems],
            success=output.validated,
            fatal_error=output.fatal_error,
            message=jar_result.stdout,
        )
    else:
        result = FormValidationResult(
            problems=[],
            success=False,
            fatal_error='',
            message=jar_result.stdout,
        )

    if get_raw:
        return {
            'success': result.success,
            'errstring': result.message,
            'outstring': result.message,
        }
    else:
        return result


def get_xsd_schema(input_data, get_raw=True):
    """Translates an xform into an xsd file"""
    return form_translate(input_data, "schema")


def readable_form(input_data, get_raw=True):
    """Gets a readable display of an xform"""
    return form_translate(input_data, "summary")


def csv_dump(input_data, get_raw=True):
    """Get the csv translation file from an xform"""
    return form_translate(input_data, "csvdump")


def form_translate(input_data, operation):
    """
    Utility for interacting with the form_translate jar,
    which provides functionality for a number of different useful form tools:
        - converting a form to an xsd file
        - turning a form into a more readable format
        - generating a list of translations as an exportable .csv file
        - form validation
        - etc.

    does this by calling
       java -jar form_translate.jar $operation < form.xml > output

    """
    with subprocess_context() as subprocess:
        location = config.get_form_translate_jar_location()

        p = subprocess.Popen(['java', '-Xmx128m', '-jar', location, operation], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(input_data)
        exit_code = p.wait()

        return ShellResult(stdout=stdout.decode('utf-8'), stderr=stderr.decode('utf-8'),
                           exit_code=exit_code)

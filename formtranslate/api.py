from subprocess import PIPE
from dimagi.utils.subprocess_manager import subprocess_context
from formtranslate import config
import json
from formtranslate.models import RichValidatorOutput, ShellResult


class FormValidationResult(object):
    def __init__(self, version, problems, success, fatal_error, message):
        self.version = version
        self.problems = problems
        self.success = success
        self.fatal_error = fatal_error
        self.message = message

    def to_json(self):
        return {
            'version': self.version,
            'problems': self.problems,
            'success': self.success,
            'fatal_error': self.fatal_error,
            'message': self.message
        }


def validate(input_data, version='1.0', get_raw=False):
    """Validates an xform into an xsd file"""
    if version == '1.0':
        jar_result = form_translate(input_data, "schema", version=version)
        success = jar_result.exit_code == 0
        result = FormValidationResult(
            version=version,
            problems=[],
            success=success,
            fatal_error=jar_result.stderr,
            message='' if success else jar_result.stderr
        )
    elif version == '2.0':
        jar_result = form_translate(input_data, "validate", version=version)
        if jar_result.stdout:
            output = RichValidatorOutput(json.loads(jar_result.stdout))
            result = FormValidationResult(
                version=version,
                problems=[problem.to_json() for problem in output.problems],
                success=output.validated,
                fatal_error=output.fatal_error,
                message=jar_result.stdout,
            )
        else:
            result = FormValidationResult(
                version=version,
                problems=[],
                success=False,
                fatal_error='',
                message=jar_result.stdout,
            )
    else:
        raise ValueError('version must be either "1.0" or "2.0"')

    if get_raw:
        return {
            'success': result.success,
            'errstring': result.message,
            'outstring': result.message,
        }
    else:
        return result


def get_xsd_schema(input_data, version='1.0', get_raw=True):
    """Translates an xform into an xsd file"""
    return form_translate(input_data, "schema", version=version)


def readable_form(input_data, version='1.0', get_raw=True):
    """Gets a readable display of an xform"""
    return form_translate(input_data, "summary", version=version)


def csv_dump(input_data, version='1.0', get_raw=True):
    """Get the csv translation file from an xform"""
    return form_translate(input_data, "csvdump", version=version)


def form_translate(input_data, operation, version='1.0'):
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
        location = config.get_form_translate_jar_location(version)

        p = subprocess.Popen(['java', '-Xmx128m', '-jar', location, operation], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(input_data)
        exit_code = p.wait()

        return ShellResult(stdout=stdout.decode('utf-8'), stderr=stderr.decode('utf-8'),
                           exit_code=exit_code)

import sh
from formtranslate import config
import json


class FormValidationResults(object):
    def __init__(self, version, data):
        self.json = data
        self.version = version
        self.problems = data.get('problems', [])
        if version == "2.0":
            self.success = data.get('validated', False)
            self.fatal_error = data.get('fatal_error', "")
        else:
            self.success = data.get('success', False)
            self.fatal_error = data.get('errstring', "")


def validate(input_data, version='1.0', get_raw=False):
    """Validates an xform into an xsd file"""
    if version == '1.0':
        vals = form_translate(input_data, "schema", version=version)
        vals["outstring"] = ""
        raw_data = vals
    else:
        vals = form_translate(input_data, "validate", version=version)
        raw_data = (json.loads(vals["outstring"])
                    if vals.get("outstring") else {})
        vals["success"] = raw_data.get("validated")
        # hack to display the response json in the formtranslate UI
        vals["errstring"] = vals["outstring"]
    return FormValidationResults(version, raw_data) if not get_raw else vals


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
       java -jar form_translate.jar <operation> < form.xml > output

    """

    location = config.get_form_translate_jar_location(version)
    try:
        result = sh.java('-jar', location, operation, _in=input_data)
        success = True
    except sh.ErrorReturnCode_1 as e:
        result = e
        success = False

    return {
        "success": success,
        "errstring": result.stderr,
        "outstring": result.stdout,
    }

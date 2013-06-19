from contextlib import nested
from dimagi.utils.subprocess_timeout import Subprocess, ProcessTimedOut
from django.conf import settings
from formtranslate import config
from tempfile import NamedTemporaryFile
import os
import json

def validate(input_data, version='1.0', output_only=True):
    """Validates an xform into an xsd file"""
    if version == '1.0':
        # hack
        vals = form_translate(input_data, "schema", version=version)
        vals["outstring"] = ""
    else:
        vals = form_translate(input_data, "validate", version=version)
        json_vals = json.loads(vals["outstring"]) if vals.get("outstring") else {}
        vals["success"] = json_vals["validated"]
        vals["errstring"] = vals["outstring"] # hack to display the response json in the
        if output_only:
            return json_vals
    return vals

def get_xsd_schema(input_data, version='1.0', output_only=False):
    """Translates an xform into an xsd file"""
    return form_translate(input_data, "schema", version=version)

def readable_form(input_data, version='1.0', output_only=False):
    """Gets a readable display of an xform"""
    return form_translate(input_data, "summary", version=version)

def csv_dump(input_data, version='1.0', output_only=False):
    """Get the csv translation file from an xform"""
    return form_translate(input_data, "csvdump", version=version)

# helpers
def open_w():
    return NamedTemporaryFile("w", suffix=".txt", delete=False)

def open_r(file):
    return open(file.name, 'r')

def delete(file):
    try:
        os.unlink(file.name)
    except Exception:
        pass

def form_translate(input_data, operation, version='1.0'):
    """Utility for interacting with the form_translate jar, which provides
       functionality for a number of different useful form tools including
       converting a form to an xsd file, turning a form into a more readable
       format, and generating a list of translations as an exportable .csv
       file."""

    # In case you're trying to produce this behavior on the command line for
    # rapid testing, the command that eventually gets called is:
    # java -jar form_translate.jar <operation> < form.xml > output
    #
    # You can pass in a filename or a full string/stream of xml data

    stdout_w = stderr_w = stdin_w = None
    location = config.get_form_translate_jar_location(version)

    try:
        with open_w() as stdin_w:
            stdin_w.write(input_data)

        with nested(open_w(), open_w(), open_r(stdin_w)) as (stdout_w, stderr_w, stdin_r):
            Subprocess(
                ["java","-jar", location, operation],
                shell=False,
                stdin=stdin_r,
                stdout=stdout_w,
                stderr=stderr_w
            ).run(timeout=getattr(settings, 'FORMTRANSLATE_TIMEOUT', 5))

        with open_r(stdout_w) as stdout_r:
            output = stdout_r.read()
        with open_r(stderr_w) as stderr_r:
            error = stderr_r.read()
    finally:
        for file in (stdout_w, stderr_w, stdin_w):
            delete(file)
    # just check if 'exception' is in the error output to know whether it failed
    success = "exception" not in error.lower()
    return {
        "success": success,
        "errstring": error,
        "outstring": output
    }

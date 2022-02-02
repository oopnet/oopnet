from re import compile

from oopnet.report.simulation_errors import get_error_list, EPANETSimulationError


class ErrorManager:
    """Class for managing errors encountered while simulating a hydraulic model.

    This class checks the EPANET report file for errors, stores these errors (and if available the error details) and
    then raises an EPANETSimulationError that contains all the encountered errors.

    Attributes:
        found_errors: list of errors found in the report file
        _error_exp: regular expression used for finding errors
        _error_list: list of possible errors that might be found in a report file as tuples where the first item is the
        exception, the second one the general error message and an optional third item stores the error details.

    """
    def __init__(self):
        self.found_errors = []
        self._error_exp = compile(r'\d{3}: ')
        self._error_list = get_error_list()

    def check_line(self, text_line: str) -> bool:
        """Checks a single line of text for error codes.

        If an error is encountered, it is added to the found_errors list together with the error message.

        Args:
            text_line: text line to be checked

        Returns:
            Returns False if no errors were encountered and True if otherwise.

        """
        text_line = text_line.replace('\n', '')
        matches = self._error_exp.search(text_line)
        if matches:
            raised_code = matches.group()
            raised_code_int = int(matches.group().replace(': ', ''))
            error_text = text_line.split(raised_code)[1]
            for error in self._error_list:
                if raised_code_int == error.code:
                    self.found_errors.append([error, error_text, None])
                    return True
        return False

    def append_error_details(self, text_line: str):
        """Appends the details of an error to the already found error.

        EPANET report files use either one or two lines of text for errors. The first one contains the error code and a
        general error message, while the following line contains a detailed error description. This function adds this
        second line of text to the corresponding error.

        """
        text_line = text_line.replace('\n', '').strip()
        err = self.found_errors[-1]
        err[2] = text_line

    def raise_errors(self):
        """Raises an EPANETSimulationError if any errors were encountered while simulating the model."""
        if self.found_errors:
            raise EPANETSimulationError([err(msg, details) for err, msg, details in self.found_errors])

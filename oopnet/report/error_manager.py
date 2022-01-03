from re import compile

from oopnet.report.simulation_errors import get_error_list, EPANETSimulationError


class ErrorManager:
    def __init__(self):
        self.error_exp = compile(r'\d{3}: ')
        self._error_list = get_error_list()
        self.found_errors = []

    def check_line(self, text_line) -> bool:
        text_line = text_line.replace('\n', '')
        matches = self.error_exp.search(text_line)
        if matches:
            raised_code = matches.group()
            raised_code_int = int(matches.group().replace(': ', ''))
            error_text = text_line.split(raised_code)[1]
            for error in self._error_list:
                if raised_code_int == error.code:
                    self.found_errors.append(error(error_text))
                    return True
        return False

    def append_error_message(self, text_line):
        text_line = text_line.replace('\n', '').strip()
        err = self.found_errors[-1]
        err.description = text_line

    def raise_errors(self):
        if self.found_errors:
            raise EPANETSimulationError(self.found_errors)

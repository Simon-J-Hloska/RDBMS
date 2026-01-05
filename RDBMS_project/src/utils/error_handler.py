import traceback


class ErrorHandler:
    @staticmethod
    def handle_exception(exception, context=""):
        """
        :param exception: Exception object
        :param context: Context description
        :return: Formatted error message
        """
        error_message = f"Chyba"
        if context:
            error_message += f" ({context})"
        error_message += f": {str(exception)}"
        return error_message

    @staticmethod
    def log_exception(exception, context=""):
        """
        :param exception: Exception object
        :param context: Context description
        :return: None
        """
        print(f"\n{'=' * 60}")
        print(f"CHYBA: {context}")
        print(f"Typ: {type(exception).__name__}")
        print(f"Zpráva: {str(exception)}")
        print(f"{'=' * 60}\n")
        traceback.print_exc()

    @staticmethod
    def validate_and_raise(condition, message):
        """
        :param condition: Condition to check
        :param message: Error message
        :return: None
        """
        if not condition:
            raise ValueError(message)


class UserInterface:
    @staticmethod
    def clear_screen():
        """
        :return: None
        """
        #os.system('cls')
        print("\n" * 100)

    @staticmethod
    def print_header(title):
        """
        :param title: Header title
        :return: None
        """
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60 + "\n")

    @staticmethod
    def print_success(message):
        """
        :param message: Success message
        :return: None
        """
        print(f"\n{message}\n")

    @staticmethod
    def print_error(message):
        """
        :param message: Error message
        :return: None
        """
        print(f"\nCHYBA: {message}\n")

    @staticmethod
    def print_info(message):
        """
        :param message: Info message
        :return: None
        """
        print(f"{message}")

    @staticmethod
    def get_input(prompt):
        """
        :param prompt: Input prompt
        :return: User input as string
        """
        return input(f"{prompt}: \n\n")

    @staticmethod
    def get_number_input(prompt):
        """
        :param prompt: Input prompt
        :return: User input as number or None
        """
        try:
            return float(UserInterface.get_input(prompt))
        except ValueError:
            return None

    @staticmethod
    def get_integer_input(prompt):
        """
        :param prompt: Input prompt
        :return: User input as integer or None
        """
        try:
            return int(UserInterface.get_input(prompt))
        except ValueError:
            return None

    @staticmethod
    def confirm(prompt):
        """
        :param prompt: Confirmation prompt
        :return: True if confirmed, False otherwise
        """
        response = input(f"{prompt} (a/n): ").lower()
        return response == 'a'

    @staticmethod
    def pause():
        """
        :return: None
        """
        input("\nStiskněte Enter pro pokračování...")

    @staticmethod
    def print_table(headers, rows):
        """
        :param headers: List of column headers
        :param rows: List of row data
        :return: None
        """
        col_widths = [max(len(str(header)), max(len(str(row[i])) for row in rows)) if rows else len(str(header))
                      for i, header in enumerate(headers)]

        header_row = " | ".join(str(headers[i]).ljust(col_widths[i]) for i in range(len(headers)))
        separator = "-+-".join("-" * width for width in col_widths)

        print(header_row)
        print(separator)

        for row in rows:
            print(" | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))))


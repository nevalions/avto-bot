from email_validator import validate_email, EmailNotValidError


class Check:

    @staticmethod
    def email_is_valid(mail: str):
        m = mail.strip()
        if m != validate_email(m).email:
            raise EmailNotValidError()


def email_is_valid(mail: str):
    m = mail.strip()
    if m != validate_email(m).email:
        raise EmailNotValidError()

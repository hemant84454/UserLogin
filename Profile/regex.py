from django.core.validators import RegexValidator

mess = """
#   must contains one digit from 0-9
#   must contains one lowercase characters
 #   must contains one uppercase characters
 #   must contains one special symbols in the list "@#$%"
 #        length at least 6 characters and maximum of 20	

"""

name_reg = RegexValidator(regex="^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$", message="Invalid Name" )
email_reg = RegexValidator(regex="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$", message="Invalid Email address")
password_reg = RegexValidator(regex="((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{6,20})", message=mess)
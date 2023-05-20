from app.libraries.sendgrid.functions import Sends
class Emails:

    # ITEMS == { EMAIL, SUBJECT, HTML(TEMPLATE) }
    class Users:
        
        def just_register(items):
            try:
                Sends.common_no_reply(items)
            except Exception as e:
                return e    

        def recover(items):
            try:
                Sends.common_no_reply(items)
            except Exception as e:
                return e    
        
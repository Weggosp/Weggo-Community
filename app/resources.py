from config.db.connection import weggo as ws

class functions:

    def create_key_v2(self):
        import string
        import secrets
        alphabet = string.ascii_letters + string.digits
        alphanumber = ''.join(secrets.choice(alphabet) for i in range(16))

        return '{}{}'.format(self,alphanumber)

    def generate_user_or_company_id(type):
        # Will be used to USER and COMPANY id
        # User or Company ID starts in number 1
        if type == 'user':
            try:
                user = ws.db.users.find().sort("_id", -1).limit(1)
                for i in user:
                    id = int(i['user_id'])+1
                    return id
                else:
                    id = 0
                    return id
            except Exception as e:
                return e
        elif type == 'professional' or type == 'company':
            try:
                business_id = ws.db.business.find().sort("_id", -1).limit(1)
                for i in business_id:
                    id = int(i['business_id'])+1
                return id
            except:
                id = 0
                return id
        else:
            return None
        
    def last_forum():
        for i in ws.db.forums.find().sort("show", -1).limit(1):
            if i['show'] or 'show' in i:
                id = int(i['show'])+1
                return id
            else:
                id = 0
                return id
        
    def generate_ascending_id():
        b = ws.db.bookings.find().sort("_id", -1).limit(1)
        if int(b['booking_id']):
            for i in b:
                id = int(i['booking_id'])+1
                return id
        else:
            id = 0
            return id


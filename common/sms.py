import ghasedak


def send_sms(phone_number, token):
    sms = ghasedak.Ghasedak("dbbd830e7fc7c29bc17223c22ef6d3eefea6cf55018ee9ff66f2fb15c21a91cc")
    sms.send({'message': token, 'receptor': phone_number, 'linenumber': "10008566"})

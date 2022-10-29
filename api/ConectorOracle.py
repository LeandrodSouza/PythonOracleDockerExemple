import cx_Oracle


def show_error(exception):
    error = exception.args
    return " Error message = %s\n" + error.message


def connection():
    p_IP = ''
    p_PORT = ''
    p_SID = ''
    p_USER = ''
    p_PASS = ''
    try:
     p_DNS = cx_Oracle.makedsn(p_IP, p_PORT, sid=p_SID)
     cx_Oracle.connect(user=p_USER, password=p_PASS, dsn=p_DNS)
     result = 'Connetion ok 🔥'
    except cx_Oracle.DatabaseError as e:
     code, mesg = e.args[0].message[:-1].split(': ', 1)
     result = '🛠️' + code + ' | ' + mesg
    return result

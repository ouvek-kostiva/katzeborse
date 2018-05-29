def existUser(userid):
    import sqlite3
    conn = sqlite3.connect("db/Users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM account WHERE userid=?", (userid,))
    data=c.fetchone()
    conn.close()
    if data is None:
        return False
    else:
        return True
        
def insertUser(userid):
    from datetime import datetime
    import sqlite3
    conn = sqlite3.connect("db/Users.db")
    c = conn.cursor()
    gdpr = "!gdpr ok "+str(datetime.now())
    check = datetime.now().strftime("%Y-%m-%d")
    conn.execute("INSERT INTO account (userid, balance, gdpr, checkin) VALUES (?,?,?,?)",(userid, 10000, gdpr,check))
    conn.commit()
    conn.close()
    return "New User: <@"+userid+"> added to database, GDPR:"+gdpr
    
def updateUserGDPR(userid):
    from datetime import datetime
    import sqlite3
    conn = sqlite3.connect("db/Users.db")
    c = conn.cursor()
    gdprmsg = "!gdpr ok "+str(datetime.now())
    c.execute("UPDATE account SET gdpr=? WHERE userid=?",(gdprmsg, userid))
    conn.commit()
    data=c.fetchone()
    conn.close()
    return "New User: <@"+userid+"> added to database, GDPR:"+gdprmsg
    
def deleteUser(userid):
    import sqlite3
    conn = sqlite3.connect("db/Users.db")
    c = conn.cursor()
    c.execute("delete from account where userid=?", (userid,))
    conn.commit()
    conn.close()
    return "資料已刪除"
    
def getUser(userid):
    import sqlite3
    conn = sqlite3.connect("db/Users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM account WHERE userid=?", (userid,))
    data=c.fetchone()
    conn.close()
    if data is None:
        userid = ""
        balance = 0
        checkin = ""
        gdpr = ""
        return False, userid, balance, checkin, gdpr
    else:
        userid = data[0]
        balance = data[1]
        checkin = data[2]
        gdpr = data[3]
        return True, userid, balance, checkin, gdpr
        
def updateUserBal(userid,balance):
    import sqlite3
    conn = sqlite3.connect("db/Users.db")
    c = conn.cursor()
    c.execute("UPDATE account SET balance=? WHERE userid=?",(balance, userid))
    conn.commit()
    data=c.fetchone()
    conn.close()
    
def checkDaily(checkin):
    from datetime import datetime
    date = datetime.now().strftime("%Y-%m-%d")
    if date != checkin:
        return True
    else:
        return False
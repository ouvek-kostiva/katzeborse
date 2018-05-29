from db.account import getUser

def clearOrder(userid):
    import sqlite3
    conn = sqlite3.connect("db/Order.db")
    c = conn.cursor()
    c.execute("delete from orders where userid=?", (userid,))
    conn.commit()
    conn.close()
    return "取消所有委託"

def insertRecord(symbol, price, amount):
    from datetime import datetime
    import sqlite3
    conn = sqlite3.connect("db/Record.db")
    c = conn.cursor()
    time = str(datetime.now())
    conn.execute("INSERT INTO record (symbol, price, amount, time) VALUES (?,?,?,?)",(symbol, price, amount, time))
    conn.commit()
    conn.close()
    return "恭喜成交：代號:"+str(symbol)+" 股數:"+str(amount)+" 價格:"+str(price)
    
def getRecord(symbol):
    import sqlite3
    conn = sqlite3.connect("db/Record.db")
    c = conn.cursor()
    c.execute("SELECT * FROM record WHERE symbol=? ORDER BY time DESC LIMIT 1", (symbol,))
    data=c.fetchone()
    conn.close()
    if data is None:
        symbol = ""
        price = 0
        amount = 0
        time = ""
        return False, symbol, price, amount, time
    else:
        symbol = data[0]
        price = data[1]
        amount = data[2]
        time = data[3]
        return True, symbol, price, amount, time
        
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def checkOrder(userid, order):
    exist, userid, balance, checkin, gdpr = getUser(userid)
    if exist:
        if is_number(str(order[2])) & is_number(str(order[3])):
            bors = str(order[0][1:])
            if chkOrderSelf(userid,order[1],bors):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
        
def chkOrderSelf(userid,symbol,bors):
    import sqlite3
    conn = sqlite3.connect("db/Order.db")
    c = conn.cursor()
    c.execute("SELECT symbol, userid, bors FROM orders WHERE symbol=? AND userid = ?", (symbol,userid))
    data=c.fetchone()
    conn.close()
    if data is None:
        borsck = ""
        return True
    else:
        borsck = data[2]
    if bors == borsck: #相同方向 #沒關係
        return True
    else:
        return False
        
def getAlphaNum():
    import random, string
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    return x

def insertOrder(userid, symbol, bors, Price, amount):
    from datetime import datetime
    import sqlite3
    conn = sqlite3.connect("db/Order.db")
    c = conn.cursor()
    orderid = getAlphaNum()
    timestamp = str(datetime.now())
    conn.execute("INSERT INTO orders (orderid, symbol, userid, bors, Price, amount, timestamp) VALUES (?,?,?,?,?,?,?)",(orderid, symbol, userid, bors, Price, amount, timestamp))
    conn.commit()
    conn.close()
    return"<@"+userid+">新增委託\n買(Buy)或賣(Sell):"+bors+"\n代號:"+symbol+"\n股數:"+amount+"\n價格:"+Price

def updateOrder(orderid,amount):
    from datetime import datetime
    import sqlite3
    conn = sqlite3.connect("db/Order.db")
    c = conn.cursor()
    c.execute("UPDATE orders SET amount=? WHERE orderid=?",(amount, orderid))
    conn.commit()
    data=c.fetchone()
    conn.close()
    
def delOrder(orderid):
    import sqlite3
    conn = sqlite3.connect("db/Order.db")
    c = conn.cursor()
    c.execute("delete from orders where orderid=?", (orderid,))
    conn.commit()
    conn.close()
    
def getBuyer(symbol):
    import sqlite3
    conn = sqlite3.connect("db/Order.db")
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE symbol=? AND bors='Buy' ORDER BY price DESC LIMIT 1", (symbol,))
    data=c.fetchone()
    conn.close()
    if data is None:
        orderid = ""
        symbol = ""
        userid = ""
        bors = ""
        price = 0
        amount = 0
        time = ""
        return False, orderid, symbol, userid, bors, price, amount, time
    else:
        orderid = data[0]
        symbol = data[1]
        userid = data[2]
        bors = data[3]
        price = data[4]
        amount = data[5]
        time = data[6]
        return True, orderid, symbol, userid, bors, price, amount, time
        
def getSeller(symbol):
    import sqlite3
    conn = sqlite3.connect("db/Order.db")
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE symbol=? AND bors='Sell' ORDER BY price ASC LIMIT 1", (symbol,))
    data=c.fetchone()
    conn.close()
    if data is None:
        orderid = ""
        symbol = ""
        userid = ""
        bors = ""
        price = 0
        amount = 0
        time = ""
        return False, orderid, symbol, userid, bors, price, amount, time
    else:
        orderid = data[0]
        symbol = data[1]
        userid = data[2]
        bors = data[3]
        price = data[4]
        amount = data[5]
        time = data[6]
        return True, orderid, symbol, userid, bors, price, amount, time
        
def listOrder(symbol):
    oxS, orderidS, symbolS, useridS, borsS, priceS, amountS, timeS = getSeller(symbol)
    oxB, orderidB, symbolB, useridB, borsB, priceB, amountB, timeB = getBuyer(symbol)
    return oxS, priceS, amountS, oxB, priceB, amountB
    
def listSymbols():
    import sqlite3
    conn = sqlite3.connect("db/Order.db")
    c = conn.cursor()
    c.execute("SELECT symbol, SUM(amount) FROM orders GROUP BY symbol")
    rows=c.fetchall()
    sym = []
    for row in rows:
        sym.append([row[0],row[1]])
    conn.close()
    return sym
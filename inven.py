from order import delOrder, insertRecord, getBuyer, getSeller, updateOrder
from db.account import getUser, updateUserBal

def listInventory(userid):
    import sqlite3
    conn = sqlite3.connect("db/Inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM inventory WHERE userid = ?", (userid,))
    rows = c.fetchall()
    inv = []
    for row in rows:
        inv.append([row[0],row[1],row[2],row[4],row[5]])
    conn.close()
    return inv

def updateInventory(userid, symbol, price, amount, short):
    import sqlite3
    conn = sqlite3.connect("db/Inventory.db")
    c = conn.cursor()
    c.execute("UPDATE inventory SET price=?, amount=? WHERE userid = ? AND symbol LIKE ? AND short LIKE ?",(price, amount, userid, symbol, short))
    conn.commit()
    conn.close()
    
def getInventory(userid, symbol, short):
    import sqlite3
    conn = sqlite3.connect("db/Inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM inventory WHERE userid=? AND symbol LIKE ? AND short LIKE ?", (userid, symbol, short))
    data=c.fetchone()
    conn.close()
    if data is None:
        symbol = ""
        price = 0
        amount = 0
        userid = "" 
        short = ""
        date = ""
        return False, userid, symbol, price, amount, short, date
    else:
        symbol = data[0]
        price = data[1]
        amount = data[2]
        userid = data[3]
        short = data[4]
        date = data[5]
        return True, userid, symbol, price, amount, short, date
    
def insertInventory(userid, symbol, price, amount, short):
    from datetime import datetime
    import sqlite3
    date = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect("db/Inventory.db")
    c = conn.cursor()
    time = str(datetime.now())
    conn.execute("INSERT INTO inventory (userid, symbol, price, amount, short, date) VALUES (?,?,?,?,?,?)",(userid, symbol, price, amount, short, date))
    conn.commit()
    conn.close()

def checkenough(balance,price, amount):
    if balance < price * amount:
        return False
    else:
        return True

def transBuy(symbol, price, amount, userid):
    ixBy, iuseridBy, isymbolBy, ipriceBy, iamountBy, ishortBy, idateBy = getInventory(userid, symbol, "yes")
    ixBn, iuseridBn, isymbolBn, ipriceBn, iamountBn, ishortBn, idateBn = getInventory(userid, symbol, "no")
    ixBm, iuseridBm, isymbolBm, ipriceBm, iamountBm, ishortBm, idateBm = getInventory(userid, symbol, "margin")
    xuB, useridBu, balanceBu, checkinBu, gdprBu = getUser(userid)
    
    short = ""
    print(userid," ",amount," buy1")
    if not ixBy:
        insertInventory(userid, symbol, "0", "0", "yes")
        print(userid," ",amount," buy2")
    if not ixBn:
        insertInventory(userid, symbol, "0", "0", "no")
        print(userid," ",amount," buy3")
    if not ixBm:
        insertInventory(userid, symbol, "0", "0", "margin")
        print(userid," ",amount," buy4")
    if checkenough(balanceBu,price, amount):
        short = "no"
        print(userid," ",amount," buy5")
    else:
        short = "margin"
        print(userid," ",amount," buy6")
    # 沖銷空頭 (開始)
    if iamountBy > 0:
        print(userid," ",amount," buy7")
        if iamountBy > amount: #沖不掉
            print(userid," ",amount," buy8")
            iamountBy = iamountBy - amount
            updateInventory(userid, symbol, price, iamountBy, "yes")
            amount = 0
            if short == "no":#沖不掉 + 足額扣款
                print(userid," ",amount," buy9")
                balanceBu = balanceBu - price * amount
                updateUserBal(userid,balanceBu)
            else: #沖不掉 + 不足融資
                print(userid," ",amount," buy10")
                iamountBm = amount + iamountBm
                updateInventory(userid, symbol, price, iamountBm, "margin")
            amount = 0
        else: #沖得掉
            print(userid," ",amount," buy11")
            amount = amount - iamountBy
            updateInventory(userid, symbol, price, "0", "yes")
            balanceBu = balanceBu - price * iamountBy
            updateUserBal(userid,balanceBu)
            updateInventory(userid, symbol, price, amount, "no")
            if amount > 0:
                if short == "no": #沖得掉 + 足額扣款
                    print(userid," ",amount," buy12")
                    balanceBu = balanceBu - price * amount
                    updateUserBal(userid,balanceBu)
                    updateInventory(userid, symbol, price, amount, "no")
                    amount = 0
                else: #沖不掉 + 不足融資
                    print(userid," ",amount," buy13")
                    iamountBm = amount + iamountBm
                    updateInventory(userid, symbol, price, iamountBm, "margin")
                    amount = 0
    # 沖銷空頭 (完成)
    # 買進
    if amount > 0:
        if short == "no":#現金買進
            print(userid," ",amount," buy14")
            balanceBu = balanceBu - price * amount
            updateUserBal(userid,balanceBu)
            updateInventory(userid, symbol, price, amount, "no")
            amount = 0
        else: #融資買股
            print(userid," ",amount," buy15")
            iamountBm = amount + iamountBm
            updateInventory(userid, symbol, price, iamountBm, "margin")
            amount = 0
    if amount == 0:
        return True
    else:
        print("Buy 未結束:"+str(amount))
        return False
######################################################
def transSell(symbol, price, amount, userid):    
    ixSy, iuseridSy, isymbolSy, ipriceSy, iamountSy, ishortSy, idateSy = getInventory(userid, symbol, "yes")
    ixSn, iuseridSn, isymbolSn, ipriceSn, iamountSn, ishortSn, idateSn = getInventory(userid, symbol, "no")
    ixSm, iuseridSm, isymbolSm, ipriceSm, iamountSm, ishortSm, idateSm = getInventory(userid, symbol, "margin")
    xuS, useridSu, balanceSu, checkinSu, gdprSu = getUser(userid)
    print(userid," ",amount," sell1")
    if not ixSy:
        print(userid," ",amount," sell2")
        insertInventory(userid, symbol, "0", "0", "yes")
    if not ixSn:
        print(userid," ",amount," sell3")
        insertInventory(userid, symbol, "0", "0", "no")
    if not ixSm:
        print(userid," ",amount," sell4")
        insertInventory(userid, symbol, "0", "0", "margin")
    # 沖銷融資
    if iamountSm > 0: #有融資
        print(userid," ",amount," sell5")
        if amount > iamountSm: #會剩下融資
            print(userid," ",amount," sell6")
            iamountSm = iamountSm - amount
            updateInventory(userid, symbol, price, iamountSm, "margin")
            amount = 0
        else: #可以沖銷
            print(userid," ",amount," sell7")
            amount = amount - iamountSm
            updateInventory(userid, symbol, price, "0", "margin")
    # 賣出
    if iamountSn > 0:
        if amount < iamountSn: #賣股票換現
            print(userid," ",amount," sell8")
            iamountSn = iamountSn - amount
            updateInventory(userid, symbol, price, iamountSn, "no")
            income = amount * price
            balanceSu = balanceSu + income
            updateUserBal(userid,balanceSu)
            amount = 0
        else:
            print(userid," ",amount," sell9")
            amount = amount - iamountSn
            updateInventory(userid, symbol, price, "0", "no")
            income = iamountSn * price
            balanceSu = balanceSu + income
            updateUserBal(userid,balanceSu)
    #做空
    if amount > 0:
        print(userid," ",amount," sell10")
        updateInventory(userid, symbol, price, amount, "yes")
        income = amount * price
        balanceSu = balanceSu + income
        updateUserBal(userid,balanceSu)
        amount = 0
    if amount == 0:
        return True
    else:
        print(amount)
        return False
    
def doTrans(symbol, price, amount, useridB, useridS):
    buytra = transBuy(symbol, price, amount, useridB)
    selltra = transSell(symbol, price, amount, useridS)
    if buytra & selltra:
        insertRecord(symbol, price, amount)
        return True
    else:
        return False

def chkTrans(symbol):
    xB, orderidB, symbolB, useridB, borsB, priceB, amountB, timeB = getBuyer(symbol)
    xS, orderidS, symbolS, useridS, borsS, priceS, amountS, timeS = getSeller(symbol)
    transAmount = 0
    transPrice = 0
    transSymbol = symbolB
    if xB & xS:
        if (priceB >= priceS):
            transPrice = priceS
            if amountB >= amountS:
                transAmount = amountS
                amountB = amountB - amountS
                amountS = 0
                updateOrder(orderidB,amountB)
            elif amountB < amountS:
                transAmount = amountB
                amountS = amountS - amountB
                amountB = 0
                updateOrder(orderidS,amountS)
            if amountB == 0:
                delOrder(orderidB)
            if amountS == 0:
                delOrder(orderidS)
            if doTrans(transSymbol, transPrice, transAmount, useridB, useridS):
                chkTrans(symbol)
            else:
                return False
        else:
            return False
    else:
        return False
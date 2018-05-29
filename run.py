import discord
import asyncio
from static import helpmsg, privacymsg, gdprnomsg
from db.account import existUser, insertUser, deleteUser, getUser, updateUserBal, checkDaily
from order import checkOrder, insertOrder, clearOrder, listOrder, listSymbols
from inven import chkTrans, listInventory

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    try:
        userid = message.author.id
        message.content = message.content.lower()
        if message.content.startswith('!test'):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
        elif message.content.startswith('!whoru'):
            usrmsg = message.content.split(" ")[1:]
            await client.send_message(message.channel, "安安 " + " ".join(usrmsg))
        elif message.content.startswith('!help'):
            await client.send_message(message.channel, "<@" + message.author.id + "> 安安你好，\n" + helpmsg())
        elif message.content.startswith('!privacy'):
            await client.send_message(message.channel, privacymsg())
        elif message.content.startswith('!gdpr ok'):
            if existUser(userid):
                await client.send_message(message.channel, "<@" + message.author.id + "> 你已經有帳號了")
            else:
                createmsg = insertUser(userid)
                await client.send_message(message.channel, createmsg + "\n您的帳號已創建成功")
        elif message.content.startswith('!gdpr no'):
            await client.send_message(message.channel, gdprnomsg())
        elif message.content.startswith('!gdpr delete'):
            deletemsg = deleteUser(userid)
            await client.send_message(message.channel, "<@"+userid+">\n" + deletemsg)
        elif message.content.startswith('!acc'):
            exist, useri, balance, checkin, gdpr = getUser(userid)
            if exist:
                if checkDaily(checkin):
                    balance = balance + 1500;
                    updateUserBal(userid,balance)
                    accmsg = "<@"+userid+"> 帳戶情況：\n帳戶餘額 : " + str(balance) + "¢\n你上次簽到時間 : "+str(checkin)
                else:
                    accmsg = "<@"+userid+"> 帳戶情況：\n帳戶餘額 : " + str(balance) + "¢\n你上次簽到時間 : "+str(checkin)
                await client.send_message(message.channel, accmsg)
            else:
                await client.send_message(message.channel, "<@"+userid+"> 你還沒創建帳號\n輸入 [!gdpr ok] 同意條款並創建帳號")
        elif message.content.startswith('!buy'):
            buyorder = message.content.split(" ")
            if checkOrder(userid, buyorder):
                symbol = str(buyorder[1])
                Price = str(buyorder[2])
                amount = str(buyorder[3])
                ordermsg = insertOrder(userid, symbol, "Buy", Price, amount)
                await client.send_message(message.channel, ordermsg)
                chkTrans(symbol)
            else:
                await client.send_message(message.channel, "範例：!buy PREIT 1.0 1000\n必須註冊 [!gdpr ok] 才能使用\n你不能同時有 Buy 和 Sell 單")
        elif message.content.startswith('!sell'):
            sellorder = message.content.split(" ")
            if checkOrder(userid, sellorder):
                symbol = str(sellorder[1])
                Price = str(sellorder[2])
                amount = str(sellorder[3])
                ordermsg = insertOrder(userid, symbol, "Sell", Price, amount)
                await client.send_message(message.channel, ordermsg)
                chkTrans(symbol)
            else:
                await client.send_message(message.channel, "範例：!sell PREIT 1.0 1000\n必須註冊 [!gdpr ok] 才能使用\n你不能同時有 Buy 和 Sell 單")
        elif message.content.startswith('!clear'):
            clearOrderMsg = clearOrder(userid)
            await client.send_message(message.channel, "<@"+userid+"> 已" + clearOrderMsg)
        elif message.content.startswith('!inv'):
            inv = listInventory(userid)
            invmsg = "<@"+userid+"> 庫存：\n[代號,價格,數量,yes(做空)no(持有)margin(融資),資料更新日]\n"
            for i in inv:
                invmsg = invmsg + str(i) + "\n"
            await client.send_message(message.channel, invmsg)
        elif message.content.startswith('!ord'):
            ordmsg = message.content.split(" ")
            if len(ordmsg) > 1:
                symbol = str(ordmsg[1])
                oxS, priceS, amountS, oxB, priceB, amountB = listOrder(symbol)
                ordmsg = "股票代號：" + str(symbol) + "\n買單\n"+"價格："+str(priceB)+"\n數量："+str(amountB)+ "\n\n賣單\n"+"價格："+str(priceS)+"\n數量："+str(amountS)
                await client.send_message(message.channel, ordmsg)
        elif message.content.startswith('!stc'):
            sym = listSymbols()
            symmsg = "股票代號列表：\n[代號,掛單數量]\n"
            for i in sym:
                symmsg = symmsg + str(i) + "\n"
            await client.send_message(message.channel, symmsg)
    except Exception:
        print("Something Wrong Happend")
        

client.run('Token')
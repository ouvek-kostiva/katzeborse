def helpmsg():
    helpMsg = "這是虛擬公爵交易所\n本系統都是虛擬的\n假的，你眼睛業障重\n僅娛樂用途，勿認真\n"
    helpMsg = helpMsg + "\n指令列表：\n"
    helpMsg = helpMsg + "幫助 [!help]\n"
    helpMsg = helpMsg + "隱私權政策及創帳號 [!privacy]\n"
    helpMsg = helpMsg + "查詢帳戶狀況 [!acc]\n"
    helpMsg = helpMsg + "查詢股票庫存 [!inv]\n"
    helpMsg = helpMsg + "股票代號列表 [!stc]\n"
    helpMsg = helpMsg + "清除自己所有掛單列表 [!clear]\n"
    helpMsg = helpMsg + "查詢股票掛單 [!ord 代號]\n"
    helpMsg = helpMsg + "下單買進 [!buy 代號 價格 數量] 範例：!buy PREIT 1.0 1000\n"
    helpMsg = helpMsg + "下單賣出 [!sell 代號 價格 數量] 範例：!sell PREIT 1.0 1000\n"
    return helpMsg
    
def privacymsg():
    privacyMsg = "基本網路系統因安全需要會記錄來往訊息\n會記錄你的使用者代號\n模擬交易資訊\n"
    privacyMsg = privacyMsg + "如果同意條款才會建帳號\n已同意條款後否決條款則可以刪帳號\n"
    privacyMsg = privacyMsg + "同意條款並創建帳號請輸入 [!gdpr ok]\n取得如何刪除資料資訊請輸入 [!gdpr no]"
    return privacyMsg
    
def gdprnomsg():
    gdprnoMsg = "依照 GDPR 所規定，當您提出刪除在我們這邊的資料時，我們就會把你的資料刪掉\n關閉帳戶並刪檔請輸入 [!gdpr delete]"
    return gdprnoMsg
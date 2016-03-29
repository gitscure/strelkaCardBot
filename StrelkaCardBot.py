import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

class BotDialog:
    def __init__(self):
        self.bot_token = "205377807:AAGBPO4fXIFCHDcUtDhLsUyitgJq0r5dhkQ"
        self.getUpdates = "https://api.telegram.org/bot" + self.bot_token + "/getUpdates"
        self.sendMessage = "https://api.telegram.org/bot" + self.bot_token + "/sendMessage"
        self.p_getUpdates = {'limit':'1', 'offset':'-1'}
        self.p_sendMessage = {}
        self.update_id = 0
        self.cards = {}
        self.MsgLoop()

    def MsgLoop(self):
        while True:
            udata = urlencode(self.p_getUpdates).encode()
            req = Request(self.getUpdates, udata)
            resp = urlopen(req).read().decode()
            if len(json.loads(resp).get('result')) == 0:
                pass
            else:
                data = json.loads(resp).get('result')[0]
                if data.get('update_id') > self.update_id:
                    self.update_id = data.get('update_id')
                    self.MsgHandler(data)

    def MsgHandler(self, data):
        if data.get('message').get('text') == '/start':
            self.MsgStart(data.get('message').get('chat').get('id'))
        elif data.get('message').get('text') == '/help':
            self.MsgHelp(data.get('message').get('chat').get('id'))
        elif data.get('message').get('text') == '/list':
            self.MsgList(data.get('message').get('chat').get('id'))
        elif data.get('message').get('text') == '/addcard':
            self.MsgAddCard(data.get('message').get('chat').get('id'))
        elif data.get('message').get('text') == '/delcard':
            self.MsgDelCard(data.get('message').get('chat').get('id'))
        elif data.get('message').get('text') == '/balance':
            self.MsgBalance(data.get('message').get('chat').get('id'))
        else:
            self.p_sendMessage['text'] = "Unavailable command! Type /help for information!"
            self.p_sendMessage['chat_id'] = str(data.get('message').get('chat').get('id'))
            udata = urlencode(self.p_sendMessage).encode()
            req = Request(self.sendMessage, udata)
            resp = urlopen(req)

    def MsgStart(self, chat_id):
        start_str = "Hi! You can view your Strelka Card balance here! Type /help for information."
        self.p_sendMessage['text'] = start_str
        self.p_sendMessage['chat_id'] = str(chat_id)
        udata = urlencode(self.p_sendMessage).encode()
        req = Request(self.sendMessage, udata)
        resp = urlopen(req)

    def MsgHelp(self, chat_id):
        help_str = "Available commands:\n\n/addcard - Add a new Strelka card\n"
        help_str += "/delcard - Delete an existing card\n/list - List of available cards\n"
        help_str += "/balance - Get card balance\n/help - List of available commands"
        self.p_sendMessage['text'] = help_str
        self.p_sendMessage['chat_id'] = str(chat_id)
        udata = urlencode(self.p_sendMessage).encode()
        req = Request(self.sendMessage, udata)
        resp = urlopen(req)

    def MsgList(self, chat_id):
        if chat_id in self.cards:
            list_str = ""
            n = 1
            for num in self.cards[chat_id]:
                list_str += "Card" + str(n) + ": " + num + "\n"
                n += 1
        else:
            list_str = "There are no available cards! Use /addcard to add a new card."
        self.p_sendMessage['text'] = list_str
        self.p_sendMessage['chat_id'] = str(chat_id)
        udata = urlencode(self.p_sendMessage).encode()
        req = Request(self.sendMessage, udata)
        resp = urlopen(req)

    def CheckCardNum(self, card_num):
        if len(card_num) != 11:
            return False
        for i in card_num:
            if not i.isdigit():
                return False
        return True

    def MsgAddCard(self, chat_id):
        self.p_sendMessage['text'] = "Enter card number [xxxxxxxxxxx]:"
        self.p_sendMessage['chat_id'] = str(chat_id)
        udata = urlencode(self.p_sendMessage).encode()
        req = Request(self.sendMessage, udata)
        resp = urlopen(req)
        bNum = False
        while not bNum:
            udata = urlencode(self.p_getUpdates).encode()
            req = Request(self.getUpdates, udata)
            resp = urlopen(req).read().decode()
            data = json.loads(resp).get('result')[0]
            if data.get('update_id') > self.update_id:
                self.update_id = data.get('update_id')
                bNum = True
        if self.CheckCardNum(data.get('message').get('text')):
            if chat_id in self.cards:
                self.cards[chat_id].append(data.get('message').get('text'))
            else:
                self.cards[chat_id] = []
                self.cards[chat_id].append(data.get('message').get('text'))
            self.p_sendMessage['text'] = "Card " + data.get('message').get('text') + " successfully added!"
            self.p_sendMessage['chat_id'] = str(chat_id)
            udata = urlencode(self.p_sendMessage).encode()
            req = Request(self.sendMessage, udata)
            resp = urlopen(req)
        else:
            self.p_sendMessage['text'] = "This doesn't look like card number!"
            self.p_sendMessage['chat_id'] = str(chat_id)
            udata = urlencode(self.p_sendMessage).encode()
            req = Request(self.sendMessage, udata)
            resp = urlopen(req)

    def MsgDelCard(self, chat_id):
        if chat_id in self.cards:
            if len(self.cards[chat_id]) > 1:
                del_text = "[1-" + str(len(self.cards[chat_id]))+']'
            else:
                del_text = '[1]'
            self.p_sendMessage['text'] = "Select card to delete " + del_text + ':'
            self.p_sendMessage['chat_id'] = str(chat_id)
            udata = urlencode(self.p_sendMessage).encode()
            req = Request(self.sendMessage, udata)
            resp = urlopen(req)
            bNum = False
            while not bNum:
                udata = urlencode(self.p_getUpdates).encode()
                req = Request(self.getUpdates, udata)
                resp = urlopen(req).read().decode()
                data = json.loads(resp).get('result')[0]
                if data.get('update_id') > self.update_id:
                    self.update_id = data.get('update_id')
                    bNum = True
            del_text = data.get('message').get('text')
            if del_text.isdigit() and int(del_text) > 0 and int(del_text) <= len(self.cards[chat_id]):
                self.cards[chat_id].pop(int(del_text)-1)
                if len(self.cards[chat_id]) == 0:
                    self.cards.pop(chat_id)
                self.p_sendMessage['text'] = "Successfully deleted!"
                self.p_sendMessage['chat_id'] = str(chat_id)
                udata = urlencode(self.p_sendMessage).encode()
                req = Request(self.sendMessage, udata)
                resp = urlopen(req)
            else:
                self.p_sendMessage['text'] = "Wrong number!"
                self.p_sendMessage['chat_id'] = str(chat_id)
                udata = urlencode(self.p_sendMessage).encode()
                req = Request(self.sendMessage, udata)
                resp = urlopen(req)
        else:
            self.p_sendMessage['text'] = "Nothing to delete!"
            self.p_sendMessage['chat_id'] = str(chat_id)
            udata = urlencode(self.p_sendMessage).encode()
            req = Request(self.sendMessage, udata)
            resp = urlopen(req)

    def GetBalance(self, card_num):
        req_url = "http://strelkacard.ru/api/cards/status/?"
        card_type_id = "3ae427a1-0f17-4524-acb1-a3f50090a8f3"
        try:
            resp = urlopen(req_url + "cardtypeid=" + card_type_id + '&' + "cardnum=" + card_num).read().decode()
        except HTTPError:
            return None
        else:
            return json.loads(resp).get('balance')/100

    def MsgBalance(self, chat_id):
        if chat_id in self.cards:
            if len(self.cards[chat_id]) > 1:
                ncard = "[1-" + str(len(self.cards[chat_id]))+']'
            else:
                ncard = '[1]'
            self.p_sendMessage['text'] = "Select card to get balance " + ncard + ':'
            self.p_sendMessage['chat_id'] = str(chat_id)
            udata = urlencode(self.p_sendMessage).encode()
            req = Request(self.sendMessage, udata)
            resp = urlopen(req)
            bNum = False
            while not bNum:
                udata = urlencode(self.p_getUpdates).encode()
                req = Request(self.getUpdates, udata)
                resp = urlopen(req).read().decode()
                data = json.loads(resp).get('result')[0]
                if data.get('update_id') > self.update_id:
                    self.update_id = data.get('update_id')
                    bNum = True
            ncard = data.get('message').get('text')
            if ncard.isdigit() and int(ncard) > 0 and int(ncard) <= len(self.cards[chat_id]):
                balance_card = self.cards[chat_id][int(ncard)-1]
                if self.GetBalance(balance_card) == None:
                    balance_text = "Can't get information about card '" + balance_card + "'. Wrong number?"
                else:
                    balance_text = "Card '" + balance_card + "' balance is " +\
                                   str(self.GetBalance(balance_card)) + " rub."
                self.p_sendMessage['text'] = balance_text
                self.p_sendMessage['chat_id'] = str(chat_id)
                udata = urlencode(self.p_sendMessage).encode()
                req = Request(self.sendMessage, udata)
                resp = urlopen(req)
            else:
                self.p_sendMessage['text'] = "Wrong number!"
                self.p_sendMessage['chat_id'] = str(chat_id)
                udata = urlencode(self.p_sendMessage).encode()
                req = Request(self.sendMessage, udata)
                resp = urlopen(req)
        else:
            self.p_sendMessage['text'] = "No cards! Use /addcard to add a card first!"
            self.p_sendMessage['chat_id'] = str(chat_id)
            udata = urlencode(self.p_sendMessage).encode()
            req = Request(self.sendMessage, udata)
            resp = urlopen(req)

dlg = BotDialog()
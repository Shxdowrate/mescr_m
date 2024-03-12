#——————————————————————————————————————————————————————————————————
# ███╗   ███╗███████╗ ██████╗ █████╗ ██████╗ ┌───────────────────────────┐
# ████╗ ████║██╔════╝██╔════╝██╔══██╗██╔══██╗ mescr modules             
# ██╔████╔██║█████╗  ╚█████╗ ██║  ╚═╝██████╔╝ not lisensed              
# ██║╚██╔╝██║██╔══╝   ╚═══██╗██║  ██╗██╔══██╗ https://t.me/mescr_m      
# ██║ ╚═╝ ██║███████╗██████╔╝╚█████╔╝██║  ██║└───────────────────────────┘
# ╚═╝     ╚═╝╚══════╝╚═════╝  ╚════╝ ╚═╝  ╚═╝  
#——————————————————————————————————————————————————————————————————
#┌──────────────────────────┐
# meta developer: @mescr_m 
#└──────────────────────────┘
#┌───────────────────────────┐
# idea:             
# thanks:                   
#└───────────────────────────┘
#——————————————————————————————————————————————————————————————————

__version__ = (1, 0, 0)

from .. import loader, utils
import random
import re

class UnlimitedRP(loader.Module):
    '''Модуль с автоматической генерацией RolePlay действий\nDeveloper: @mescr_m'''

    strings = {
        'name': 'UnlimitedRP',
        'max_words_limit': 'Максимальное кол-во слов, чтобы модуль работал',
        'ban_words': 'Если эти слова есть в вашем сообщении, то модуль проигнорирует их',
        'emojies': 'Эмоджи, которые могут появиться в вашем RP действии',
        'form': 'Форма RP. Как будет выглядеть ваше сообщение после обработки модулем.\n{emoji} - случайный эмоджи из списка, {you} - ваш ник, {rp} - текст RP, {user} - ник того, с кем взаимодействуете'
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "max_words_limit", 3,
                lambda: self.strings("max_words_limit"),
                validator=loader.validators.Integer()
            ),
            loader.ConfigValue(
                "ban_words", ['**'],
                lambda: self.strings("ban_words"),
                validator=loader.validators.Series()
            ),
            loader.ConfigValue(
                "emojies", ['😀', '😂', '😊', '🤔', '😍', '🙌',
                            '😎', '🤣', '😘', '👍', '👏', '😉',
                            '😜', '🤪', '😇', '🥳', '🤩', '😛',
                            '😆', '😁', '🥺', '😡', '🤬', '😭',
                            '😱', '😴', '🤯', '🥴', '👻', '👽',
                            '🤡', '👺', '👿', '💀', '👑', '🎩',
                            '👚', '🧥', '👗', '👠', '👑', '🧣',
                            '👢', '🎒', '⛄️', '🌞', '🌈', '🍉',
                            '🍕', '🍔', '🍦', '🍭', '🍩', '🍿',
                            '<emoji document_id=5384232450362719371>⚡</emoji>'],
                lambda: self.strings("emojies"),
                validator=loader.validators.Series()
            ),
            loader.ConfigValue(
                "form", '{emoji} | <b>{you}</b> {rp} <b>{user}</b>',
                lambda: self.strings("form"),
                validator=loader.validators.String()
            ),
        )

    async def client_ready(self):
        id = self.tg_id
        mm = await self.client.get_messages(-1002031293898, 1)
        if str(id) in mm[0].text:
            raise loader.LoadError('К сожалению, вы находитесь в черном списке модулей от @mescr_m.\nСвяжитесь в владельцем канала для возможного решения этой проблемы.')
        self.set('status', False) if self.get('status') == None else None

    @loader.watcher(no_commands = True, out = True)
    async def watcher(self, message):
        # Предварительная настройка
        max_word_limit = self.config['max_words_limit']
        ban_words = self.config['ban_words']
        r = await message.get_reply_message()

        # Если выключено: 1
        if self.get('status') == False:
            return

        # Если нет второго участника RP: 2
        if not r:
            return

        # Подсчет кол-ва слов: 3
        if len(message.raw_text.split(' ')) > max_word_limit:
            return
        
        # Обнаружение запрещенных слов: 4
        for word in ban_words:
            if message.raw_text.count(word) > 0:
                return
        
        # Обнаружение RP слов: 5
        su = ['ать', 'ять', 'уть', 'ють', 'ить', 'ыть', 'еть']
        words = 0
        for word in message.raw_text.split(' '):
            if len(word) < 4:
                continue
            if word[-3:] not in su:
                continue
            words += 1

        # Есть ли RP слова?: 6
        if words == 0:
            return
        
        # Замена: 7
        c_words = []
        for word in message.raw_text.split(' '):
            if word[-3:] == 'ать':
                c_words.append(word.replace('ать', 'ал'))
            elif word[-3:] == 'ять':
                c_words.append(word.replace('ять', 'ял'))
            elif word[-3:] == 'уть':
                c_words.append(word.replace('уть', 'ул'))
            elif word[-3:] == 'ють':
                c_words.append(word.replace('ють', 'ял'))
            elif word[-3:] == 'ить':
                c_words.append(word.replace('ить', 'ил'))
            elif word[-3:] == 'ыть':
                c_words.append(word.replace('ыть', 'ыл'))
            elif word[-3:] == 'еть':
                c_words.append(word.replace('еть', 'ел'))
            else:
                c_words.append(word)

        # {emoji} - случайный эмоджи из списка, {you} - ваш ник, {rp} - текст RP, {user} - ник того, с кем взаимодействуете

        # Вывод: 8
        res = ' '.join(c_words)
        text = self.config['form'].format(emoji = random.choice(self.config['emojies']), you = message.sender.first_name, rp = res, user = r.sender.first_name)
        await message.edit(text)
        return
    
    @loader.command()
    async def unemstatus(self, message):
        '''- включить / отключить модуль'''
        if self.get('status') == False:
            self.set('status', True)
            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> <b>UnlimitedRP</b> включен.')
            return
        else:
            self.set('status', False)
            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> <b>UnlimitedRP</b> отключен.')
            return

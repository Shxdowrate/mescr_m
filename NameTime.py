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

from .. import utils, loader
import asyncio
import datetime
from telethon.tl import functions

__version__ = (1, 0, 1)

class NameTime(loader.Module):
    '''Модуль для времени в нике\nDeveloper: @mescr_m'''

    strings = {
        'name': 'NameTime',
        'timezone': 'Ваш часовой пояс от МСК. Подсказка: Москва = 0, Калининград = -1, Омск = 3, Владивосток = 7',
        'sleep': 'Раз в сколько минут обновлять время в нике? Чем выше показатель, тем ниже вероятность бана аккаунта.',
        'autostart': 'Запускать ли модуль автоматически, при запуске юзербота?'
    }

    async def client_ready(self):
        self.set('status', False) if self.get('status') == None else None
        self.set('fact_status', False) if self.get('fact_status') == None else None
        if self.get('status') == True:
            await self.inline.bot.send_message(self.tg_id, f'❗️ Модуль NameTime был автоматически запущен.')
            await self.nametime_function()
        else:
            self.set('status', False)
            self.set('fact_status', False)
        
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "timezone", 0,
                lambda: self.strings("timezone"),
                validator=loader.validators.Integer()
            ),
            loader.ConfigValue(
                "sleep", 1,
                lambda: self.strings("sleep"),
                validator=loader.validators.Choice([1, 2, 5, 10, 20, 30, 45, 60, 120])
            ),
            loader.ConfigValue(
                "autostart", False,
                lambda: self.strings("autostart"),
                validator=loader.validators.Boolean()
            ),
        )

    @loader.command()
    async def nameformat(self, message):
        '''[ ник + {time} ] - установить формат ника'''
        args = utils.get_args_raw(message)
        if args:
            if '{time}' in args:
                self.set('nick', args)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Формат ника задан: "<code>{args}</code>". Теперь вы можеет включить время в нике или выключить его.')
                return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВ аргументе нет "{time}".'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\n')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргумент.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите правильный аргумент, например, "EarlyStar | {time}". Учтите, что "{time}" не нужно заменять на ваше время, так как это слово служит переменной.')
            return
        
    @loader.command()
    async def namecheck(self, message):
        '''- просмотреть формат никнейма'''
        text = f'<emoji document_id=5334882760735598374>📝</emoji> Ваш формат: <code>{self.get("nick")}</code>' if self.get('nick') != None else '<emoji document_id=5334882760735598374>📝</emoji> Формат ника не установлен.'
        await utils.answer(message, text)
        
    @loader.command()
    async def namestatus(self, message):
        '''- включить / выключить модуль'''
        if self.get('status') == True:
            self.set('status', False)
            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Модуль NameTime выключен.')
            return
        else:
            if self.get('nick') != None:
                if self.get('fact_status') == False:
                    self.set('status', True)
                    await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Модуль NameTime запущен.')
                    await self.nametime_function()
                    return
                else:
                    self.set('status', True)
                    await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Модуль NameTime перезапущен.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не установили формат ника.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажиет формат никнейма, а затем запустите модуль.')
                return
        
    async def nametime_function(self):
        while True:
            await asyncio.sleep(0.5)
            if self.get('status') == True:
                if self.get('nick') != None:
                    self.set('fact_status', True)
                    nick = self.get('nick')
                    current_time = datetime.datetime.now()
                    timezone = self.config['timezone'] 
                    new_time = current_time + datetime.timedelta(hours=timezone)
                    time = new_time.strftime("%H:%M")
                    nick = nick.format(time = time)
                    await self.client(functions.account.UpdateProfileRequest(first_name=nick))
                    await asyncio.sleep(self.config['sleep'] * 60)
                else:
                    await self.inline.bot.send_message(self.tg_id, f'❗️ Модуль NameTime не может работать, тк вы не установили формат ника.')
                    self.set('status', False)
                    self.set('fact_status', False)
                    break
            else:
                self.set('fact_status', False)
                break
                


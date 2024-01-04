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
c = loader.command
import datetime
import asyncio
from telethon.tl import functions

__version__ = (1, 0, 0)

class NameProfiles(loader.Module):
    '''Автоматическая смена ника по времени\nDeveloper: @mescr_m'''

    strings = {
        'name': 'NameProfiles',
        'timezone': 'Ваш часовой пояс',
        'autostart': 'Запускать ли модуль автоматически при запуске юзербота?'
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "timezone", 0,
                lambda: self.strings("timezone"),
                validator=loader.validators.Integer()
            ),
            loader.ConfigValue(
                "autostart", False,
                lambda: self.strings("autostart"),
                validator=loader.validators.Boolean()
            ),
        )

    async def client_ready(self):
        self.set('status', False) if self.get('status') == None else None
        self.set('profiles', []) if self.get('profiles') == None else None
        self.set('fact_status', False) if self.get('fact_status') == None else None
        if self.config['autostart'] == True:
            if self.get('status') == True:
                await self.nameprofiles_function()
                return
        else:
            self.set('status', False)
            self.set('fact_status', False)

    @c()
    async def nameprofileadd(self, message):
        '''[ время в формате {hh:mm} ] [ Ник ] - создать новый профиль для ника'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' in args:
                time = args.split(' ')[0]
                nick = ' '.join(args.split(' ')[1:])
                if len(time) == 5 and time.split(':')[0].isdigit() and time.split(':')[1].isdigit() and int(time.split(':')[0]) >= 0 and int(time.split(':')[0]) <= 23 and int(time.split(':')[1]) >= 0 and int(time.split(':')[1]) <= 59:
                    if time not in self.get('profiles'):
                        self.get('profiles').append(time)
                        self.set(time, nick)
                        await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Профиль "<code>{nick}</code>" создан. Он будет срабатывать в {time}.')
                        return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭто время уже занято.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nИспользуйте другое время для профиля или удалите текущее, а после попробуйте снова.')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНеверный формат времени.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите верный формат времени в первом аргументе. Формат: hh:mm, пример: 01:28')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали только 1 аргумент, хотя нужно 2.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите 2 аргумента.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргументы согласно подсказкам в help.')
            return
        
    @c()
    async def nameprofiledel(self, message):
        '''[ профиль(время) ] - удалить профиль для ника'''
        args = utils.get_args_raw(message)
        if args:
            if len(args) == 5 and args.split(':')[0].isdigit() and args.split(':')[1].isdigit():
                if args in self.get('profiles'):
                    self.get('profiles').remove(args)
                    self.set(args, None)
                    await utils.answer(message, f'Профиль для <code>{args}</code> удален.')
                    return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nПрофиля на это время не существует.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите время, на которое был задан профиль.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНеверный формат времени.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите верный формат времени. Формат: hh:mm, пример: 01:28')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргументы согласно подсказкам в help.')
            return
        
    @c()
    async def nameprofiles(self, message):
        '''- просмотреть профили'''
        if self.get('profiles'):
            times = self.get('profiles')
            text = f'<emoji document_id=5334882760735598374>📝</emoji> Ваши профили ({len(self.get("profiles"))}):\n'
            for time in times:
                nick = self.get(time)
                text += f'\n{time} | {nick}'
            await utils.answer(message, text)
            return
        else:
            await utils.answer(message, f'<emoji document_id=5334882760735598374>📝</emoji> У вас нет профилей.')
            return

    @c()
    async def nameprofilesreset(self, message):
        '''- удалить все профили'''
        for time in self.get('profiles'):
            self.set(time, None)
        self.set('profiles', [])
        await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Все профили удалены.')
        
    @c()
    async def nameprofilesstatus(self, message):
        '''- включить / выключить модуль'''
        if self.get('status') == True:
            self.set('status', False)
            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> NameProfiles отключен.')
            return
        else:
            if self.get('fact_status') == False:
                self.set('status', True)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> NameProfiles запущен.')
                await self.nameprofiles_function()
                return
            else:
                self.set('status', True)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> NameProfiles перезапущен.')
                return
            
    @c()
    async def nameprofilesguide(self, message):
        '''- помощь по модулю'''
        await utils.answer(message, f'<emoji document_id=5452069934089641166>❓</emoji> <b>Как использовать модуль NameProfiles?</b>\n\nНапример, добавим профиль "12:00 MyNick Day", теперь, в 12:00 ваш ник автоматически изменится на "MyNick Day", профили можно устанавливать на любое время с 00:00 до 23:59, до 1440 профилей.')

    async def nameprofiles_function(self):
        while True:
            await asyncio.sleep(0.5)
            if self.get('status') == True:
                self.set('fact_status', True)
                current_time = datetime.datetime.now()
                timezone = self.config['timezone'] 
                new_time = current_time + datetime.timedelta(hours=timezone)
                time = new_time.strftime("%H:%M")
                if self.get(time) != None:
                    await self.client(functions.account.UpdateProfileRequest(first_name=self.get(time)))
                await asyncio.sleep(60)
            else:
                self.set('fact_status', False)
                break
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
# idea: @dziru              
# thanks:                   
#└───────────────────────────┘
#——————————————————————————————————————————————————————————————————

__version__ = (1, 0, 0)

from .. import utils, loader
import asyncio
from asyncio import sleep
import inspect
from ..inline.types import InlineCall

class AutoCommentPlus(loader.Module):
    '''Продвинутый модуль для авто-комментирования постов в каналах.\nDeveloper: @mescr_m'''

    strings = {
        'name': 'AutoCommentPlus',
        'sleep': 'Через сколько секунд комментировать пост?',
        'delay': 'Сколько ждать между отправкой двух комментов в один канал(если есть)?'
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "sleep", 0,
                lambda: self.strings("sleep"),
                validator=loader.validators.Integer()
            ),
            loader.ConfigValue(
                "delay", 3,
                lambda: self.strings("delay"),
                validator=loader.validators.Integer()
            ),
        )

    async def client_ready(self):
        self.set('channels', []) if self.get('channels') == None else None
        self.set('status', False) if self.get('status') == None else None
        self.set('shortnames', []) if self.get('shortnames') == None else None

    @loader.watcher(only_messages=True, only_channels=True)
    async def autocomment(self, message):
        if message.from_id in self.get('channels'):
            if self.get('status') == True:
                shortnames = self.get(f'{message.from_id}')
                await asyncio.sleep(self.config['sleep'])
                for shortname in shortnames:
                    text = self.get(f'{shortname}')
                    chat = utils.get_chat_id(message)
                    await self.client.send_message(entity=chat, message=text, comment_to=message)
                    await asyncio.sleep(self.config['delay'])

    @loader.command()
    async def commentadd(self, message):
        '''<ответ на текст> [ ID канала ] [ Короткое название ] - создать объект комментирования'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' in args:
                if len(args.split(' ')) < 3:
                    cid = args.split(' ')[0]
                    shortname = args.split(' ')[1]
                    try:
                        channel = await self.client.get_entity(int(cid))
                    except Exception:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели неверный ID канала. Он недоступен или не существует вовсе.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите верный ID канала.')
                        return
                    if channel.broadcast == True:
                        reply = await message.get_reply_message()
                        if reply:
                            text = reply.text
                            if shortname not in self.get('shortnames'): # Если короткого названия нет в списке коротких названий
                                if int(cid) not in self.get('channels'): # Если этого ID нет в списке каналов модуля
                                    self.get('channels').append(int(cid)) # Добавляем в список каналов модуля
                                    self.set(f'{cid}', []) # Создаем пустой список под короткие названия
                                self.get(f'{cid}').append(shortname) # Добавляем короткое название в канал
                                self.get('shortnames').append(shortname) # Добавляет короткое название в список коротких названий
                                self.set(f'{shortname}', text) # Присваиваем короткому названию текст для комментирования
                                await utils.answer(message, f'<emoji document_id=5332654441508119011>✅</emoji> <b>Объект комментирования "<code>{shortname}</code>" был создан. Канал:</b> "<code>{channel.title} ({cid})</code>".\n\n<emoji document_id=5819022220348886685>💬</emoji> <b>Текст сообщения:</b>\n<code>{text}</code>')
                                return
                            
                            # Обработа ошибок
                            else:
                                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭто короткое название уже занято.'
                                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nИспользуйте другое короткое название для создания нового объекта.')
                                return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не ответили на сообщение, которое должно быть текстом для комментирования.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nОтветьте на сообщение, текст которого должен стать текстом для комментирования.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВведенный вами ID не пренадлежит каналу.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите ID канала. ')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nБыло указано слишком много аргументов.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите 2 аргумента.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nБыло указано слишком мало аргументов.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите 2 аргумента.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите только 2 аргумента.')
            return
        
    @loader.command()
    async def commentdel(self, message):
        '''[ короткое название ] - удалить объект комментирования'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' not in args:
                if args in self.get('shortnames'):
                    self.get('shortnames').remove(args)
                    for channel in self.get('channels'):
                        if args in self.get(f'{channel}'):
                            self.get(f'{channel}').remove(args)
                        if not self.get(f'{channel}'):
                            self.get('channels').remove(channel)
                    await utils.answer(message, f'<emoji document_id=5332654441508119011>✅</emoji> <b>Объект комментирования "<code>{args}</code>" был удален.</b>')
                    return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭтого объекта комментирования не существует.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите существующий объект комментирования.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали 2 аргумента, хотя короткое название может представлять из себя только одно слово.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите правильный аргумент.')
                return
        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргумент.'
        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который должен представлять из себя короткое название ранее созданного объекта комментирования.')
        return
    
    @loader.command()
    async def commentlist(self, message):
        '''- вывести список объектов комментирования'''
        channels = self.get('channels')
        if channels:
            objects = 0
            channelss = 0
            for channel in channels:
                channelss += 1
                objects += len(self.get(f'{channel}'))
            text = f'<emoji document_id=5280697358839986011>📄</emoji> <b>Список объектов комментирования:\nКаналов: {channelss}, Объектов: {objects}.</b>\n\n\n'
            for channel in channels:
                objects = self.get(f'{channel}')
                text += f'▪️ <b>{channel}</b>: '
                for object in objects:
                    text += f'<i>{object}</i>, '
                text += '\n\n'
            await utils.answer(message, text)
            return
        else:
            await utils.answer(message, '<emoji document_id=5280697358839986011>📄</emoji> <b>Список объектов комментирования пуст.</b>')
            return

    @loader.command()
    async def commentcheck(self, message):
        '''[ короткое название ] - просмотреть текст объекта комментирования'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' not in args:
                if args in self.get('shortnames'):
                    for channel in self.get('channels'):
                        if args in self.get(f'{channel}'):
                            channel_s = channel
                    channel = channel_s
                    shortname = args
                    o_text = self.get(args)
                    await utils.answer(message, f'<emoji document_id=5334675996714999970>🔹</emoji> <b>Объект сообщения</b> "<code>{args}</code>":\n\n▪ <b>Канал:</b> <code>{channel}</code>\n▪ <b>Короткое название:</b> <code>{shortname}</code>\n▪ <b>Текст объекта:</b>\n\n{o_text}')
                    return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nТакого объекта не сущестует.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите существующий объект, вы можете скопировать название в списке объектов.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали пробел в аргументе, хотя короткое название может состоять только из одного слова.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который должен представлять из себя короткое название ранее созданного объекта комментирования.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргумент.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который должен представлять из себя короткое название ранее созданного объекта комментирования.')
            return
        
    @loader.command()
    async def commentstatus(self, message):
        '''- включить/выключить авто-комментирование'''
        if self.get('status') == False:
            self.set('status', True)
            await utils.answer(message, f'<emoji document_id=5332654441508119011>✅</emoji> <b>Авто-комментирование включено.</b>')
            return
        else:
            self.set('status', False)
            await utils.answer(message, f'<emoji document_id=5332654441508119011>✅</emoji> <b>Авто-комментирование отключено.</b>')
            return
        
    @loader.command()
    async def commentreset(self, message):
        '''- удалить все каналы и объекты'''
        await self.inline.form(
            text = '❗️ Вы уверены, что хотите очистить модуль? Это действие будет необратимо.',
            message=message,
            reply_markup=[
                [
                    {
                        "text": "Да.",
                        "callback": self.reset,
                    },
                ],
                [
                    {
                        "text": "Нет.",
                        "action":'close',
                    },
                ],
            ],
        )

    async def reset(self, call: InlineCall):
        for channel in self.get('channels'):
            self.set(f'{channel}', None)
        for shortname in self.get('shortnames'):
            self.set(f'{shortname}', None)
        self.set('channels', [])
        self.set('shortnames', [])
        self.set('status', False)
        await call.answer('❗️ Модуль сброшен.')
        await call.edit(
                text='❗️ Модуль сброшен.'
        )
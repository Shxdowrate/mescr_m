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
import random
import asyncio

__version__ = (1, 1, 0)

class FastNotes(loader.Module): # Класс
    '''Модуль для быстрого полученимя заметок.\nDeveloper: @mescr_m'''

    strings = {
        'name': 'FastNotes',
        'sleep': 'Сколько секунд юзерботу ждать перед повторным изменением сообщения, если было указано более одной заметки?',
    }

    async def client_ready(self): # Настройка БД
        self.set('shortnames', []) if self.get('shortnames') == None else None
        self.set('status', False) if self.get('status') == None else None

    @loader.watcher(out=True, no_commands=True)
    async def notes(self, message): # Наблюдатель
        if self.get('status'):
            text = message.text
            for i in self.get('shortnames'):
                if f'#{i}' in message.text:
                    text += f'\n\n<b>#{i}</b>:\n{self.get(i)}'
                    await message.edit(text)
                    await asyncio.sleep(self.config['sleep'])

    def __init__(self): # Конфиг
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "sleep", 1,
                lambda: self.strings("sleep"),
                validator=loader.validators.Integer()
            ),
        )

    @loader.command()
    async def addnote(self, message): # Добавить заметку
        '''[ короткое название ] < ответ на текст заметки > - создать заметку'''
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if args:
            if ' ' not in args:
                if '#' not in args:
                    shortname = args
                    if reply:
                        note = reply.text
                        if shortname not in self.get('shortnames'):
                            self.set(shortname, note)
                            self.get('shortnames').append(shortname)
                            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Заметка <code>#{shortname}</code> создана.\n<emoji document_id=5334882760735598374>📝</emoji> Текст заметки:\n{note}.')
                            return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭто короткое название уже занято.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nИспользуйте другое короткое название.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали текст заметки.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nОтветьте на сообщение, которое станет текстом заметки.')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали запрещенный символ в коротком названии.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nНе используйте символ "#" в коротких названиях.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nКороткое название должно состоять только из одного слова.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите короткое название, которое состоит из одного слова.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали короткое название заметки.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите короткое название, которое состоит из одного слова.')
            return
        
    @loader.command()
    async def delnote(self, message): # Удалить заметку
        '''[ короткое название ] - удалить заметку'''
        args = utils.get_args_raw(message)
        if args:
            if args in self.get('shortnames'):
                self.set(args, None)
                self.get('shortnames').remove(args)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Заметка <code>#{args}</code> удалена.')
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЗаметки не найдено.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите верное название заметки.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали короткое название.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите короткое название заметки, которую нужно удалить.')
            return
        
    @loader.command()
    async def fnotes(self, message): # Список заметок
        '''[ full / ничего ] - просмотреть заметки'''
        args = utils.get_args_raw(message)
        if not self.get('shortnames'):
            await utils.answer(message, f'<emoji document_id=5334882760735598374>📝</emoji> Заметок нет.')
            return
        else:
            text = f'<emoji document_id=5334882760735598374>📝</emoji> Ваши заметки ({len(self.get("shortnames"))}):'
        if args == 'full':
            for i in self.get('shortnames'):
                text += f'\n\n<b>#{i}</b>:\n{self.get(i)}'
        elif not args:
            for i in self.get('shortnames'):
                text += f'\n<b>#{i}</b>'
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nКоманда не имеет аргумента "<code>{args}</code>".'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент "full" или не указывайте ничего.')
            return
        await utils.answer(message, text)

    @loader.command()
    async def snotes(self, message): # Статус заметок
        '''- включить / отключить заметки'''
        if self.get('status'):
            self.set('status', False)
            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Заметки отключены.')
            return
        else:
            self.set('status', True)
            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Заметки включены.')

    @loader.command()
    async def helpnotes(self, message): # Помощь
        '''- вывести помощь по модулю'''
        text = '<emoji document_id=5334882760735598374>📝</emoji> Чтобы получить заметку в вашем сообщение должно быть "<code>#{короткое название}</code>"'
        if self.get('shortnames'):
            text += f', например: "<code>Моя заметка: #{random.choice(self.get("shortnames"))}</code>"'
        await utils.answer(message, text)
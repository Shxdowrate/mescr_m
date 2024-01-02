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
import io

__version__ = (1, 3, 1)

class FastNotes(loader.Module): # Класс
    '''Модуль для быстрого полученимя заметок.\nDeveloper: @mescr_m'''

    strings = {
        'name': 'FastNotes',
        'sleep': 'Сколько секунд юзерботу ждать перед повторным изменением сообщения, если было указано более одной заметки?',
    }
    

    async def client_ready(self): # Настройка БД
        self.set('shortnames', []) if self.get('shortnames') == None else None
        self.set('status', False) if self.get('status') == None else None
        self.set('allows_users', []) if self.get('allows_users') == None else None

    @loader.watcher(no_commands=True)
    async def notes(self, message): # Наблюдатель
        if self.get('status'):
            if message.text:
                text = message.raw_text
                myid = self.tg_id
                if message.from_id == myid:
                    for i in self.get('shortnames'):
                        if f'#{i}' in message.text:
                            text += f'\n\n<b>#{i}</b>:\n{self.get(i)}'
                            await message.edit(text)
                            await asyncio.sleep(self.config['sleep'])
                elif message.from_id in self.get('allows_users'):
                    s = False
                    text = ''
                    for i in self.get('shortnames'):
                        if f'#{i}' in message.text:
                            text += f'\n\n<b>#{i}</b>:\n{self.get(i)}'
                            if s == False:
                                new_message = await message.reply(text)
                                s = True
                                await asyncio.sleep(self.config['sleep'])
                            else:
                                await new_message.edit(text)
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
    async def notesuser(self, message):
        '''< ответ на сообщение > - дать/забрать у пользователя доступ к заметкам'''
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if args:
            if ' ' not in args: 
                if '-' not in args:
                    if args.isdigit():
                        id = int(args)
                        try:
                            user = await self.client.get_entity(id)
                            nick = user.first_name
                        except Exception:
                            nick = '_user_'
                        if id not in self.get('allows_users'):
                            self.get('allows_users').append(id)
                            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Пользователю {nick} (<code>{id}</code>) выдан доступ к заметкам.')
                            return
                        else:
                            self.get('allows_users').remove(id)
                            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> У пользователя {nick} (<code>{id}</code>) забран доступ к заметкам.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВ аргументе содержатся запрещенные символы.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите правильное ID пользователя в котором нет букв или других символов, кроме цифр.')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВ аргументе содержатся запрещенные символы.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите правильное ID пользователя в котором нет букв или других символов, кроме цифр.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВ аргументе содержатся пробелы.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите правильное ID пользователя в котором нет букв или других символов, кроме цифр.')
                return
        elif reply:
            id = reply.from_id
            nick = reply.sender.first_name
            if id not in self.get('allows_users'):
                self.get('allows_users').append(id)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Пользователю {nick} (<code>{id}</code>) выдан доступ к заметкам.')
                return
            else:
                self.get('allows_users').remove(id)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> У пользователя {nick} (<code>{id}</code>) забран доступ к заметкам.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не ответили не на чье сообщение и не указали аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nОтветьте на сообщения пользователя, которому хотите дать доступ или укажите его ID.')
            return
            
    @loader.command(alias = 'fnus')
    async def notesusers(self, message):
        '''- просмотреть пользователей с доступом к заметкам'''
        if not self.get('allows_users'):
            await utils.answer(message, f'<emoji document_id=5334882760735598374>📝</emoji> Список пользователей пуст.')
        else:
            text = f'<emoji document_id=5334882760735598374>📝</emoji> Пользователи с доступом к вашим заметкам({len(self.get("allows_users"))}):'
            for i in self.get('allows_users'):
                id = i
                num = 0
                try:
                    user = await self.client.get_entity(i)
                    nick = user.first_name
                except Exception:
                    nick = '_user_'
                num += 1
                text += f'\n{num} | {nick} (<code>{id}</code>)'
            await utils.answer(message, text)

    @loader.command(alias = 'fnan')
    async def notesadd(self, message): # Добавить заметку
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
    async def notesdel(self, message): # Удалить заметку
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
    async def noteslist(self, message): # Список заметок
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
    async def notesstatus(self, message): # Статус заметок
        '''- включить / отключить заметки'''
        if self.get('status'):
            self.set('status', False)
            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Заметки отключены.')
            return
        else:
            self.set('status', True)
            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Заметки включены.')

    @loader.command()
    async def noteshelp(self, message): # Помощь
        '''- вывести помощь по модулю'''
        text = '<emoji document_id=5334882760735598374>📝</emoji> Чтобы получить заметку в вашем сообщение должно быть "<code>#{короткое название}</code>"'
        if self.get('shortnames'):
            text += f', например: "<code>Моя заметка: #{random.choice(self.get("shortnames"))}</code>"'
        await utils.answer(message, text)

    @loader.command()
    async def notesbackup(self, message):
        '''[ reset(сброс) / backup(создать) / restore(восстановить) ] - создать/восстановить бекап или удалить все заметки'''
        args = utils.get_args_raw(message)
        if args == 'backup':
            text = 'FastNotesBackup <<<>>> '
            num = 0
            snum = len(self.get('shortnames'))
            for i in self.get('shortnames'):
                text += f'{i} <<>> {self.get(i)}'
                num += 1
                if num != snum:
                    text += ' <<<>>> '
            text = bytes(text, 'utf')
            file = io.BytesIO(text)
            file.name = f'FastNoteBackup_{self.tg_id}.txt'
            file.seek(0)
            await self.client.send_message('me', file=file)
            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Бэкап сохранен к вам в избранные.')
            return
        elif args == 'restore':
            reply = await message.get_reply_message()
            if reply:
                text = await reply.download_media(bytes)
                text = str(text, "utf8")
                if ' <<<>>> ' in text and ' <<>> ' in text:
                    notes = text.split(' <<<>>> ')
                    await utils.answer(message, f'<emoji document_id=5307717998826497825>🌀</emoji> Восстановление бэкапа FastNotes...')
                    for note in notes:
                        if ' <<>> ' in note:
                            shortname, note = note.split(' <<>> ')
                            if shortname not in self.get('shortnames'):
                                self.get('shortnames').append(shortname)
                            self.set(shortname, note)
                    await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Бэкап FastNotes восстановлен.')
                    return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nФайл, на который вы ответили, не является бэкапом FastNotes.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nОтветьте на файл, который содержит бэкап  FastNotes.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не ответили на файл с бэкапом.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nОтветьте на файл, который содержит бэкап  FastNotes.')
                return
        elif args == 'reset':
            for note in self.get('shortnames'):
                self.set(note, None)
            self.set('shortnames', [])
            await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Все заметки удалены.')
            return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали неизвестный параметр.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите в аргумент: <code>backup</code> - чтобы создать бэкап, <code>restore</code> - что восстановить бэкап или <code>reset</code> - чтобы удалить все заметки.')
            return
            
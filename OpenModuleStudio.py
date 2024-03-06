from .. import loader, utils
import asyncio

__version__ = (1, 0, 0)

class OpenModuleStudio(loader.Module):
    '''Модуль для создания и управления микроскриптами eval\nDeveloper: @mescr_m'''

    strings = {
        'name': 'OpenModuleStudio',
        'auto_delete_message': 'Удалять ли сообщение с командой modrun автоматически?',
        'sleep': 'Если к одному наблюдателю привязано сразу несколько модулей, то между ними должна быть какая-то задержка.'
    }

    async def client_ready(self):
        self.set('names', []) if self.get('names') == None else None
        self.set('watch_names', []) if self.get('watch_names') == None else None

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "auto_delete_message", True,
                lambda: self.strings("auto_delete_message"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "sleep", 1,
                lambda: self.strings("sleep"),
                validator=loader.validators.Integer()
            ),
        )

    @loader.watcher(no_commands = True, only_messages = True)
    async def watcher_m(self, message):
        watchers = self.get('watch_names')
        if watchers:
            for watcher_name in watchers:
                watcher = self.get(f'watcher_{watcher_name}')
                if watcher['users']:
                    if message.from_id in watcher['users']:
                        pass
                    else:
                        return
                if watcher['chats']:
                    if message.chat_id in watcher['chats']:
                        pass
                    else:
                        return

                
                modules = watcher['modules']

                e_status = False
                for str in watcher['e_str']:
                    if e_status == True:
                        pass
                    if message.raw_text.count(str) > 0:
                        e_status = True
                        for module in modules:
                            await self.invoke(
                                'e',
                                self.get(module),
                                message = message
                            )
                            await asyncio.sleep(self.config['sleep'])
                for str in watcher['p_str']:
                    if message.raw_text == str:
                        for module in modules:
                            await self.invoke(
                                'e',
                                self.get(module),
                                message = message
                            )
                            await asyncio.sleep(self.config['sleep'])
        
    @loader.command()
    async def modadd(self, message):
        '''[ответ на код] [имя] - добавить модуль ("/darg/" - динамический аргумент)'''
        args = utils.get_args_raw(message)
        r = await message.get_reply_message()

        if not args:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе указаны аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который будет обозначать название модуля.')
            return
        
        if not r:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе указан код.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nОтветьте на сообщение, которое содержит код для eval.')
            return
        
        name = args.split(' ')[0] 
        code = r.raw_text
        names = self.get('names')

        if name in names:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭто имя уже занято.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите другое имя, которое ранее не использовалось.')
            return
        
        self.set(name, code)
        names.append(name)
        self.set('names', names)
        await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Модуль "{name}" создан.')
        return
        
    @loader.command()
    async def moddel(self, message):
        '''[имя] - удалить модуль'''
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе указаны аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите имя модуль, чтобы его удалить.')
            return
        
        name = args.split(' ')[0] 
        names = self.get('names')

        if name not in names:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nМодуль не найден.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите имя модуля, который ранее был создан.')
            return
        
        names.remove(name)
        self.set('names', names)
        self.set(name, None)
        await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Модуль "{name}" успешно удален.')
        return
    
    @loader.command()
    async def modlist(self, message):
        '''- вывести список модулей'''
        names = self.get('names')

        if not names:
            await utils.answer(message, '<emoji document_id=5294096239464295059>🔴</emoji> Ни одного модуля не обнаружено.')
            return
        
        text = '<b>Список ваших модулей:</b>\n'
        for name in names:
            text += f'<emoji document_id=4974307891025543730>▫️</emoji> {name}\n'
        await utils.answer(message, text)

    @loader.command()
    async def modget(self, message):
        '''[имя] - получить код модуля'''
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе указан аргумент.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите имя модуля, который ранее был создан.')
            return
        
        name = args.split(' ')[0]
        names = self.get('names')

        if name not in names:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nМодуль не найден.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите имя модуля, который ранее был создан.')
            return
        
        code = self.get(name)
        
        await utils.answer(message, f'<b>Модуль</b> <code>{name}</code>:\n<pre><code class="language-python">{code}</code></pre>')
        return
    
    @loader.command()
    async def modrun(self, message):
        '''[имя] [аргумет(если требуется)] - выполнить модуль'''
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе введен аргумент.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который будет обозначает название модуля.')
            return
        
        name = args.split(' ')[0]
        names = self.get('names')

        if ' ' in args:
            darg = ' '.join(args.split(' ')[1:])

        if name not in names:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nМодуль не найден.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите имя модуля, который ранее был создан.')
            return
        
        code = self.get(name)
        if '/darg/' in code:
            code = code.replace('/darg/', darg)

        await self.invoke(
            'e',
            code,
            message=message
        )
        if self.config['auto_delete_message']:
            await message.delete()
    
    @loader.command()
    async def watchadd(self, message):
        '''[имя] - создать новый наблюдатель'''
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе введен аргумент.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который будет обозначать название для нового наблюдателя.')
            return
        
        name = args.split(' ')[0]
        watch_names = self.get('watch_names')

        if name in watch_names:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНаблюдатель с таким названием уже существует.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите другое имя для наблюдателя, чтобы создать его.')
            return
        
        watcher = {
            'name': name,
            'chats': [],
            'users': [],
            'modules': [],
            'e_str': [],
            'p_str': [],
        }
        self.set(f'watcher_{name}', watcher)
        watch_names.append(name)
        self.set('watch_names', watch_names)
        await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Наблюдатель "{name}" создан.')
        return
    
    @loader.command()
    async def watchdel(self, message):
        '''[имя] - удалить наблюдатель'''
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе введен аргумент.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который будет обозначать название наблюдателя, который вы хотите удалить.')
            return
        
        name = args.split(' ')[0]
        watch_names = self.get('watch_names')

        if name not in watch_names:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНаблюдателя с таким именем не существует.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите имя ранее созданного наблюдателя, чтобы удалить его.')
            return

        self.set(f'watсher_{name}', None)
        watch_names.remove(name)
        self.set('watch_names', watch_names)
        await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Наблюдатель "{name}" удален.')
        return
    
    @loader.command()
    async def watchlist(self, message):
        '''- вывести список наблюдателей'''
        watch_names = self.get('watch_names')

        if not watch_names:
            await utils.answer(message, '<emoji document_id=5294096239464295059>🔴</emoji> Ни одного наблюдателя не обнаружено.')
            return
        
        text = f'<emoji document_id=5787237370709413702>⚙️</emoji> Список наблюдателей:\n'
        for i in watch_names:
            text += f'<emoji document_id=4974467474830394346>▫️</emoji> {i}\n'
        await utils.answer(message, text)
        return
    
    @loader.command()
    async def watchget(self, message):
        '''[имя] - получить информацию о наблюдателе'''
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе введен аргумент.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который будет обозначать название наблюдателя')
            return
        
        name = args.split(' ')[0]
        watch_names = self.get('watch_names')

        if name not in watch_names:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНаблюдателя с таким именем не существует.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите имя ранее созданного наблюдателя, чтобы посмотреть информацию о нем.')
            return
        
        watcher = self.get(f'watcher_{name}')
        text = (
            f'<emoji document_id=5787237370709413702>⚙️</emoji> <b>Наблюдатель</b> <code>{name}</code>:\n\n' +
            f'<emoji document_id=5219943216781995020>⚡</emoji> Имя: {watcher["name"]}\n' +
            f'<emoji document_id=5821374629771480129>✈️</emoji> Чаты: {watcher["chats"]}\n' +
            f'<emoji document_id=5819154994967874788>🧑‍💻</emoji> Пользователи: {watcher["users"]}\n' +
            f'<emoji document_id=5821238376228981917>🟦</emoji> Модули: {watcher["modules"]}\n' +
            f'<emoji document_id=5819095256267755019>⏺</emoji> e_str: {watcher["e_str"]}\n' +
            f'<emoji document_id=5819143265412189249>⏺</emoji> p_str: {watcher["p_str"]}\n\n'
                )
        text += '*e_str - фильтр "если строка есть в сообщении", p_str - фильтр "если сообщение == строка"\n\n'
        text += '*если chats не пустой, а users пустой, то наблюдатель реагирует на сообщения от всех пользователей в соотвественных чатах\nесли chats пустой, а users не пустой, то наблюдатель реагирует на сообщения от соответственных пользователей во всех чатах\nесли и chats и users не пустой, то наблюдатель регирует только на сообщения от соответственных пользователей в соотвественных чатах'
        await utils.answer(message, text)
        return
    
    @loader.command()
    async def watchset(self, message):
        '''[имя(help - помощь)] [тип] [действие] [значение(или ничего, если действие = chats, users)] - настроить наблюдатель'''
        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент для типа настроек наблюдателя.')
            return
        
        if args == 'help':
            text = (
                '<b>Помощь по настройке наблюдателей:</b>\n' +
                '<emoji document_id=4974467474830394346>▫️</emoji> типы: <code>chats</code>, <code>users</code>, <code>modules</code>, <code>p_str</code>, <code>e_str</code>.\n' +
                '<emoji document_id=4974467474830394346>▫️</emoji> действия: <code>add</code>, <code>del</code>, <code>clear</code>\n' +
                '<emoji document_id=4974467474830394346>▫️</emoji> значение:\n' +
                '  <emoji document_id=4974467474830394346>▫️</emoji> users: ID пользователя или ответ на его сообщение\n' +
                '  <emoji document_id=4974467474830394346>▫️</emoji> chats: ID чата или сообщение в чате, с которым хотите работать\n' +
                '  <emoji document_id=4974467474830394346>▫️</emoji> modules: название модуля\n' +
                '  <emoji document_id=4974467474830394346>▫️</emoji> p_str: строка, которую хотите добавить в p_str\n' +
                '  <emoji document_id=4974467474830394346>▫️</emoji> e_str: строка, которую хотите добавить в e_str\n'
            )
            await utils.answer(message, text)
            return
        
        if ' ' not in args:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали только 1 аргумент.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите более одного аргумента, как этого требует команда.')
            return
        
        # watcher = {
        #     'name': name,
        #     'chats': [],
        #     'users': [],
        #     'modules': [],
        #     'e_str': [],
        #     'p_str': [],
        # }

        args = args.split(' ')
        watcher = self.get(f'watcher_{args[0]}')

        if watcher == None:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНаблюдателя с таким именем не найдено.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите наблюдатель, ранее созданный вами.')
            return

        if args[1].lower() == 'chats':

            if len(args) < 3:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНедостаточно аргументов.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите все необходимые аргумент для успешной настройки наблюдателя.')
                return
            
            chat_id = None

            if len(args) == 4:
                try:
                    chat_id = int(args[3])
                except ValueError:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nID чата, который вы указали, содержит ошибки.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите правильный ID чата для взаимодействия с ним.')
                    return
                
            chat = chat_id if chat_id != None else message.chat_id
            if args[2].lower() == 'add':

                if chat in watcher['chats']:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭтот чат уже есть в наблюдателе <code>{watcher["name"]}</code>.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите чат, которого нет в текущем наблюдателе.')
                    return
                
                watcher['chats'].append(chat)
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Чат ID:<code>{chat}</code> успешно добавлен в чаты наблюдателя <code>{watcher["name"]}</code>.')
                return
            
            if args[2].lower() == 'del':
                
                if chat not in watcher['chats']:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭтот чат не состоит в чатах наблюдателя <code>{watcher["name"]}</code>.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите чат, который состоит в чатах текущего наблюдателя.')
                    return
                
                watcher['chats'].remove(chat)
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Чат ID:<code>{chat}</code> успешно удален из чатов наблюдателя <code>{watcher["name"]}</code>.')
                return
            
            if args[2].lower() == 'clear':
                watcher['chats'] = []
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Чаты наблюдателя <code>{watcher["name"]}</code> успешно очищены.')
                return
            
        if args[1].lower() == 'users':

            if len(args) < 3:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНедостаточно аргументов.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите все необходимые аргумент для успешной настройки наблюдателя.')
                return
            
            user_id = None

            if len(args) == 4:
                try:
                    user_id = int(args[3])
                except ValueError:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nID пользователя, который вы указали, содержит ошибки.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите правильный ID пользователя для взаимодействия с ним.')
                    return
            
            r = await message.get_reply_message()

            if user_id:
                user = user_id

            else:

                if r:
                    user = r.from_id

                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали ID пользователя для добавления его в users наблюдателя <code>{watcher["name"]}</code>.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите ID пользователя последним аргументом, или ответьте на его сообщение.')
                    return
                
            if args[2].lower() == 'add':

                if user in watcher['users']:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭтот пользователь уже есть в наблюдателе <code>{watcher["name"]}</code>.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите пользователя, которого нет в текущем наблюдателе.')
                    return
                
                watcher['users'].append(user)
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Пользователь ID:<code>{user}</code> успешно добавлен в пользователи наблюдателя <code>{watcher["name"]}</code>.')
                return
            
            if args[2].lower() == 'del':
                if user not in watcher['users']:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭтот пользователь не состоит в пользователях наблюдателя <code>{watcher["name"]}</code>.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите пользователя, который состоит в пользователях текущего наблюдателя.')
                    return
                
                watcher['users'].remove(user)
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Пользователь ID:<code>{user}</code> успешно удален из пользователей наблюдателя <code>{watcher["name"]}</code>.')
                return
            
            if args[2].lower() == 'clear':
                watcher['users'] = []
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Пользователи наблюдателя <code>{watcher["name"]}</code> успешно очищены.')
                return
            
        if args[1].lower() == 'modules':

            if len(args) < 4:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНедостаточно аргументов.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите все необходимые аргумент для успешной настройки наблюдателя.')
                return
            
            module = args[3]
            names = self.get('names')
            code = self.get(module)

            if module not in names:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nМодуль не найден.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите ранее созданный модуль, чтобы добавить его в наблюдатель.')
                return
            
            if '/darg/' in code:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВ данном модуле используется динамический аргумент(<code>__darg__</code>), который не может быть использован в наблюдателе.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите модуль, который не использует динамический аргумент, чтобы добавить его в наблюдатель.')
                return
                
            if args[2].lower() == 'add':

                if module in watcher['modules']:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭтот модуль уже есть в наблюдателе <code>{watcher["name"]}</code>.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите модуль, которого нет в текущем наблюдателе.')
                    return
                
                watcher['modules'].append(module)
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Модуль: <code>{module}</code> успешно добавлен в модули наблюдателя <code>{watcher["name"]}</code>.')
                return
            
            if args[2].lower() == 'del':
                if module not in watcher['modules']:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭтот модуль не состоит в модулях наблюдателя <code>{watcher["name"]}</code>.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите модуль, который состоит в модулях текущего наблюдателя.')
                    return
                
                watcher['modules'].remove(module)
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Модуль: <code>{module}</code> успешно удален из модулей наблюдателя <code>{watcher["name"]}</code>.')
                return
            
            if args[2].lower() == 'clear':
                watcher['modules'] = []
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Модули наблюдателя <code>{watcher["name"]}</code> успешно очищены.')
                return
            
        if args[1].lower() == 'p_str':

            if len(args) < 4:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНедостаточно аргументов.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите все необходимые аргумент для успешной настройки наблюдателя.')
                return
            
            s_str = args[3:]
            str = ' '.join(s_str)
            p_str = watcher['p_str']
                
            if args[2].lower() == 'add':

                if str in p_str:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭта строка уже есть в p_str модуля <code>{watcher["name"]}</code>.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите строку, которой нет в текущем наблюдателе.')
                    return
                
                watcher['p_str'].append(str)
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Строка: <code>{str}</code> успешно добавлена в p_str наблюдателя <code>{watcher["name"]}</code>.')
                return
            
            if args[2].lower() == 'del':
                if str not in watcher['p_str']:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭта строка не состоит в p_str наблюдателя <code>{watcher["name"]}</code>.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите строку, которая состоит в p_str текущего наблюдателя.')
                    return
                
                watcher['p_str'].remove(str)
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Строка: <code>{str}</code> успешно удалена из p_str наблюдателя <code>{watcher["name"]}</code>.')
                return
            
            if args[2].lower() == 'clear':
                watcher['p_str'] = []
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Строки p_str наблюдателя <code>{watcher["name"]}</code> успешно очищены.')
                return
            
        if args[1].lower() == 'e_str':

            if len(args) < 4:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНедостаточно аргументов.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите все необходимые аргумент для успешной настройки наблюдателя.')
                return
            
            s_str = args[3:]
            str = ' '.join(s_str)
            e_str = watcher['e_str']
                
            if args[2].lower() == 'add':

                if str in e_str:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭта строка уже есть в e_str модуля <code>{watcher["name"]}</code>.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите строку, которой нет в текущем наблюдателе.')
                    return
                
                watcher['e_str'].append(str)
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Строка: <code>{str}</code> успешно добавлена в e_str наблюдателя <code>{watcher["name"]}</code>.')
                return
            
            if args[2].lower() == 'del':
                if str not in watcher['e_str']:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭта строка не состоит в e_str наблюдателя <code>{watcher["name"]}</code>.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите строку, которая состоит в e_str текущего наблюдателя.')
                    return
                
                watcher['e_str'].remove(str)
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Строка: <code>{str}</code> успешно удалена из e_str наблюдателя <code>{watcher["name"]}</code>.')
                return
            
            if args[2].lower() == 'clear':
                watcher['e_str'] = []
                self.set(f'watcher_{watcher["name"]}', watcher)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Строки e_str наблюдателя <code>{watcher["name"]}</code> успешно очищены.')
                return
            
                


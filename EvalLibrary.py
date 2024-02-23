from .. import loader, utils

__version__ = (1, 0, 0)

class EvalLibrary(loader.Module):
    '''Модуль для записи кода. Developer: @mescr_m'''

    strings = {
        'name': 'EvalLibrary',
        'code': 'Отображать ли код при его вызове?',
        'result': 'Отображать ли результат кода при его вызове?',
    }

    async def client_ready(self):
        self.set('library', []) if self.get('library') == None else None

    @loader.command(alias = 'eladd')
    async def evallibraryadd(self, message):
        '''[ответ на код] [название] - добавить код в библиотеку'''
        args = utils.get_args_raw(message)
        r = await message.get_reply_message()
        if args:
            if r:
                name = args.split(' ')[0]
                if name not in self.get('library'):
                    code = r.raw_text
                    lib = self.get('library')
                    lib.append(name)
                    self.set(name, code)
                    await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Код сохранен. Название: <code>{name}</code>.')
                    return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭто имя уже занято.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nИспользуйте другое имя для добавления кода в библиотеку.')
                return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не задали код.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nЧтобы задать код, ответьте на сообщение, в котором написан необходимый для вас код.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе указаны аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который будет обозначать имя для кода в вашей библиотеке.')
            return
        
    @loader.command(alias = 'eldel')
    async def evallibrarydel(self, message):
        '''[название] - удалить код из библиотеки'''
        args = utils.get_args_raw(message)
        if args:
            name = args.split(' ')[0]
            lib = self.get('library')
            if name in lib:
                self.set(name, None)
                lib.remove(name)
                self.set('library', lib)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Код "<code>{name}</code>" удален.')
                return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВведенное название кода не найдено в библиотеке...'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите название кода, который ранее был сохранен в библиотеку.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе указаны аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который будет обозначать имя кода в вашей библиотеке.')
            return
        
    @loader.command(alias = 'el')
    async def evallibrary(self, message):
        '''- вывести библиотеку'''
        lib = self.get('library')
        if lib:
            text = '<emoji document_id=5334882760735598374>📝</emoji> Ваша библиотека кода:\n\n'
            for e in lib:
                text += f'🔸 {e}\n'
            await utils.answer(message, text)
            return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nУ вас нет ни одного кода в библиотеке.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nЧтобы вывести свою библиотеку сохраните в нее хотя бы один код.')
            return
        
    @loader.command(alias = 'elget')
    async def evallibraryget(self, message):
        '''[название] - получить код из библиотеки'''
        args = utils.get_args_raw(message)
        if args:
            name = args.split(' ')[0]
            lib = self.get('library')
            if name in lib:
                code = self.get(name)
                text = f'<emoji document_id=4985626654563894116>💻</emoji> Ваш код:\n\n<code>{code}</code>'
                await utils.answer(message, text)
                return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВведенное название кода не найдено в библиотеке.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите название, ранее сохраненное в вашу библиотеку.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе указаны аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который будет обозначать имя кода в вашей библиотеке.')
            return
        
    @loader.command(alias = 'elrun')
    async def evallibraryrun(self, message):
        '''[название] - выполнить код из библиотеки'''
        args = utils.get_args_raw(message)
        if args:
            name = args.split(' ')[0]
            lib = self.get('library')
            if name in lib:
                code = self.get(name)
                await self.invoke(
                    'e',
                    code,
                    message = message
                )
                await message.delete()
                return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВведенное название кода не найдено в библиотеке.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите название, ранее сохраненное в вашу библиотеку.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе указаны аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, который будет обозначать имя кода в вашей библиотеке.')
            return

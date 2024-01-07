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

from .. import loader, utils
c = loader.command

__version__ = (1, 0, 0)

class BotManager(loader.Module):
    '''Раскрытие твоего бота...\nDeveloper: @mescr_m'''

    strings = {
        'name': 'BotManager',
    }

    @c()
    async def botsendmessage(self, message):
        '''[ ID чата / ничего ] [ текст сообщения ] - отправить сообщение'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' in args:
                testchat = args.split(' ')[0]
                if testchat[1:].isdigit():
                    chat = int(args.split(' ')[0])
                    text = ' '.join(args.split(' ')[1:])
                    try:
                        await self.inline.bot.send_message(chat, text)
                        await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Сообщение отправлено.')
                        return
                    except Exception as e:
                        await utils.answer(message, f'<emoji document_id=5877477244938489129>🚫</emoji> <b>Ошибка!</b>\n\n<emoji document_id=5328311576736833844>🔴</emoji> {e}')
                        return
                else:
                    chat = message.chat_id
                    text = args
                    try:
                        await self.inline.bot.send_message(chat, text)
                        await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Сообщение отправлено.')
                        return
                    except Exception as e:
                        await utils.answer(message, f'<emoji document_id=5877477244938489129>🚫</emoji> <b>Ошибка!</b>\n\n<emoji document_id=5328311576736833844>🔴</emoji> {e}')
                        return
            else:
                chat = message.chat_id
                text = args
                try:
                    await self.inline.bot.send_message(chat, text)
                    await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Сообщение отправлено.')
                    return
                except Exception as e:
                    await utils.answer(message, f'<emoji document_id=5877477244938489129>🚫</emoji> <b>Ошибка!</b>\n\n<emoji document_id=5328311576736833844>🔴</emoji> {e}')
                    return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргументы, согласно описанию команды в help.')
            return
        
    @c()
    async def botreplymessage(self, message):
        '''< ответ на сообщение > [ текст ] - ответить на сообщение'''
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if args:
            if reply:
                chat = message.chat_id
                reply_message_id = reply.id
                text = args
                try:
                    await self.inline.bot.send_message(chat, text, reply_to_message_id=reply_message_id)
                    await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Сообщение отправлено.')
                except Exception as e:
                    await utils.answer(message, f'<emoji document_id=5877477244938489129>🚫</emoji> <b>Ошибка!</b>\n\n<emoji document_id=5328311576736833844>🔴</emoji> {e}')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не ответили на сообщение, на которое должен ответить ваш бот.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nНапишите команду в ответ на сообщение, на которое должен ответить ваш бот.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргументы, согласно описанию команды в help.')
            return
        
    @c()
    async def boteditchattitle(self, message):
        '''[ ID чата / ничего ] [ новое название ] - изменить название чата'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' in args:
                testchat = args.split(' ')[0]
                if testchat[1:].isdigit():
                    chat = int(args.split(' ')[0])
                    title = ' '.join(args.split(' ')[1:])
                    try:
                        await self.inline.bot.set_chat_title(chat, title)
                        await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Название чата изменено.')
                        return
                    except Exception as e:
                        await utils.answer(message, f'<emoji document_id=5877477244938489129>🚫</emoji> <b>Ошибка!</b>\n\n<emoji document_id=5328311576736833844>🔴</emoji> {e}')
                        return
                else:
                    chat = message.chat_id
                    title = args
                    try:
                        await self.inline.bot.set_chat_title(chat, title)
                        await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Название чата изменено.')
                        return
                    except Exception as e:
                        await utils.answer(message, f'<emoji document_id=5877477244938489129>🚫</emoji> <b>Ошибка!</b>\n\n<emoji document_id=5328311576736833844>🔴</emoji> {e}')
                        return
            else:
                chat = message.chat_id
                title = args
                try:
                    await self.inline.bot.set_chat_title(chat, title)
                    await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Название чата изменено.')
                    return
                except Exception as e:
                    await utils.answer(message, f'<emoji document_id=5877477244938489129>🚫</emoji> <b>Ошибка!</b>\n\n<emoji document_id=5328311576736833844>🔴</emoji> {e}')
                    return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргументы, согласно описанию команды в help.')
            return
        
    @c()
    async def botforwardmessage(self, message):
        '''< ответ на сообщение > [ ID чата / ничего ] - переслать сообщение'''
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if reply:
            if args:
                try:
                    chat_to_id = args
                except Exception as e:
                    await utils.answer(message, f'<emoji document_id=5877477244938489129>🚫</emoji> <b>Ошибка!</b>\n\n<emoji document_id=5328311576736833844>🔴</emoji> {e}')
                    return
            else:
                chat_to_id = message.chat_id
            reply_message_chat_id = reply.chat_id
            reply_message_id = reply.id
            try:
                await self.inline.bot.forward_message(chat_to_id, reply_message_chat_id, reply_message_id)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Сообщение переслано.')
            except Exception as e:
                await utils.answer(message, f'<emoji document_id=5877477244938489129>🚫</emoji> <b>Ошибка!</b>\n\n<emoji document_id=5328311576736833844>🔴</emoji> {e}')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не ответили на сообщение, которое нужнно переслать.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nНапишите команду в ответ на сообщение, которое нужно переслать.')
            return
        
    @c()
    async def botforwardmessagehide(self, message):
        '''< ответ на сообщение > [ ID чата / ничего ] - переслать сообщение без "переслано от"'''
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if reply:
            if args:
                try:
                    chat_to_id = args
                except Exception as e:
                    await utils.answer(message, f'<emoji document_id=5877477244938489129>🚫</emoji> <b>Ошибка!</b>\n\n<emoji document_id=5328311576736833844>🔴</emoji> {e}')
                    return
            else:
                chat_to_id = message.chat_id
            reply_message_chat_id = reply.chat_id
            reply_message_id = reply.id
            try:
                await self.inline.bot.copy_message(chat_to_id, reply_message_chat_id, reply_message_id)
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Сообщение переслано (<code>hide</code>).')
            except Exception as e:
                await utils.answer(message, f'<emoji document_id=5877477244938489129>🚫</emoji> <b>Ошибка!</b>\n\n<emoji document_id=5328311576736833844>🔴</emoji> {e}')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не ответили на сообщение, которое нужнно переслать.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nНапишите команду в ответ на сообщение, которое нужно переслать.')
            return
            
                

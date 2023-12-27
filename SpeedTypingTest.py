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
import time

__version__ = (1, 1, 0)

class STT(loader.Module):
    '''Модуль для проверки скоропечати. \nDeveloper: @mescr_m'''

    strings = {
        'name': 'SpeedTypingTest',
    }

    easy = [
        "Автомобиль",
        "Транспорт",
        "Домашний",
        "Телефон",
        "Компьютер",
        "Оконный",
        "Подъезд",
        "Африка",
        "Тренажер",
        "Монитор"
    ]
    medium = [
        "Я уехал загород, чтобы отдохнуть.",
        "Я сделал хороший выбор.",
        "Мне сегодня гараздо лучше, чем вчера.",
        "Я никогда не думал об этом.",
        "Ты действительно хочешь этого?",
        "Я не думаю, что так будет правильно.",
        "Приехав сюда я понял, что все не так просто.",
        "Я же не один это увидил?",
        "И что? Ты думаешь, что ты один такой?",
        "Чего ты хочешь добиться этим?"
    ]
    hard = [
        "Сегодня ходил на презентацию новых AirPods.",
        "Вчера переустанавливал свой Windows.",
        "Вот тебе пару английских слов: apple, cloud, phone.",
        "Как ты думаешь, новый Samsung S21 сможет появиться на этой неделе?",
        "Вчера купил себе Xbox, завтра пойду за PlayStation.",
        "Как скзаать 'Россия' по английски? - Russia!",
        "Что такое Userbot? Это автомобильный бренд?",
        "Как тебе сериал от Netflix - 'Arcane'?",
        "Вчера я подключил Internet, как вам мемы с котиками?",
        "Ваш 'Microsoft' - план по захвату человечества."
    ]
    fword = 'слово'
    status = False
    start_time = 0
    end_time = 0

    async def client_ready(self):
        self.set('shortnames', []) if self.get('shortnames') == None else None

    @loader.command()
    async def sttcustom(self, message):
        '''[ + / - / = / reset] [ короткое название ] [ строка ] - добавить/удалить/просмотреть кастом строки для тестов'''
        args = utils.get_args_raw(message)
        if args:
            if args == 'reset':
                for i in self.get('shortnames'):
                    self.set(i, None)
                self.set('shortnames', [])
                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Все кастом строки удалены.')
                return
            elif args == '=':
                if not self.get('shortnames'):
                    await utils.answer(message, f'<emoji document_id=5328311576736833844>🔴</emoji> Кастом строк не найдено.')
                    return
                else:
                    txt = f'<emoji document_id=5334882760735598374>📝</emoji> Список кастом строк ({len(self.get("shortnames"))}):'
                    for i in self.get('shortnames'):
                        txt += f'\n\n<b>{i}</b>\n   <code>{self.get(i)}</code>'
                    await utils.answer(message, txt)
            else:
                if ' ' in args:
                    status = args.split(' ')[0]
                    shortname = args.split(' ')[1]
                    string = ' '.join(args.split(' ')[2:])
                    if status == '+':
                        if len(args.split(' ')) >= 3:
                            if shortname not in self.get('shortnames'):
                                self.set(shortname, string)
                                self.get('shortnames').append(shortname)
                                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Добавлена новая кастом строка: <code>{shortname}</code>.\n<emoji document_id=5334882760735598374>📝</emoji> Текст: {string}')
                                return
                            else:
                                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭто короткое имя уже успользуется.'
                                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите другое короткое имя.')
                                return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nКоманде требуется минимум 3 аргумента.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите минимум 3 аргумента.')
                            return
                    elif status == '-':
                        if len(args.split(' ')) >= 3:
                            if shortname in self.get('shortnames'):
                                self.set(shortname, None)
                                self.get('shortnames').remove(shortname)
                                await utils.answer(message, f'<emoji document_id=5332533929020761310>✅</emoji> Кастом строка "<code>{shortname}</code>" удалена.')
                                return
                            else:
                                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭто короткое имя не занято.'
                                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУбедитесь в правильности написания короткого имени.')
                                return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nКоманде требуется минимум 3 аргумента.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите минимум 3 аргумента.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                        f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы использовали символ "{status}", который не зарегистрирован.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nИспользуйте в первом аргументе один из следующих символов: + / - / =')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nУ вас всего один аргумент, хотя требуется минимум три.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите три аргумента.')
                    return

    @loader.watcher(out=True, only_messages=True, no_commands=True)
    async def tester_w(self, message):
        if self.status == True and self.status == True:
            self.end_time = time.time()
            text = message.text
            elapsed_time = time.time() - self.start_time
            seconds = int(elapsed_time)
            milliseconds = int((elapsed_time - seconds) * 1000)
            time_formatted = f"{seconds}.{milliseconds:03d}"
            self.dstatus = False
            self.status = False
            await utils.answer(message, f'{text}\n\n<emoji document_id=5307717998826497825>🌀</emoji> Подготовка результата...')
            txt_f, txt_t = '', ''
            error_count = 0
            txt_t, txt_f = ''.join(self.fword.split()), ''.join(text.split())
            for f, t in zip(list(txt_f), list(txt_t)):
                if f != t:
                    error_count += 1
            percent = 100 - error_count/len(txt_t)*100
            result = "идеально" if percent == 100 else "хорошо" if percent >= 90 else "средне" if percent >= 70 else "плохо"
            await utils.answer(message, f"{text}\n\n<emoji document_id=5445284980978621387>🚀</emoji> Ваш результат: {time_formatted}\n<emoji document_id=5188208446461188962>💯</emoji> Схожесть: {percent}%\n<emoji document_id=5334882760735598374>📝</emoji> Результат: {result}")

    @loader.command()
    async def sttstart(self, message):
        '''[ easy / medium / hard / custom ] - начать тест\n\n🟢 easy - легкий уровень, только одно слово.\n🟡 medium - предложений на русском языке.\n🔴 hard - предложений с английским словом.\n⚪️ custom - ваши кастомные строки.\n'''
        args = utils.get_args_raw(message)
        if args:
            if args == 'easy':
                word = random.choice(self.easy)
            elif args == 'medium':
                word = random.choice(self.medium)
            elif args == 'hard':
                word = random.choice(self.hard)
            elif args == 'custom':
                strings = self.get('shortnames')
                string = random.choice(strings)
                word = self.get(string)
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе выбрано ни одной сложности.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите одну из следующих сложностей: easy, medium, hard.')
                return
            self.fword = word
            await utils.answer(message, f'<emoji document_id=5334882760735598374>📝</emoji> Напишите: {word}\n<emoji document_id=5451732530048802485>⏳</emoji> Старт через 3...')
            await asyncio.sleep(1)
            await utils.answer(message, f'<emoji document_id=5334882760735598374>📝</emoji> Напишите: {word}\n<emoji document_id=5451732530048802485>⏳</emoji> Старт через 2...')
            await asyncio.sleep(1)
            await utils.answer(message, f'<emoji document_id=5334882760735598374>📝</emoji> Напишите: {word}\n<emoji document_id=5451732530048802485>⏳</emoji> Старт через 1...')
            await asyncio.sleep(1)
            await utils.answer(message, f'<emoji document_id=5334882760735598374>📝</emoji> Напишите: {word}\n<emoji document_id=5219943216781995020>⚡️</emoji> ПИШИТЕ!')
            self.status = True
            self.start_time = time.time()
            return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message.raw_text}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНе выбрано ни одной сложности.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите одну из следующих сложностей: easy, medium, hard.')
            return

    @loader.command()
    async def sttreset(self, message):
        '''- сброс, если возникла ошибка (не трогает кастом строки)'''
        self.fword = 'слово'
        self.status = False
        self.start_time = 0
        self.end_time = 0
        await utils.answer(message, f'<emoji document_id=5292226786229236118>🔄</emoji> Модуль сброшен.')
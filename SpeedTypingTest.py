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

__version__ = (1, 0, 0)

class SpeedTypingTest(loader.Module):
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
        '''[ easy / medium / hard ] - начать тест\n\n🟢 easy - легкий уровень, только одно слово.\n🟡 medium - предложений на русском языке.\n🔴 hard - предложений с английским словом.\n'''
        args = utils.get_args_raw(message)
        if args:
            if args == 'easy':
                word = random.choice(self.easy)
            elif args == 'medium':
                word = random.choice(self.medium)
            elif args == 'hard':
                word = random.choice(self.hard)
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
        '''- сброс, если возникла ошибка'''
        self.fword = 'слово'
        self.status = False
        self.start_time = 0
        self.end_time = 0
        await utils.answer(message, f'<emoji document_id=5292226786229236118>🔄</emoji> Модуль сброшен.')

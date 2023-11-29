#——————————————————————————————————————————————————————————————————
# ███╗   ███╗███████╗ ██████╗ █████╗ ██████╗   ┌───────────────────────────┐
# ████╗ ████║██╔════╝██╔════╝██╔══██╗██╔══██╗  │ mescr modules             │
# ██╔████╔██║█████╗  ╚█████╗ ██║  ╚═╝██████╔╝  │ not lisensed              │
# ██║╚██╔╝██║██╔══╝   ╚═══██╗██║  ██╗██╔══██╗  │ https://t.me/mescr_m      │
# ██║ ╚═╝ ██║███████╗██████╔╝╚█████╔╝██║  ██║  └───────────────────────────┘
# ╚═╝     ╚═╝╚══════╝╚═════╝  ╚════╝ ╚═╝  ╚═╝  
#——————————————————————————————————————————————————————————————————
#  ┌──────────────────────────┐
#  │ meta developer: @mescr_m │
#  └──────────────────────────┘
#  ┌───────────────────────────┐
#  │ idea:                     │
#  │ thanks:                   │
#  └───────────────────────────┘
#——————————————————————————————————————————————————————————————————

__version__ = (1, 2, 0)

from .. import utils, loader
import random
import inspect

class Randoms(loader.Module):
    '''Модуль для получения всего рандомного.\nDeveloper: @mescr_m'''

    strings = {
        'name':'Randoms',
        'sep':'Знак-разделитель для команд randval и randvals',
    }

    def __init__(self):  
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "sep", ',',
                lambda: self.strings("sep"),
                validator=loader.validators.String()
            ),
        )

    @loader.command()
    async def randint(self, message):
        '''[ от ] [ до ] - вывести случайное число в заданном диапазоне'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' in args: 
                if len(args.split(' ')) == 2:
                    try:
                        int1 = int(args.split(' ')[0])
                    except ValueError:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели неправильное первое значение.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите целочисленное значение.')
                        return
                    try:
                        int2 = int(args.split(' ')[1])
                    except ValueError:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели неправильное второе значение.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите целочисленное значение.')
                        return
                    if int1 < int2:
                        result = random.randint(int1, int2) # Вывод результата
                        await utils.answer(message, f'| <b>Режим:</b> <code>случайное целочисленное</code>\n| <b>Диапазон:</b> <code>{int1} - {int2}</code>\n| <b>Результат:</b> <code>{result}</code>')
                        return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nПервое значение должно быть меньше, чем второе.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nПопробуйте поменять значения местами.')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели больше аргументов, чем нужно.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите только два аргумента.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели всего один аргумент.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите два аргумента, этого требует команда.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не ввели аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите два аргумента, этого требует команда.')
            return
        
    @loader.command()
    async def randints(self, message):
        '''[ кол-во чисел ] [ от ] [ до ] - вывести несколько случайных чисел в заданном диапазоне'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' in args: 
                if len(args.split(' ')) == 2:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали два аргумента, эта команда требует три.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите три аргумента.')
                    return
                if len(args.split(' ')) < 4:
                    try:
                        qty = int(args.split(' ')[0])
                    except ValueError:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели неправильное кол-во чисел.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nКол-во чисел должно быть так же целочисленным значением.')
                        return
                    try:
                        int1 = int(args.split(' ')[1])
                    except ValueError:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели неправильное первое значение.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите целочисленное значение.')
                        return
                    try:
                        int2 = int(args.split(' ')[2])
                    except ValueError:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели неправильное второе значение.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите целочисленное значение.')
                        return
                    if qty <= 1000:
                        if qty > 0:
                            if int1 < int2:
                                txt = ''
                                g = 0
                                for i in range(qty):
                                    result = random.randint(int1, int2)
                                    if g < 3 and g != 0:
                                        txt += ' | '
                                    if g < 2:
                                        txt += f'{result}'
                                        g += 1
                                    else:
                                        txt += f'{result}\n'
                                        g = 0
                                # Вывод результата
                                await utils.answer(message, f'| <b>Режим:</b> <code>случайные целочисленные</code>\n| <b>Диапазон:</b> <code>{int1} - {int2}</code>\n| <b>Кол-во чисел:</b> <code>{qty}</code>\n| <b>Результат:</b>\n\n{txt}')
                                return
                            else:
                                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nПервое значение должно быть больше второго.'
                                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nПопробуйте поменять значения местами.')
                                return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя вызвать 0 случайных значений.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите число больше нуля.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя вызвать больше случайных чисел, чем 1000.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите число меньше 1000.')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели больше аргументов, чем нужно.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите три аргумента.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели только 1 аргумент.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите три аргумента.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали ни единого аргумента.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите три аргумента.')
            return

    @loader.command()
    async def randword(self, message):
        '''[ слова разделенные пробелом ] - вывести случайное слово из заданных'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' in args:
                words = args.split(' ')
                result = random.choice(words) # Вывод результата
                await utils.answer(message, f'| <b>Режим:</b> <code>случайное слово</code>\n| <b>Диапазон:</b> <code>{words}</code>\n| <b>Результат:</b> <code>{result}</code>')
                return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали лишь одно слово, хотя нужно минимум 2.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите больше слов.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали ни единого аргумента.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите минимум два слова.')
            return
        
    @loader.command()
    async def randwords(self, message):
        '''[ кол-во слов ] [ слова разделенные пробелом ] - вывести несколько случайных слов из заданных'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' in args:
                if len(args.split(' ')) > 2:
                    try:
                        qty = int(args.split(' ')[0])
                    except ValueError:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nПервым аргументом должно быть целочисленное, обозначающее кол-во слов, которое вы хотите получить.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите первым аргументом целочисленное.')
                        return
                    if qty <= 1000:
                        if qty > 0:
                            words = args.split(' ')[1:]
                            txt = ''
                            g = 0
                            for i in range(qty):
                                result = random.choice(words)
                                if g < 3 and g != 0:
                                    txt += ' | '
                                if g < 2:
                                    txt += f'{result}'
                                    g += 1
                                else:
                                    txt += f'{result}\n'
                                    g = 0
                            # Вывод результата
                            await utils.answer(message, f'| <b>Режим:</b> <code>случайные слова</code>\n| <b>Диапазон:</b> <code>{words}</code>\n| <b>Кол-во слов:</b> <code>{qty}</code>\n| <b>Результат:</b>\n\n{txt}')
                            return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя вызвать 0 случайных значений.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите число больше нуля.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя вызвать больше случайных чисел, чем 1000.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите число меньше 1000.')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали лишь два аргумента, когда необходимо минимум 3.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите больше аргументов.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали лишь один аргумент, когда необходимо минимум 3.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите больше аргументов.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали ни единого аргумента.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите минимум 3 аргумента.')
            return
        
    @loader.command()
    async def randval(self, message):
        '''[ значения, разделенные знаком-разделителем(подефолт - запятая) ] - вывести случайное значение из заданных'''
        args = utils.get_args_raw(message)
        if args:
            if self.config['sep'] in args:
                values = args.split(self.config['sep'])
                result = random.choice(values) # Вывод результата
                await utils.answer(message, f'| <b>Режим:</b> <code>случайное значение</code>\n| <b>Диапазон:</b> <code>{values}</code>\n| <b>Результат:</b> <code>{result}</code>')
                return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали лишь одно слово, хотя нужно минимум 2.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите больше слов.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали ни единого аргумента.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите минимум два слова.')
            return
        
    @loader.command()
    async def randvals(self, message):
        '''[ кол-во значений ], [ значения, разделенные знаком-разделителем(дефолт - запятая) ] - вывести несколько случайных значений из заданных'''
        args = utils.get_args_raw(message)
        if args:
            if self.config['sep'] in args:
                if len(args.split(self.config['sep'])) > 2:
                    try:
                        qty = int(args.split(self.config['sep'])[0])
                    except ValueError:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nПервым аргументом должно быть целочисленное, обозначающее кол-во слов, которое вы хотите получить.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите первым аргументом целочисленное.')
                        return
                    if qty <= 1000:
                        if qty > 0:
                            values = args.split(self.config['sep'])[1:]
                            txt = ''
                            g = 0
                            for i in range(qty):
                                result = random.choice(values)
                                if g < 3 and g != 0:
                                    txt += ' | '
                                if g < 2:
                                    txt += f'{result}'
                                    g += 1
                                else:
                                    txt += f'{result}\n'
                                    g = 0
                            # Вывод результата
                            await utils.answer(message, f'| <b>Режим:</b> <code>случайные значения</code>\n| <b>Диапазон:</b> <code>{values}</code>\n| <b>Кол-во слов:</b> <code>{qty}</code>\n| <b>Результат:</b>\n\n{txt}')
                            return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя вызвать 0 случайных значений.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите число больше нуля.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя вызвать больше случайных чисел, чем 1000.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите число меньше 1000.')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали лишь два аргумента, когда необходимо минимум 3.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите больше аргументов.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали лишь один аргумент, когда необходимо минимум 3.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите больше аргументов.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали ни единого аргумента.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите минимум 3 аргумента.')
            return
        
    @loader.command()
    async def randuser(self, message):
        '''- получить случайного пользователя из чата'''
        if message.is_private == False:
            users = []
            async for user in self.client.iter_participants(message.chat_id):
                users.append(user)
            result = random.choice(users)
            full = await self.client.get_entity(result)
            name = full.first_name
            id = result.id
            txt = f'<a href="tg://user?id={id}">{name}</a> (<code>{id}</code>)' # Вывод результата
            await utils.answer(message, f'| <b>Режим:</b> <code>случайный юзер</code>\n| <b>Результат:</b> {txt}')
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭта команда может работать только в группах.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nИспользуйте команду в группе.')
            return

    @loader.command()
    async def randusers(self, message):
        '''[ кол-во ] - получить несколько случайных пользователей из чата (-r после кол-ва, чтобы не повторялись)'''
        args = utils.get_args_raw(message)
        if message.is_private == False:
            if args:
                if ' ' not in args:
                    try:
                        qty = int(args)
                    except ValueError:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nПервый аргумент может быть только целочисленным.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите целочисленное значение.')
                        return
                    if qty <= 50:
                        if qty > 0:
                            users = []
                            async for user in self.client.iter_participants(message.chat_id):
                                users.append(user)
                            gusers = []
                            for i in range(qty):
                                gusers.append(random.choice(users))
                            txt = 'Ник | Юзернейм | ID\n'
                            for user in gusers:
                                txt += f'<a href="tg://user?id={user.id}">{user.first_name}</a> (<code>{user.id}</code>)\n' # Вывод результата
                            await utils.answer(message, f'| <b>Режим:</b> <code>случайные юзеры</code>\n| <b>Кол-во юзеров:</b> <code>{qty}</code>\n| <b>Результат:</b>\n\n{txt}')
                            return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя вызвать 0 случайных пользователей'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите кол-во, которое больше нуля.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя делать кол-во запрашиваемых людей больше 50.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите меньшее кол-во.')
                        return
                if ' ' in args:
                    if args.split(' ')[1] == '-r':
                        try:
                            qty = int(args.split(' ')[0])
                        except ValueError:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nПервый аргумент может быть только целочисленным.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите целочисленное значение.')
                            return
                        if qty <= 50:
                            if qty > 0:
                                users = []
                                async for user in self.client.iter_participants(message.chat_id):
                                    users.append(user)
                                if len(users) > qty:
                                    gusers = []
                                    for i in range(qty):
                                        uu = random.choice(users)
                                        gusers.append(uu)
                                        users.remove(uu)
                                    txt = ''
                                    for user in gusers:
                                        txt += f'<a href="tg://user?id={user.id}">{user.first_name}</a> (<code>{user.id}</code>)\n' # Вывод результата
                                    await utils.answer(message, f'| <b>Режим:</b> <code>случайные юзеры -r</code>\n| <b>Кол-во юзеров:</b> <code>{qty}</code>\n| <b>Результат:</b>\n\n{txt}')
                                    return
                                else:
                                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЧисло полученных участников группы больше или равно запрашиваемому вами кол-ву, в таком случае рандом без повторейний невозможен.'
                                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите меньше кол-во.')
                                    return
                            else:
                                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя вызвать 0 случайных пользователей.'
                                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите кол-во, которое больше нуля.')
                                return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя делать кол-во запрашиваемых людей больше 50.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите меньшее кол-во.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        f'\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНеизхвестный аргумент - {args.split(" ")[1]}'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nЕсли вы хотите результат без повторей, введите "-r"')
                        return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргументы.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргументы.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЭта команда может работать только в группах.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nИспользуйте команду в группе.')
            return

    @loader.command()
    async def randfloat(self, message):
        '''[ от ] [ до ] [ кол-во знаков, после запятой ] - вывести случайное дробное число'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' in args: 
                if len(args) > 2:
                    if len(args.split(' ')) < 4:
                        try:
                            float1 = float(args.split(' ')[0])
                        except ValueError:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели неправильное первое значение.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите дробное значение.')
                            return
                        try:
                            float2 = float(args.split(' ')[1])
                        except ValueError:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели неправильное второе значение.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите дробное значение.')
                            return
                        try:
                            qtyv = int(args.split(' ')[2])
                        except ValueError:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели неправильный третий аргумент.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите для третего аргумент целочисленное значение.')
                            return
                        if float1 < float2:
                            if qtyv <= 15 and qtyv > 0:
                                result = random.uniform(float1, float2)
                                result = round(result - 0.5 * 10**(-2), qtyv) # Вывод результата
                                await utils.answer(message, f'| <b>Режим:</b> <code>случайное дробное</code>\n| <b>Диапазон:</b> <code>{float1} - {float2}</code>\n| <b>Знаков после запятой:</b> <code>{qtyv}</code>\n| <b>Результат:</b>\n\n{result}')
                                return
                            else:
                                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nКол-во знаков после запятой не может превышать 15 или быть меньше 1.'
                                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент в упомянутом выше диапазоне.')
                                return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nПервое значение должно быть меньше, чем второе.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nПопробуйте поменять значения местами.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели больше аргументов, чем нужно.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите только два аргумента.')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели больше аргументов, чем нужно.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите только три аргумента.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы ввели всего один аргумент.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите два аргумента, этого требует команда.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не ввели аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите два аргумента, этого требует команда.')
            return
                
    @loader.command()
    async def randfloats(self, message):
        '''[ кол-во ] [ от ] [ до ] [ кол-во знаков, после запятой] - вывести несколько случайных дробных чисел'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' in args:
                if len(args.split(' ')) > 3:
                    if len(args.split(' ')) < 5:
                        try:
                            qty = int(args.split(' ')[0])
                        except ValueError:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nПервый аргумент может быть только целочисленным.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите целочисленный аргумент.')
                            return
                        try:
                            float1 = float(args.split(' ')[1])
                        except ValueError:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВторой аргумент может быть только дробным.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите второй аргумент в виде дробного значения.')
                            return
                        try:
                            float2 = float(args.split(' ')[2])
                        except ValueError:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nТретий аргумент может быть только дробным.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите третий аргумент в виде дробного значения.')
                            return
                        try:
                            qtyv = int(args.split(' ')[3])
                        except ValueError:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЧетвертый аргумент может быть только целочисленным.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите целочисленный аргумент.')
                            return
                        if float1 < float2:
                            if qty <= 1000:
                                if qty > 0:
                                    if qtyv <= 15 and qtyv > 0:
                                        txt = ''
                                        g = 0
                                        for i in range(qty):
                                            result = random.uniform(float1, float2)
                                            result = round(result - 0.5 * 10**(-2), qtyv)
                                            if g < 3 and g != 0:
                                                txt += ' | '
                                            if g < 2:
                                                txt += f'{result}'
                                                g += 1
                                            else:
                                                txt += f'{result}\n'
                                                g = 0
                                        # Вывод результата
                                        await utils.answer(message, f'| <b>Режим:</b> <code>случайные дробные</code>\n| <b>Диапазон:</b> <code>{float1} - {float2}</code>\n| <b>Знаков после запятой:</b> <code>{qtyv}</code>\n| <b>Кол-во чисел:</b> <code>{qty}</code>\n| <b>Результат:</b>\n\n{txt}')
                                    else:
                                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nКол-во знаков после запятой не может превышать 15 или быть меньше 1.'
                                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент в упомянутом выше диапазоне.')
                                        return
                                else:
                                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя вызвать 0 случайных значений.'
                                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите число больше нуля.')
                                    return
                            else:
                                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя вызвать больше случайных чисел, чем 1000.'
                                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nВведите число меньше 1000.')
                                return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nЗначение "от" не может быть больше, чем значение "до"'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nПопробуйте поменять значения местами.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали слишком много аргументов.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите 4 аргумента.')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали слишком мало аргументов.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите 4 аргумента.')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nНельзя вызвать больше случайных чисел, чем 1000.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите 4 аргумента.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали лишь 1 аргумент.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите 4 аргумента.')
            return
        
    @loader.command()
    async def rb(self, message):
        '''- вывести случайное логическое значение (True / False)''' # Вывод результата
        await utils.answer(message, f'| <b>Режим:</b> <code>случайное логическое значение</code>\n| <b>Результат:</b> <code>{random.choice([True, False])}</code>')
        
    @loader.command()
    async def randb(self, message):
        '''[ кол-во бит ] - вывести битное целочисленное'''
        args = utils.get_args_raw(message)
        if args:
            try:
                bits = int(args)
            except ValueError:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nКол-во бит должно быть только целочисленным значением.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите целочисленное значение.')
                return
            if bits < 0:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nКол-во бит не может быть меньше нуля, тк бит - единица информации и не может иметь отрицательный показатель.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите большее кол-во бит.')
                return
            if bits == 0:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nКол-во бит не может равняться нулю, так как любая информация имеет свой вес.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите большее кол-во бит.')
                return
            if bits > 14285:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не можете указать больше бит, чем 14285 (я сам высчитывал).'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите меньшее кол-во бит.')
                return
            # Вывод результата
            await utils.answer(message, f'| <b>Режим:</b> <code>случайное битное целочисленное</code>\n| <b>Кол-во бит:</b> <code>{bits}</code>\n| <b>Результат:</b> <code>{random.getrandbits(bits)}</code>')

    @loader.command()
    async def randstr(self, message):
        '''[ кол-во символов ] [ символы через пробел ] - сгенерировать случайную строку'''
        args = utils.get_args_raw(message)
        if args:
            if ' ' in args:
                if len(args) > 3:
                    try:
                        n = int(args.split(' ')[0])
                    except ValueError:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nКол-вом букв может быть только целочесленное значение.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите в первом аргументе целочисленное значение.')
                        return
                    if n > 0:
                        if n < 1000:
                            alphabet = args.split(' ')[1:]
                            txt = ''
                            for i in range(n):
                                txt += f'{random.choice(alphabet)}'
                            await utils.answer(message, f'| <b>Режим:</b> <code>случайная строка</code>\n| <b>Кол-во символов:</b> <code>{n}</code>\n| <b>Символы:</b> <code>{alphabet}</code>\n| <b>Результат:</b> <code>{txt}</code>')
                            return
                        else:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали в кол-во символов слишком болье число.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУУкажиет число в диапазоне 0-999.')
                            return
                    else:
                        await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                        '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nКол-вом букв может быть только целочесленное значение больше нуля.'
                        '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите в кол-во букв число больше нуля.')
                        return
                else:
                    await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                    '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nДолжно быть как минимум 3 аргумента, а именно: кол-во букв и перечень букв, букв должно быть минимум 2.'
                    '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите больше букв')
                    return
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы указали только 1 аргумент, хотя должно быть минимум 3, а именно: кол-во букв и перечень букв, букв должно быть минимум 2.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите больше аргументов.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{utils.escape_html(self.get_prefix())}{inspect.currentframe().f_code.co_name}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргументы.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргументы, как минимум 3.')
            return
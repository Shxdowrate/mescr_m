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

__version__ = (1 ,0 ,0)

class Passwords(loader.Module):
    '''Модуль для создания паролей.\nDeveloper: @mescr_m'''

    strings = {
        'name':'Passwords',
        'password_numbers':'Какие цифры можно использовать в пароле?',
        'alphabets':'Буквы каких алфавитов можно использовать в пароле?',
        'custom_symbols':'Ваши символы, которые можно использоватьв пароле при "#"'
    }
    # Буквы русского языкa
    ru = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    en = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    de = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ä', 'ö', 'ü', 'ß']
    fr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'à', 'â', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'î', 'ï', 'ô', 'œ', 'ù', 'û', 'ü']
    kz = ['а', 'ә', 'б', 'в', 'г', 'ғ', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'қ', 'л', 'м', 'н', 'ң', 'о', 'ө', 'п', 'р', 'с', 'т', 'у', 'ұ', 'ү', 'ф', 'х', 'һ', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'і', 'ь', 'э', 'ю', 'я']

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "password_numbers",
                ['0','1','2','3','4','5','6','7','8','9'],
                lambda: self.strings("password_numbers"),
                validator=loader.validators.MultiChoice(
                    [
                        '0','1','2','3','4','5','6','7','8','9',
                    ]
                ),
            ),
            loader.ConfigValue(
                "alphabets",
                ['🇬🇧 English'],
                lambda: self.strings("alphabets"),
                validator=loader.validators.MultiChoice(
                    [
                        '🇷🇺 Русский','🇬🇧 English','🇩🇪 Deutsch','🇫🇷 Français','🇰🇿 Қазақша'
                    ]
                ),
            ),
            loader.ConfigValue(
                "custom_symbols", ['!', '?', '-'],
                lambda: self.strings("alphabets"),
                validator=loader.validators.Series(),
            )
        )

    @loader.command()
    async def password(self, message):
        '''[ текст ] - сгенерировать пароль'''
        args = utils.get_args_raw(message)
        if args:
            if '*' in args or '$' in args or '#' in args:
                txt = ''
                for ent in args:
                    if ent == '%':
                        if not self.config['password_numbers'] or len(self.config['password_numbers']) == 1:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВ конфиге указано лишь одна цифра или не указано ни одной.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите хотя бы две цифры, которые можно использовать в вашем пароле.')
                            return
                        txt += random.choice(self.config['password_numbers'])
                    elif ent == '$':
                        alphabets = self.config['alphabets']
                        if not alphabets:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВ конфиге не указано ни одного алфавита.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите хотя бы один алфавит, буквы которого можно использовать в вашем пароле.')
                            return
                        alphabetss = []
                        if '🇷🇺 Русский' in alphabets:
                            for val in self.ru:
                                alphabetss.append(val)
                        if '🇬🇧 English' in alphabets:
                            for val in self.en:
                                alphabetss.append(val)
                        if '🇩🇪 Deutsch' in alphabets:
                            for val in self.de:
                                alphabetss.append(val)
                        if '🇫🇷 Français' in alphabets:
                            for val in self.fr:
                                alphabetss.append(val)
                        if '🇷🇺🇰🇿 Қазақша' in alphabets:
                            for val in self.kz:
                                alphabetss.append(val)
                        txt += random.choice(alphabetss)
                    elif ent == '#':
                        if not self.config['custom_symbols'] or len(self.config['custom_symbols']) == 1:
                            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message}</code>'
                            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВ конфиге "custom_symbols" указан лишь один символ или ни одного.'
                            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите хотя бы два символа в "custom_symbols".')
                            return
                        txt += random.choice(self.config['custom_symbols'])
                    else:
                        txt += ent
                await utils.answer(message, f'<emoji document_id=5328272518304243616>💠</emoji> Ваш пароль: {txt}')
            else:
                await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message}</code>'
                '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали ни одного из служебных символов (*, #, $) в генераторе, генерация не имеет смысла.'
                '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите хотя бы один служебный символ.')
                return
        else:
            await utils.answer(message, f'<emoji document_id=5980953710157632545>🚫</emoji> <b>Error</b> // <code>{message}</code>'
            '\n\n<emoji document_id=5818973781707722673>🗣</emoji> <b><u>Суть ошибки:</u></b>\nВы не указали аргумент.'
            '\n\n<emoji document_id=5821302890932736039>🗣</emoji> <b><u>Способы исправления:</u></b>\nУкажите аргумент, в котором должен быть хотя бы один служебный символ.')
            return
            
    @loader.command()
    async def passwordhelp(self, message):
        '''- вывести помощь по модулю'''
        txt = f'<b>Как генерировать пароль в <u>Passwords</u>?</b>\n\n'
        txt += f'Введите команду <code>{self.get_prefix()}password</code>, а после нее текст, в котором должен быть хотя бы один из следующих символов: % $ #\n'
        txt += f'<code>%</code> - вставляет случайную цифру\n<code>$</code> - вставляет случайную букву\n<code>#</code> - вставляет случайный кастомный символ\n\n'
        txt += f'Так же не забудьте заглянуть в конфиг.'
        await utils.answer(message, txt)

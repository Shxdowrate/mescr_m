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

__verion__ = (1, 0, 0)

class ShortHelp(loader.Module):
    '''Просмотреть список установленных модулей без дополнительной информации.\nDeveloper: @mescr_m'''

    strings = {
        'name':'ShortHelp',
        'core':'Эмоджи встроенных модулей',
        'core_modules':'Отображать встроеные модули?',
        'loaded':'Эмоджи загруженных модулей',
        'sort':'Как сортировать модули?',
        'lowercase':'Привести названия модулей к нижнему регистру?',
        'modulecount':'Отображать количество модулей?',
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "core", '🧩',
                lambda: self.strings("core"),
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "core_modules", True,
                lambda: self.strings("core_modules"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "loaded", '🧩',
                lambda: self.strings("loaded"),
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "lowercase", False,
                lambda: self.strings("lowercase"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "modulecount", True,
                lambda: self.strings("modulecount"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "sort", 'alphabet',
                lambda: self.strings("sort"),
                validator=loader.validators.Choice(['alphabet', 'length'])
            ),
        )

    @loader.command()
    async def shelp(self, message):
        '''- показать хелп'''
        modules = self.allmodules.modules
        txt = ''
        core_modules = []
        core_v = 0
        loaded_modules = []
        loaded_v = 0

        # Получение модулей
        for module in modules:
            modulename = module.strings['name']
            if self.config['lowercase'] == True:
                modulename = modulename.lower()
            if module.__origin__.startswith("<core"):
                core_modules.append(modulename)
                core_v += 1
            else:
                loaded_modules.append(modulename)
                loaded_v += 1

        # Сортировка
        def sorting_key(module):
            if self.config['sort'] == 'length':
                return (len(module), module)
            elif self.config['sort'] == 'alphabet':
                return module
        core_modules = sorted(core_modules, key=sorting_key)
        loaded_modules = sorted(loaded_modules, key=sorting_key)

        # Создаение визуального списка модулей
        if self.config['core_modules'] == True:
            for module in core_modules:
                txt += f'{self.config["core"]} {module}\n'
        for module in loaded_modules:
            txt += f'{self.config["loaded"]} {module}\n'

        # Отображение кол-ва модулей
        if self.config['modulecount'] == True:
            mc = f'\n{self.config["core"]} Встроенных: {core_v}, {self.config["loaded"]} Загруженных: {loaded_v}'
        else:
            mc = ''

        # Вывод
        await utils.answer(message, f'<emoji document_id=5188377234380954537>🌘</emoji> <b>Ваши модули:</b>{mc}\n\n{txt}')
            
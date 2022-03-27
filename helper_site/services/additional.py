import re

def instance_slug(instance):
    return instance.title


def replace_space_with_character(value, character: str = "-"):
    if isinstance(character, str):
        res = re.sub(r'[^-a-zA-Zа-яёА-ЯЁ0-9_]', character, value)
        return re.sub(r'-{2,10}', character, res)
    else:
        raise TypeError(f"{character} must be str")


def get_context(self, model_name, name_context, add_context, **kwargs):
    # получаем базовую реализацию контекста
    context = super(model_name, self).get_context_data(**kwargs)
    # Добавляем новую переменную к контексту и инициализируем её  значением
    context[name_context] = add_context
    return context

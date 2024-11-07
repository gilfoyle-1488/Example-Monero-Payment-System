import re
from aiogram.filters import BaseFilter
from aiogram.types import Message


# Функция для проверки адреса
def is_valid_monero_address(address):
    pattern = r'^(?:[48][0-9AB]|8[0-9AB]|4[1-9A-HJ-NP-Za-km-z]{12}(?:[1-9A-HJ-NP-Za-km-z]{30})?)[1-9A-HJ-NP-Za-km-z]{93}$'
    return bool(re.match(pattern, address))


class CheckForDigit(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        print(f"фильтр message: {message.text}")

        # Проверка с использованием регулярного выражения для чисел
        if bool(re.fullmatch(r'^\d+(\.\d+)?$', message.text)):
            # Преобразуем строку в число
            try:
                value = float(message.text)
                if value > 0:
                    return True
                else:
                    await message.answer(text="Введите число больше 0.")
                    return False
            except ValueError:
                # Если преобразование не удается, возвращаем False
                await message.answer(text="Произошла ошибка при обработке числа.")
                return False

        await message.answer(text="Введите целое или дробное число (например, 15 или 200.20), больше 0.")
        return False
# ComfyUI/custom_nodes/ComfyUI-mikheys/__init__.py

# Импортируем класс нашей ноды из файла wan_resolution_node.py
from .nodes.wan_resolution_node import WanOptimalResolution 
from .nodes.image_info_node import WanImageDimensions # <--- ДОБАВЛЕНО

# Словарь, который ComfyUI будет использовать для поиска классов нод
# Ключ - это уникальное имя класса для ComfyUI (может совпадать с именем класса Python)
# Значение - это сам класс Python
NODE_CLASS_MAPPINGS = {
    "WanOptimalResolution": WanOptimalResolution,  # "ИмяДляComfyUI": ИмяКлассаВPython
    "WanImageDimensions": WanImageDimensions  # <--- ДОБАВЛЕНО
}

# Словарь для отображаемых имен нод в интерфейсе ComfyUI
# Ключ - тот же, что и в NODE_CLASS_MAPPINGS
# Значение - строка, которую пользователь увидит в меню
NODE_DISPLAY_NAME_MAPPINGS = {
    "WanOptimalResolution": "WAN Optimal Resolution Selector",
    "WanImageDimensions": "WAN Show Image Dimensions" # <--- ДОБАВЛЕНО
}

# Сообщаем ComfyUI, что экспорт прошел успешно (необязательно, но полезно для отладки)
print("-------------------------------------------------------------------------------------------------------------------")
print("    MIKHEYS Custom Utils: Node pack loaded")
print("      - WanOptimalResolution (WAN Optimal Resolution Selector)")
print("      - WanImageDimensions (WAN Show Image Dimensions)") # <--- ДОБАВЛЕНО
print("-------------------------------------------------------------------------------------------------------------------")


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] # Обязательно для ComfyUI
# ComfyUI/custom_nodes/wan_utils/nodes/image_info_node.py (предполагая твою новую структуру)

import torch

class WanImageDimensions:
    CATEGORY = "wan_utils/info"
    RETURN_TYPES = ("STRING", "INT", "INT")
    RETURN_NAMES = ("dimensions_text", "width", "height")
    FUNCTION = "get_dimensions"

    # Говорим ComfyUI, что эта нода изменяет свои виджеты (выходные данные на самой ноде)
    OUTPUT_NODE = True 

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            },
            "hidden": { # Скрытые входы используются для создания виджетов, которые не подключаются
                "info_display": ("STRING", {"forceInput": True, "default": "Подключите изображение..."}), 
                # "forceInput": True делает так, что этот "вход" не будет отображаться как пин для подключения,
                # а будет представлен виджетом. Однако, для простого отображения текста, лучше это убрать
                # и обновлять через возвращаемое значение UI.

                # Более правильный способ для отображения информации, обновляемой нодой:
                # Мы определим его здесь, а обновлять будем через возвращаемое значение UI в `get_dimensions`
                "unique_id": ("UNIQUE_ID",), # Для обновления виджетов
                "displayed_text": ("STRING", {"multiline": True, "default": "Размеры: [неизвестно]"}),
            }
        }

    def get_dimensions(self, image: torch.Tensor, unique_id=None, displayed_text=None): # Добавляем аргументы для скрытых входов
        _batch_size, img_height, img_width, _channels = image.shape
        
        dimensions_text_output = f"{img_width}x{img_height}"
        
        # Текст, который мы хотим видеть на самой ноде
        ui_displayed_text = f"Размеры: {img_width}x{img_height}\nШирина: {img_width}px\nВысота: {img_height}px"

        # Возвращаем основные выходы и словарь для обновления UI (виджетов)
        return {
            "ui": {"displayed_text": [ui_displayed_text]}, # Обновляем виджет "displayed_text"
            "result": (dimensions_text_output, img_width, img_height)
        }
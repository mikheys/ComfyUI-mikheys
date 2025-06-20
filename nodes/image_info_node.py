# ComfyUIcustom_nodeswan_utilsimage_info_node.py

import torch

class WanImageDimensions
    CATEGORY = wan_utilsinfo # Можем создать подкатегорию для информационных нод
    RETURN_TYPES = (STRING, INT, INT)
    RETURN_NAMES = (dimensions_text, width, height)
    FUNCTION = get_dimensions

    @classmethod
    def INPUT_TYPES(s)
        return {
            required {
                image (IMAGE,),
            }
        }

    def get_dimensions(self, image torch.Tensor)
        # Изображение в ComfyUI обычно имеет формат (batch_size, height, width, channels)
        # Мы берем размеры первого изображения в батче
        _batch_size, img_height, img_width, _channels = image.shape
        
        dimensions_text = f{img_width}x{img_height}
        
        return (dimensions_text, img_width, img_height)

# Если ты хочешь, чтобы эту ноду можно было использовать для вывода текста
# в стандартную ноду ShowText (которая ожидает список строк), можно сделать так
# class WanImageDimensionsForShowText
#     CATEGORY = wan_utilsinfo
#     RETURN_TYPES = ([STRING],) # Возвращаем список строк
#     RETURN_NAMES = (text,)
#     FUNCTION = get_dimensions_for_text

#     @classmethod
#     def INPUT_TYPES(s)
#         return {
#             required {
#                 image (IMAGE,),
#             }
#         }

#     def get_dimensions_for_text(self, image torch.Tensor)
#         _batch_size, img_height, img_width, _channels = image.shape
#         dimensions_text = fImage Dimensions {img_width}x{img_height}
#         return ([dimensions_text],) # Возвращаем как список
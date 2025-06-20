# ComfyUI/custom_nodes/ComfyUI-mikheys/wan_resolution_node.py

import torch
import re # Для регулярных выражений, чтобы извлечь '1080p', '720p' и т.д.

# Твой список разрешений
PREDEFINED_RESOLUTIONS_DATA = [
    # 1080p
    ("1920x832 (21:9, 1080p)", "1920x832"),
    ("832x1920 (9:21, 1080p)", "832x1920"),
    ("1920x1280 (3:2, 1080p)", "1920x1280"),
    ("720x1088 (2:3, 1080p)", "720x1088"),
    # 720p
    ("1280x720 (16:9, 720p)", "1280x720"),
    ("720x1280 (9:16, 720p)", "720x1280"),
    ("1296x864 (3:2, 720p)", "1296x864"),
    ("864x1296 (2:3, 720p)", "864x1296"),
    ("1024x1024 (1:1, 720p)", "1024x1024"),
    ("1280x544 (21:9, 720p)", "1280x544"),
    ("544x1280 (9:21, 720p)", "544x1280"),
    ("1104x832 (4:3, 720p)", "1104x832"),
    ("832x1104 (3:4, 720p)", "832x1104"),
    ("960x960 (1:1, 720p)", "960x960"),
    # 540p
    ("960x544 (16:9, 540p)", "960x544"),
    ("544x960 (9:16, 540p)", "544x960"),
    ("960x640 (3:2, 540p)", "960x640"),
    ("368x544 (2:3, 540p)", "368x544"),
    # 480p
    ("832x480 (16:9, 480p)", "832x480"),
    ("480x832 (9:16, 480p)", "480x832"),
    ("816x544 (3:2, 480p)", "816x544"),
    ("320x480 (2:3, 480p)", "320x480"),
    ("832x624 (4:3, 480p)", "832x624"),
    ("624x832 (3:4, 480p)", "624x832"),
    ("720x720 (1:1, 480p)", "720x720"),
    ("512x512 (1:1, 480p)", "512x512"),
]

PARSED_RESOLUTIONS = []
RESOLUTION_GROUPS = set()

for desc, wh_str in PREDEFINED_RESOLUTIONS_DATA:
    try:
        w_str, h_str = wh_str.split('x')
        w = int(w_str)
        h = int(h_str)
        aspect_ratio_val = w / h if h != 0 else float('inf')

        match = re.search(r'(\d+p)', desc)
        group_key = match.group(1) if match else "unknown"
        RESOLUTION_GROUPS.add(group_key)

        PARSED_RESOLUTIONS.append({
            "description": desc,
            "width": w,
            "height": h,
            "group_key": group_key,
            "aspect_ratio_val": aspect_ratio_val
        })
    except Exception as e:
        print(f"Error parsing resolution data '{desc}, {wh_str}': {e}")

SORTED_RESOLUTION_GROUPS = sorted(list(RESOLUTION_GROUPS), key=lambda x: int(x[:-1]), reverse=True)

# Определяем значение по умолчанию для выпадающего списка
# Убедимся, что "720p" есть в списке, иначе возьмем первый элемент
DEFAULT_RESOLUTION_GROUP = "720p"
if DEFAULT_RESOLUTION_GROUP not in SORTED_RESOLUTION_GROUPS:
    if SORTED_RESOLUTION_GROUPS: # Если список не пуст
        DEFAULT_RESOLUTION_GROUP = SORTED_RESOLUTION_GROUPS[0]
    else: # Если список групп пуст (маловероятно с вашими данными, но для надежности)
        DEFAULT_RESOLUTION_GROUP = "unknown" # или какое-то другое значение по умолчанию


class WanOptimalResolution:
    CATEGORY = "wan_utils"
    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "selected_resolution_info")
    FUNCTION = "get_optimal_resolution"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                # Изменяем определение для resolution_group, чтобы указать default
                "Base resolution": (SORTED_RESOLUTION_GROUPS, {
                    "default": DEFAULT_RESOLUTION_GROUP
                }),
            },
        }

    def get_optimal_resolution(self, image: torch.Tensor, resolution_group: str):
        _batch_size, img_height, img_width, _channels = image.shape
        
        if img_height == 0 or img_width == 0:
            print("Warning: Input image has zero height or width. Returning default 512x512.")
            return (512, 512, "Error: Invalid input image dimensions")

        input_aspect_ratio = img_width / img_height

        candidate_resolutions = [
            res for res in PARSED_RESOLUTIONS if res["group_key"] == resolution_group
        ]

        if not candidate_resolutions:
            print(f"Warning: No resolutions found for group '{resolution_group}'. Returning default based on first available or 512x512.")
            # Попробуем вернуть первое доступное разрешение из общего списка, если есть
            first_res = PARSED_RESOLUTIONS[0] if PARSED_RESOLUTIONS else {"width": 512, "height": 512, "description": "Default 512x512 (No candidates)"}
            return (first_res["width"], first_res["height"], f"Error: No resolutions for {resolution_group}. Used: {first_res['description']}")

        best_match = None
        min_aspect_diff = float('inf')

        for res_data in candidate_resolutions:
            diff = abs(res_data["aspect_ratio_val"] - input_aspect_ratio)
            
            if diff < min_aspect_diff:
                min_aspect_diff = diff
                best_match = res_data
            elif diff == min_aspect_diff:
                pass 
        
        if best_match is None:
            print(f"Error: Could not determine best match for group {resolution_group}. Using first candidate.")
            best_match = candidate_resolutions[0]

        return (best_match["width"], best_match["height"], best_match["description"])
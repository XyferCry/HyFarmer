import system.lib.minescript as m
import time, random, math
from java import JavaClass

def look(target_yaw, target_pitch, duration=0.22, steps=70):
    CONFIRM_YAW_PITCH = True  # If it should manually correct at the end (If you need exact Yaw and Pitch

    sy, sp = m.player_orientation()

    def angle_diff(a, b):
        return (b - a + 180) % 360 - 180

    dy = angle_diff(sy, target_yaw)
    dp = target_pitch - sp

    if abs(dy) < 1.0 and abs(dp) < 1.0:
        m.player_set_orientation(target_yaw, target_pitch)
        return

    step_time = duration / steps

    power = 5

    for i in range(1, steps + 1):
        t = i / steps

        if t < 0.5:
            s = 0.5 * (2 * t) ** power
        else:
            s = 1 - 0.5 * (2 * (1 - t)) ** power

        jy = (1 - abs(0.5 - t) * 2) * 0.2

        m.player_set_orientation(
            sy + dy * s + random.uniform(-jy, jy),
            sp + dp * s + random.uniform(-jy * 0.7, jy * 0.7)
        )

        time.sleep(step_time)

    if CONFIRM_YAW_PITCH:
        m.player_set_orientation(target_yaw, target_pitch)

def json_entities():
    entities = m.entities()

    if not entities:
        return []

    ref = entities[0].position

    def dist(e):
        x1, y1, z1 = ref
        x2, y2, z2 = e.position
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

    entities_sorted = sorted(entities, key=dist)

    json_entities = []

    for entity in entities_sorted:
        entry = {
            "name": entity.name,
            "type": entity.type,
            "uuid": entity.uuid,
            "position": entity.position,
            "orientation": [entity.yaw, entity.pitch]
        }
        json_entities.append(entry)

    return json_entities

def target_yaw_pitch_entity(player_pos, entity_pos):
    px, py, pz = player_pos
    ex, ey, ez = entity_pos

    dx = ex - px
    dy = ey - py
    dz = ez - pz

    yaw = math.degrees(math.atan2(-dx, dz))
    pitch = math.degrees(-math.atan2(dy, math.sqrt(dx * dx + dz * dz)))

    return yaw, pitch


def get_tablist():
    m.set_default_executor(m.script_loop)

    Minecraft = JavaClass("net.minecraft.client.Minecraft")
    mc = Minecraft.getInstance()

    connection = mc.getConnection()
    if not connection:
        return []

    players = connection.getOnlinePlayers()
    tablist = []

    for info in players:
        comp = info.getTabListDisplayName()
        if not comp:
            continue

        text = comp.getString()
        tablist.append(text)

    return tablist

def hotbar_dict():
    player_items = m.player_inventory()

    hotbar_items = {}

    for item in player_items:
        if 0 <= item.slot <= 8:
            hotbar_items[item.slot] = item

    return hotbar_items

def find_hotbar_item(target_item):
    if target_item.startswith("minecraft:"):
        target_item = target_item.split(":")[1]

    hotbar = hotbar_dict()
    found_slots = []

    for slot, item in hotbar.items():
        if target_item == item.item.split(":")[1]:
            found_slots.append(slot)

    return found_slots

def get_selected_slot():
    for item in m.player_inventory():
        if item.selected:
            return item.slot
    return None

## Hypixel Exclusive
def extract_number(text):
    num = ""
    for c in text:
        if c.isdigit():
            num += c
        elif num:
            break
    return num if num else "0"

def get_scoreboard_info():
    data = {
        "area": None,
        "server": None,
        "gems": None,
        "copper": None,
        "speed": None,
        "farming_fortune": None,
        "strength": None,
        "pet_name": None,
        "pet_level": None,
        "profile": None,
        "sb_level": None,
        "bank": None,
        "interest": None,
        "farming_level": None
    }

    try:
        with m.script_loop:
            mc = JavaClass("net.minecraft.client.Minecraft").getInstance()
            connection = mc.getConnection()
            if connection is None:
                return data

            for entry in connection.getOnlinePlayers():
                display = entry.getTabListDisplayName()
                if display is None:
                    continue

                text = display.getString().strip()

                try:
                    if "Area:" in text:
                        data["area"] = text.split("Area:")[1].strip()

                    elif "Server:" in text:
                        data["server"] = text.split("Server:")[1].strip()

                    elif "Gems:" in text:
                        data["gems"] = int(extract_number(text))

                    elif "Copper:" in text:
                        data["copper"] = int(extract_number(text))

                    elif "Speed:" in text:
                        data["speed"] = int(extract_number(text))

                    elif "Farming Fortune:" in text:
                        data["farming_fortune"] = int(extract_number(text))

                    elif "Strength:" in text:
                        data["strength"] = int(extract_number(text))

                    elif "[Lvl " in text:
                        lvl_start = text.find("[Lvl ")
                        lvl_end = text.find("]", lvl_start)
                        if lvl_end != -1:
                            level = int(text[lvl_start+5:lvl_end])
                            pet = text[lvl_end+2:].strip()
                            data["pet_level"] = level
                            data["pet_name"] = pet

                    elif "Profile:" in text:
                        data["profile"] = text.split("Profile:")[1].strip()

                    elif "SB Level:" in text:
                        data["sb_level"] = int(extract_number(text))

                    elif "Bank:" in text:
                        data["bank"] = int(extract_number(text))

                    elif "Interest:" in text:
                        data["interest"] = text.split("Interest:")[1].strip()

                    elif "Farming " in text and "%" in text:
                        data["farming_level"] = int(extract_number(text))

                except:
                    continue

    except:
        return data

    return data

def find_hypixel_id(hypixel_id):

    hotbar = hotbar_dict()
    found_slots = []

    for slot, item in hotbar.items():
        if hypixel_id == get_hypixel_id(item):
            found_slots.append(slot)

    return found_slots


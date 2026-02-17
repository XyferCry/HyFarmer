import system.lib.minescript as minescript
import random
import time

CONFIRM_YAW_PITCH = False # If it should manuallly correct at the end (If you need exact Yaw and Pitch

def look(target_yaw, target_pitch, duration=0.22, steps=70):
    sy, sp = minescript.player_orientation()

    def angle_diff(a, b):
        return (b - a + 180) % 360 - 180

    dy = angle_diff(sy, target_yaw)
    dp = target_pitch - sp

    if abs(dy) < 1.0 and abs(dp) < 1.0:
        minescript.player_set_orientation(target_yaw, target_pitch)
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

        minescript.player_set_orientation(
            sy + dy * s + random.uniform(-jy, jy),
            sp + dp * s + random.uniform(-jy * 0.7, jy * 0.7)
        )

        time.sleep(step_time)

    if CONFIRM_YAW_PITCH:
        minescript.player_set_orientation(target_yaw, target_pitch)
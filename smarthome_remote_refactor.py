# Import 

from abc import ABC, abstractmethod

# === Abstract commands ===

class Command(ABC): 
    @abstractmethod
    def execute(self): 
        pass

class UndoableCommand(Command):
    @abstractmethod 
    def unexecute(self): 
        pass 

# Concrete commands === 
class LightOnCommand(UndoableCommand):
    ...

class LightOffCommand(UndoableCommand):
    ...

class SetFanSpeedCommand(UndoableCommand):
    ...

class PlaySongCommand(UndoableCommand):
    ...

class StopSongCommand(UndoableCommand):
    ...

# === History === 
class History(): 
    def __init__(self): 
        # This is our list of commands
        self._commands: list[UndoableCommand] = []

     # Now build it out like a regular stack 
    def push(self, command):
        self._commands.append(command)

    def pop(self):
        return self._commands.pop()
    
    # This is important to prevent crashing when undoing 
    def __len__(self): 
        return len(self._commands)

# === Devices/Receivers === 

class Light:
    def __init__(self) -> None:
        self.is_on = False

    def turn_on(self) -> None:
        self.is_on = True

    def turn_off(self) -> None:
        self.is_on = False

    def __str__(self) -> str:
        return f"Light(is_on={self.is_on})"


class Fan:
    def __init__(self) -> None:
        self.speed = 0

    def set_speed(self, speed: int) -> None:
        self.speed = speed

    def __str__(self) -> str:
        return f"Fan(speed={self.speed})"


class MusicPlayer:
    def __init__(self) -> None:
        self.current_song = None
        self.playing = False

    def play(self, song: str) -> None:
        self.current_song = song
        self.playing = True

    def stop(self) -> None:
        self.playing = False

    def __str__(self) -> str:
        return (
            f"MusicPlayer(current_song={self.current_song!r}, "
            f"playing={self.playing})"
        )

# === Invoker === 

class SmartHomeRemote:

    # def __init__(self, light: Light, fan: Fan, player: MusicPlayer) -> None:
    #     self.light = light
    #     self.fan = fan
    #     self.player = player
    #     self.history = []

    # def press(self, action: str, value=None) -> None:
    #     if action == "light_on":
    #         old_state = self.light.is_on
    #         self.light.turn_on()
    #         self.history.append(("light", old_state))

    #     elif action == "light_off":
    #         old_state = self.light.is_on
    #         self.light.turn_off()
    #         self.history.append(("light", old_state))

    #     elif action == "fan_speed":
    #         old_speed = self.fan.speed
    #         self.fan.set_speed(value)
    #         self.history.append(("fan", old_speed))

    #     elif action == "play_song":
    #         old_song = self.player.current_song
    #         old_playing = self.player.playing
    #         self.player.play(value)
    #         self.history.append(("music_play", old_song, old_playing))

    #     elif action == "stop_music":
    #         old_song = self.player.current_song
    #         old_playing = self.player.playing
    #         self.player.stop()
    #         self.history.append(("music_stop", old_song, old_playing))

    #     else:
    #         raise ValueError("Unknown action")

    # def undo(self) -> None:
    #     if not self.history:
    #         return

    #     last = self.history.pop()

    #     if last[0] == "light":
    #         if last[1]:
    #             self.light.turn_on()
    #         else:
    #             self.light.turn_off()

    #     elif last[0] == "fan":
    #         self.fan.set_speed(last[1])

    #     elif last[0] == "music_play":
    #         old_song = last[1]
    #         old_playing = last[2]
    #         self.player.current_song = old_song
    #         self.player.playing = old_playing

    #     elif last[0] == "music_stop":
    #         old_song = last[1]
    #         old_playing = last[2]
    #         self.player.current_song = old_song
    #         self.player.playing = old_playing


if __name__ == "__main__":
    light = Light()
    fan = Fan()
    player = MusicPlayer()

    remote = SmartHomeRemote(light, fan, player)

    remote.press("light_on")
    remote.press("fan_speed", 3)
    remote.press("play_song", "Take Five")

    print(light)
    print(fan)
    print(player)

    remote.undo()
    remote.undo()

    print(light)
    print(fan)
    print(player)

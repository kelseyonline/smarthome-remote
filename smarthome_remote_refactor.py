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


# === Concrete commands === 
class LightOnCommand(UndoableCommand):
    def __init__(self, light):
        self.light = light
    
    def execute(self): 
        self.light.is_on = True 

    def unexecute(self): 
        self.light.is_on = False 

class LightOffCommand(UndoableCommand):
    def __init__(self, light):
        self.light = light
    
    def execute(self): 
        self.light.is_on = False 

    def unexecute(self): 
        self.light.is_on = True 

class SetFanSpeedCommand(UndoableCommand):
    def __init__(self, fan):
        self.fan = fan
        self.speed = 0
    
    def execute(self, speed): 
        self.fan.speed = speed

    def unexecute(): 
         ...

class PlaySongCommand(UndoableCommand):
    def __init__(self, player):
        self.player = player 
    
    def execute(self, song): 
        self.player.playing = True
        self.player.current_song = song

    def unexecute(): 
        ...

class StopSongCommand(UndoableCommand):
    def __init__(self, player):
        self.player = player 
    
    def execute(self): 
        self.player.playing = False

    def unexecute(): 
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

    def __str__(self) -> str:
        return f"Light(is_on={self.is_on})"

class Fan:
    def __init__(self) -> None:
        self.speed = 0

    def __str__(self) -> str:
        return f"Fan(speed={self.speed})"

class MusicPlayer:
    def __init__(self) -> None:
        self.current_song = None
        self.playing = False

    def __str__(self) -> str:
        return (
            f"MusicPlayer(current_song={self.current_song!r}, "
            f"playing={self.playing})"
        )

# === Invoker === 

class SmartHomeRemote:
    def __init__(self, light: Light, fan: Fan, player: MusicPlayer) -> None:
        self.light = light
        self.fan = fan
        self.player = player
        self.history = []

    # def press(self, action: str, value=None) -> None:
    #     if action == "light_on":
    #         old_state = self.light.is_on
    #         self.light.turn_on()
    #         self.history.append(("light", old_state))

if __name__ == "__main__":
    light = Light()
    fan = Fan()
    player = MusicPlayer()

    remote = SmartHomeRemote(light, fan, player)

    # Turn the light on 
    light_on = LightOnCommand(light)
    light_on.execute()
    print(light)

    # Turn the light off 
    light_off = LightOffCommand(light)
    light_off.execute() 
    print(light)

    # Set fan speed to 3
    print(fan)
    set_fan_speed = SetFanSpeedCommand(fan)
    set_fan_speed.execute(3)
    print(fan)

    # Play a song 
    print(player)
    play_song = PlaySongCommand(player)
    play_song.execute("Never Gonna Give You Up")
    print(player)

    # Stop the song 
    stop_song = StopSongCommand(player) 
    stop_song.execute()
    print(player)

    # remote.press("light_on")
    # remote.press("fan_speed", 3)
    # remote.press("play_song", "Take Five")

    # print(light)
    # print(fan)
    # print(player)

    # remote.undo()
    # remote.undo()

    # print(light)
    # print(fan)
    # print(player)

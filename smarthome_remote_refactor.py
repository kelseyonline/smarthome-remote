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
    def __init__(self, light, history):
        self.light = light
        self.history = history
    
    def execute(self): 
        self.light.is_on = True 
        self.history.push(self)

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
        self.prev_speed = fan.speed
    
    def execute(self, speed): 
        self.prev_speed = self.fan.speed
        self.fan.speed = speed

    def unexecute(self): 
         self.fan.speed = self.prev_speed

class PlaySongCommand(UndoableCommand):
    def __init__(self, player):
        self.player = player 
        self.prev_song = None
        self.prev_playing = False
    
    def execute(self, song): 
        self.prev_song = self.player.current_song
        self.prev_playing = self.player.playing

        self.player.playing = True
        self.player.current_song = song

    def unexecute(self): 
        self.player.current_song = self.prev_song
        self.player.playing = self.prev_playing

class StopSongCommand(UndoableCommand):
    def __init__(self, player):
        self.player = player 
        self.prev_playing = player.playing
    
    def execute(self): 
        self.prev_playing = self.player.playing
        self.player.playing = False

    def unexecute(self): 
        self.player.playing = self.prev_playing

class UndoCommand(Command): 
    def __init__(self, history):
        self.history = history

    def execute(self): 
        if len(self.history) > 0: # Prevents crash on empty list
            self.history.pop().unexecute()

# === History === 
class History(): 
    def __init__(self): 
        # This is our list of commands
        self.commands: list[UndoableCommand] = []

     # Now build it out like a regular stack 
    def push(self, command):
        self.commands.append(command)

    def pop(self):
        return self.commands.pop()
    
    # This is important to prevent crashing when undoing 
    def __len__(self): 
        return len(self.commands)


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

    def undo(self):
        ...

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

    history = History()

    # Just for debugging
    print(history.commands)

    # Turn the light on 
    light_on = LightOnCommand(light, history)
    light_on.execute()
    print(light)

    # Turn the light off 
    light_off = LightOffCommand(light)
    light_off.execute() 
    print(light)

    # Now try turning the light on and then unexecuting
    light_on = LightOnCommand(light, history)
    light_on.execute()
    print(light)

    undo = UndoCommand(history)
    undo.execute()
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

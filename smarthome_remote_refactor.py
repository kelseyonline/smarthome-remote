# Please see my README for short answer questions

# === Import ===
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
    def __init__(self, light, history):
        self.light = light
        self.history = history
    
    def execute(self): 
        self.light.is_on = False 
        self.history.push(self)

    def unexecute(self): 
        self.light.is_on = True 

class SetFanSpeedCommand(UndoableCommand):
    def __init__(self, fan, history):
        self.fan = fan
        self.prev_speed = fan.speed
        self.history = history
    
    def execute(self, speed): 
        self.prev_speed = self.fan.speed
        self.fan.speed = speed
        self.history.push(self)

    def unexecute(self): 
         self.fan.speed = self.prev_speed

class PlaySongCommand(UndoableCommand):
    def __init__(self, player, history):
        self.player = player 
        self.prev_song = None
        self.prev_playing = False
        self.history = history
    
    def execute(self, song): 
        self.prev_song = self.player.current_song
        self.prev_playing = self.player.playing
        self.history.push(self)

        self.player.playing = True
        self.player.current_song = song

    def unexecute(self): 
        self.player.current_song = self.prev_song
        self.player.playing = self.prev_playing

class StopSongCommand(UndoableCommand):
    def __init__(self, player, history):
        self.player = player 
        self.prev_playing = player.playing
        self.history = history 
    
    def execute(self): 
        self.prev_playing = self.player.playing
        self.player.playing = False
        self.history.push(self)

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

if __name__ == "__main__":
    light = Light()
    fan = Fan()
    player = MusicPlayer()

    remote = SmartHomeRemote(light, fan, player)

    history = History()

    # Turn the light on 
    light_on = LightOnCommand(light, history)
    light_on.execute()
    print(light)

    # Turn the light off 
    light_off = LightOffCommand(light, history)
    light_off.execute() 
    print(light)

    # Now try turning the light on and then unexecuting
    light_on = LightOnCommand(light, history)
    light_on.execute()
    print(light)

    undo = UndoCommand(history)
    undo.execute()
    print(light)

    # Try turning the light off and unexecuting
    light_off = LightOffCommand(light, history)
    light_off.execute()
    print(light)

    undo = UndoCommand(history)
    undo.execute()
    print(light)

    # Set fan speed to 3
    print(fan)
    set_fan_speed = SetFanSpeedCommand(fan, history)
    set_fan_speed.execute(3)
    print(fan)

    # Try unexecuting fan speed 
    undo = UndoCommand(history)
    undo.execute()
    print(fan)

    # Try changing fan speed twice, then unexecuting twice
    set_fan_speed = SetFanSpeedCommand(fan, history)
    set_fan_speed.execute(4)
    print(fan)
    set_fan_speed = SetFanSpeedCommand(fan, history)
    set_fan_speed.execute(5)
    print(fan)

    undo = UndoCommand(history)
    undo.execute()
    print(fan)

    undo = UndoCommand(history)
    undo.execute()
    print(fan)

    # Play a song 
    print(player)
    play_song = PlaySongCommand(player, history)
    play_song.execute("Never Gonna Give You Up")
    print(player)

    # Stop the song 
    stop_song = StopSongCommand(player, history) 
    stop_song.execute()
    print(player)

    # Now play a song and unexecute 
    play_song = PlaySongCommand(player, history)
    play_song.execute("Is It A Crime")
    print(player)

    undo = UndoCommand(history)
    undo.execute()
    print(player)

    # Lastly, play a song, stop it, then unexecute
    play_song = PlaySongCommand(player, history)
    play_song.execute("My Name Is Jonas")
    print(player)

    # Stop the song 
    stop_song = StopSongCommand(player, history) 
    stop_song.execute()
    print(player)

    undo = UndoCommand(history)
    undo.execute()
    print(player)


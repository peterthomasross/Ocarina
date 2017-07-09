import pygame
import pygame.midi
from pygame.locals import *
import sounddevice as sd

sounds = {}
FS = 48000
mode = 1
last_pad_no = 0

pygame.init()

pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post

pygame.midi.init()
input_id = pygame.midi.get_default_input_id()
i = pygame.midi.Input( input_id )


pygame.display.set_caption("midi test")
screen = pygame.display.set_mode((400, 300), RESIZABLE, 32)

print ("starting")

def handle_event(event):
    global mode
    global last_pad_no
    pad_no = event[0][1]
    if pad_no == 66:
        if mode < 4:
            mode += 1
        else:
            mode = 1
    else:
        if mode == 3:
            record(pad_no)
        else:
            last_pad_no = 0
            play_note(pad_no)

def play_note(pad_no):
    sound = sounds[pad_no]
    sd.play(sound, FS)

def record(pad_no):
    global last_pad_no
    if last_pad_no != pad_no:
        global sounds
        duration = 2
        print("recording")
        sound = sd.rec(int(duration * FS), samplerate=FS, channels=2)
        sd.wait()
        print("stop recording")
        actual_pad_no = pad_no - 32
        sounds[actual_pad_no] = sound
        last_pad_no = pad_no

going = True

while going:

        events = event_get()
        for e in events:
                if e.type in [QUIT]:
                        going = False
                if e.type in [KEYDOWN]:
                        going = False

        if i.poll():
                midi_events = i.read(10)
                event = midi_events[0]
                handle_event(event)
                print(mode)
                # print("?: {}".format(note[0][0]))
                # print("Pad: {}".format(event[0][1]))
                # print("Pressure: {}".format(note[0][2]))
                # print("Pressure?: {}".format(note[1]))
                #print ("full midi_events " + str(midi_events))
                #print ("my midi note is ") + str(midi_events[0])
                # convert them into pygame events.
                midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

                for m_e in midi_evs:
                        event_post( m_e )



print ("exit button clicked.")
i.close()
pygame.midi.quit()
pygame.quit()
exit()

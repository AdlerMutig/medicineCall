'''
   
    timidity -iA &
'''

import pygame
import pygame.midi
from time import sleep
import time
import Adafruit_MPR121.MPR121 as MPR121

notes=[28,29,31,33,35,36,38,40,41,43,45,47,48,50]

def setup_capacitive_hat():
	cap = MPR121.MPR121()

	if not cap.begin():
    		print 'Error initializing MPR121.  Check your wiring!'
    		sys.exit(1)


	cap._i2c_retry(cap._device.write8,0x5E,0x00)

	cap.set_thresholds(50, 10)

	cap._i2c_retry(cap._device.write8,0x5E,0x8F)

	return cap

def midiExample(parInstrument, parOCtaves):
    
    GRAND_PIANO = 0
    CHURCH_ORGAN = 19
    GUITAR=25
    DRUMB=115
    SAX=65
    VIOLA=42
    TROMBONE=58
    
    instrument_array=[GRAND_PIANO,CHURCH_ORGAN,GUITAR,DRUMB,SAX,VIOLA,TROMBONE]
    current_instrument=parInstrument
    
    pygame.init()	

    pygame.midi.init()
    midi_out = pygame.midi.Output(2, 0)

    
    cap=setup_capacitive_hat();

    
    octave=parOCtaves
    notes_offset=[x+12*octave for x in notes]

    
    try:
        midi_out.set_instrument(instrument_array[current_instrument])

	
	print 'Press Ctrl-C to quit.'
	last_touched = cap.touched()	

	while True:
    		current_touched = cap.touched()
    		
    		for i in range(12):
        		
        		pin_bit = 1 << i
        		
        		if current_touched & pin_bit and not last_touched & pin_bit:
            			print '{0} touched!'.format(i)
            			print cap.touched()
				if i == 11:
					print "no key"
					
				elif i== 10:
					print "Octave increased, actual: "+str(octave)
					octave+=1
					if octave>8:
						octave=8
					for i in notes_offset:
                                                midi_out.note_off(i,127)

					notes_offset=[x+12*octave for x in notes]
				elif i==9:
					
					print ""
				else:
                                        print "plaz file"
                                        datName = "audio/0" + str(i) + ".wav"
                                        pygame.mixer.music.load(datName)
                                        pygame.mixer.music.play()
                                        #while pygame.mixer.music
					##midi_out.note_on(notes_offset[i],127)
        		if not current_touched & pin_bit and last_touched & pin_bit:
            			print '{0} released!'.format(i)

				if i== 9:
                                        print "Octave decremented, actual: "+str(octave)
                                        octave-=1
                                        if octave<0:
                                                octave=0
					for i in notes_offset:
						midi_out.note_off(i,127)

                                        notes_offset=[x+12*octave for x in notes]
				else:
					midi_out.note_off(notes_offset[i],127)
    		last_touched = current_touched
    		time.sleep(0.1)

	

    finally:
        del midi_out
        pygame.midi.quit()
#
#
#


        
midiExample(6, 0)

# 3 FEBRUARY 2023
# Pynapse Source #

import random
import time
import math

class Always: # StateID = 0
	def s_Session_start():
		p_State.switch(StartTrial)

	def s_Session_stop():
		p_State.switch(EndExperiment)

class StartTrial: # StateID = ?
	def s_State_enter():
		Cond = random.randint(1,2) # 1 = alcohol, 2 = water

		p_Metric.ntrials.inc()

		# if we reach 20 alcohol trials, switch to water trials
		if p_Metric.Alcohol.toInt() == 2:
			Cond = 2

		# if we reach 20 water trials, switch to alcohol trials
		if p_metric.Water.toInt() == 2:
			Cond = 1

		if (p_Metric.ntrials.toInt() != 5):
			if Cond == 1:
				p_Metric.Alcohol.inc()
				p_State.switch(StartAlcoholTrial)
			if Cond == 2:
				p_Metric.Water.inc()
				p_State.switch(StartWaterTrial)
			else:
				p_Session.stopSession()

class StartAlcoholTrial: # StateID = ?
	def s_State_enter():
		print("Trial #: ", p_Metric.ntrials.toString())
		print("Alcohol")
		print("Alcohol Trial #: ", p_Metric.Alcohol.read())
		print("Water Trial #: ", p_Metric.Water.read())
		p_Session.startTrial()
		p_State.switch(AlcoholLightOn)

class AlcoholLightOn: # StateID = ?
	# turn on alcohol light for 2 seconds
	def s_State_enter():
		p_Rig.RCueLight.turnOn()
		p_State.setTimeout(2, AlcoholLightOff)

class AlcoholLightOff: # StateID = ?
	# turn off alcohol light
	# wait 1 second before switching to Alcohol Trial
	def s_State_enter():
		p_Rig.RCueLight.turnOff()
		p_State.setTimeout(1, AlcoholTrial)

class AlcoholTrial:  # StateID = ?
    # spout out for 15 seconds 
    # counts lick if RLick is triggered
    def s_State_enter():
        p_Rig.RSpout.turnOn()
        p_State.setTimeout(10, AlcoholSipperOff)
        
    # if RLick is triggered,
        # increment RLickNum
    def s_RLick_rise():
        if p_Rig.RSpout.isOn():
            p_Metric.RLickNum.inc()

class AlcoholSipperOff: # StateID = ?
    # bring the sipper back in
    def s_State_enter():
        p_Rig.RSpout.turnOff()
        print(p_Metric.RLickNum.toPretty())
        p_State.switch(IntertrialInterval)

class StartWaterTrial: # StateID = ?
	def s_State_enter():
		print("Trial #: ", p_Metric.ntrials.toString())
		print("Water")
		print("Alcohol Trial #: ", p_Metric.Alcohol.read())
		print("Water Trial #: ", p_Metric.Water.read())
		p_Session.startTrial()
		p_State.switch(WaterLightOn)

class WaterLightOn: # StateID = ?
	# turn on water light for 2 seconds (blinking light!)
	def s_State_enter():
		p_Timer.Timer1.setPeriod(0.2)
		p_Timer.Timer1.setRepeats(10)
		p_Timer.Timer1.start()
		p_State.setTimeout(2, WaterTrial)
		
    def s_Timer1_tick(count):
        p_Rig.LCueLight.fire()

class WaterTrial:  # StateID = ?
    # wait 1 second before sending spout out
    # spout out for 15 seconds
    # counts lick if LLick is triggered
    def s_State_enter():
        time.sleep(1)
        p_Rig.LSpout.turnOn()
        p_State.setTimeout(10, WaterSipperOff)
    
    # if LLick is triggered, increment LLickNum
    def s_LLick_rise():
        if p_Rig.LSpout.isOn():
            p_Metric.LLickNum.inc()

class WaterSipperOff: # StateID = ?
    # bring sipper back in
    def s_State_enter():
        p_Rig.LSpout.turnOff()
        print(p_Metric.LLickNum.toPretty())
        p_State.switch(intertrialInterval)
        
class IntertrialInterval: # StateID = ?
    # randomize intertrial intervals
    # 30, 60, 90 seconds
    def s_State_enter():
        interval = random.randint(1, 3)
        if interval == 1:
            interval = 30
        if interval == 2:
            interval = 60
        if interval == 3:
            interval = 90
        print("Intertrial Interval: ", interval, " seconds")
        print(" ")
        p_State.setTimeout(5, StartTrial)
        p_Session.endTrial()
        
class EndExperiment: # StateID = ?
    def s_State_enter():
        print("experiment done!")
        print(p_Metric.ntrials.toInt() - 1, " trials completed")

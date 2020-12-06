import Leap, sys, thread, time, os, time, datetime, numpy, select

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

SLEEP = 0
CNT = 0
MAXSIZE = 200
STACK = []
FINGERPRINT = []

class SampleListener(Leap.Listener):
	finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

	def on_frame(self, controller):
		# Get the most recent frame and report some basic information
		frame = controller.frame()

		fingers = frame.hands.rightmost.fingers
		if not fingers.is_empty:
			controller.remove_listener(self)

			fbase = fingers.leftmost
			fingerprint = []
			for finger in fingers:
				ft = finger.tip_position - fbase.tip_position
				fingerprint.append(ft.to_tuple())

			global CNT, STACK, MAXSIZE, FINGERPRINT, SLEEP
			if CNT < MAXSIZE:
				STACK.append(fingerprint)
				CNT += 1
			elif CNT == MAXSIZE:
				FINGERPRINT = numpy.mean(STACK, axis=0)
				print numpy.linalg.norm(numpy.std(STACK, axis=0), ord='fro')
				print("Hand remembered.")
				CNT += 1
			else:
				diff = numpy.linalg.norm(fingerprint - FINGERPRINT, ord='fro')
				print diff
				global SLEEP

				if diff < 100 and SLEEP == 0:
					SLEEP = 1
					# go to sleep
					print("{0} Sleeping...".format(datetime.datetime.now()))
					os.system("pmset displaysleepnow")
					os.system("say Goodbye.")
					time.sleep(3)

				elif diff < 100 and SLEEP == 1:
					SLEEP = 0
					# wake up
					print("{0} Waking...".format(datetime.datetime.now()))
					os.system("say Just one moment please.")
					time.sleep(3)

				elif diff >= 100 and SLEEP == 0:
					# do nothing
					print("{0} Hand not recognized...".format(datetime.datetime.now()))
					os.system("say I'm afraid I can't do that.")

				elif diff >= 100 and SLEEP == 1:
					# keep sleeping
					print("{0} Keep sleeping...".format(datetime.datetime.now()))
					os.system("pmset displaysleepnow")
					os.system("say I'm afraid I can't do that.")
				
				# time.sleep(3)
				print("{0} Mission complete.".format(datetime.datetime.now()))

			controller.add_listener(self)


def main():
	# Create a sample listener and controller
	listener = SampleListener()
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)

	# Keep this process running until Enter is pressed
	print("LeapID Started. Scan your hand...")
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the sample listener when done
		controller.remove_listener(listener)

if __name__ == "__main__":
	main()

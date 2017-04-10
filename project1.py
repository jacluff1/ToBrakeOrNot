import numpy as np 
import matplotlib.pyplot as plt 

# GLOBAL DEFINITIONS

# final time - seconds
tf = 7.

# time increment - seconds
dt = .1

# time array - seconds
T = np.arange(0,tf+dt,dt)

# reaction time - seconds
t_react = .8

# yellow -> red time for light - seconds
t_light = 3.

# width of intersection - meters
W = 45.

# initial velocity - meters/second
v0 = 55 * (5/18) # 5/18 is km/hr -> m/s conversion factor 

# braking deceleration - meters/seconds^2
a = -3

# small correction used for heavistep function
ep = .01

def ASSERT(x0,v0,a):
	assert x0 <= 0, "problem geometry dictates that x0 <= 0."
	assert v0 > 0, "problem geometry dictates that v0 > 0."
	assert a < 0, "problem geometry dictates that a < 0."
	return

def H(x):
	"""Heaviside step function.

	Arguments
	---------
	x : scalar or array

	Returns
	-------
	float64 scalar or array

	From http://stackoverflow.com/a/15122658/334357
	"""
	return (1/2)*(np.sign(x) + 1)

# TASK A 

def x_brake(x0,t,v0=v0):
	"""Equation of motion
	x(t) if you decide to brake

	Arguments
	---------
	x0: scalar - meters
	t: scalar or array - seconds
	v0: keyward argument, scalar - meters/second

	Returns
	-------
	scalar or array - meters
	"""
	ASSERT(x0,v0,a)
	t_stop = -v0/a + t_react
	x_react = x0 + v0*t
	x_f = x0 + v0*t + (1/2)*a*(t-t_react)**2
	x_stop = x0 + v0*t_stop + (1/2)*a*(t_stop-t_react)**2
	return H(t_react-t+ep)*x_react + H(t-t_react-ep)*x_f*H(t_stop-t-ep) + H(t-t_stop+ep)*x_stop

def x_go(x0,t,v0=v0):
	"""Equation of motion
	x(t) if ou decide to not brake

	Arguments
	---------
	x0: scalar - meters
	t: scalar or array - seconds
	v0: keyward argument, scalar - meters/second

	Returns
	-------
	scalar - meters
	"""
	ASSERT(x0,v0,a)
	return x0 + v0*t

def v_brake(t,v0=v0,x0=0):
	"""Equation of motion
	v(t) if you decide to brake

	Arguments
	---------
	t: scalar or array - seconds
	v0: keyward argumnet, scalar - meters/second
	x0: keyward argument - only used for ASSERT()

	Returs
	------
	scalar or array - meters/second
	"""

	ASSERT(x0,v0,a)
	t_stop = -v0/a + t_react
	v_react = H(t_react-t+ep) * v0
	v_brake = H(t-t_react-ep) * (v0 + a*(t-t_react)) * H(t_stop-t-ep)
	return v_react + v_brake

def v_go(t,v0=v0,x0=0):
	"""Equation of motion
	v(t) if you decide to not brake

	Arguments
	---------
	t: scalar or array - seconds
	v0: keyward argumnet, scalar - meters/second
	x0: keyward argument - only used for ASSERT()

	Returns
	-------
	scalar or array - meters/second
	"""
	ASSERT(x0,v0,a)
	return v0 

# TAKD B

def axis_pos(plot_num,x0,v0=v0,space=5,fs=20):
	"""Defines and plots on a position axis

	Arguments
	---------
	plot_num: subplot number of axis
	x0: scalar - meters
	v0: keyward argument, scalar - meters/second
	space: keyword argument, extra space along the y-axis for better visability
	fs: keyword argument, fontsize - integer

	Returns
	-------
	matplotlib axis
	"""

	P1 = x_brake(x0,T,v0=v0)
	P2 = x_go(x0,T,v0=v0)
	posmax = max([max(P1),max(P2),W+space])
	t_stop = -v0/a + t_react
	title = 'Position vs. Time - x$_0$ = %s m' % str(x0)

	ax = plt.subplot(plot_num)
	ax.plot(T,P1,'-b', lw=2, label='$x_{brake}$')
	ax.plot(T,P2,'-g', lw=2, label='$x_{go}$')
	ax.set_ylim([x0-space,posmax+space])
	ax.vlines(t_react, ymin=x0-space, ymax=posmax+space, linestyle='dashed', linewidth=2, color='orange', label='$t_{react}$')
	ax.vlines(t_light, ymin=x0-space, ymax=posmax+space, linestyle='dashed', linewidth=2, color='red', label='$t_{light}$')
	ax.vlines(t_stop, ymin=x0-space, ymax =posmax+space, linestyle='dashed', linewidth=2, color='k', label='$t_{stop}$')
	ax.fill_between([0,tf], [W,W], color='k', alpha=.3)

	ax.set_xlabel('time[s]',fontsize=fs)
	ax.set_ylabel('position [m]',fontsize=fs)
	ax.set_title(title,fontsize=fs+2)

	ax.legend(loc='best',fontsize=fs)

	return ax

def axis_vel(plot_num,v0=v0,space=5,fs=20):
	"""Defines and plots on a velocity axis

	Arguments
	---------
	plot_num: subplot number of axis
	v0: keyword argument, scalar - meters/second
	space: keyword argument, extra space along the y-axis for better visability
	fs: keyword argument, fontsize - integer

	Returns
	-------
	matplotlib axis
	"""

	V1 = v_brake(T,v0=v0)
	V2 = v_go(T,v0=v0)
	velmax = max([max(V1),V2])
	t_stop = -v0/a + t_react

	ax = plt.subplot(plot_num)
	ax.plot(T,V1,'-b', lw=2, label='$v_{brake}$')
	ax.hlines(V2, xmin=0, xmax=tf, color='g', linewidth=2, label='$v_{go}$')
	ax.set_ylim([0-space,v0+space])
	ax.vlines(t_react, ymin=0-space, ymax=v0+space, linestyle='dashed', linewidth=2, color='orange', label='$t_{react}$')
	ax.vlines(t_light, ymin=0-space, ymax=v0+space, linestyle='dashed', linewidth=2, color='r', label='$t_{light}$')
	ax.vlines(t_stop, ymin=0-space, ymax =v0+space, linestyle='dashed', linewidth=2, color='k', label='$t_{stop}$')
	ax.set_xlabel('time[s]',fontsize=fs)
	ax.set_ylabel('velocity [m/s]',fontsize=fs)
	ax.set_title('Velocity vs. Time - v$_0$ = 55 m.s',fontsize=fs+2)

	ax.legend(loc='best',fontsize=fs)

	return ax
	
def plotB(fs=20,saveA=False):
	"""Plots what is asked for in Task b

	Arguments
	---------
	fs: keyword argument, fontsize - integer
	saveA: keyword argument, decides to show or save the plot - boolean

	Returns
	-------
	either shows or saves matplotlib figure, but does not return anything
	"""

	plt.close('all')
	fig = plt.figure(figsize=(30,15))
	plt.title('To Brake or Not',fontsize=fs+2)

	ax1 = axis_vel(221)
	ax2 = axis_pos(222,-.5)
	ax3 = axis_pos(223,-30)
	ax4 = axis_pos(224,-70)

	plt.tight_layout()

	if saveA == True:
		fig.savefig('plot_taskB.png')
		plt.close(fig)
	else:
		plt.show()

	return

# TASK C

def decide_pos(x0,v0=v0,printA=False):
	"""Decide to brake or not - position

	Arguments
	---------
	x0: scalar - meters
	a: scalar - meters/seconds^2
	v0: keyword argument - meters/second
	printA: keyword argument, decide to print statements or not - boolean

	Returns
	-------
	printed statement on suggested action - if printA == True
	'go' OR 'brake' OR 'danger zone'
	"""

	t_stop = -v0/a + t_react

	go = x_go(x0,t_light,v0=v0)
	brake = x_brake(x0,t_stop,v0=v0)
	if printA == True:
		print("")
		print(x0, " outcome")
	if go >= 45:
		if printA == True:
			print("don't break")
		return 1
	elif brake <= 0:
		if printA == True:
			print("you shall not pass!! -- brake")
		return 1
	else:
		if printA == True:
			print("you are now in... the dilema zone")
		return 0

def decide_vel(x0=0,v0=v0,printA=False):
	"""Decide to brake or not - velocity

	Arguments
	---------
	v0: keyword argument, scalar - meters/second

	Returns
	-------
	printed stated on suggested course of action
	"""

	if printA == True:
		print("")
		print(v0, " outcome")
	vel_brake = v_brake(t_light,v0=v0)
	vel_go = v_go(t_light,v0=v0)

	dt = .01
	T = np.arange(0,t_light+dt,dt)
	VEL_brake = v_brake(T,v0=v0)
	VEL_go = v_go(T,v0=v0)

	pos_brake = x0 + np.sum(VEL_brake)*dt
	pos_go = x0 + np.sum(VEL_go)*dt

	if x0 != 0:
		if pos_go >= 45:
			if printA == True:
				print("don't break")
			return 1
		elif pos_brake <= 0:
			if printA == True:
				print("you shall not pass!! -- brake")
			return 1
		else:
			if printA == True:
				print("you are now in... the dilema zone")
			return 0

def decide_B():
	decide_vel()
	decide_pos(-.5,printA=True)
	decide_pos(-30,printA=True)
	decide_pos(-70,printA=True)
	return

# TASK D

# incremental position - meters
dx = .5

# initial position array - meters
X0= np.arange(-100,dx,dx)

# map of safe initial positions
X0map = np.array([decide_pos(x0) for x0 in X0])

def printMap():
	print("")
	print("classification map: pos , classification")
	for i,j in zip(X0,X0map):
		print(i,j)
	return

def plotD(fs=20,saveA=False):
	ylim = [-.2,1.2]
	xs = [-51.5,-.5]

	plt.close('all')
	fig = plt.figure(figsize=(30,15))
	plt.title('The Dilemma Zone as a function of x$_0$',fontsize=fs+2)
	plt.xlabel("$x_0\ [m]$", fontsize=fs)
	plt.ylabel("classification", fontsize=fs)
	plt.plot(X0,X0map,'-m',lw=2, label='safe/unsafe')
	plt.vlines(xs[0], ymin=ylim[0], ymax=ylim[1], linestyle='dashed', linewidth=2, color='b', label='$x_0^B$')
	plt.vlines(xs[1], ymin=ylim[0], ymax=ylim[1], linestyle='dashed', linewidth=2, color='g', label='$x_0^A$')
	plt.ylim(ylim)
	plt.yticks([0,1])
	plt.hlines(.5, xmin=xs[0], xmax=xs[1], color='r', linewidth=3, label='s')
	plt.annotate('$s = x_0^A - x_0^B$\n$\ = -.5\ m + 51.5\ m$\n$\ = 51\ m$', xy=(-35,.52), color='r', fontsize=fs+3)
	plt.legend(loc='best',fontsize=fs)

	if saveA == True:
		fig.savefig('plot_TaskD.png')
		plt.close(fig)
	else:
		plt.show()

# TASK E

def x0B(t_react,v0,a):
	"""Safe distance to break

	Arguments
	---------
	t_react: scalar - seconds
	v0: scalar - meters/second
	a: acceleration - meters/second^2

	Returns
	-------
	scalar - meters
	"""

	return v0**2/(2*a) - v0*t_react
xB = x0B(t_react,v0,a)

def x0A(t_light,W,v0):
	"""Safe distance to keep going

	Arguments
	---------
	t_light: scalar - seconds
	W: scalar - meters
	v0: scalar - meters/second

	Returns
	-------
	scalar - meters
	"""

	return W - v0*t_light
xA = x0A(t_light,W,v0)
s = xA-xB

# TASK F

def s(v0):
	"""dilema zone

	args
	----
	v0:scalar or array - meters/second

	returns
	-------
	scalar or array - meters/second
	"""

	return W - v0*t_light + v0*t_react - v0**2/(2*a)

# velocity array for s(v0) - meters/second
V0 = np.arange(20*(5/18),100*(5/18) + .1,.1)

# dilema zone array - meters
S = s(V0)

def plotF(fs=20,saveA=False):
	plt.close('all')
	fig = plt.figure(figsize=(30,15))

	ax1 = plt.subplot(211)
	ax1.set_title("Dilema Zone as a Function of V$_0$",fontsize=fs+2)
	ax1.plot(V0,S,'-m', lw=2, label='$s(v_0)$')
	ax1.set_xlabel("velocity [m/s]", fontsize=fs)
	ax1.set_ylabel("dilema zone [m]", fontsize=fs)
	ax1.set_xlim(min(V0),max(V0))
	ax1.legend(loc='best',fontsize=fs)

	ax2 = plt.subplot(212)
	ax2.set_title("$x_0^A$ and $x_0^B$",fontsize=fs+2)
	ax2.plot(V0,x0B(t_react,V0,a),'-g', lw=2, label='$x_0^B$')
	ax2.plot(V0,x0A(t_light,W,V0),'-b', lw=2, label='$x_0^A$')
	ax2.legend(loc='best',fontsize=fs)
	ax2.set_xlim(min(V0),max(V0))
	ax2.set_xlabel('velocity [m/s]', fontsize=fs)
	ax2.set_ylabel('$x_0(v_0)\ [m]$', fontsize=fs)

	plt.tight_layout()

	if saveA == True:
		fig.savefig('plot_taskF.png')
		plt.close(fig)
	else:
		plt.show()

	return

# RUN IMPORTANT RESULTS

def ab_err(res):
	"""absolute error

	args
	----
	res: n x 2 array

	returns
	ans: 1 x n array of absolute error
	"""

	ans = []
	for row in res:
		n,a = row[0],row[1]
		ans.append(a-n)
	return ans

def rel_err(res):
	"""relative error

	args
	----
	res: n x 2 array

	returns
	ans: 1 x n array of relative error
	"""

	ans = []
	for row in res:
		n,a = row[0],row[1]
		ans.append((a-n)/a)
	return ans

def per_err(res):
	"""percent error

	args
	----
	res: n x 2 array

	returns
	ans: 1 x n array of percent error
	"""
	ans = []
	for row in res:
		n,a = row[0],row[1]
		ans.append(100 * (a-n)/a)
	return ans

numerical = np.array([-51.5,-.5,51])
analytical = np.array([xB,xA,xA-xB])
res = np.vstack((numerical,analytical)).T

def RUN():
	plotB()
	decide_B()
	printMap()
	plotD()
	print("numerical: [xB, xA, s] = ", numerical)
	print("analytical: [xB, xA, s] = ", analytical)
	print("absolute error: [xB, xA, s] = ", ab_err(res))
	print("relative error: [xB, xA, s] = ", rel_err(res))
	print("percentage error:: [xB, xA, s] = ", per_err(res))
	plotF()
	return
RUN()
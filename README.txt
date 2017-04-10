There is a function "RUN" defined on line 513 that calls all the relevant functions and produces all the plots and prints all the necessary results.

Most functions have "helpful" string docs

the basic global definitons are found on lines 4-31




FUNCTIONS:

Assert(x0,t, **v0)
(33) 
calls all the assertions on x0,v0, and a. This function is used in the equations of motion

H(x)
(39)
The Heaviside function, also used in the equations of motion

x_brake(x0,t, **v0)
(56)
the position function if applying brakes

x_go(x0,t, **v0)
(77)
the position function if crossing interection

v_brake(t, **v0,x0)
(94)
the velocity function if applying brakes

v_go(t, **v0,x0)
(115)
the velocity function if crossing intersection

axis_pos(plot_num,x0, **v0,space,fs)
(134)
takes a given x0 and plots x_brake and x_go on an subplot,
adds titles, labels, legends, etc...
this function is called withing the plotting function for taskB, fig1

axis_vel(plot_num, **v0,space,fs)
(173)
plots v_brake and v_go on an subplot
adds titles, labels, legends, etc...
this function is called withing the plotting function for taskB, fig1

plotB(**fs,saveA)
(208)
calls axis_pos and axis_vel to produce the subplots
either saves or shows figure depending on saveA boolean

decide_pos(x0, **v0,printA)
(242)
defines \tau, x_brake(\tau), and x_go(\tau)
goes through logical statements and returns 0 for unsafe; 1 for safe
can also print results if printA == True

decide_vel(**x0,v0,printA)
(278)
defines a time array 0 < t < tau with dt = .01
finds final positions by calling initial positions and integrating v_brake and v_go
goes through logical statements and returns 0 for unsafe; 1 for safe
can also print results if printA == True

decide_B()
(318)
calls decide_vel and decide_pos to determine if the situations in taskB, fig1 are safe or not

lines 327-334: a positions array is created from -100 < x < 0 with dx = .5
the positions array is used to create an array of safe-unsafe (0,1) used for taskD

printMap()
(336)
prints each position and its corresponding 0 or 1 to easily deterine the numerial
boundaries and regions for safe/unsafe zones.

plotD(**fs,saveA)
(343)
plots the safety map vs position array for taskD, fig2
adds titles, labels, legends, etc...

x0B(t_react,v0,a)
(369)
returns the analytical solution for x_0^B

x0A(t_light,W,v0)
(386)
returns the analytical solution for x_0^A

s(v_0)
(406)
returns the anaylitical solution for s

lines 421-424:
a velocity array is created from 20 < v_0 < 100 km/hr with dt = .1
the velocity array is passed through s(v_0) to create array of lengths of dilemma zone

plotF(**fs,saveA)
(426)
plots the analytical solutions for s, x_0^B, and x_0^A.
adds titles, labels, legends, etc...

ab_err(res)
(459)
takes both analytical and numerical vales of s, x_0^A, and x_0^B
returns list of absolute error

rel_err(res)
(476)
takes both analytical and numerical vales of s, x_0^A, and x_0^B
returns list of relative error

per_err(res)
(493)
takes both analytical and numerical vales of s, x_0^A, and x_0^B
returns list of percent error

lines 509-511:
array of numerical results: x_0^B, x_0^A, s
array of analytical results: x_0^B, x_0^A, s
combine both arrays into 3 X 2 array

RUN()
(513)
calls plotB, printMap, plotD, plotF
prints the numerical and analytical results
prints the absolute, relative, and percentage error






































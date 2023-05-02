from scipy.interpolate import CubicSpline
from scipy.interpolate import CubicHermiteSpline
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
import numpy as np

x_knots = np.array([-6, -5, -2.5, 0.5, 3.5, 6, 7])/2.2 - 1
y_knots = np.array([-17, -15, -13.5, -13, -13.5, -15, -17]) * 13/17 -4
dy_knots = np.array([5,1,0.5,0,-0.5,-1,-5])

t_knots = np.linspace(0, 2.5, 7)
t_eval = np.linspace(0, 2.5, 20)

# Use 3 different spline functions to interpolate the x and y knots
c_spline_x = CubicSpline(t_knots, x_knots, bc_type='natural')
c_spline_y = CubicSpline(t_knots, y_knots, bc_type='natural')
ch_spline_x = CubicHermiteSpline(t_knots, x_knots, dy_knots)
ch_spline_y = CubicHermiteSpline(t_knots, y_knots, dy_knots)
p_spline_x = PchipInterpolator(t_knots, x_knots)
p_spline_y = PchipInterpolator(t_knots, y_knots)

# Calculate the individual x and y values based on the time steps
cubic_x = c_spline_x(t_eval)
cubic_y = c_spline_y(t_eval)
hermite_x = ch_spline_x(t_eval)
hermite_y = ch_spline_y(t_eval)
pchip_x = p_spline_x(t_eval)
pchip_y = p_spline_y(t_eval)

plt.clf()
plt.plot(x_knots,y_knots,'o')
plt.plot(cubic_x,cubic_y, label='Cubic Spline')
plt.plot(hermite_x,hermite_y, label='Cubic Hermite')
plt.plot(pchip_x,pchip_y, label='Pchip Interpolator')

plt.ylim(-18, 0)
plt.xlim(-9,9)
plt.legend()

plt.show()

#np.savetxt('/Users/aidanbeckett/Library/Mobile Documents/com~apple~CloudDocs/Documents/MATLAB/ME31/x_vals.csv', pchip_x, delimiter=',')
#np.savetxt('/Users/aidanbeckett/Library/Mobile Documents/com~apple~CloudDocs/Documents/MATLAB/ME31/y_vals.csv', pchip_y, delimiter=',')

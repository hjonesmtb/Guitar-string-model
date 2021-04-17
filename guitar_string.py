import numpy as np
import scipy.integrate as integrate
import pprint

sqrt = np.sqrt
pi = np.pi

L = 0.30 #pre-tensioned length 
y0 = 0.01  #initial displacement
v0 = 0.0 #initial velocity

# [inches]
diameter = {'e' : 0.012, 
        'b' : 0.016, 
        'g' : 0.020,
        'd' : 0.032,
        'a' : 0.042,
        'E' : 0.054}

#Takes string diameter (inches) and returns period of oscillation.
#Calculation explained in project document
def period(d):

  k = 200e9 * pi/4*(d*2.54/100)**2 / (2*L)   #spring stiffness
  L0 = L - 100/(2*k) #pre tensioned to 100N

  m = pi/4*(d*2.54/100)**2 * 2*L0 * 8000
  E = 2 * k * L**2 * (0.5 * (y0/L)**2 + 1-L0/L )**2 + m * v0**2 / 8 

  ymax = sqrt( 2*L * ( sqrt(E/(2*k)) - (L - L0)))

  return 2*integrate.quad(integrand, ymax, -ymax, args = (m,k,E,L0))[0]

#Integration helper
def integrand(y,m,k,E,L0):
  return -sqrt(m/( 8 * (E - 2*k * L**2 *(0.5*(y/L)**2 + 1 - L0/L)**2 )))

freq_measured = {'e' : 330, 
        'b' : 247, 
        'g' : 196,
        'd' : 145,
        'a' : 110,
        'E' : 82}

results = {}

for d in diameter.keys():
  freq =  1/period(diameter[d])
  results[d] = round(freq) , round(freq_measured[d],2)

print('String: (predicted, measured)\n')
pprint.pprint(results)
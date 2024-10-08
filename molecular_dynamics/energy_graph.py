import numpy as np
import matplotlib.pyplot as plt

def carregar_dados(arquivo,n_particles):
    # Carrega os dados assumindo que estão em colunas t, x, y
    dados = np.loadtxt(arquivo)
    t = dados[:, 0]  # Coluna de tempo
    x = [dados[:, 1 + 2*i] for i in range(n_particles)]  # Coluna de posição x
    y = [dados[:, 2 + 2*i] for i in range(n_particles)]  # Coluna de posição y
    k_index = (1+2*n_particles)
    k = dados[:,k_index]
    p = dados[:,(1+2*n_particles+1)]
    return t, x, y, k, p

arquivo = 'data_LJ.dat'
t,x,y,k,p = carregar_dados(arquivo,25)
k = np.array(k)
t = np.array(t)
p = np.array(p)

e = k+p
plt.plot(t,k)
plt.plot(t,p)
plt.plot(t,e)
plt.show()
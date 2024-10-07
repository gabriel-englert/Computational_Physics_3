import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')
data = np.loadtxt('verlet_data.dat',comments='#')

t = data[:, 0]  # Coluna 0 é o tempo
x = data[:, 1]  # Coluna 1 é a posição
v = data[:, 2]  # Coluna 2 é a velocidade

# Criar a figura e os subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  # 2 linhas, 1 coluna

# Primeiro gráfico: posição em função do tempo
ax1.plot(t, x, label='Posição (m)', color='blue')
ax1.set_title("Posição em função do tempo")
ax1.set_xlabel("Tempo (s)")
ax1.set_ylabel("Posição (m)")
ax1.grid(True)
ax1.legend()

# Segundo gráfico: velocidade em função do tempo
ax2.plot(t, v, label='Velocidade (m/s)', color='orange')
ax2.set_title("Velocidade em função do tempo")
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("Velocidade (m/s)")
ax2.grid(True)
ax2.legend()

# Ajustar o layout para que os gráficos não se sobreponham
plt.tight_layout()

# Mostrar a figura
plt.show()
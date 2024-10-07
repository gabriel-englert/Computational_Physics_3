import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')
data = np.loadtxt('verlet_data_2.dat',comments='#')

t = data[:, 0]  # Coluna 0 é o tempo
x1 = data[:, 1]  # Coluna 1 é a posição
x2 = data[:, 2]
v1 = data[:, 3]  # Coluna 2 é a velocidade
v2 = data[:, 4]
# Criar a figura e os subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  # 2 linhas, 1 coluna

# Primeiro gráfico: posição em função do tempo
ax1.plot(t, x1, label='Posição 1 (m)', color='blue')
ax1.set_title("Posição 1 em função do tempo")
ax1.set_xlabel("Tempo (s)")
ax1.set_ylabel("Posição (m)")
ax1.grid(True)
ax1.legend()

# Segundo gráfico: velocidade em função do tempo
ax2.plot(t, x2, label='Posição 2 (m)', color='orange')
ax2.set_title("Posição 2 em função do tempo")
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("Posição 2(m)")
ax2.grid(True)
ax2.legend()

# Ajustar o layout para que os gráficos não se sobreponham
plt.tight_layout()

# Mostrar a figura
plt.show()
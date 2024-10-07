import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
n_particles = 50
# Função para carregar os dados do arquivo .dat
def carregar_dados(arquivo,n_particles):
    # Carrega os dados assumindo que estão em colunas t, x, y
    dados = np.loadtxt(arquivo)
    t = dados[:, 0]  # Coluna de tempo
    x = [dados[:, 1 + 2*i] for i in range(n_particles)]  # Coluna de posição x
    y = [dados[:, 2 + 2*i] for i in range(n_particles)]  # Coluna de posição y
    return t, x, y


# Função para inicializar o gráfico
def init():
    for particula in particulas:
        particula.set_data([], [])  # Inicia vazio
    tempo_text.set_text('Tempo = 0.0s')  # Inicializa o texto de tempo
    return particulas + [tempo_text]

# Função para atualizar a posição da partícula em cada quadro
def atualizar(frame):
    for i, particula in enumerate(particulas):
        particula.set_data([x[i][frame]], [y[i][frame]])  # Atualiza as coordenadas de cada partícula
    tempo_text.set_text(f'Tempo = {t[frame]:.2f}s')
    return particulas + [tempo_text]

# Carregar os dados do arquivo .dat
arquivo = 'particle_animation.dat'  # Substitua pelo caminho do seu arquivo
t, x, y = carregar_dados(arquivo,n_particles)
print(x[0][1000])
# Configuração do gráfico
fig, ax = plt.subplots()
ax.set_xlim(0,100)
ax.set_ylim(0,100)
ax.set_xlabel('Posição X')
ax.set_ylabel('Posição Y')

# Criando o marcador da partícula
particulas = [ax.plot([], [], 'bo', ms=10)[0] for _ in range(n_particles)]
print(particulas)

# Adicionando o texto para mostrar o tempo
tempo_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12, verticalalignment='top')

# Criação da animação
anim = FuncAnimation(fig, atualizar, frames=len(t), init_func=init, interval=1, blit=True)

# Mostra a animação
plt.show()
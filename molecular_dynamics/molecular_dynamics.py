import numpy as np
import matplotlib.pyplot as plt
import random
from numba import jit
import time
start = time.time()

def maxwell_distribution(T):
    sigma = np.sqrt(T)
    vx = np.random.normal(0,sigma)
    vy = np.random.normal(0,sigma)
    return vx,vy

def apply_periodic_boundary(self, particula):
    if particula.x > self.L:
        particula.x -= self.L
    if particula.x < 0:
        particula.x += self.L
    if particula.y > self.L:
        particula.y -= self.L
    if particula.y < 0:
        particula.y += self.L
    return


def distance(p1,p2):
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def periodic_distance(p1, p2, L):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    if abs(dx) > L/2:
        if dx<0:
            dx = abs(dx) - L
        else:
            dx = L - dx
    else:
        dx = -dx
    if abs(dy) > L/2:
        if dy<0:
            dy = abs(dy) - L
        else:
            dy = L - dy
    else:
        dy = -dy
    
        
    return dx,dy,np.sqrt(dx**2 + dy**2)

def add_if_not_collision(self,new_particle):
    collision = False
    for particula in self.particles:
        if distance(particula,new_particle) < 2*new_particle.radius:
            collision = True
            break
    if not collision:
        self.particles = np.append(self.particles,new_particle)
    return

def collision_test_walls(self,particula):
    if (particula.x>self.L):
        particula.x = 2*self.L - particula.x
        particula.vx = -1*particula.vx
    if (particula.x<0):
        particula.x = -particula.x
        particula.vx = -particula.vx
    if (particula.y>self.L):
        particula.y = 2*self.L - particula.y
        particula.vy = -1*particula.vy
    if (particula.y<0):
        particula.y =  -particula.y
        particula.vy = -particula.vy
    return 


class particle():
    def __init__(self,x,y,radius):
        self.radius = radius
        self.x = x
        self.y = y
        self.vx,self.vy = maxwell_distribution(100)
        #self.vx = self.x-L/2
        #self.vy = self.y-L/2



class box():
    def __init__(self,L):
        self.L = L
        self.particles = np.array([])
    def create_particles_random(self,radius,N):
        self.N = N
        while len(self.particles)<N:
            x = random.uniform(radius,self.L-radius)
            y = random.uniform(radius,self.L-radius)
            new_particle = particle(x,y,radius)
            add_if_not_collision(self,new_particle)
            #test if new_particle collides with the rest 
    def create_particles_square(self,radius):
        max_particles_line = int(np.floor(self.L/(2*radius)))
        self.N = max_particles_line**2
        for i in range(max_particles_line):
            for j in range(max_particles_line):
                x = (j + 0.5)* 2 * radius
                y = (i + 0.5) * 2 * radius
                new_particle = particle(x,y,radius)
                self.particles = np.append(self.particles,new_particle)
    def create_particles_triangle(self,radius):
        triangle_height = np.sqrt(3)*radius
        max_particles_line = int(np.floor(self.L/(2*radius)))
        max_particles_column = int(np.floor(self.L/triangle_height))
        self.N = max_particles_line*max_particles_column
        for i in range(max_particles_column):
            for j in range(max_particles_line):
                x = (j + 0.5)* 2 * radius
                if i%2 == 1:
                    x += radius
                y = (i + 0.5) * triangle_height
                if (x+radius < self.L) and (y + radius < self.L):
                    new_particle = particle(x,y,radius)
                    self.particles = np.append(self.particles,new_particle)
                
    def plotar(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.set_xlim(0, self.L)
        ax.set_ylim(0, self.L)

        for particula in self.particles:
            circulo = plt.Circle((particula.x, particula.y), particula.radius, color='b', fill=True)
            ax.add_patch(circulo)

        plt.title(f'{self.N} Partículas em uma Caixa {self.L}x{self.L}')
        plt.show()
    
    def MRU(self,tf,dt,dat_name):
        t = 0
        N = len(self.particles)
        with open(f'{dat_name}.dat','w') as out:
            out.write('# t ' + ' '.join([f'x{i+1} y{i+1}' for i in range(N)]) + '\n')
            while t<tf:
                line_data = [f'{t:.5f}']  # Adiciona o tempo
                for p in self.particles:
                    p.x += p.vx*dt
                    p.y += p.vy*dt
                    collision_test_walls(self,p)
                    line_data.append(p.x)
                    line_data.append(p.y)
                    # Escreve a linha de dados no arquivo
                out.write(' '.join(map(str, line_data)) + '\n')
                t += dt
        return
    def calculate_kinetic_energy(self):
        E_kin = 0
        for p in self.particles:
            E_kin += 0.5 * (p.vx**2 + p.vy**2)
        return E_kin

    def calculate_potential_energy(self, sigma, eps):
        E_pot = 0
        N = len(self.particles)
        for i in range(N):
            for j in range(i + 1, N):
                dx,dy,rij = periodic_distance(self.particles[i], self.particles[j], self.L)
                E_pot += 4 * eps * ((sigma / rij)**12 - (sigma / rij)**6)
        return E_pot
    #calcula a força do potencial LJ para todas as partículas
    def lennard_jones(self,sigma,eps):
        N = len(self.particles)
        Fx = np.zeros(N)
        Fy = np.zeros(N)
        for i in range(N):
            for j in range(i+1,N):
                dx,dy,rij = periodic_distance(self.particles[i],self.particles[j],self.L)
                
                A = (48*eps/(sigma)**2)*((sigma/rij)**14-0.5*(sigma/rij)**8)
                Fx[i] -= A*dx
                Fy[i] -= A*dy
                Fx[j] += A*dx
                Fy[j] += A*dy
        return Fx, Fy
    
    def verlet_LJ(self,tf,dt,sigma,eps,dat_name):
        t=0
        N = len(self.particles)
        out = open(f'{dat_name}.dat','w')
        out.write(f'# L={self.L} N={N}\n')
        out.write('# t ' + ' '.join([f'x{i+1} y{i+1}' for i in range(N)]) +' K P' + '\n')
        Fx, Fy = self.lennard_jones(sigma,eps)
        while t<tf:
            line_data = [f'{t:.5f}']  # Adiciona o tempo
            #atualizo velocidades e posições de todas as partículas
            for i,p in enumerate(self.particles):
                p.vx = p.vx + (1/2)*Fx[i]*dt
                p.vy = p.vy + (1/2)*Fy[i]*dt
                p.x = p.x + p.vx*dt
                p.y = p.y + p.vy*dt
                apply_periodic_boundary(self,p)
            #recalculo as forças
            Fx, Fy = self.lennard_jones(sigma,eps)
            #atualizo velocidades novamente, agora com a nova força
            for i,p in enumerate(self.particles):
                p.vx = p.vx + (1/2)*Fx[i]*dt
                p.vy = p.vy + (1/2)*Fy[i]*dt
                line_data.append(p.x)
                line_data.append(p.y)
            ktemp = self.calculate_kinetic_energy()/N
            ptemp = self.calculate_potential_energy(sigma,eps)/N
            line_data.append(ktemp)
            line_data.append(ptemp)
            out.write(' '.join(map(str, line_data)) + '\n')
            t+=dt
        return
L = 100
sigma = 10
eps = 10
b = box(L)
b.create_particles_square(10)
b.plotar()
b.verlet_LJ(30,0.01,sigma,eps,'data_LJ')
#print(b.particles)
#p = b.MRU(30,0.01,'particle_animation')
end = time.time()
print(end-start)



        

    
import networkx as nx
import random
import matplotlib.pyplot as plt
import argparse
import sys

def generar_instancia_mwcp(n_nodos, probabilidad_arista, semilla=42):
    """
    Genera un grafo aleatorio, asigna pesos y encuentra la solución exacta.
    
    Args:
        n_nodos: Número de nodos del grafo
        probabilidad_arista: Probabilidad de que exista una arista entre dos nodos (0-1)
        semilla: Semilla para reproducibilidad
    
    Returns:
        G: Grafo de NetworkX
        pesos: Diccionario con los pesos de cada nodo
        clique_nodos: Conjunto de nodos que forman el clique de peso máximo
        peso_total: Peso total del clique óptimo
    """
    random.seed(semilla)
    
    # 1. Crear grafo aleatorio (G(n, p))
    G = nx.fast_gnp_random_graph(n_nodos, probabilidad_arista, seed=semilla)
    
    # 2. Asignar pesos a los nodos (Ej: 1 a 200)
    pesos = {}
    for nodo in G.nodes():
        peso = random.randint(1, 200)
        G.nodes[nodo]['weight'] = peso
        pesos[nodo] = peso
    
    print(f"Grafo generado: {n_nodos} nodos, {G.number_of_edges()} aristas.")
    print("Calculando solución exacta (esto puede tardar en grafos muy grandes)...")
    
    # 3. Encontrar el Clique de Peso Máximo EXACTO
    # NetworkX usa una variante del algoritmo de Östergård o Carraghan-Pardalos
    clique_nodos, peso_total = nx.max_weight_clique(G, weight='weight')
    
    return G, pesos, clique_nodos, peso_total

def exportar_dimacs(G, pesos, archivo_salida):
    """
    Exporta el grafo a formato DIMACS modificado para programas C++/Java.
    Formato: 
        - Primera línea: número de nodos y aristas
        - Líneas 'n': definición de nodo con peso (índice base-1)
        - Líneas 'e': definición de arista (índices base-1)
    """
    with open(archivo_salida, "w") as f:
        f.write(f"{len(G.nodes)} {len(G.edges)}\n")
        for n in G.nodes:
            f.write(f"n {n+1} {pesos[n]}\n")  # +1 para índice base-1
        for u, v in G.edges:
            f.write(f"e {u+1} {v+1}\n")
    print(f"Grafo exportado a: {archivo_salida}")

def exportar_solucion(clique_nodos, peso_total, pesos, archivo_salida):
    """
    Exporta la solución óptima a un archivo de texto.
    """
    with open(archivo_salida, "w") as f:
        f.write(f"Peso Total: {peso_total}\n")
        f.write(f"Número de nodos en el clique: {len(clique_nodos)}\n")
        f.write(f"Nodos del Clique: {sorted(clique_nodos)}\n")
        f.write(f"Pesos individuales: {[pesos[n] for n in sorted(clique_nodos)]}\n")
    print(f"Solución exportada a: {archivo_salida}")

def main():
    parser = argparse.ArgumentParser(
        description='Generador de instancias MWCP (Maximum Weight Clique Problem) con solución exacta'
    )
    parser.add_argument('-n', '--nodos', type=int, default=100,
                        help='Número de nodos del grafo (default: 100)')
    parser.add_argument('-p', '--probabilidad', type=float, default=0.5,
                        help='Probabilidad de arista entre dos nodos (default: 0.5)')
    parser.add_argument('-s', '--semilla', type=int, default=42,
                        help='Semilla para reproducibilidad (default: 42)')
    parser.add_argument('-o', '--output', type=str, default='test_instance.txt',
                        help='Archivo de salida para el grafo (default: test_instance.txt)')
    parser.add_argument('--solucion', type=str, default='solucion.txt',
                        help='Archivo de salida para la solución (default: solucion.txt)')
    parser.add_argument('--no-export', action='store_true',
                        help='No exportar archivos, solo mostrar resultados')
    
    args = parser.parse_args()
    
    # Validar parámetros
    if args.nodos < 1:
        print("Error: El número de nodos debe ser al menos 1", file=sys.stderr)
        sys.exit(1)
    if not 0 <= args.probabilidad <= 1:
        print("Error: La probabilidad debe estar entre 0 y 1", file=sys.stderr)
        sys.exit(1)
    
    # Generar instancia
    G, pesos, sol_nodos, sol_peso = generar_instancia_mwcp(
        args.nodos, 
        args.probabilidad, 
        args.semilla
    )
    
    # Mostrar resultados
    print("-" * 50)
    print(f"SOLUCIÓN ÓPTIMA (Ground Truth):")
    print(f"Peso Total: {sol_peso}")
    print(f"Nodos del Clique: {sorted(sol_nodos)}")
    print(f"Pesos individuales: {[pesos[n] for n in sorted(sol_nodos)]}")
    print("-" * 50)
    
    # Exportar archivos si se solicita
    if not args.no_export:
        exportar_dimacs(G, pesos, args.output)
        exportar_solucion(sol_nodos, sol_peso, pesos, args.solucion)

if __name__ == "__main__":
    main()


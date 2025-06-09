import numpy as np

def baum_welch(x, states, symbols, Transition, Emission, I):
    n = len(x)
    k = len(states)
    m = len(symbols)
    
    symbol_to_idx = {s: i for i, s in enumerate(symbols)}
    state_to_idx = {s: i for i, s in enumerate(states)}
    
    for iteration in range(I):
        # Forward
        alpha = np.zeros((n, k))
        for i in range(k):
            alpha[0][i] = Emission[i][symbol_to_idx[x[0]]] * (1.0 / k)
        for t in range(1, n):
            for j in range(k):
                alpha[t][j] = Emission[j][symbol_to_idx[x[t]]] * np.sum(alpha[t-1] * Transition[:, j])
        
        # Backward
        beta = np.zeros((n, k))
        beta[-1] = 1
        for t in reversed(range(n-1)):
            for i in range(k):
                beta[t][i] = np.sum(Transition[i, :] * Emission[:, symbol_to_idx[x[t+1]]] * beta[t+1])
        
        # Gamma and Xi
        gamma = np.zeros((n, k))
        xi = np.zeros((n-1, k, k))
        
        for t in range(n-1):
            denom = 0
            for i in range(k):
                for j in range(k):
                    denom += alpha[t][i] * Transition[i][j] * Emission[j][symbol_to_idx[x[t+1]]] * beta[t+1][j]
            for i in range(k):
                gamma[t][i] = 0
                for j in range(k):
                    xi[t][i][j] = (alpha[t][i] * Transition[i][j] * Emission[j][symbol_to_idx[x[t+1]]] * beta[t+1][j]) / denom
                    gamma[t][i] += xi[t][i][j]
        gamma[n-1] = alpha[n-1] / np.sum(alpha[n-1])
        
        # Re-estimate Transition matrix
        for i in range(k):
            denom = np.sum(gamma[:-1, i])
            for j in range(k):
                numer = np.sum(xi[:, i, j])
                Transition[i][j] = numer / denom if denom != 0 else 0
        
        # Re-estimate Emission matrix
        for i in range(k):
            denom = np.sum(gamma[:, i])
            for l in range(m):
                numer = 0
                for t in range(n):
                    if x[t] == symbols[l]:
                        numer += gamma[t][i]
                Emission[i][l] = numer / denom if denom != 0 else 0
    
    return Transition, Emission

def print_output(Transition, Emission, states, symbols):
    print("  " + "   ".join(states))
    for i, state in enumerate(states):
        print(state + " " + " ".join(f"{Transition[i][j]:.3f}" for j in range(len(states))))
    print("--------")
    print("  " + "   ".join(symbols))
    for i, state in enumerate(states):
        print(state + " " + " ".join(f"{Emission[i][j]:.3f}" for j in range(len(symbols))))

def main():
    # Dados do Sample Dataset:
    I = 10
    x = "xzyyzyzyxy"
    symbols = ['x', 'y', 'z']
    states = ['A', 'B']
    Transition = np.array([
        [0.019, 0.981],
        [0.668, 0.332]
    ])
    Emission = np.array([
        [0.175, 0.003, 0.821],
        [0.196, 0.512, 0.293]
    ])

    Transition, Emission = baum_welch(x, states, symbols, Transition, Emission, I)
    print_output(Transition, Emission, states, symbols)

if __name__ == "__main__":
    main()

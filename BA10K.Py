import numpy as np

def soft_decoding(x, alphabet, states, transition, emission):
    n = len(x)
    m = len(states)

    # Map symbols and states to indices
    symbol_idx = {c: i for i, c in enumerate(alphabet)}
    state_idx = {s: i for i, s in enumerate(states)}

    # Convert transition and emission to numpy arrays
    transition = np.array(transition)
    emission = np.array(emission)

    # Forward algorithm
    alpha = np.zeros((n, m))
    # Initialization
    alpha[0, :] = emission[:, symbol_idx[x[0]]] / m  # assume uniform initial distribution

    for i in range(1, n):
        for j in range(m):
            alpha[i, j] = emission[j, symbol_idx[x[i]]] * np.sum(alpha[i-1, :] * transition[:, j])
    
    # Backward algorithm
    beta = np.zeros((n, m))
    beta[-1, :] = 1

    for i in reversed(range(n-1)):
        for j in range(m):
            beta[i, j] = np.sum(beta[i+1, :] * transition[j, :] * emission[:, symbol_idx[x[i+1]]])

    # Calculate posterior probabilities
    posterior = alpha * beta
    posterior /= posterior.sum(axis=1, keepdims=True)

    return posterior

# Exemplo de entrada, baseado no sample dataset do Rosalind

x = "zyxxxxyxzz"
alphabet = ['x', 'y', 'z']
states = ['A', 'B']

transition = [
    [0.911, 0.089],
    [0.228, 0.772]
]

emission = [
    [0.356, 0.191, 0.453],
    [0.040, 0.467, 0.493]
]

posterior = soft_decoding(x, alphabet, states, transition, emission)

# Print formatado conforme esperado
print(" ".join(states))
for row in posterior:
    print(" ".join(f"{prob:.4f}" for prob in row))


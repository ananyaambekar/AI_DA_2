import numpy as np

# Define conditional probabilities
P_A = {True: 0.8, False: 0.2}
P_C = {True: 0.5, False: 0.5}
P_G_given_A_C = {
    (True, True): {True: 0.9, False: 0.1},
    (True, False): {True: 0.6, False: 0.4},
    (False, True): {True: 0.7, False: 0.3},
    (False, False): {True: 0.3, False: 0.7}
}
P_J_given_G = {True: {True: 0.8, False: 0.2}, False: {True: 0.2, False: 0.8}}
P_S_given_G = {True: {True: 0.7, False: 0.3}, False: {True: 0.3, False: 0.7}}

# Monte Carlo simulation to estimate P(J = yes | S = yes)
def monte_carlo_simulation(num_samples=10000):
    count_J_yes_given_S_yes = 0
    count_S_yes = 0

    for sample in range(1, num_samples + 1):
        print(f"\nSample {sample}:")

        # Sample Aptitude Skills (A)
        A = np.random.rand() < P_A[True]
        print(f"  Sampled A (Aptitude Skills): {'Yes' if A else 'No'}")

        # Sample Coding Skills (C)
        C = np.random.rand() < P_C[True]
        print(f"  Sampled C (Coding Skills): {'Yes' if C else 'No'}")

        # Sample Grade (G) given A and C
        G = np.random.rand() < P_G_given_A_C[(A, C)][True]
        print(f"  Sampled G (Grade): {'Good' if G else 'OK'}")

        # Sample Go for Job (J) given G
        J = np.random.rand() < P_J_given_G[G][True]
        print(f"  Sampled J (Go for Job): {'Yes' if J else 'No'}")

        # Sample Start a Startup (S) given G
        S = np.random.rand() < P_S_given_G[G][True]
        print(f"  Sampled S (Start a Startup): {'Yes' if S else 'No'}")

        # Check if S is True and accumulate counts
        if S:
            count_S_yes += 1
            if J:
                count_J_yes_given_S_yes += 1
            print(f"  Count S=Yes: {count_S_yes}, Count J=Yes and S=Yes: {count_J_yes_given_S_yes}")

    # Calculate conditional probability
    if count_S_yes == 0:
        return 0  # Avoid division by zero
    return count_J_yes_given_S_yes / count_S_yes

# Run simulation
estimated_probability = monte_carlo_simulation()
print(f"\nEstimated P(J = yes | S = yes): {estimated_probability}")

import random
import statistics
from collections import Counter
import matplotlib.pyplot as plt

def simulate_darkness_escape(
    threshold=7, 
    track_length=16, 
    start_position=0, 
    simulations=100000
):
    results = []

    for _ in range(simulations):
        darkness = start_position
        turns = 0

        while darkness < track_length:
            turns += 1
            d1, d2 = random.randint(1, 6), random.randint(1, 6)

            # Advance darkness if sum < threshold, but not on doubles
            if (d1 + d2) < threshold and d1 != d2:
                darkness += 1

        results.append(turns)

    # Frequency distribution
    freq = Counter(results)

    # Output results
    print("Turns Distribution (turns : count)")
    for turns in sorted(freq):
        print(f"{turns}: {freq[turns]}")

    avg = statistics.mean(results)
    median = statistics.median(results)

    print("\nSummary Statistics:")
    print(f"Average turns until escape: {avg:.2f}")
    print(f"Median turns until escape: {median:.2f}")

    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(results, bins=range(min(results), max(results) + 2), edgecolor="black", alpha=0.7)
    plt.title(f"Darkness Escape Distribution (threshold={threshold}, sims={simulations})")
    plt.xlabel("Turns until Darkness escapes")
    plt.ylabel("Frequency")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


if __name__ == "__main__":
    # Example usage
    simulate_darkness_escape(
        threshold=7,        # Change threshold (7, 8, or 9 usually)
        track_length=16,    # Track size
        start_position=0,   # Starting position
        simulations=10000   # Number of Monte Carlo simulations
    )

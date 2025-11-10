import random
import statistics
from collections import Counter
#import matplotlib.pyplot as plt

def simulate_darkness_escape(
    threshold=7, 
    threshold_changes=None, 
    track_length=16, 
    start_position=0, 
    simulations=100000
):
    """
    Monte Carlo simulation for Darkness escape in Shadows of Brimstone.

    threshold          = starting threshold
    threshold_changes  = dict of {turn_number: new_threshold}
    track_length       = position at which Darkness escapes
    start_position     = initial position of Darkness
    simulations        = number of Monte Carlo runs
    """
    if threshold_changes is None:
        threshold_changes = {}

    results = []

    for _ in range(simulations):
        darkness = start_position
        turns = 0
        current_threshold = threshold

        while darkness < track_length:
            turns += 1

            # Update threshold if this turn is in the change list
            if turns in threshold_changes:
                current_threshold = threshold_changes[turns]

            d1, d2 = random.randint(1, 6), random.randint(1, 6)

            # Advance darkness if sum < threshold, but not on doubles
            if (d1 + d2) < current_threshold and d1 != d2:
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
#    plt.figure(figsize=(10, 6))
#    plt.hist(results, bins=range(min(results), max(results) + 2), edgecolor="black", alpha=0.7)
#    plt.title(f"Darkness Escape Distribution (sims={simulations})")
#    plt.xlabel("Turns until Darkness escapes")
#    plt.ylabel("Frequency")
#    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show average and median lines
#    plt.axvline(avg, color="red", linestyle="dashed", linewidth=1.5, label=f"Average = {avg:.2f}")
#    plt.axvline(median, color="green", linestyle="dotted", linewidth=1.5, label=f"Median = {median:.2f}")
#    plt.legend()
#    plt.show()


if __name__ == "__main__":
    # Example usage with threshold changes
    simulate_darkness_escape(
        threshold=8,
        threshold_changes={15: 8, 30: 9},  # turn → threshold
        track_length=16,
        start_position=0,
        simulations=10000
    )

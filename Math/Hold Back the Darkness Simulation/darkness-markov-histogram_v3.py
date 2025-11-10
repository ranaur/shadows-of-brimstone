import random
import statistics
from collections import Counter
import plotly.graph_objects as go

def simulate_darkness_escape(
    threshold=7, 
    threshold_changes=None, 
    track_length=16, 
    start_position=0, 
    simulations=100000,
    output_html="darkness_simulation.html"
):
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

    # Create histogram with Plotly
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=results,
        nbinsx=(max(results) - min(results) + 1),
        marker=dict(color="royalblue"),
        opacity=0.75
    ))

    # Add average and median lines
    fig.add_vline(x=avg, line=dict(color="red", dash="dash"), annotation_text=f"Avg={avg:.2f}")
    fig.add_vline(x=median, line=dict(color="green", dash="dot"), annotation_text=f"Median={median:.2f}")

    fig.update_layout(
        title=f"Darkness Escape Distribution (sims={simulations})",
        xaxis_title="Turns until Darkness escapes",
        yaxis_title="Frequency",
        bargap=0.1
    )

    # Save as HTML (always works)
    fig.write_html(output_html, auto_open=True)
    print(f"\n✅ Chart saved as {output_html}. It should open in your browser.")

if __name__ == "__main__":
    # Example usage with threshold changes
    simulate_darkness_escape(
        threshold=7,
        threshold_changes={24: 8, 36: 9},  # turn → threshold
        track_length=16,
        start_position=0,
        simulations=50000
    )

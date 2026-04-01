import csv
import plotly.graph_objects as go

# ---------------------------------------------------
# Fractional composition of PFOA as a function of pH
# ---------------------------------------------------
# PFOA is treated here as a monoprotic acid:
#   HA <-> H+ + A-
#
# Fraction of anion (A-) is:
#   alpha_A- = 1 / (1 + 10^(pKa - pH))
#
# Percent anion is:
#   %A- = 100 * alpha_A-
# ---------------------------------------------------

# User-defined parameters
pKa = 3.8
pH_start = 0.0
pH_end = 10.0
pH_step = 0.1

# Output file names
csv_filename = "pfoa_fractional_composition.csv"
plot_filename = "pfoa_fractional_composition.png"


def percent_pfoa_anion(pH, pKa):
    """
    Calculate the percentage of PFOA present as the anion (A-)
    at a given pH using the fractional composition equation.
    """
    return 100.0 / (1.0 + 10.0 ** (pKa - pH))


# Create pH values from 0.0 to 10.0 inclusive at 0.1 intervals
# Example: 0.0, 0.1, 0.2, ..., 9.9, 10.0
num_points = int(round((pH_end - pH_start) / pH_step)) + 1
pH_values = [round(pH_start + i * pH_step, 1) for i in range(num_points)]

# Calculate percent anion and percent neutral acid
anion_percent = [percent_pfoa_anion(pH, pKa) for pH in pH_values]
neutral_percent = [100.0 - value for value in anion_percent]

# ---------------------------------------------------
# Save data to CSV
# ---------------------------------------------------
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Write header row
    writer.writerow(["pH", "PFOA_anion_percent", "PFOA_neutral_percent"])

    # Write data rows
    for pH, anion, neutral in zip(pH_values, anion_percent, neutral_percent):
        writer.writerow([f"{pH:.1f}", f"{anion:.6f}", f"{neutral:.6f}"])

print(f"CSV file saved: {csv_filename}")

# ---------------------------------------------------
# Create the plot
# ---------------------------------------------------
fig = go.Figure()

# Main curve: pH vs % PFOA anion
fig.add_trace(go.Scatter(x=pH_values, y=anion_percent, 
                         mode='lines', name='PFOA anion (%)',
                         line=dict(width=2)))

# Reference line at pKa
fig.add_vline(x=pKa, line_dash="dash", line_width=1.5, 
              annotation_text=f"pKa = {pKa}")

# Reference line at 50%
fig.add_hline(y=50, line_dash="dot", line_width=1.2)

# Update layout
fig.update_layout(
    title="Fractional Composition Diagram for PFOA",
    xaxis_title="pH",
    yaxis_title="PFOA anion (%)",
    hovermode='x unified',
    xaxis=dict(range=[pH_start, pH_end]),
    yaxis=dict(range=[0, 100]),
    width=900,
    height=600
)

fig.write_html(plot_filename.replace('.png', '.html'))

print(f"Interactive plot saved: {plot_filename.replace('.png', '.html')}")
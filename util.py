from dataclasses import dataclass
import math
import matplotlib.pyplot as plt
import pandas as pd


@dataclass
class ExerciseConfig:
    """Configuration for a specific exercise, including joint points and angle thresholds."""

    name: str   # Name of the exercise (e.g., 'Overhead Squat')
    point_a: str  # Outer joint 1 ('hip')
    point_b: str  # Pivot joint ('knee')
    point_c: str  # Outer joint 2 ('ankle')
    outbound_threshold: (
        float  # Threshold for transition from/to start phase to/from outbound state (e.g., 160°)
    )
    inflection_threshold: (
        float  # Threshold for transition from/to outbound phase to/from inflection state (e.g., 120°)
    )
    inbound_buffer: (
        float  # Buffer to transition from inflection state to inbound state (e.g., 15°)
    )
    is_angle_decreasing: bool  # True if angle drops during rep
    min_angle: (
        float  # Buffer to transition from inflection state to inbound state (e.g., 15°)
    )
    max_angle: (
        float  # Buffer to transition from inflection state to inbound state (e.g., 15°)
    )
    max_frame_delta: (
        float  # Maximum allowed change in angle between consecutive frames (e.g., 25°)
    )


def calc_3d_angle(a: list, b: list, c: list) -> float:
    """
    Calculates the 3D angle in degrees at vertex b formed by points a, b, and c
    """
    # Compute vector components ba and bc
    ba_x, ba_y, ba_z = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    bc_x, bc_y, bc_z = c[0] - b[0], c[1] - b[1], c[2] - b[2]

    # Compute vector magnitudes (Euclidean norm) using sqrt
    norm_ba = math.sqrt(ba_x * ba_x + ba_y * ba_y + ba_z * ba_z)
    norm_bc = math.sqrt(bc_x * bc_x + bc_y * bc_y + bc_z * bc_z)

    # Handle degenerate case (zero-length vector)
    if norm_ba == 0.0 or norm_bc == 0.0:
        return 180.0

    # Compute dot product
    dot_product = (ba_x * bc_x) + (ba_y * bc_y) + (ba_z * bc_z)

    # Compute cosine and clip manually to [-1.0, 1.0] to avoid acos domain errors
    cosine_angle = dot_product / (norm_ba * norm_bc)
    if cosine_angle > 1.0:
        cosine_angle = 1.0
    elif cosine_angle < -1.0:
        cosine_angle = -1.0

    # Convert angle from radians to degrees
    angle_radians = math.acos(cosine_angle)
    angle_degrees = angle_radians * (180.0 / math.pi)

    return round(angle_degrees, 4)


def calc_2d_angle(a: list, b: list, c: list) -> float:
    """
    Calculates the 2D angle in degrees at vertex b formed by points a, b, and c
    """
    # Compute 2D vector components ba and bc
    ba_x, ba_y = a[0] - b[0], a[1] - b[1]
    bc_x, bc_y = c[0] - b[0], c[1] - b[1]

    # Compute 2D vector magnitudes (Euclidean norm)
    norm_ba = math.sqrt(ba_x * ba_x + ba_y * ba_y)
    norm_bc = math.sqrt(bc_x * bc_x + bc_y * bc_y)

    # Handle degenerate case (zero-length vector)
    if norm_ba == 0.0 or norm_bc == 0.0:
        return 180.0

    # Compute 2D dot product
    dot_product = (ba_x * bc_x) + (ba_y * bc_y)

    # Compute cosine and clip manually to [-1.0, 1.0] to avoid acos domain errors
    cosine_angle = dot_product / (norm_ba * norm_bc)
    if cosine_angle > 1.0:
        cosine_angle = 1.0
    elif cosine_angle < -1.0:
        cosine_angle = -1.0

    # Convert angle from radians to degrees
    angle_radians = math.acos(cosine_angle)
    angle_degrees = angle_radians * (180.0 / math.pi)

    return round(angle_degrees, 4)


def plot_data(df: pd.DataFrame, columns: list[str], title: str = "Angle", filename: str = "plot.png") -> int:
    """Plots rows of a DataFrame as overlaid line charts across specified columns."""
    color_list = ["Red", "Blue", "Green", "Orange", "Purple", "Brown", "Teal", "Gold", "Tomato", "Slate gray"]
    plt.figure(figsize=(12, 6))
        
    # Plot both lines against idx
    i = 0
    for col in columns:
        plt.plot(df['idx'], df[col], label=col, color=color_list[i])
        i += 1

    # Customization
    plt.title(title)
    plt.xlabel("frame")
    plt.ylabel("Angle Values")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.ylim(0, 200)

    plt.tight_layout()
    plt.savefig(filename)
    return 1


if __name__ == "__main__":
    print("Utils")
import h5py
import numpy as np
from pynwb import NWBHDF5IO, TimeSeries


def add_tracking_data_simple(tracking_h5_file, nwb_file):
    """Add treadmill tracking data using simple TimeSeries - avoids extension conflicts."""

    # Read tracking data
    with h5py.File(tracking_h5_file, "r") as f:
        tracking_data = f["tracking_data"][:]

    print(f"Tracking data shape: {tracking_data.shape}")
    print(f"Tracking data dtype: {tracking_data.dtype}")

    # Extract individual components - CORRECTLY handle the 4-field structure
    # The data shape is (23300, 4) but dtype shows it's a structured array
    # Each "row" contains 4 fields: loc_x, loc_y, theta, tmst

    loc_x = tracking_data["loc_x"]  # Don't flatten yet
    loc_y = tracking_data["loc_y"]
    theta = tracking_data["theta"]
    timestamps = tracking_data["tmst"]

    print(f"Before flattening:")
    print(f"  loc_x shape: {loc_x.shape}")
    print(f"  timestamps shape: {timestamps.shape}")

    # Now flatten properly - the issue was that we had (23300, 4)
    # being treated as if each field was expanded
    if len(loc_x.shape) > 1:
        loc_x = loc_x.flatten()
        loc_y = loc_y.flatten()
        theta = theta.flatten()
        timestamps = timestamps.flatten()

    print(f"After flattening:")
    print(f"  loc_x shape: {loc_x.shape}")
    print(f"  Sample timestamps: {timestamps[:5]}")
    print(f"  Timestamp range: {timestamps[0]} to {timestamps[-1]}")

    # Convert timestamps to seconds if needed
    if np.max(timestamps) > 10000:
        timestamps = timestamps / 1000.0
        print("Converted timestamps from milliseconds to seconds")
        print(f"New range: {timestamps[0]:.3f} to {timestamps[-1]:.3f} seconds")

    # Prepare data
    position_data = np.column_stack([loc_x, loc_y])

    # Calculate speed
    dx = np.diff(loc_x)
    dy = np.diff(loc_y)
    dt = np.diff(timestamps)
    dt[dt == 0] = np.finfo(float).eps  # Avoid division by zero
    speed = np.sqrt(dx**2 + dy**2) / dt
    speed = np.concatenate([[0], speed])  # Add initial zero

    # Add to NWB file using simple TimeSeries
    with NWBHDF5IO(nwb_file, "r+") as io:
        nwbfile = io.read()

        # Create TimeSeries for position (avoid SpatialSeries to prevent conflicts)
        position_ts = TimeSeries(
            name="treadmill_position_xy",
            description="treadmill tracking position (x, y coordinates)",
            data=position_data,
            timestamps=timestamps,
            unit="units",  # Replace with your actual units
            comments="Columns: loc_x, loc_y from treadmill tracking system",
        )

        # Create TimeSeries for orientation
        orientation_ts = TimeSeries(
            name="treadmill_orientation_theta",
            description="Animal orientation angle on treadmill",
            data=theta,
            timestamps=timestamps,
            unit="radians",
            comments="Theta angle from treadmill tracking system",
        )

        # Create TimeSeries for speed
        speed_ts = TimeSeries(
            name="treadmill_movement_speed",
            description="Instantaneous movement speed on treadmill",
            data=speed,
            timestamps=timestamps,
            unit="units/second",
            comments="Calculated from position derivatives",
        )

        # Add to behavior module
        if "behavior" not in nwbfile.processing:
            behavior_module = nwbfile.create_processing_module(
                name="behavior", description="Behavioral tracking and analysis"
            )
        else:
            behavior_module = nwbfile.processing["behavior"]

        # Add all tracking data as simple TimeSeries
        behavior_module.add(position_ts)
        behavior_module.add(orientation_ts)
        behavior_module.add(speed_ts)

        io.write(nwbfile)

    print("✅ Treadmill tracking data added successfully!")
    print(f"   Position data: {len(timestamps)} timepoints")
    print(f"   Duration: {timestamps[-1] - timestamps[0]:.2f} seconds")
    print(f"   Average speed: {speed.mean():.3f} units/second")

    return True


# Use this simple approach
add_tracking_data_simple(
    "tracking_data_100_36_2022-05-30-14-21-03.h5", "nwb_animal_277_session_22.nwb"
)

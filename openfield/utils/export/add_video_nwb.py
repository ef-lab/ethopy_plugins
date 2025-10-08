import h5py
from pynwb import NWBHDF5IO
from pynwb.image import ImageSeries


def add_video_with_structured_timestamps(h5_file, nwb_file, video_path):
    # Read structured timestamp data
    with h5py.File(h5_file, "r") as f:
        timestamps_structured = f["frame_tmst"][:]

        # Extract the timestamp field from structured array
        timestamps_numeric = timestamps_structured["timestamp"].flatten()

        # Convert to seconds if needed
        if timestamps_numeric.max() > 10000:  # Likely milliseconds
            timestamps_seconds = timestamps_numeric / 1000.0
            print(
                f"Converted {len(timestamps_seconds)} timestamps from milliseconds to seconds"
            )
        else:
            timestamps_seconds = timestamps_numeric
            print(f"Using {len(timestamps_seconds)} timestamps as seconds")

    # Add to NWB file
    with NWBHDF5IO(nwb_file, "r+") as io:
        nwbfile = io.read()

        # Check if behavioral_video already exists and remove it
        if "behavioral_video" in nwbfile.acquisition:
            print("Removing existing behavioral_video entry...")
            del nwbfile.acquisition["behavioral_video"]

        video_series = ImageSeries(
            name="behavioral_video",
            description="Behavioral video recorded during session",
            external_file=[video_path],  # Path to your MP4 file
            format="external",
            timestamps=timestamps_seconds,
            unit="n.a.",
        )

        nwbfile.add_acquisition(video_series)
        io.write(nwbfile)

    print("Video added successfully!")
    print(f"   Timestamps: {len(timestamps_seconds)} frames")
    print(f"   Duration: {timestamps_seconds[-1] - timestamps_seconds[0]:.3f} seconds")
    print(
        f"   Frame rate: ~{len(timestamps_seconds) / (timestamps_seconds[-1] - timestamps_seconds[0]):.1f} fps"
    )

    return timestamps_seconds


if __name__ == "__main__":
    # Use the function
    timestamps_seconds = add_video_with_structured_timestamps(
        "video_tmst_animal_id_277_session_22.h5",
        "nwb_animal_277_session_22.nwb",
        "277_22.mp4",
    )
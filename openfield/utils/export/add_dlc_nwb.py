"""DLC to NWB conversion script with proper ndx-pose structure."""

import h5py
import numpy as np
from ndx_pose import PoseEstimation, PoseEstimationSeries, Skeleton, Skeletons
from pynwb import NWBHDF5IO, TimeSeries
from pynwb.file import Subject

# ============================================================================
# USER CONFIGURATION - MODIFY THESE PARAMETERS FOR YOUR EXPERIMENT
# ============================================================================

CONFIG = {
    # File paths
    "dlc_h5_file": "dlc_277_22_2025-01-30-13-28-56.h5",
    "nwb_file": "nwb_animal_277_session_22.nwb",
    # Subject information
    "subject_id": "animal_277",
    "species": "Mus musculus",
    # Bodyparts (must match the field names in your DLC H5 file)
    "bodyparts": [
        "nose",
        "leftear",
        "rightear",
        "middle",
        "tailbase",
        "tailmiddle",
        "tailedge",
    ],
    # Skeleton connections (indices refer to bodyparts list above)
    "skeleton_edges": [
        [0, 3],  # nose to middle
        [1, 3],  # leftear to middle
        [2, 3],  # rightear to middle
        [3, 4],  # middle to tailbase
        [4, 5],  # tailbase to tailmiddle
        [5, 6],  # tailmiddle to tailedge
    ],
    # Camera/Device information
    "camera_name": "camera",
    "camera_description": "Behavioral recording camera",
    "camera_manufacturer": "Unknown",
    # Video information
    "original_videos": ["behavioral_video.mp4"],  # List of video file paths
    "video_dimensions": [640, 480],  # [width, height] in pixels
    # DLC model information
    "dlc_scorer": "DLC_Openfield_ratbox_resnet_50_iteration-3_shuffle-1",
    "dlc_software": "DeepLabCut",
    "dlc_version": "2.x",
    # Data processing options
    "convert_timestamps_from_ms": True,  # False if timestamps are already in seconds
    "timestamp_threshold": 10000,  # Values above this are considered milliseconds
    # Metadata
    "reference_frame": "top-left corner of video frame",
    "confidence_definition": "DeepLabCut confidence score (likelihood)",
    "processed_confidence_definition": "Processed data - confidence not applicable",
    # Processing module information
    "behavior_module_name": "behavior",
    "behavior_module_description": "Behavioral pose estimation and analysis",
    # Pose estimation names and descriptions
    "raw_pose_name": "DLC_pose_estimation",
    "raw_pose_description": "DeepLabCut pose estimation",
    "processed_pose_name": "DLC_processed_pose",
    "processed_pose_description": "Processed DeepLabCut head tracking",
    "orientation_name": "head_orientation",
    "orientation_description": "Head orientation angle from processed DLC data",
    "orientation_unit": "radians",  # or "degrees"
}

# ============================================================================
# MAIN FUNCTION - NO NEED TO MODIFY BELOW THIS LINE
# ============================================================================


def add_dlc_data_ndx_pose(config=None):
    """Add DLC data using proper ndx-pose structure based on the examples.

    Parameters:
    -----------
    config : dict, optional
        Configuration dictionary. If None, uses the global CONFIG.
    """
    if config is None:
        config = CONFIG

    print("Starting DLC to NWB conversion...")
    print(f"Input file: {config['dlc_h5_file']}")
    print(f"Output file: {config['nwb_file']}")

    # Read DLC data
    with h5py.File(config["dlc_h5_file"], "r") as f:
        dlc_raw = f["dlc"][:]
        dlc_processed = f["dlc_processed"][:]

    print(f"Loaded DLC data: {dlc_raw.shape[0]} frames")

    # Extract timestamps
    timestamps_raw = dlc_raw["timestamp"].flatten()
    timestamps_processed = dlc_processed["timestamp"].flatten()

    # Convert timestamps to seconds if needed
    if (
        config["convert_timestamps_from_ms"]
        and timestamps_raw.max() > config["timestamp_threshold"]
    ):
        timestamps_raw = timestamps_raw / 1000.0
        timestamps_processed = timestamps_processed / 1000.0
        print("Converted timestamps from milliseconds to seconds")

    with NWBHDF5IO(config["nwb_file"], "r+") as io:
        nwbfile = io.read()

        # Add subject if not present
        if nwbfile.subject is None:
            subject = Subject(
                subject_id=config["subject_id"], species=config["species"]
            )
            nwbfile.subject = subject
            print(f"Added subject: {config['subject_id']}")
        else:
            subject = nwbfile.subject

        # Create skeleton for mouse bodyparts
        skeleton = Skeleton(
            name="mouse_skeleton",
            nodes=config["bodyparts"],
            edges=np.array(config["skeleton_edges"], dtype="uint8"),
            subject=subject,
        )

        # Store skeleton in container
        skeletons = Skeletons(skeletons=[skeleton])

        # Create device for camera (if not exists)
        try:
            camera = nwbfile.devices[config["camera_name"]]
        except KeyError:
            camera = nwbfile.create_device(
                name=config["camera_name"],
                description=config["camera_description"],
                manufacturer=config["camera_manufacturer"],
            )
            print(f"Created camera device: {config['camera_name']}")

        # Create individual PoseEstimationSeries for each bodypart
        pose_estimation_series = []

        # Create the first bodypart with timestamps, others will reference it
        first_bodypart = config["bodyparts"][0]
        x_data = dlc_raw[f"{first_bodypart}_x"].flatten()
        y_data = dlc_raw[f"{first_bodypart}_y"].flatten()
        confidence_data = dlc_raw[f"{first_bodypart}_score"].flatten()

        # Combine x,y coordinates for this bodypart
        bodypart_data = np.column_stack([x_data, y_data])

        first_series = PoseEstimationSeries(
            name=first_bodypart,
            description=f"DLC estimated position of {first_bodypart}",
            data=bodypart_data,
            unit="pixels",
            reference_frame=config["reference_frame"],
            timestamps=timestamps_raw,  # Only first series has timestamps
            confidence=confidence_data,
            confidence_definition=config["confidence_definition"],
        )
        pose_estimation_series.append(first_series)

        # Create remaining bodyparts (referencing first series for timestamps)
        for bodypart in config["bodyparts"][1:]:
            x_data = dlc_raw[f"{bodypart}_x"].flatten()
            y_data = dlc_raw[f"{bodypart}_y"].flatten()
            confidence_data = dlc_raw[f"{bodypart}_score"].flatten()

            bodypart_data = np.column_stack([x_data, y_data])

            series = PoseEstimationSeries(
                name=bodypart,
                description=f"DLC estimated position of {bodypart}",
                data=bodypart_data,
                unit="pixels",
                reference_frame=config["reference_frame"],
                timestamps=first_series,  # Reference first series for timestamps
                confidence=confidence_data,
                confidence_definition=config["confidence_definition"],
            )
            pose_estimation_series.append(series)

        print(f"Created {len(pose_estimation_series)} pose estimation series")

        # Create PoseEstimation object
        pose_estimation = PoseEstimation(
            name=config["raw_pose_name"],
            pose_estimation_series=pose_estimation_series,
            description=config["raw_pose_description"],
            original_videos=config["original_videos"],
            dimensions=np.array([config["video_dimensions"]], dtype="uint16"),
            devices=[camera],
            scorer=config["dlc_scorer"],
            source_software=config["dlc_software"],
            source_software_version=config["dlc_version"],
            skeleton=skeleton,
        )

        # Create separate PoseEstimation for processed head data
        head_x = dlc_processed["head_x"].flatten()
        head_y = dlc_processed["head_y"].flatten()
        head_coords = np.column_stack([head_x, head_y])

        processed_head_series = PoseEstimationSeries(
            name="processed_head",
            description="Processed head position from DLC",
            data=head_coords,
            unit="pixels",
            reference_frame=config["reference_frame"],
            timestamps=timestamps_processed,
            confidence=np.ones(len(head_coords)),  # Dummy confidence for processed data
            confidence_definition=config["processed_confidence_definition"],
        )

        pose_estimation_processed = PoseEstimation(
            name=config["processed_pose_name"],
            pose_estimation_series=[processed_head_series],
            description=config["processed_pose_description"],
            original_videos=config["original_videos"],
            dimensions=np.array([config["video_dimensions"]], dtype="uint16"),
            devices=[camera],
            scorer="DLC_processed",
            source_software=config["dlc_software"],
            source_software_version=config["dlc_version"],
        )

        # Add head orientation as TimeSeries (since it's not pose coordinates)
        orientation_series = TimeSeries(
            name=config["orientation_name"],
            description=config["orientation_description"],
            data=dlc_processed["angle"].flatten(),
            timestamps=timestamps_processed,
            unit=config["orientation_unit"],
        )

        # Add to behavior processing module
        if config["behavior_module_name"] not in nwbfile.processing:
            behavior_module = nwbfile.create_processing_module(
                name=config["behavior_module_name"],
                description=config["behavior_module_description"],
            )
        else:
            behavior_module = nwbfile.processing[config["behavior_module_name"]]

        # Add all objects to behavior module
        behavior_module.add(skeletons)
        behavior_module.add(pose_estimation)
        behavior_module.add(pose_estimation_processed)
        behavior_module.add(orientation_series)

        # Write changes
        io.write(nwbfile)

    print("DLC data added successfully with proper ndx-pose structure!")
    print(f"Raw pose estimation: {len(config['bodyparts'])} bodyparts")
    print("Processed pose estimation: head tracking")
    print("Head orientation: separate TimeSeries")
    return True


def validate_config(config):
    """Validate the configuration parameters."""
    required_fields = [
        "dlc_h5_file",
        "nwb_file",
        "subject_id",
        "species",
        "bodyparts",
        "skeleton_edges",
        "video_dimensions",
        "dlc_scorer",
    ]

    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required configuration field: {field}")

    if len(config["skeleton_edges"]) > 0:
        max_index = max(max(edge) for edge in config["skeleton_edges"])
        if max_index >= len(config["bodyparts"]):
            raise ValueError(
                f"Skeleton edge index {max_index} exceeds bodyparts list length"
            )

    print("Configuration validation passed!")
    return True


if __name__ == "__main__":
    # Validate configuration
    validate_config(CONFIG)

    # Run the conversion
    add_dlc_data_ndx_pose()

    # Alternative: Create custom configuration
    # custom_config = CONFIG.copy()
    # custom_config["subject_id"] = "animal_123"
    # custom_config["dlc_h5_file"] = "my_dlc_data.h5"
    # add_dlc_data_ndx_pose(custom_config)

import pandas as pd
from pathlib import Path
from util import calc_3d_angle, calc_2d_angle, plot_data

def insert_into_buffer(arr, new_val, size=6):
    arr.append(new_val)
    if len(arr) > size:
        arr.pop(0)
    return arr


def process_3d_exercise(exercise_json: dict, csv_file_path: str) -> int:
    """Simulates exercise motion capture data one frame at a time and runs angle calculation."""

    # Load exercise data
    df = pd.read_csv(csv_file_path, sep=';' if ';' in open(csv_file_path).readline() else ',')
    df = df.dropna().reset_index(drop=True)

    name = exercise_json['name']
    angles = exercise_json['angles']
    angle_name_list = []
    angle_rows = []

    for angle_name, landmarks in angles.items():
        angle_name_list.append(angle_name)
        
        # Build CSV column names
        point_a_cols = [f"{landmarks[0]}_3D_{c}" for c in ['X', 'Y', 'Z']]
        point_b_cols = [f"{landmarks[1]}_3D_{c}" for c in ['X', 'Y', 'Z']]

        point_a_data = df[point_a_cols].values.tolist()
        point_b_data = df[point_b_cols].values.tolist()

        # Check if landmark C is a vertical reference (landmarks[1] == landmarks[2])
        if landmarks[1] == landmarks[2]:
            # Construct Point C by adding +1.0 meter along the Y-axis relative to Point B (vertex)
            point_c_data = [[b[0], b[1] + 1.0, b[2]] for b in point_b_data]
        else:
            point_c_cols = [f"{landmarks[2]}_3D_{c}" for c in ['X', 'Y', 'Z']]
            point_c_data = df[point_c_cols].values.tolist()

        # Iterate one row at a time to simulate receiving frame-by-frame data
        for idx, a, b, c in zip(df.index, point_a_data, point_b_data, point_c_data):
            # Calculate angle value
            value = calc_3d_angle(a, b, c)

            print(f"{idx}: angle={angle_name}, value={value}")
            angle_rows.append({'idx': idx, 'angle_name': angle_name, 'value': value})

    # Save calculated 3D angles to CSV
    output_path = Path('outputs') / f"{Path(csv_file_path).stem}_3d-angles.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    angle_df = pd.DataFrame(angle_rows, columns=['idx', 'angle_name', 'value'])
    angle_df = angle_df.pivot(index='idx', columns='angle_name', values='value').reset_index()
    angle_df.columns.name = None
    angle_df.to_csv(output_path, index=False)

    # Filtered Plot Generation
    available_cols = angle_df.columns.tolist()

    # Knee Angles
    knee_cols = [c for c in ['right_knee_angle', 'left_knee_angle'] if c in available_cols]
    if knee_cols:
        output_png_path = Path('outputs') / f"{Path(csv_file_path).stem}_3d-knee.png"
        plot_data(angle_df, columns=knee_cols, title=f"{name} - 3D Knee Angles", filename=output_png_path)

    # Shoulder Angles
    shoulder_cols = [c for c in ['right_shoulder_angle', 'left_shoulder_angle'] if c in available_cols]
    if shoulder_cols:
        output_png_path = Path('outputs') / f"{Path(csv_file_path).stem}_3d-shoulder.png"
        plot_data(angle_df, columns=shoulder_cols, title=f"{name} - 3D Shoulder Angles", filename=output_png_path)

    # Spine Angle
    spine_cols = [c for c in ['spine_angle'] if c in available_cols]
    if spine_cols:
        output_png_path = Path('outputs') / f"{Path(csv_file_path).stem}_3d-spine.png"
        plot_data(angle_df, columns=spine_cols, title=f"{name} - 3D Spine Angles", filename=output_png_path)

    return 1


def process_2d_exercise(exercise_json: dict, csv_file_path: str) -> int:
    """Simulates exercise motion capture data one frame at a time and runs 2D angle calculation."""

    # Load exercise data
    df = pd.read_csv(csv_file_path, sep=';' if ';' in open(csv_file_path).readline() else ',')
    df = df.dropna().reset_index(drop=True)

    name = exercise_json['name']
    angles = exercise_json['angles']
    angle_name_list = []
    angle_rows = []

    for angle_name, landmarks in angles.items():
        angle_name_list.append(angle_name)
        
        # Build 2D CSV column names
        point_a_cols = [f"{landmarks[0]}_2D_{c}" for c in ['X', 'Y']]
        point_b_cols = [f"{landmarks[1]}_2D_{c}" for c in ['X', 'Y']]

        point_a_data = df[point_a_cols].values.tolist()
        point_b_data = df[point_b_cols].values.tolist()

        # Check if landmark C is a vertical reference line (landmarks[1] == landmarks[2])
        if landmarks[1] == landmarks[2]:
            # Construct Point C by adding offset along the +Y axis (downward toward ground)
            # Use +1.0 for normalized coordinates [0, 1] or +100.0 for screen pixel space
            offset_y = 1.0 if max(b[1] for b in point_b_data) <= 2.0 else 100.0
            point_c_data = [[b[0], b[1] + offset_y] for b in point_b_data]
        else:
            point_c_cols = [f"{landmarks[2]}_2D_{c}" for c in ['X', 'Y']]
            point_c_data = df[point_c_cols].values.tolist()

        # Iterate one row at a time to simulate receiving frame-by-frame data
        for idx, a, b, c in zip(df.index, point_a_data, point_b_data, point_c_data):
            # Calculate 2D angle value
            value = calc_2d_angle(a, b, c)

            print(f"{idx}: angle={angle_name}, value={value}")
            angle_rows.append({'idx': idx, 'angle_name': angle_name, 'value': value})

    # Save calculated 2D angles to CSV
    output_path = Path('outputs') / f"{Path(csv_file_path).stem}_2d-angles.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    angle_df = pd.DataFrame(angle_rows, columns=['idx', 'angle_name', 'value'])
    angle_df = angle_df.pivot(index='idx', columns='angle_name', values='value').reset_index()
    angle_df.columns.name = None
    angle_df.to_csv(output_path, index=False)

    # Filtered Plot Generation
    available_cols = angle_df.columns.tolist()

    # Knee Angles
    knee_cols = [c for c in ['right_knee_angle', 'left_knee_angle'] if c in available_cols]
    if knee_cols:
        output_png_path = Path('outputs') / f"{Path(csv_file_path).stem}_2d-knee.png"
        plot_data(angle_df, columns=knee_cols, title=f"{name} - 2D Knee Angles", filename=output_png_path)

    # Shoulder Angles
    shoulder_cols = [c for c in ['right_shoulder_angle', 'left_shoulder_angle'] if c in available_cols]
    if shoulder_cols:
        output_png_path = Path('outputs') / f"{Path(csv_file_path).stem}_2d-shoulder.png"
        plot_data(angle_df, columns=shoulder_cols, title=f"{name} - 2D Shoulder Angles", filename=output_png_path)

    # Spine Angle
    spine_cols = [c for c in ['spine_angle'] if c in available_cols]
    if spine_cols:
        output_png_path = Path('outputs') / f"{Path(csv_file_path).stem}_2d-spine.png"
        plot_data(angle_df, columns=spine_cols, title=f"{name} - 2D Spine Angles", filename=output_png_path)

    return 1



if __name__ == "__main__":

    # Overhead Squat Testing
    # Mirrored Scenario
    exercise_json = {
        'name': 'Overhead Squat - 45 Degree Test',
        'angles': { 'right_knee_angle': ['HipLeft', 'KneeLeft', 'AnkleLeft'],
                    'left_knee_angle': ['HipRight', 'KneeRight', 'AnkleRight'],
                    'right_shoulder_angle': ['WristLeft', 'ShoulderLeft', 'ShoulderLeft'],
                    'left_shoulder_angle': ['WristRight', 'ShoulderRight', 'ShoulderRight'],
                    'spine_angle': ['Neck', 'Pelvis', 'Pelvis']} 
    }
    csv_file = "data//45.Deg.Rotated.Full.Depth.OVHD.SQ.9.25.26.csv"
    process_2d_exercise(exercise_json, csv_file)
    process_3d_exercise(exercise_json, csv_file)

    """
    #------------------------------------------------------------------------------------

    exercise_json = {
        'name': 'KB Deadlift',
        'angles': { 'spine': ['Chest', 'Waist', 'Pelvis']}
                    #'left_shoulder_angle': ['WristLeft', 'ShoulderLeft', 'ShoulderLeft_0'], 
                    #'right_shoulder_angle': ['WristRight', 'ShoulderRight', 'ShoulderRight_0']}
    }

    csv_file = "data//LB.KB.Deadlift.csv"
    #process_2d_exercise(exercise_json, csv_file)

    #------------------------------------------------------------------------------------
    exercise_json = {
        'name': 'Reverse Lunge',
        'angles': { 'right_spine': ['Nose', 'HipLeft', 'HipLeft'], # 0 line angle 
                    'right_hip': ['KneeLeft', 'HipLeft', 'HipLeft'], # 0 line angle 
                    'right_knee': ['HipLeft', 'KneeLeft', 'AnkleLeft'],
                    'right_shin': ['KneeLeft', 'AnkleLeft', 'AnkleLeft'], # 0 line angle
                    'right_counting_angle': ['HipLeft', 'KneeLeft', 'KneeLeft'], # 0 line angle
                    'left_spine': ['Nose', 'HipRight', 'HipRight'], # 0 line angle 
                    'left_hip': ['KneeRight', 'HipRight', 'HipRight'], # 0 line angle 
                    'left_knee': ['HipRight', 'KneeRight', 'AnkleRight'],
                    'left_shin': ['KneeRight', 'AnkleRight', 'AnkleRight'], # 0 line angle
                    'left_counting_angle': ['HipRight', 'KneeRight', 'KneeRight']} # 0 line angle

    }



    csv_file = "data//LB.Reverse.Lunge.csv"
    #process_2d_exercise(exercise_json, csv_file)

    #------------------------------------------------------------------------------------
    exercise_json = {
        'name': 'Straight Leg Raise',
        'angles': { 'right_hip': ['AnkleLeft', 'HipLeft', 'HipLeft'], # 0 line angle 
                    'right_knee': ['AnkleLeft', 'KneeLeft', 'HipLeft'],
                    'right_counting_angle': ['AnkleLeft', 'HipLeft', 'ShoulderLeft'], # 0 line angle
                    'left_hip': ['AnkleRight', 'HipRight', 'HipRight'], # 0 line angle 
                    'left_knee': ['AnkleRight', 'KneeRight', 'HipRight'],
                    'left_counting_angle': ['AnkleRight', 'HipRight', 'ShoulderRight']} # 0 line angle

    }


    csv_file = "data//LB.straight.leg.raise.csv"
    #process_2d_exercise(exercise_json, csv_file)




    # Overhead Squat Configuration
    exercise_json = {
        'name': 'Overhead Squat',
        'angles': { 'left_knee_angle': ['HipLeft', 'KneeLeft', 'AnkleLeft'], 
                    'right_knee_angle': ['HipRight', 'KneeRight', 'AnkleRight'],
                    'left_shoulder_angle': ['WristLeft', 'ShoulderLeft', 'ShoulderLeft'],
                    'right_shoulder_angle': ['WristRight', 'ShoulderRight', 'ShoulderRight'],
                    'spine_angle': ['Neck', 'Pelvis', 'Pelvis'],
                    'counting_angle': ['AnkleRight', 'KneeRight', 'HipRight']} 
                    #'right_shoulder_angle': ['WristRight', 'ShoulderRight', 'ShoulderRight_0']}
    }
    csv_file = "data//Straight-Leg-Test-09212026.csv"
    process_3d_exercise(exercise_json, csv_file)
    """
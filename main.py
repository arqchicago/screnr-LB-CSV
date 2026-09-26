import pandas as pd
from pathlib import Path
from util import calc_3d_angle, calc_2d_angle

def insert_into_buffer(arr, new_val, size=6):
    arr.append(new_val)
    if len(arr) > size:
        arr.pop(0)
    return arr

def process_3d_exercise(exercise_json: dict, csv_file_path: str) -> int:
    """ This simulates exercise motion capture data one frame at a time and runs angle filtering and rep counting """

    # Load exercise data
    df = pd.read_csv(csv_file_path, sep=';' if ';' in open(csv_file_path).readline() else ',')
    df = df.dropna().reset_index(drop=True)

    angles = exercise_json['angles']
    angle_rows = []

    for angle_name, landmarks in angles.items():
        point_a_cols = []
        point_b_cols = []
        point_c_cols = []

        for coord in ['X', 'Y', 'Z']:
            point_a_cols.append(landmarks[0] + "_3D_"+coord)
            point_b_cols.append(landmarks[1] + "_3D_"+coord)
            point_c_cols.append(landmarks[2] + "_3D_"+coord)

        point_a_data = df[point_a_cols].values.tolist()
        point_b_data = df[point_b_cols].values.tolist()
        point_c_data = df[point_c_cols].values.tolist()

        if landmarks[1] == landmarks[2]:
            for point_c in point_c_data:
                point_c[1] += point_c[1] * 0.10 if point_c[1] != 0 else 1.0

        # Iterate one row at a time to simulate receiving motion capture data one frame at a time
        for idx, a, b, c in zip(df.index, point_a_data, point_b_data, point_c_data):

            # Calculate angle value
            value = calc_3d_angle(a, b, c)

            # Prepare an array of size n containing most recent angles received (e.g., [170, 165, 74, 154, 148]) 
            print(f"{idx}: angle={angle_name},  value={value}")
            angle_rows.append({'idx': idx, 'angle_name': angle_name, 'value': value})

    output_path = Path('outputs') / f"{Path(csv_file_path).stem}_angles.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(angle_rows, columns=['idx', 'angle_name', 'value']).to_csv(output_path, index=False)

    return 1


def process_2d_exercise(exercise_json: dict, csv_file_path: str) -> int:
    """ This simulates exercise motion capture data one frame at a time and runs angle filtering and rep counting """

    # Load exercise data
    df = pd.read_csv(csv_file_path, sep=';' if ';' in open(csv_file_path).readline() else ',')
    df = df.dropna().reset_index(drop=True)

    angles = exercise_json['angles']
    angle_rows = []

    for angle_name, landmarks in angles.items():
        point_a_cols = []
        point_b_cols = []
        point_c_cols = []

        for coord in ['X', 'Y']:
            point_a_cols.append(landmarks[0] + "_2D_"+coord)
            point_b_cols.append(landmarks[1] + "_2D_"+coord)
            point_c_cols.append(landmarks[2] + "_2D_"+coord)

        point_a_data = df[point_a_cols].values.tolist()
        point_b_data = df[point_b_cols].values.tolist()
        point_c_data = df[point_c_cols].values.tolist()

        if landmarks[1] == landmarks[2]:
            for point_c in point_c_data:
                point_c[1] *= 1.10

        # Iterate one row at a time to simulate receiving motion capture data one frame at a time
        for idx, a, b, c in zip(df.index, point_a_data, point_b_data, point_c_data):

            # Calculate angle value
            value = calc_2d_angle(a, b, c)

            # Prepare an array of size n containing most recent angles received (e.g., [170, 165, 74, 154, 148]) 
            print(f"{idx}: angle={angle_name},  value={value}")
            angle_rows.append({'idx': idx, 'angle_name': angle_name, 'value': value})

    output_path = Path('outputs') / f"{Path(csv_file_path).stem}_angles.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(angle_rows, columns=['idx', 'angle_name', 'value']).to_csv(output_path, index=False)

    return 1

if __name__ == "__main__":

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
    csv_file = "data//LB.Overhead.Squat.test.csv"
    #process_3d_exercise(exercise_json, csv_file)

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
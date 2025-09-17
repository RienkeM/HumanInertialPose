# File to try the data processing with our own datasets

from hipose.data.trial_parsing.extract_xsens_analyse import extract_xsens_analyse_raw_data2
# example_data_path = "C:\\Users\\rienk\\OneDrive - University of Twente\\BME\\Internship\\3. project content\\Python\\Xsens_data\\0905_demo2_seated"
example_data_path = "C:\\Users\\rienk\\OneDrive - University of Twente\\BME\\Internship\\3. project content\\Python\\Xsens_data\\0915_demo3_Npose"
# example_data_path = "C:\\Users\\rienk\\OneDrive - University of Twente\\BME\\Internship\\3. project content\\Python\\Xsens_data\\0915_demo4_Npose"
# example_data_path = "C:\\Users\\rienk\\OneDrive - University of Twente\\BME\\Internship\\3. project content\\Python\\Xsens_data\\0915_demo5_Tpose"
# example_data_path = "C:\\Users\\rienk\\OneDrive - University of Twente\\BME\\Internship\\3. project content\\Python\\Xsens_data"

imu_data = extract_xsens_analyse_raw_data2(example_data_path)  # use the Sensor Angular Velocity tab

# print(imu_data)

# initialize filter fusion (example trial has 17 IMUs)
from hipose.api.fusion_filter import InertialPoseFusionFilter
ffilts = InertialPoseFusionFilter(
        num_imus=11, 
        ignore_mag=False,
        fusion_filter_alg="madgwick",
        s2s_calib_method="static_mag",
        default_data_freq=imu_data["freq"],
)

# # initialize calibration params from static NPose
# (example trial has 5s of NPose at the start)
calib_start = int(imu_data["freq"] * 2)
calib_end = int(imu_data["freq"] * 7)

ffilts.compute_imus_calibration(acc_calib_data=imu_data["acc"][calib_start:calib_end],
                                gyr_calib_data=imu_data["gyr"][calib_start:calib_end],
                                mag_calib_data=imu_data["mag"][calib_start:calib_end])

# perform filter fusion on trial data to obtain segment orientations
for idx, (acc, gyr, mag) in enumerate(zip(imu_data["acc"][calib_end:],
                                          imu_data["gyr"][calib_end:],
                                          imu_data["mag"][calib_end:])):
    pred_ori = ffilts.update(acc=acc, gyr=gyr, mag=mag)

print(pred_ori)

from hipose.skeleton import SkeletonXsens, SkeletonMTwAwinda, SkeletonVisualizer, SkeletonMTwAwindaUpperBody
skel_pred = SkeletonMTwAwindaUpperBody(ref_angles="npose", segment_lengths=None)
skel_gt = SkeletonXsens(ref_angles="npose", segment_lengths=None)

vis = SkeletonVisualizer(dict(skel_pred=skel_pred),
                        display_segment_axis=False,         # turn off for faster rendering
                        animation_fps=imu_data["freq"])

# visualize motion in 3D (pred vs GT)
vis.show3d(
        skeletons_orient_dict=dict(skel_pred=pred_ori)
        # skeletons_root_pos=dict(
        #         skel_gt=root_pos[0],
        #         skel_pred=root_pos[0] + [0, 1.25, 0]),
)

from pyqtgraph.Qt import QtWidgets
app = QtWidgets.QApplication.instance()
if app is None:
    app = QtWidgets.QApplication([])
app.exec_()
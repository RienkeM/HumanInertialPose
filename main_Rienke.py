# File to try the data processing with our own datasets

from hipose.data.trial_parsing.extract_xsens_analyse import extract_xsens_analyse_raw_data
# example_data_path = "C:/Users/rienk/OneDrive - University of Twente/BME/BME/Internship/3. project content/Python/"
example_data_path = "C:\\Users\\rienk\\OneDrive - University of Twente\\BME\\Internship\\3. project content\\Python\\Xsens_data\\0915_demo3_ Npose"
imu_data = extract_xsens_analyse_raw_data(example_data_path)

print(imu_data)

# initialize filter fusion (example trial has 17 IMUs)
from hipose.api.fusion_filter import InertialPoseFusionFilter
ffilts = InertialPoseFusionFilter(
        num_imus=17, 
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

# # # perform filter fusion on trial data to obtain segment orientations
# # for idx, (acc, gyr, mag) in enumerate(zip(imu_data["acc"][calib_s:],
# #                                           imu_data["gyr"][calib_s:],
# #                                           imu_data["mag"][calib_s:])):
# #     pred_ori = ffilts.update(acc=acc, gyr=gyr, mag=mag)
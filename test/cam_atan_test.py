# ----------------------------------------------------------------------------
# SymForce - Copyright 2022, Skydio, Inc.
# This source code is under the Apache 2.0 license found in the LICENSE file.
# ----------------------------------------------------------------------------

import numpy as np

from symforce import cam
from symforce import geo
from symforce import sympy as sm
from symforce.ops import StorageOps
from symforce.test_util import TestCase
from symforce.test_util.lie_group_ops_test_mixin import LieGroupOpsTestMixin
from symforce.test_util.cam_cal_test_mixin import CamCalTestMixin


class CamATANTest(LieGroupOpsTestMixin, CamCalTestMixin, TestCase):
    """
    Test the ATANCameraCal class.
    Note the mixin that tests all storage ops and camera projection/reprojection ops.
    """

    @classmethod
    def element(cls) -> cam.ATANCameraCal:
        [f_x, f_y, c_x, c_y] = np.random.uniform(low=0.0, high=1000.0, size=(4,))
        omega = np.random.uniform(low=0.1, high=0.8)
        return cam.ATANCameraCal(focal_length=(f_x, f_y), principal_point=(c_x, c_y), omega=omega)

    def test_omega_property(self) -> None:
        """
        Test that the omega property can be written to and read.
        """
        omega, omega_alt = sm.symbols("omega omega_alt")
        cal = cam.ATANCameraCal(focal_length=[0, 0], principal_point=[0, 0], omega=omega)

        self.assertEqual(omega, cal.omega)

        cal.omega = omega_alt

        self.assertEqual(omega_alt, cal.omega)

    def test_is_valid(self) -> None:
        """
        Tests if random points and pixels are correctly labeled as valid/invalid
        """
        for _ in range(10):
            cam_cal = self.element()
            point = geo.V3(np.random.uniform(low=-1.0, high=1.0, size=(3,)))
            pixel, is_valid_forward_proj = cam_cal.pixel_from_camera_point(point)

            # Points behind the camera should be invalid
            if point[2] > 0:
                self.assertTrue(is_valid_forward_proj == 1)
            else:
                self.assertTrue(is_valid_forward_proj == 0)

            _, is_valid_back_proj = cam_cal.camera_ray_from_pixel(pixel)

            linear_camera_cal = cam.LinearCameraCal(
                cam_cal.focal_length.to_flat_list(), cam_cal.principal_point.to_flat_list()
            )
            distorted_unit_depth_coords = linear_camera_cal.unit_depth_from_pixel(pixel)
            distorted_radius = distorted_unit_depth_coords.norm()
            if abs(distorted_radius * cam_cal.distortion_coeffs[0]) >= np.pi / 2.0:
                self.assertStorageNear(is_valid_back_proj, 0)
            else:
                self.assertStorageNear(is_valid_back_proj, 1)

    def test_invalid_points(self) -> None:
        """
        Tests if specific invalid points are correctly labeled as invalid
        """
        invalid_points = [
            geo.V3(0, 0, -1),
            geo.V3(0, 0, -1e-9),
            geo.V3(0, 0, -1000),
            geo.V3(1, 1, -1),
            geo.V3(-1, -1, -1),
            geo.V3(1000, 1000, -1000),
        ]
        for point in invalid_points:
            for _ in range(10):
                cam_cal = self.element()
                _, is_valid_forward_proj = cam_cal.pixel_from_camera_point(point)
                self.assertTrue(is_valid_forward_proj == 0)

    def test_invalid_pixels(self) -> None:
        """
        Tests if specific invalid pixels are correctly labeled as invalid
        """
        f_x, f_y = (380, 380)
        c_x, c_y = (320, 240)
        omega = 0.35
        cam_cal = cam.ATANCameraCal(
            focal_length=(f_x, f_y), principal_point=(c_x, c_y), omega=omega
        )
        invalid_pixels = [
            geo.V2(f_x * (np.pi / 2.0 + 1e-6) / omega + c_x, 0),
            geo.V2(0, f_y * (np.pi / 2.0 + 1e-6) / omega + c_y),
            geo.V2(f_x * (-np.pi / 2.0 - 1e-6) / omega + c_x, 0),
            geo.V2(0, f_y * (-np.pi / 2.0 - 1e-6) / omega + c_y),
            geo.V2(10000, 10000),
            geo.V2(-10000, -10000),
        ]
        for pixel in invalid_pixels:
            _, is_valid_back_proj = cam_cal.camera_ray_from_pixel(pixel)
            self.assertTrue(StorageOps.evalf(is_valid_back_proj) == 0.0)


if __name__ == "__main__":
    TestCase.main()

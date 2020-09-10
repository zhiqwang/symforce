//  ----------------------------------------------------------------------------
// This file was autogenerated by symforce. Do NOT modify by hand.
// -----------------------------------------------------------------------------

#include "./storage_ops.h"

namespace cam {
namespace equidistant_epipolar_camera_cal {

template <typename Scalar>
void StorageOps<Scalar>::ToStorage(const EquidistantEpipolarCameraCal<Scalar>& a, std::vector<Scalar>* vec) {
  assert(vec != nullptr);
  const typename EquidistantEpipolarCameraCal<Scalar>::DataVec& data = a.Data();
  vec->resize(data.size());
  std::copy_n(data.data(), data.size(), vec->begin());
}

template <typename Scalar>
EquidistantEpipolarCameraCal<Scalar> StorageOps<Scalar>::FromStorage(const std::vector<Scalar>& vec) {
  assert(vec.size() == StorageOps<Scalar>::StorageDim());
  return EquidistantEpipolarCameraCal<Scalar>(
    Eigen::Map<const typename EquidistantEpipolarCameraCal<Scalar>::DataVec>(vec.data()));
}

}  // namespace equidistant_epipolar_camera_cal
}  // namespace cam


// Explicit instantiation
template struct cam::equidistant_epipolar_camera_cal::StorageOps<double>;
template struct cam::equidistant_epipolar_camera_cal::StorageOps<float>;
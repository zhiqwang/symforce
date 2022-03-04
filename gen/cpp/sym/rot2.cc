// -----------------------------------------------------------------------------
// This file was autogenerated by symforce from template:
//     cpp_templates/geo_package/CLASS.cc.jinja
// Do NOT modify by hand.
// -----------------------------------------------------------------------------

#include "./rot2.h"

namespace sym {

// Print implementations
std::ostream& operator<<(std::ostream& os, const Rot2d& a) {
  const Eigen::IOFormat fmt(Eigen::StreamPrecision, Eigen::DontAlignCols, ", ", "\n", "[", "]");
  os << "<Rot2d " << a.Data().transpose().format(fmt) << ">";
  return os;
}
std::ostream& operator<<(std::ostream& os, const Rot2f& a) {
  const Eigen::IOFormat fmt(Eigen::StreamPrecision, Eigen::DontAlignCols, ", ", "\n", "[", "]");
  os << "<Rot2f " << a.Data().transpose().format(fmt) << ">";
  return os;
}

}  // namespace sym

// --------------------------------------------------------------------------
// Custom generated methods
// --------------------------------------------------------------------------

template <typename Scalar>
Eigen::Matrix<Scalar, 2, 1> sym::Rot2<Scalar>::Compose(
    const Eigen::Matrix<Scalar, 2, 1>& right) const {
  // Total ops: 6

  // Input arrays
  const Eigen::Matrix<Scalar, 2, 1>& _self = Data();

  // Intermediate terms (0)

  // Output terms (1)
  Eigen::Matrix<Scalar, 2, 1> _res;

  _res(0, 0) = _self[0] * right(0, 0) - _self[1] * right(1, 0);
  _res(1, 0) = _self[0] * right(1, 0) + _self[1] * right(0, 0);

  return _res;
}

template <typename Scalar>
sym::Rot2<Scalar> sym::Rot2<Scalar>::FromAngle(const Scalar theta) {
  // Total ops: 2

  // Input arrays

  // Intermediate terms (0)

  // Output terms (1)
  Eigen::Matrix<Scalar, 2, 1> _res;

  _res[0] = std::cos(theta);
  _res[1] = std::sin(theta);

  return sym::Rot2<Scalar>(_res);
}

template <typename Scalar>
Eigen::Matrix<Scalar, 2, 2> sym::Rot2<Scalar>::ToRotationMatrix() const {
  // Total ops: 1

  // Input arrays
  const Eigen::Matrix<Scalar, 2, 1>& _self = Data();

  // Intermediate terms (0)

  // Output terms (1)
  Eigen::Matrix<Scalar, 2, 2> _res;

  _res(0, 0) = _self[0];
  _res(0, 1) = -_self[1];
  _res(1, 0) = _self[1];
  _res(1, 1) = _self[0];

  return _res;
}

// Explicit instantiation
template class sym::Rot2<double>;
template class sym::Rot2<float>;

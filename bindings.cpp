#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>

// Forward declarations from indicator_engine.cpp
std::vector<double> simple_moving_average(const std::vector<double>& close_prices, int window);
std::vector<double> exponential_moving_average(const std::vector<double>& close_prices, int window);

namespace py = pybind11;

pybind11::array_t<double> py_sma(pybind11::array_t<double> input, int window) {
    auto buf = input.request();
    double *ptr = static_cast<double *>(buf.ptr);
    std::vector<double> prices(ptr, ptr + buf.shape[0]);
    
    std::vector<double> result = simple_moving_average(prices, window);
    
    return pybind11::array_t<double>(result.size(), result.data());
}

pybind11::array_t<double> py_ema(pybind11::array_t<double> input, int window) {
    auto buf = input.request();
    double *ptr = static_cast<double *>(buf.ptr);
    std::vector<double> prices(ptr, ptr + buf.shape[0]);
    
    std::vector<double> result = exponential_moving_average(prices, window);
    
    return pybind11::array_t<double>(result.size(), result.data());
}

PYBIND11_MODULE(indicator_engine, m) {
    m.def("simple_moving_average", &py_sma, 
          "Compute Simple Moving Average",
          py::arg("close_prices"), 
          py::arg("window"));
    
    m.def("exponential_moving_average", &py_ema,
          "Compute Exponential Moving Average",
          py::arg("close_prices"),
          py::arg("window"));
    
    m.doc() = "Indicator Engine - C++ compiled moving average calculations";
}

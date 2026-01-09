//implement simple moving average with window and close prices as inputs
#include <vector>
#include <numeric>
#include <iostream>
#include <fstream>
#include <cstring>
#include <stdexcept>
#include <cstdint>

std::vector<double> simple_moving_average(const std::vector<double>& close_prices, int window) {
    std::vector<double> sma;
    int n = close_prices.size();
    sma.resize(n, 0.0);

    double sum = 0.0;
    for (int i = 0; i < n; ++i) {
        sum += close_prices[i];
        if (i >= window) {
            sum -= close_prices[i - window];
        }
        if (i >= window - 1) {
            sma[i] = sum / window;
        } else {
            sma[i] = 0.0;
        }
    }
    return sma;
}

std::vector<double> exponential_moving_average(const std::vector<double>& close_prices, int window) {
    std::vector<double> ema;
    int n = close_prices.size();
    ema.resize(n, 0.0);
    double alpha = 2.0 / (window + 1);
    ema[0] = close_prices[0];
    for (int i = 1; i < n; ++i) {
        ema[i] = alpha * close_prices[i] + (1 - alpha) * ema[i - 1];
    }
    return ema;
}

std::vector<double> load_npy_file(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Cannot open file: " + filename);
    }

    char magic[6];
    file.read(magic, 6);
    if (std::string(magic, 6) != "\x93NUMPY") {
        throw std::runtime_error("Invalid NPY file format");
    }

    unsigned char version_major, version_minor;
    file.read((char*)&version_major, 1);
    file.read((char*)&version_minor, 1);

    uint16_t header_len;
    file.read((char*)&header_len, 2);

    std::vector<char> header(header_len);
    file.read(&header[0], header_len);

    std::cout << "NPY version: " << (int)version_major << "." << (int)version_minor << std::endl;
    std::cout << "Header length: " << header_len << std::endl;

    std::vector<double> data;
    double value;
    int count = 0;
    while (file.read((char*)&value, sizeof(double))) {
        data.push_back(value);
        count++;
    }

    std::cout << "Loaded " << count << " values" << std::endl;
    
    if (data.empty()) {
        throw std::runtime_error("No data found in NPY file");
    }

    file.close();
    return data;
}

void save_npy_file(const std::string& filename, const std::vector<double>& data) {
    std::ofstream file(filename, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Cannot create file: " + filename);
    }

    file.write("\x93NUMPY", 6);
    unsigned char version[2] = {1, 0};
    file.write((char*)version, 2);

    std::string header = "{'descr': '<f8', 'fortran_order': False, 'shape': (" + std::to_string(data.size()) + ",), }";
    while (header.size() % 16 != 0) header += " ";

    uint16_t header_len = header.size();
    file.write((char*)&header_len, 2);
    file.write(header.c_str(), header.size());

    for (double val : data) {
        file.write((char*)&val, sizeof(double));
    }

    file.close();
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <window_size> <input.npy> <output_prefix>" << std::endl;
        std::cerr << "Example: " << argv[0] << " 10 close_prices.npy result" << std::endl;
        std::cerr << "This will create result_sma.npy and result_ema.npy" << std::endl;
        return 1;
    }

    int window = std::atoi(argv[1]);
    std::string input_file = argv[2];
    std::string output_prefix = argv[3];

    try {
        std::cout << "Loading data from " << input_file << "..." << std::endl;
        std::vector<double> close_prices = load_npy_file(input_file);
        
        std::cout << "Loaded " << close_prices.size() << " data points" << std::endl;
        std::cout << "Computing SMA and EMA with window size " << window << "..." << std::endl;
        
        std::vector<double> sma = simple_moving_average(close_prices, window);
        std::vector<double> ema = exponential_moving_average(close_prices, window);
        
        std::cout << "\n=== SMA Results ===" << std::endl;
        std::cout << "SMA size: " << sma.size() << std::endl;
        std::cout << "First 20 SMA values: ";
        for (int i = 0; i < 20 && i < (int)sma.size(); ++i) {
            std::cout << sma[i] << " ";
        }
        std::cout << "\n\n=== EMA Results ===" << std::endl;
        std::cout << "EMA size: " << ema.size() << std::endl;
        std::cout << "First 20 EMA values: ";
        for (int i = 0; i < 20 && i < (int)ema.size(); ++i) {
            std::cout << ema[i] << " ";
        }
        std::cout << "\n" << std::endl;
        
        std::string sma_file = output_prefix + "_sma.npy";
        std::string ema_file = output_prefix + "_ema.npy";
        
        std::cout << "Saving SMA to " << sma_file << "..." << std::endl;
        save_npy_file(sma_file, sma);
        
        std::cout << "Saving EMA to " << ema_file << "..." << std::endl;
        save_npy_file(ema_file, ema);
        
        std::cout << "Done! Results saved to " << sma_file << " and " << ema_file << std::endl;
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}


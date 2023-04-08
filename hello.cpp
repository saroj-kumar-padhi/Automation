#include <iostream>
#include <iomanip>

int main()
{
    double d = 122.345;
    double c = 90.0;

    std::cout << std::fixed;
    std::cout << std::setprecision(2);
    std::cout << d;
    std::cout << c;
}
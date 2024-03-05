#include <algorithm>
#include <iterator>
#include <ostream>
#include <vector>

class Sudoku {
public:
    friend std::ostream& operator<<(std::ostream &output, Sudoku);
    Sudoku();
private:
    std::vector<std::vector<int>> table;
    std::vector<int> get_available_values(int, int);
};


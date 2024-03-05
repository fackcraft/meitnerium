#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>

#include "sudoku.h"

using std::find;
using std::cout;
using std::endl;
using std::ostream;
using std::vector;

Sudoku::Sudoku() {
    for (int i; i <= 9; i++) {
        vector<int> column;
        for (int j; j <= 9; j++) {
            column.push_back(0);
        }
        table.push_back(column);
    }
    for (int i; i <= 9; i++) {
        for (int j; j <= 9; j++) {
            vector<int> available_values = get_available_values(i, j);
            table[i][j] = available_values[0];
            cout << this;
        }
    }
}

vector<int> Sudoku::get_available_values(const int x, const int y) {
    vector<int> available_values = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    for (int i; i <= 9; i++) {
        for (int j; j <= 9; j++) {
            // line
            if (i == 0) {
                auto index = find(available_values.begin(), available_values.end(), table[i][j]);
                available_values.erase(index);
                continue;
            }
            // row
            if (j == 0) {
                auto index = find(available_values.begin(), available_values.end(), table[i][j]);
                available_values.erase(index);
                continue;
            }
            // block
            int begin_x = i / 3;
            int end_x = i / 3 + 3;
            int begin_y = j / 3;
            int end_y = i / 3 + 3;
            if (i >= begin_x and i < end_x and j >= begin_y and j < end_y) {
                auto index = find(available_values.begin(), available_values.end(), table[i][j]);
                available_values.erase(index);
            }
        }
    }
    return available_values;
}

ostream& operator<<(ostream& output, Sudoku sudoku) {
    for (std::vector<int> row: sudoku.table) {
        for (int element: row) {
            output << element << " ";
        }
        output << endl;
    }
    return output;
}

int main() {
    Sudoku sudoku;
    cout << sudoku;
    return 0;
}

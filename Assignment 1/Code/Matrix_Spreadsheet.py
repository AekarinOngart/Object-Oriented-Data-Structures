#!/usr/bin/env python3

import re
import json

# Defining A 2D Array
#
# +---+---+---+---+---+
# |A1 |B1 |C1 |D1 |E1 |
# +---+---+---+---+---+
# |A2 |B2 |C2 |D2 |E2 |
# +---+---+---+---+---+
# |A3 |B3 |C3 |D3 |E3 |
# +---+---+---+---+---+
# |A4 |B4 |C4 |D4 |E4 |
# +---+---+---+---+---+
#


class Sheet:
    def __init__(self, name):
        with open(name, "r") as file:
            sheet = file.read()
            sheet = json.loads(sheet)
        self.col = sheet["size"]["col"]
        self.row = sheet["size"]["row"]
        self.Columns = sheet["table"]

    def insert_col(self, at_col):
        # you can write like this
        # self.Columns.insert(at_col, [None for _ in range(self.row)])
        # But

        # Store and make entry
        temp = [None for _ in range(self.row)]

        # Now shift
        for i in range(at_col, self.col):
            temp, self.Columns[i] = self.Columns[i], temp
        # Appending increases the size of array and then adds it
        self.Columns.append(temp)
        self.col += 1

    def insert_row(self, at_row):
        # can do
        # for column in self.Columns:
        #     column.insert(row, None)
        #
        for rows in self.Columns:
            temp = None
            for i in range(at_row, self.row):
                temp, rows[i] = rows[i], temp
            rows.append(temp)
        self.row += 1

    def delete_col(self, col):
        # can do
        # Columns.pop(col)
        #
        self.Columns = self.Columns[:col] + self.Columns[col + 1:]
        self.col -= 1

    def delete_row(self, row):
        # can do
        # for column in self.Columns:
        #   column.pop(row)
        #
        for r in range(self.col):
            self.Columns[r] = self.Columns[r][:row] + self.Columns[r][row + 1:]

        self.row -= 1

    def search(self, value):
        cells = []
        for col in range(self.col):
            for row in range(self.row):
                if self.Columns[col][row] == value:
                    cells.append((col, row))
        return cells

    def set(self, cell, value):
        col, row = self._cell(cell)
        self.Columns[col][row] = value

    def unset(self, cell):
        col, row = self._cell(cell)
        self.Columns[col][row] = None

    def _cell(self, cell):
        cell = re.match(r"([a-z]+)(\d+)", cell.lower())
        if cell is None:
            return (0, 0)
        col, row = cell.group(1, 2)
        return (self._coli(col) - 1, int(row) - 1)

    def _coli(self, col):
        sum = 0
        order = 0
        for ch in col[::-1]:
            sum += (ord(ch) - 96) * (26 ** order)
            order += 1
        return sum

    def __str__(self):
        # table start
        column_lens = [self._max_len(column) + 2 for column in self.Columns]

        for row in range(self.row):
            self._separate(column_lens)
            for col in range(self.col):
                row_v = self.Columns[col][row]
                row_l = 0
                if row_v is not None:
                    row_l = len(str(row_v))
                print("| ", end="")
                if row_v is not None:
                    print(row_v, end="")
                print(" " * (column_lens[col] - row_l - 1), end="")
            print("|")
        self._separate(column_lens)
        return "\n"

    def _separate(self, col_lens):
        for l in col_lens:
            print("+" + ("-" * l), end="")
        print("+")
        pass

    def _max_len(self, column):
        m = 1
        for row in column:
            if row is not None:
                row_l = len(str(row))
                m = max(m, row_l)
        return m

    def make_entry(self, entries):
        for col, val in entries:
            self.set(col, val)

    def save(self, name):
        with open(name, "w") as file:
            file.write(json.dumps(
                {"size": {"col": self.col, "row": self.row}, "table": self.Columns}))


if __name__ == "__main__":
    sheet = Sheet("example.json")
    sheet.make_entry([("A3", "abara"), ("B3", "20"), ("C3", "cadabra")])
    print(sheet)
    sheet.insert_col(1)
    print("Ran: sheet.insert_col(1)\n", sheet, sep="")
    sheet.insert_row(1)
    print("Ran: sheet.insert_row(1)\n", sheet, sep="")
    sheet.delete_col(1)
    print("Ran: sheet.delete_col(1)\n", sheet, sep="")
    sheet.delete_row(1)
    print("Ran: sheet.delete_row(1)\n", sheet, sep="")
    print('\nRan: sheet.search("coding") returns ', sheet.search("coding"))
    sheet.save("example_modified.json")

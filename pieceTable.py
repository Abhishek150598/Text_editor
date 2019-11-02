from copy import deepcopy
from time import perf_counter

class textEditor:
    
    def __init__(self):
        self.original_buffer = ""
        self.add_buffer = ""
        self.end_org = 0
        self.end_add = 0
        self.piece_table = []
        self.piece_tables = [[]]
        self.snaps = 0
        self.start_time = perf_counter()
        
    def insert(self, str, index):
        # If given index = end index
        if index == self.end_org :
            
            if index == 0:
                row = {'filename': 'original', 'start': 0, 'length': len(str) }
                self.piece_table.append(row)
            else:
                l = len(self.piece_table)
                self.piece_table[l - 1]['length'] += len(str)

            self.original_buffer += str
            self.end_org += len(str)
        
        # If given index != end index
        else :
            if index == 0:
                row = {'filename': 'add', 'start': self.end_add, 'length': len(str) }
                self.piece_table.insert(0, row)
                
            else :
                current_index = 0
                row_index = -1       
                for i in range(len(self.piece_table)):
                    current_index += self.piece_table[i]['length']
                    if current_index >= index:
                        row_index = i
                        break

                if current_index == index:
                    if self.piece_table[row_index]['filename'] == 'add' and self.piece_table[row_index]['start'] + self.piece_table[row_index]['length'] == self.end_add:
                        self.piece_table[row_index]['length'] += len(str)
                    else:
                        row = {'filename': 'add', 'start': self.end_add, 'length': len(str) }
                        self.piece_table.insert(row_index + 1, row)

                elif current_index > index:
                    self.piece_table[row_index]['length'] += index - current_index
                    row = {'filename': 'add', 'start': self.end_add, 'length': len(str) }
                    self.piece_table.insert(row_index + 1, row)
                    row = {'filename': self.piece_table[row_index]['filename'], 
                          'start': self.piece_table[row_index]['start'] + self.piece_table[row_index]['length'], 
                          'length': current_index - index}
                    self.piece_table.insert(row_index + 2, row)
                    
            self.add_buffer += str
            self.end_add += len(str)

        self.storePieceTable()
        
        return self.getSequence()

    def delete(self, index1, index2):

        current_index_1 = 0
        current_index_2 = 0
        row_index = -1
        row_index_2 = -1

        for i in range(len(self.piece_table)):
            current_index_1 += self.piece_table[i]['length']
            if current_index_1 > index1:
                row_index = i
                break;

        for i in range(len(self.piece_table)):
            current_index_2 += self.piece_table[i]['length']
            if current_index_2 > index2:
                row_index_2 = i
                break;

        if row_index == row_index_2:
            
            row = {'filename': self.piece_table[row_index_2]['filename'], 
                    'start': self.piece_table[row_index_2]['start'] + self.piece_table[row_index_2]['length'] - current_index_2 + index2 + 1,
                    'length': current_index_2 - index2 - 1}
            self.piece_table[row_index]['length'] += index1 - current_index_1
            self.piece_table.insert(row_index + 1, row)

        else:
            self.piece_table[row_index]['length'] += index1 - current_index_1
            self.piece_table[row_index_2]['start'] += self.piece_table[row_index_2]['length'] - current_index_2 + index2 + 1 
            self.piece_table[row_index_2]['length'] = current_index_2 - index2 - 1

        for i in range(row_index + 1, row_index_2):
            self.piece_table.pop(i)

        if self.piece_table[row_index]['length'] == 0:
            self.piece_table.pop(row_index)

        if self.piece_table[row_index_2]['length'] == 0:
            self.piece_table.pop(row_index_2)

        self.storePieceTable()

        return self.getSequence()

    def storePieceTable(self):
        curr_time = perf_counter()
        if (curr_time - self.start_time) > 2.0:
            self.snaps += 1
            self.piece_tables = self.piece_tables[:self.snaps]
            self.piece_tables.append(deepcopy(self.piece_table))
            self.start_time = perf_counter()


    def getSequence(self):
        string = ""
        for row in self.piece_table:
            s = row['start']
            e = row['start'] + row['length']
            if row['filename'] == 'original':
                string += self.original_buffer[s:e]
            else:
                string += self.add_buffer[s:e]

        return string

    def getSubsequence(self, index1, index2):
        s = self.getSequence()
        return s[index1 : index2 + 1]

    def undo(self):
        if self.snaps > 0:
            self.snaps -= 1
            self.piece_table = self.piece_tables[self.snaps]

        #print(self.snaps)
        return self.getSequence()

    def redo(self):
        try:
            self.piece_table = self.piece_tables[self.snaps + 1]
            self.snaps += 1
        except:
            pass

        print(self.snaps)
        return self.getSequence()
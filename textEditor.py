from copy import deepcopy
from time import perf_counter

class textEditor:
    
    def __init__(self, text = ""):
        self.original_buffer = text
        self.add_buffer = ""
        self.end_org = len(text)
        self.end_add = 0
        self.piece_table = []
        if text:
            self.piece_table.append({'filename': 'original', 'start': 0, 'length': len(text) })
        self.piece_tables = [deepcopy(self.piece_table)]
        self.snaps = 0
        self.start_time = perf_counter()
 
    # Function to insert a string at a given index in the piece table       
    def insert(self, str, index):
        # If given index = end index
        if index == len(self.getSequence()):
            
            if index == 0:
                row = {'filename': 'original', 'start': self.end_org, 'length': len(str) }
                self.piece_table.append(row)
            else:
                l = len(self.piece_table)
                if self.piece_table[l - 1]['start'] + self.piece_table[l - 1]['length'] == self.end_org:
                    self.piece_table[l - 1]['length'] += len(str)
                else:
                    row = {'filename': 'original', 'start': self.end_org, 'length': len(str) }
                    self.piece_table.append(row)

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

    # Function to delete a portion of text in a given inex range
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

        self.piece_table = self.piece_table[: row_index] + self.piece_table[row_index: ]

        self.piece_table = list(filter(lambda x: x['length'] > 0, self.piece_table))

        self.storePieceTable()

        return self.getSequence()

    # Function that archives the piece table every 2 seconds for undo/redo operation
    def storePieceTable(self):
        curr_time = perf_counter()
        if (curr_time - self.start_time) > 2.0:
            self.snaps += 1
            self.piece_tables = self.piece_tables[:self.snaps]
            self.piece_tables.append(deepcopy(self.piece_table))
            self.start_time = perf_counter()

    # Function that returns the text stored in the piece table
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

    # Function that returns a portion of text stored in the piece table
    def getSubsequence(self, index1, index2):
        s = self.getSequence()
        return s[index1 : index2 + 1]

    # Undo function
    def undo(self):
        if self.snaps > 0:
            self.snaps -= 1
            self.piece_table = self.piece_tables[self.snaps]

        return self.getSequence()

    # Redo function
    def redo(self):
        try:
            self.piece_table = self.piece_tables[self.snaps + 1]
            self.snaps += 1
        except:
            pass

        return self.getSequence()
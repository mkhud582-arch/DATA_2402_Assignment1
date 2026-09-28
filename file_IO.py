def load_from_html(filename: str) -> list[dict]:
    """
    reads a dataset in HTML format. converts numeric data to float.
    raises an AttributeError if the table rows do not all have the same number of values.
    :param filename: the file path of the html data to read
    :return: the dataset as a list of dictionaries - one dict per object in the file
            each dictionary should map column names to values
    """    
    with open(filename, 'r') as file:
        contents = file.read()
        all_rows = []

        head, body = contents.split('</thead>')

        # process the head first, pull out the column names
        head_parts = head.split('<td>')

        columns = []
        for column_name in head_parts[1:]:
            columns.append(
                column_name.replace('</td>', '').replace('</tr>', '').strip()
            )
        
        # strip off some unnecessary tags
        body = body.replace('</tr>', '')
        body = body.replace('</tbody>\n</table>', '')

        # process the rest of the text: the table body
        rows_text = body.split('<tr>')
        for row_text in rows_text[1:]:
            row_text = row_text.replace('</td>', '')
            values = row_text.split('<td>')
            values = values[1:]

            # check the row has the right number of values in it
            if len(values) != len(columns):
                raise AttributeError(f'wrong number of values in row: {row_text}')

            this_row_dict = dict()
            for i in range(len(columns)):
                this_column = columns[i]
                this_value = values[i].strip()

                # convert to float if the value is a number
                try:
                    this_value = float(this_value)
                except ValueError:
                    pass

                this_row_dict[this_column] = this_value
            
            all_rows.append(this_row_dict)
    
    return all_rows


def load_from_CSV(filename: str) -> list[dict]: # [{k:v}] 
    """ This CSV function will open the file, then read the lines, 
    then separate the first line from the remaining lines, then extract the first  (header),  
    then each remaining line after the first first row are the values, 
    then put those column names and values into a dictionary,  
    then append that dictionary to a list  
    then have the function return a list of dictionary values""" 
 
     
    with open(filename, "r") as file: # Open the file 
        contents = file.read() # read the lines 
        all_rows = [] 
 
        lines = contents.split('\n') # split the contents into lines  
 
 
        header = lines[0] # extract and locate the header row  
 
        header = header.strip() # use .strip() to remove newline and whitespace  
        columns = header.split(',') # separate the first row into individual values 
 
        for value in lines[1:]: # start from the second row and process the values till the end  
            strip_value = value.strip() 
            split_value = strip_value.split(',') # separate the row of values from row 2 and onwards into individual parts such as 001234,Alice,Sales,25.0 --> [001234, Alice, Sales, 25.0] 
 
            if strip_value == "": 
                continue 

            if len(split_value) != len(columns): # FIXED: check that each row has the same number of values as the header
                raise AttributeError(f'wrong number of values in row: {value}')
 
            row_dict = {} 
            for i in range(len(columns)): # loop through each column that contain the header and the values 
                current_column = columns[i] # this will be like the key in the dictionary to access by the column header (Key: Name) 
                current_value = split_value[i] # this will be like the value in the dictionary that can accessed by the key (Value: Alice) 
 
                try: # convert numeric values to float before the floating point values get stored inside the dictionary  
                    current_value = float(current_value) 
                except ValueError: 
                    pass 
 
                row_dict[current_column] = current_value # dictionary[key] = value; each dictionary should map column names to their respective values; so basically in the row dictionary, access by the index of the key of the value assigned to the key 
            all_rows.append(row_dict) 
 
            
    return all_rows


def load_data(filename):
    try:
        CSV_result = load_from_CSV(filename)
        return CSV_result

    except (ValueError, AttributeError, IndexError):  
        pass

    try:
        HTML_result = load_from_html(filename)
        return HTML_result
    # try:
        #     HTML_result = load_from_html(filename)
        #     return HTML_result
        # except AttributeError:
        #     raise Exception("Error, data must be in valid CSV or HTML format")
    except (ValueError, AttributeError, IndexError):  
        raise Exception("Error, data must be in valid CSV or HTML format")
        
import pandas as pd

def read_care_area(file):
    return pd.read_csv(file, header=None)

def read_metadata(file):
    metadata = pd.read_csv(file, header=None)
    main_field_size = float(metadata.iloc[1, 0])
    sub_field_size = float(metadata.iloc[3, 0])
    return main_field_size, sub_field_size

def place_main_fields(care_area, main_field_size):
    main_fields = []
    field_id = 0

    for _, row in care_area.iterrows():
        x1, x2, y1, y2 = row[1], row[3], row[2], row[4]
        while x1 <= x2:
            y_current = y1
            while y_current <= y2:
                main_fields.append([field_id, x1, x1 + main_field_size, y_current, y_current + main_field_size])
                y_current += main_field_size
                field_id += 1
            x1 += main_field_size

    return pd.DataFrame(main_fields, columns=['ID', 'x1', 'x2', 'y1', 'y2'])

def place_sub_fields(care_area, main_fields, sub_field_size):
    sub_fields = []
    sub_field_id = 0

    for _, field in main_fields.iterrows():
        x1, y1, x2, y2 = field['x1'], field['y1'], field['x2'], field['y2']
        while x1 < x2:
            y_current = y1
            while y_current < y2:
                sub_fields.append([sub_field_id, x1, x1 + sub_field_size, y_current, y_current + sub_field_size, field['ID']])
                y_current += sub_field_size
                sub_field_id += 1
            x1 += sub_field_size

    return pd.DataFrame(sub_fields, columns=['ID', 'x1', 'x2', 'y1', 'y2', 'MF_ID'])

def main():
    care_area_file = 'CareAreas.csv'
    metadata_file = 'metadata.csv'

    care_area = read_care_area(care_area_file)
    main_field_size, sub_field_size = read_metadata(metadata_file)

    main_fields = place_main_fields(care_area, main_field_size)
    sub_fields = place_sub_fields(care_area, main_fields, sub_field_size)

    main_fields.to_csv('MainFields.csv', index=False)
    sub_fields.to_csv('SubFields.csv', index=False)

if __name__ == "__main__":
    main()
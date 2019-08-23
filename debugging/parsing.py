import csv

COLOR_MAPPING = {
    1: 'black',
    2: 'blue',
    3: 'green',
    4: 'yellow',
    5: 'red',
    6: 'white',
    0: 'clear'
}

BASE_MAPPING = {
    'green':  'A',
    'blue':   'C',
    'red':    'T',
    'yellow': 'G'
}


def map_val_to_coll(val, coll):
    try:
        return coll[val]
    except KeyError:
        return "n/a"


def parse_raw(filepath):
    with open(filepath, "r") as fp:
        reader = csv.DictReader(fp)

        rows = []
        time_col = None
        value_col = None

        for row in reader:
            if value_col is None or time_col is None:
                time_header = list(x for x in row.keys() if x and 'Time' in x)[0]
                val_header = list(x for x in row.keys() if x and 'Time' not in x)[-1]

            time, value = row[time_header], row[val_header]
            color = map_val_to_coll(int(float(value)), COLOR_MAPPING)
            base = map_val_to_coll(color, BASE_MAPPING)

            rows.append({
                'time': time,
                'value': value,
                'color': color,
                'base': base
            })

        return rows


def normalized_rows(rows):

    pass

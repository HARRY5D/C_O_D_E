def sort_tuples():
    lines = []
    while True:
        try:
            line = input()
            if not line:
                break
            lines.append(tuple(line.split(',')))
        except EOFError:
            break
    
    sorted_lines = sorted(lines, key=lambda x: (x[0], int(x[1]), int(x[2])))
    print(sorted_lines)

sort_tuples()
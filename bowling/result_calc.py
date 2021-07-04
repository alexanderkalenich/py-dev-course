from collections import defaultdict

from bowling import get_score


class ProcessingResults:

    def files_processing(self, input_file, out_file, rules):
        bowler_dic = defaultdict(int)
        with open(input_file, 'r', encoding='utf8') as fi, open(out_file, 'a') as fo:
            for line in fi:
                line = line[:-1]
                if 'Tour' in line:
                    tour_line = line
                    fo.write(f'{tour_line}\n')
                elif 'winner is .........' in line:
                    win_line = line[:-9]
                    res = sorted(bowler_dic.items(), key=lambda x: (x[1], x[0]))
                    for k, v in res:
                        winner = k
                    fo.write(f'{win_line}     {winner}\n\n')
                    fo.flush()
                    bowler_dic.clear()
                elif line == "":
                    continue
                else:
                    value_1, value_2 = line.split('\t')
                    try:
                        score = get_score(value_2, rules)
                    except Exception as exc:
                        print(f' {exc} - {tour_line} - {value_1}  {value_2}')
                        fo.write(f'Результат {value_1} некорректный\n')
                        score = 0
                    bowler_dic[value_1] = score
                    fo.write(f'{value_1: <10}{value_2: <22}{score: >4d}\n')

# input_file = 'tournament.txt'
# out_file = 'tournament_result.txt'
# processing_results = ProcessingResults()
# processing_results.files_processing(input_file, out_file)

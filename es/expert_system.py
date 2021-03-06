import subprocess
import os
import time


class ExpertSystem:
    @staticmethod
    def train():
        print('training')

    @staticmethod
    def get_scores(id, data):
        now = time.time()
        input_path = 'es/data/'
        output_path = 'es/output/'
        ExpertSystem.create_folders(input_path, output_path)

        input_file = f'{input_path}data_{id}_{now}.txt'
        output_file = f'{output_path}output_{id}_{now}.txt'

        # Input file config
        ExpertSystem.create_input_file(input_file, data)

        # ES config
        knb = 'es/test_db.knb'
        if os.name == 'nt':
            subprocess.call(f'.\es\hierarchic_base.exe -k {knb} -i {input_file} -o {output_file}')
        else:
            subprocess.call(
                f'/usr/bin/wine-stable ./es/hierarchic_base.exe -k {knb} -i {input_file} -o {output_file}',
                shell=True)

        output_data = ExpertSystem.get_output_data(output_file)
        end = time.time()
        print(f'Expert system scores computed in: {end - now}s')
        for i, value in enumerate(output_data):
            data[i]['es_score'] = value
        ExpertSystem.delete_files(input_file, output_file)
        end = time.time()
        print(f'Expert system finished in: {end - now}s')

        return data

    @staticmethod
    def create_folders(input_path, output_path):
        if os.path.exists(input_path) is not True:
            os.mkdir(input_path)

        if os.path.exists(output_path) is not True:
            os.mkdir(output_path)

    @staticmethod
    def create_input_file(input_file_path, data):
        input_headers = 'INP1\tINP2\tINP3\tINP4\n'
        # input_headers = 'INP1\tINP2\tINP3\n'
        f = open(input_file_path, 'w')
        f.write(input_headers)
        for row in data:
            inp = [
                str(row['average_rating']).replace('.', ','),
                str(row['ratings_count']).replace('.', ','),
                str(row['penalized']).replace('.', ','),
                str(row['similarity']).replace('.', ',')
            ]
            input_row = f'{inp[0]}\t{inp[1]}\t{inp[2]}\t{inp[3]}\n'
            # input_row = f'{inp[0]}\t{inp[1]}\t{inp[2]}\n'
            f.write(input_row)
        f.close()

    @staticmethod
    def get_output_data(output_file_path):
        data = []
        with open(output_file_path, 'r') as fp:
            next(fp)
            for line in fp:
                values = line.split('\t')
                output_value = values[-1].strip().replace(',', '.')
                data.append(float(output_value))

        return data

    @staticmethod
    def delete_files(input_file_path, output_file_path):
        if os.path.exists(input_file_path):
            os.remove(input_file_path)

        if os.path.exists(output_file_path):
            os.remove(output_file_path)

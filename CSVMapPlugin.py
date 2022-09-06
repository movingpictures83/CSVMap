# Not used in the analysis


import pandas as pd

def get_mapping_dict(metadata):
    metadata_path = metadata

    name_col = 1 #started from 0
    metabolite_col=-1

    map_dict = {}

    with open(metadata_path, 'r') as f:
        f.readline()
        for line in f.readlines():
            line = line.strip("\n")
            row = line.split("\t")
            id = row[metabolite_col]
            if id!="":
                map_dict[id] = id + "__" + row[name_col].replace(",","").replace(" ","_")
    return map_dict


def rename_abundance(abundance_file, abundance_out, metadata):
    abundance_df = pd.read_csv(abundance_file)

    cols = list(abundance_df.columns)

    cols_map = {}
    hmdb_map = get_mapping_dict(metadata)

    for name in cols:
        name = name.strip()
        if "HMDB" in name:
            cols_map[name] = hmdb_map[name]

    abundance_df = abundance_df.rename(columns=cols_map)
    abundance_df.to_csv(abundance_out)

import PyPluMA
class CSVMapPlugin:
    def input(self, infile):
        inputfile = open(infile, 'r')
        self.parameters = dict()
        for line in inputfile:
            contents = line.strip().split('\t')
            self.parameters[contents[0]] = contents[1]

    def run(self):
        pass

    def output(self, outputfile):
        rename_abundance(PyPluMA.prefix()+"/"+self.parameters["csvfile"], outputfile, PyPluMA.prefix()+"/"+self.parameters["metadata"])


import pandas as pd
import time

from extraction.catalogue import Catalogue
from extraction.pdd import Pdd


class ReportManager:
    COLUMNS = ['Methodology', 'Name', 'Total Projects',
               'PDD Number', 'First of its Kind', 'Laws and Regulations', 'Investment Analysis', 'Barrier Analysis',
               ]

    def __init__(self, catalogue_path, pdd_path, report_name='Report.xlsx', is_trace=False):
        self.catalogue_path = catalogue_path
        self.pdd_path = pdd_path
        self.report_name = report_name
        self.is_trace = is_trace

        self.df = pd.DataFrame(columns=ReportManager.COLUMNS)
        self.counter = 0

    def load_all_data(self):
        Catalogue.load_all(self.catalogue_path)
        Pdd.load_all(self.pdd_path)

    def create(self):
        print(f'Generating report {self.report_name}')
        overall_start_time = time.time()
        for cdm, info_as_list in Catalogue.CDMS.items():
            methodology = info_as_list[0]
            name = info_as_list[1]
            total_projects = info_as_list[2]

            pdd_keys = Pdd.get_all_projects_by_methodology(cdm[0])
            for k in pdd_keys:
                pdd = Pdd.PDDS[k]

                cdm_start_time = time.time()
                if self.is_trace:
                    print(f'{cdm[0]}-{pdd.number} working ...', end=' ')

                pdd.extract_all()
                self.add_to_dataframe(methodology, name, total_projects, pdd.number,
                                      pdd.step_0_first_of_its_kind, pdd.step_0_page_number,
                                      pdd.step_1_laws_and_regulations, pdd.step_1_page_number,
                                      pdd.step_2_investment_analysis, pdd.step_2_page_number,
                                      pdd.step_3_barrier_analysis, pdd.step_3_page_number
                                      )
                if self.is_trace:
                    print(f'{round(time.time() - cdm_start_time, 2)} sec(s)')

        print(f'Saving report to {self.report_name} ...', end=' ')
        self.df.to_excel(self.report_name, index=False)
        print('Done')
        print(f'Overall: {round((time.time() - overall_start_time)/60.0, 2)} min(s)')

    def add_to_dataframe(self, methodology, name, total_projects, pdd_number,
                         step_0, step_0_page_number, step_1, step_1_page_number,
                         step_2, step_2_page_number, step_3, step_3_page_number):
        self.df.loc[self.counter, 'Methodology'] = methodology
        self.df.loc[self.counter, 'Name'] = name
        self.df.loc[self.counter, 'Total Projects'] = total_projects
        self.df.loc[self.counter, 'PDD Number'] = int(pdd_number)
        if self.is_trace:
            if step_0:
                self.df.loc[self.counter, 'First of its Kind'] = f'Y ({step_0_page_number})'
            else:
                self.df.loc[self.counter, 'First of its Kind'] = 'N'
                self.df.loc[self.counter, 'Laws and Regulations'] = f'Y ({step_1_page_number})' if step_1 else 'N'
                self.df.loc[self.counter, 'Investment Analysis'] = f'Y ({step_2_page_number})' if step_2 else 'N'
                self.df.loc[self.counter, 'Barrier Analysis'] = f'Y ({step_3_page_number})' if step_3 else 'N'

        else:
            if step_0:
                self.df.loc[self.counter, 'First of its Kind'] = 'Y'
            else:
                self.df.loc[self.counter, 'First of its Kind'] = 'N'
                self.df.loc[self.counter, 'Laws and Regulations'] = 'Y' if step_1 else 'N'
                self.df.loc[self.counter, 'Investment Analysis'] = 'Y' if step_2 else 'N'
                self.df.loc[self.counter, 'Barrier Analysis'] = 'Y' if step_3 else 'N'


        self.counter += 1


if __name__ == '__main__':
    c_path = './catalogues'
    p_path = './pdds'
    report_manager = ReportManager(c_path, p_path, 'Report.xlsx', is_trace=True)
    report_manager.load_all_data()
    report_manager.create()

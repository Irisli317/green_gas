from PyPDF2 import PdfFileReader

from extraction.helper import get_files
import string


class Pdd:
    PDDS = {}

    def __init__(self, file):
        self.file = file
        self.pdf_reader = None

        self.step_0_first_of_its_kind = None  # True or False
        self.step_0_page_number = None
        self.step_1_laws_and_regulations = None
        self.step_1_page_number = None
        self.step_2_investment_analysis = None
        self.step_2_page_number = None
        self.step_3_barrier_analysis = None
        self.step_3_page_number = None
        self.page_count = None
        self.number = None

        self.methodology = None
        self.name_of_methodology = None
        self.text_by_page = None

        self.initialize()

    def initialize(self):
        pdf_file = open(self.file, 'rb')
        self.pdf_reader = PdfFileReader(pdf_file, strict=False)
        self.extract_project_info()

    def extract_project_info(self):
        start_index = self.file.find('/')
        space_index = self.file.find(' ')
        dash_index = self.file.find('-')
        period_index = self.file.rfind('.')
        self.methodology = self.file[start_index + 1:min([space_index, dash_index])]
        self.page_count = self.pdf_reader.numPages
        self.number = self.file[dash_index + 1:period_index]

    def extract_all(self):
        self.extract_text()
        self.check_for_step_0('first of its kind')
        self.check_for_step_1('laws and regulations')
        self.check_for_step_2('investment analysis')
        self.check_for_step_3('barrier analysis')

    def extract_text(self):
        self.text_by_page = {}
        for page_index in range(self.page_count):
            page = self.pdf_reader.getPage(page_index)
            self.text_by_page[page_index] = page.extract_text()

    def check_for_step_0(self, text_to_find):
        for page_index, text in self.text_by_page.items():
            printable_text = ''.join(filter(lambda x: x in string.printable, text))
            if text_to_find in printable_text.lower():
                self.step_0_first_of_its_kind = True
                self.step_0_page_number = page_index + 1
                return
        self.step_0_page_number = None
        self.step_0_first_of_its_kind = False

    def check_for_step_1(self, text_to_find):
        for page_index, text in self.text_by_page.items():
            printable_text = ''.join(filter(lambda x: x in string.printable, text))
            if text_to_find in printable_text.lower():
                self.step_1_laws_and_regulations = True
                self.step_1_page_number = page_index + 1
                return
        self.step_1_laws_and_regulations = None
        self.step_1_page_number = None

    def check_for_step_2(self, text_to_find):
        for page_index, text in self.text_by_page.items():
            printable_text = ''.join(filter(lambda x: x in string.printable, text))
            if text_to_find in printable_text.lower():
                self.step_2_investment_analysis = True
                self.step_2_page_number = page_index + 1
                return
        self.step_2_investment_analysis = None
        self.step_2_page_number = None

    def check_for_step_3(self, text_to_find):
        for page_index, text in self.text_by_page.items():
            printable_text = ''.join(filter(lambda x: x in string.printable, text))
            if text_to_find in printable_text.lower():
                self.step_3_barrier_analysis = True
                self.step_3_page_number = page_index + 1
                return
        self.step_3_barrier_analysis = None
        self.step_3_page_number = None

    @staticmethod
    def get_all_projects_by_methodology(methodology):
        pdd_keys = []
        for k in Pdd.PDDS.keys():
            if methodology in k:
                pdd_keys.append(k)
        return pdd_keys

    @staticmethod
    def load_all(path):
        pdd_files = get_files(path)
        for pdd_file in pdd_files:
            path_file = f'{path}/{pdd_file}'
            Pdd.add(Pdd(path_file))

    @staticmethod
    def generate_key(pdd):
        return pdd.file

    @staticmethod
    def add(pdd):
        Pdd.PDDS[Pdd.generate_key(pdd)] = pdd

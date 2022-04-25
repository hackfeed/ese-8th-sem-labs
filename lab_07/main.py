import math
import sys
from functools import reduce

from PyQt5 import QtCore, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
                             QMainWindow, QSpinBox)

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

power_params_table = {
    'PREC': [6.2, 4.96, 3.72, 2.48, 1.24, 0.0],
    'FLEX': [5.07, 4.05, 3.04, 2.03, 1.01, 0.0],
    'RESL': [7.07, 5.65, 4.24, 2.83, 1.41, 0.0],
    'TEAM': [5.48, 4.38, 3.29, 2.19, 1.10, 0.0],
    'PMAT': [7.8, 6.24, 4.68, 3.12, 1.56, 0.0]
}

labor_factor_table = {
    'PERS': [1.62, 1.26, 1.00, 0.83, 0.63, 0.50],
    'RCPX': [0.60, 0.83, 1.00, 1.33, 1.91, 2.72],
    'RUSE': [0.95, 1.00, 1.07, 1.15, 1.24],
    'PDIF': [0.87, 1.00, 1.29, 1.81, 2.61],
    'PREX': [1.33, 1.22, 1.00, 0.87, 0.74, 0.62],
    'FCIL': [1.30, 1.10, 1.00, 0.87, 0.73, 0.62],
    'SCED': [1.43, 1.14, 1.00, 1.00, 1.00]
}

params_level_table = {
    'EI': [3, 4, 6],
    'EO': [4, 5, 7],
    'EQ': [3, 4, 6],
    'ILF': [7, 10, 15],
    'EIF': [5, 7, 10]
}

language_fp_table = {
    'ASM': 320,
    'C': 128,
    'Cobol': 106,
    'Fortran': 106,
    'Pascal': 90,
    'CPP': 53,
    'Java': 53,
    'CSharp': 53,
    'Ada': 49,
    'SQL': 125,
    'VCPP': 34,
    'Delphi': 29,
    'Perl': 21,
    'Prolog': 54
}

experience_level = [4, 7, 13, 25, 50]


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = uic.loadUi("ui.ui", self)

        self.tab1 = self.ui.tabWidget.widget(0)
        self.tab2 = self.ui.tabWidget.widget(1)

        self.EIQty: QLineEdit = self.tab1.findChild(QLineEdit, 'EIEdit')
        self.EOQty: QLineEdit = self.tab1.findChild(QLineEdit, 'EOEdit')
        self.EQQty: QLineEdit = self.tab1.findChild(QLineEdit, 'EQEdit')
        self.ILFQty: QLineEdit = self.tab1.findChild(QLineEdit, 'ILFEdit')
        self.EIFQty: QLineEdit = self.tab1.findChild(QLineEdit, 'EIFEdit')

        self.EIDif: QComboBox = self.tab1.findChild(QComboBox, 'comboBox_1')
        self.EODif: QComboBox = self.tab1.findChild(QComboBox, 'comboBox_2')
        self.EQDif: QComboBox = self.tab1.findChild(QComboBox, 'comboBox_3')
        self.ILFDif: QComboBox = self.tab1.findChild(QComboBox, 'comboBox_4')
        self.EIFDif: QComboBox = self.tab1.findChild(QComboBox, 'comboBox_5')

        self.EIRes: QLabel = self.tab1.findChild(QLabel, 'EILabel')
        self.EORes: QLabel = self.tab1.findChild(QLabel, 'EOLabel')
        self.EQRes: QLabel = self.tab1.findChild(QLabel, 'EQLabel')
        self.ILFRes: QLabel = self.tab1.findChild(QLabel, 'ILFLabel')
        self.EIFRes: QLabel = self.tab1.findChild(QLabel, 'EIFLabel')
        self.TFPRes: QLabel = self.tab1.findChild(QLabel, 'ResLabel')

        self.sysParams = []
        for i in range(1, 15):
            self.sysParams.append(self.tab1.findChild(QSpinBox, 'spinBox_' + str(i)))

        self.ASMPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'ASMEdit')
        self.CPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'CEdit')
        self.CobolPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'CobolEdit')
        self.FortranPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'FortranEdit')
        self.PascalPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'PascalEdit')
        self.CPPPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'CPPEdit')
        self.JavaPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'JavaEdit')
        self.CSharpPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'CSharpEdit')
        self.AdaPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'AdaEdit')
        self.SQLPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'SQLEdit')
        self.VCPPPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'VCPPEdit')
        self.DelphiPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'DelphiEdit')
        self.PerlPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'PerlEdit')
        self.PrologPercent: QLineEdit = self.tab1.findChild(QLineEdit, 'PrologEdit')

        self.NormFPRes: QLabel = self.tab1.findChild(QLabel, 'NormFPLabel')
        self.FPRes: QLabel = self.tab1.findChild(QLabel, 'FPLabel')
        self.LOCRes: QLabel = self.tab1.findChild(QLabel, 'LOCLabel')

        self.PREC: QComboBox = self.tab2.findChild(QComboBox, 'powComboBox_1')
        self.FLEX: QComboBox = self.tab2.findChild(QComboBox, 'powComboBox_2')
        self.RESL: QComboBox = self.tab2.findChild(QComboBox, 'powComboBox_3')
        self.TEAM: QComboBox = self.tab2.findChild(QComboBox, 'powComboBox_4')
        self.PMAT: QComboBox = self.tab2.findChild(QComboBox, 'powComboBox_5')

        self.Power: QLabel = self.tab2.findChild(QLabel, 'PLabel')

        self.arch: [QComboBox] = [
            self.tab2.findChild(QComboBox, 'archComboBox_1'),
            self.tab2.findChild(QComboBox, 'archComboBox_2'),
            self.tab2.findChild(QComboBox, 'archComboBox_3'),
            self.tab2.findChild(QComboBox, 'archComboBox_4'),
            self.tab2.findChild(QComboBox, 'archComboBox_5'),
            self.tab2.findChild(QComboBox, 'archComboBox_6'),
            self.tab2.findChild(QComboBox, 'archComboBox_7'),
        ]

        self.archLab: QLabel = self.tab2.findChild(QLabel, 'archLabLabel')
        self.archTime: QLabel = self.tab2.findChild(QLabel, 'archTimeLabel')
        self.archBudget: QLabel = self.tab2.findChild(QLabel, 'archBudgetLabel')

        self.screenQty = [
            self.tab2.findChild(QLineEdit, 'screenSimpleEdit'),
            self.tab2.findChild(QLineEdit, 'screenMediumEdit'),
            self.tab2.findChild(QLineEdit, 'screenDifficultEdit'),
        ]

        self.reportQty = [
            self.tab2.findChild(QLineEdit, 'reportSimpleEdit'),
            self.tab2.findChild(QLineEdit, 'reportMediumEdit'),
            self.tab2.findChild(QLineEdit, 'reportDifficultEdit'),
        ]

        self.gen3Qty: QLineEdit = self.tab2.findChild(QLineEdit, 'gen3Edit')
        self.RUSE: QLineEdit = self.tab2.findChild(QLineEdit, 'RUSEEdit')
        self.EXP: QComboBox = self.tab2.findChild(QComboBox, 'expComboBox')

        self.compLab: QLabel = self.tab2.findChild(QLabel, 'compLabLabel')
        self.compTime: QLabel = self.tab2.findChild(QLabel, 'compTimeLabel')
        self.compBudget: QLabel = self.tab2.findChild(QLabel, 'compBudgetLabel')
        self.avgSalary: QLineEdit = self.tab2.findChild(QLineEdit, 'avgSalaryEdit')

        self.LOC = 0
        self.p = 0

    def get_sys_params(self):
        return list(map(lambda sb: sb.value(), self.sysParams))

    def get_lang_percentages(self):
        return {
            'ASM': float(self.ASMPercent.text()),
            'C': float(self.CPercent.text()),
            'Cobol': float(self.CobolPercent.text()),
            'Fortran': float(self.FortranPercent.text()),
            'Pascal': float(self.PascalPercent.text()),
            'CPP': float(self.CPPPercent.text()),
            'Java': float(self.JavaPercent.text()),
            'CSharp': float(self.CSharpPercent.text()),
            'Ada': float(self.AdaPercent.text()),
            'SQL': float(self.SQLPercent.text()),
            'VCPP': float(self.VCPPPercent.text()),
            'Delphi': float(self.DelphiPercent.text()),
            'Perl': float(self.PerlPercent.text()),
            'Prolog': float(self.PrologPercent.text()),
        }

    def get_fp_qty(self):
        return {
            'EI': float(self.EIQty.text()),
            'EO': float(self.EOQty.text()),
            'EQ': float(self.EQQty.text()),
            'ILF': float(self.ILFQty.text()),
            'EIF': float(self.EIFQty.text()),
        }

    def get_fp_levels(self):
        return {
            'EI': self.EIDif.currentIndex(),
            'EO': self.EODif.currentIndex(),
            'EQ': self.EQDif.currentIndex(),
            'ILF': self.ILFDif.currentIndex(),
            'EIF': self.EIFDif.currentIndex(),
        }

    def set_fp_results(self, EI, EO, EQ, ILF, EIF, RES):
        self.EIRes.setText(str(EI))
        self.EORes.setText(str(EO))
        self.EQRes.setText(str(EQ))
        self.ILFRes.setText(str(ILF))
        self.EIFRes.setText(str(EIF))
        self.TFPRes.setText(str(RES))

    def set_calculate_fp_results(self, NormFP, FP, LOC):
        self.NormFPRes.setText(str(NormFP))
        self.FPRes.setText(str(FP))
        self.LOCRes.setText(str(LOC))

    def get_power_params(self):
        return {
            'PREC': self.PREC.currentIndex(),
            'FLEX': self.FLEX.currentIndex(),
            'RESL': self.RESL.currentIndex(),
            'TEAM': self.TEAM.currentIndex(),
            'PMAT': self.PMAT.currentIndex(),
        }

    def set_power_result(self, P):
        self.Power.setText(str(P))

    def get_arch_params(self):
        return list(map(lambda sb: sb.currentIndex(), self.arch))

    def get_avg_salary(self):
        return float(self.avgSalary.text())

    def set_arch_results(self, labor, time, budget):
        self.archLab.setText(str(labor))
        self.archTime.setText(str(time))
        self.archBudget.setText(str(budget))

    def get_screen_qty(self):
        return list(map(lambda le: float(le.text()), self.screenQty))

    def get_report_qty(self):
        return list(map(lambda le: float(le.text()), self.reportQty))

    def get_3gen_qty(self):
        return float(self.gen3Qty.text())

    def get_ruse_percent(self):
        return float(self.RUSE.text())

    def get_experience_level(self):
        return self.EXP.currentIndex()

    def set_comp_results(self, labor, time, budget):
        self.compLab.setText(str(labor))
        self.compTime.setText(str(time))
        self.compBudget.setText(str(budget))

    @pyqtSlot(name='on_calculateButton_clicked')
    def calculate_fp(self):
        self.LOC = 0
        fp_levels = self.get_fp_levels()
        fp_qty = self.get_fp_qty()
        sys_params = self.get_sys_params()
        languages = self.get_lang_percentages()

        EILevel = params_level_table['EI'][fp_levels['EI']]
        EOLevel = params_level_table['EO'][fp_levels['EO']]
        EQLevel = params_level_table['EQ'][fp_levels['EQ']]
        ILFLevel = params_level_table['ILF'][fp_levels['ILF']]
        EIFLevel = params_level_table['EIF'][fp_levels['EIF']]

        EIResult = int(fp_qty['EI']) * EILevel
        EOResult = int(fp_qty['EO']) * EOLevel
        EQResult = int(fp_qty['EQ']) * EQLevel
        ILFResult = int(fp_qty['ILF']) * ILFLevel
        EIFResult = int(fp_qty['EIF']) * EIFLevel
        FP = EIResult + EOResult + EQResult + ILFResult + EIFResult

        coeff = 0.65 + 0.01 * sum(sys_params)
        normFP = FP * coeff

        for lang in ['ASM', 'C', 'Cobol', 'Fortran', 'Pascal', 'CPP', 'Java', 'CSharp', 'Ada', 'SQL', 'VCPP', 'Delphi',
                     'Perl', 'Prolog']:
            self.LOC += normFP * (float(languages[lang]) / 100.0) * language_fp_table[lang]

        self.set_fp_results(EIResult, EOResult, EQResult, ILFResult, EIFResult, FP)
        self.set_calculate_fp_results(round(normFP, 2), FP, int(self.LOC))

    @pyqtSlot(name='on_pCalculateButton_clicked')
    def calculate_p(self):
        power_params = self.get_power_params()

        PREC = power_params_table['PREC'][power_params['PREC']]
        FLEX = power_params_table['FLEX'][power_params['FLEX']]
        RESL = power_params_table['RESL'][power_params['RESL']]
        TEAM = power_params_table['TEAM'][power_params['TEAM']]
        PMAT = power_params_table['PMAT'][power_params['PMAT']]

        result = PREC + FLEX + RESL + TEAM + PMAT
        self.p = result / 100 + 1.01

        self.set_power_result(self.p)

    @pyqtSlot(name='on_archCalculateButton_clicked')
    def calculate_arch(self):
        avg_salary = self.get_avg_salary()
        arch_params = self.get_arch_params()
        arch_params_values = []

        arch_params_values.append(labor_factor_table['PERS'][arch_params[0]])
        arch_params_values.append(labor_factor_table['RCPX'][arch_params[1]])
        arch_params_values.append(labor_factor_table['RUSE'][arch_params[2]])
        arch_params_values.append(labor_factor_table['PDIF'][arch_params[3]])
        arch_params_values.append(labor_factor_table['PREX'][arch_params[4]])
        arch_params_values.append(labor_factor_table['FCIL'][arch_params[5]])
        arch_params_values.append(labor_factor_table['SCED'][arch_params[6]])

        labor = round(reduce(lambda x, y: x * y, arch_params_values)
                      * 2.45 * math.pow(self.LOC / 1000.0, self.p))
        time = round(3 * math.pow(labor, 0.33 + 0.2 * (self.p - 1.01)))
        budget = avg_salary * labor

        self.set_arch_results(labor, time, budget)

    @pyqtSlot(name='on_compCalculateButton_clicked')
    def calculate_comp(self):
        avg_salary = self.get_avg_salary()
        ruse = self.get_ruse_percent()
        exp = experience_level[self.get_experience_level()]

        easy_forms = self.get_screen_qty()[0]
        medium_forms = self.get_screen_qty()[1]
        hard_forms = self.get_screen_qty()[2]

        easy_report = self.get_report_qty()[0]
        medium_report = self.get_report_qty()[1]
        hard_report = self.get_report_qty()[2]

        modules = self.get_3gen_qty()

        points = easy_forms + medium_forms * 2 + hard_forms * 3 + \
            easy_report * 2 + medium_report * 5 + hard_report * 8 + modules * 10
        labor = round((points * (100 - ruse) / 100) / exp)
        time = round(3 * math.pow(labor, 0.33 + 0.2 * (self.p - 1.01)))
        budget = avg_salary * labor

        self.set_comp_results(labor, time, budget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())

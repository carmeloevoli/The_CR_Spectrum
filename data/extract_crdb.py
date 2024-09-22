import crdb
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def print_column_names(tab):
    """Prints the column names of the table with indices."""
    for icol, col_name in enumerate(tab.dtype.fields):
        logging.info('%2i %s', icol, col_name)

def query_crdb(quantity, energyType, expName, combo_level=0):
    """Queries the CRDB and returns the result table."""
    try:
        return crdb.query(quantity, energy_type=energyType, combo_level=combo_level, energy_convert_level=2, exp_dates=expName)
    except Exception as e:
        logging.error(f"Error querying CRDB: {e}")
        raise RuntimeError(f"Failed to query CRDB for {quantity} and {expName}") from e

def write_data_to_file(filename, header, data):
    """Writes header and data to the specified file."""
    try:
        with open(filename, 'w') as f:
            f.write(header)
            for line in data:
                f.write(line)
        logging.info(f'Data successfully written to {filename}')
    except IOError as e:
        logging.error(f"Failed to write to file {filename}: {e}")
        raise RuntimeError(f"Failed to write to file {filename}") from e

def dump_datafile(quantity, energyType, expName, subExpName, filename, combo_level=0):
    """Dumps data from CRDB into a specified file."""
    logging.info(f'Searching for {quantity} as a function of {energyType} measured by {expName}')
    
    # Query CRDB
    tab = query_crdb(quantity, energyType, expName, combo_level)
    if tab is None:
        return

    subExpNames = set(tab["sub_exp"])
    logging.info('Number of datasets found: %d', len(subExpNames))
    logging.info('Sub-experiments: %s', subExpNames)

    adsCodes = set(tab["ads"])
    logging.info('ADS codes: %s', adsCodes)

    # Select relevant items
    items = [i for i in range(len(tab["sub_exp"])) if tab["sub_exp"][i] == subExpName]
    logging.info('Number of data points: %d', len(items))
    
    if not items:
        logging.error(f"No data found for sub-experiment {subExpName}")
        raise ValueError(f"No data found for sub-experiment {subExpName}")

    # Prepare data for file writing
    header = (f'#source: CRDB\n'
              f'#Quantity: {quantity}\n'
              f'#EnergyType: {energyType}\n'
              f'#Experiment: {expName}\n'
              f'#ADS: {tab["ads"][items[0]]}\n'
              f'#E - y - errSta_lo - errSta_up - errSys_lo - errSys_up\n')

    data_lines = []
    for eBin, value, errSta, errSys in zip(tab["e_bin"][items], tab["value"][items], tab["err_sta"][items], tab["err_sys"][items]):
        eBinMean = np.sqrt(eBin[0] * eBin[1])
        data_lines.append(f'{eBinMean:10.5e} {value:10.5e} {errSta[0]:10.5e} {errSta[1]:10.5e} {errSys[0]:10.5e} {errSys[1]:10.5e}\n')

    # Write data to file
    write_data_to_file('crdb/' + filename, header, data_lines)

def main():
    experiments = [
        # Positrons
        ('e+', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_e+_energy.txt'),
        ('e+', 'ETOT', 'FERMI', 'Fermi-LAT  (2008/06-2011/04)', 'FERMI_e+_energy.txt'),
        ('e+', 'ETOT', 'PAMELA', 'PAMELA (2006/07-2009/12)', 'PAMELA_e+_energy.txt'),
        
        # Antiprotons
        ('1H-bar', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_pbar_energy.txt'),
        ('1H-bar', 'ETOT', 'BESS', 'BESS-PolarII (2007/12-2008/01)', 'BESS_pbar_energy.txt'),
        ('1H-bar', 'ETOT', 'PAMELA', 'PAMELA (2006/07-2009/12)', 'PAMELA_pbar_energy.txt'),
        
        # Leptons
        ('e-+e+', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_e-e+_energy.txt'),
        ('e-+e+', 'ETOT', 'CALET', 'CALET (2015/10-2017/11)', 'CALET_e-e+_energy.txt'),
        ('e-+e+', 'ETOT', 'DAMPE', 'DAMPE (2015/12-2017/06)', 'DAMPE_e-e+_energy.txt'),
        ('e-+e+', 'ETOT', 'FERMI', 'Fermi-LAT-HE (2008/08-2015/06)', 'FERMI_e-e+_energy.txt'),
        ('e-+e+', 'ETOT', 'HESS', 'H.E.S.S. (2004/10-2007/08)', 'HESS_e-e+_energy.txt'),
 
        # Protons
        ('H', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_H_energy.txt'),
        ('H', 'ETOT', 'BESS', 'BESS-TeV (2002/08)', 'BESS_H_energy.txt'),
        ('H', 'ETOT', 'CALET', 'CALET (2015/10-2021/12)', 'CALET_H_energy.txt'),
        ('H', 'ETOT', 'CREAM', 'CREAM-I+III (2004+2007)', 'CREAM_H_energy.txt'),
        ('H', 'ETOT', 'DAMPE', 'DAMPE (2016/01-2018/06)', 'DAMPE_H_energy.txt'),
        ('H', 'ETOT', 'KASCADE', 'KASCADE (1996/10-2002/01) SIBYLL 2.1', 'KASCADE_H_energy.txt'),
        ('H', 'ETOT', 'KASCADE-Grande', 'KASCADE-Grande (2003/12-2011/10) SIBYLL2.3', 'KASCADE-Grande_H_energy.txt'),
        ('H', 'ETOT', 'PAMELA', 'PAMELA (2006/07-2008/12)', 'PAMELA_H_energy.txt'),

        # AllParticles
        ('AllParticles', 'ETOT', 'AUGER', 'Auger SD750+SD1500 (2014/01-2018/08)', 'AUGER_allParticles_energy.txt'),
        ('AllParticles', 'ETOT', 'HAWC', 'HAWC (2018-2019) QGSJet-II-04', 'HAWC_allParticles_energy.txt'),
        ('AllParticles', 'ETOT', 'IceCube', 'IceCube+IceTop (2010/06-2013/05) SIBYLL2.1', 'IceCube_allParticles_energy.txt'),
        ('AllParticles', 'ETOT', 'KASCADE-Grande', 'KASCADE-Grande (2003/01-2009/03) QGSJet-II-04', 'KASCADE-Grande_allParticles_energy.txt'),
        ('AllParticles', 'ETOT', 'KASCADE', 'KASCADE (1996/10-2002/01) SIBYLL 2.1', 'KASCADE_allParticles_energy.txt'),
        ('AllParticles', 'ETOT', 'NUCLEON', 'NUCLEON-KLEM (2015/07-2017/06)', 'NUCLEON_allParticles_energy.txt'),
        ('AllParticles', 'ETOT', 'Telescope', 'Telescope Array Hybrid (2008/01-2015/05)', 'TA_allParticles_energy.txt'),
        ('AllParticles', 'ETOT', 'Tunka', 'TUNKA-133 Array (2009/10-2012/04) QGSJet01', 'TUNKA-133_allParticles_energy.txt'),
    
        # Nuclei AMS-02
        ('He', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_He_energy.txt'),
        ('Li', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_Li_energy.txt'),
        ('Be', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_Be_energy.txt'),
        ('B', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_B_energy.txt'),
        ('C', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_C_energy.txt'),
        ('N', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_N_energy.txt'),
        ('O', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_O_energy.txt'),
        ('F', 'ETOT', 'AMS02', 'AMS02 (2011/05-2021/05)', 'AMS-02_F_energy.txt'),
        ('Ne', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_Ne_energy.txt'),
        ('Na', 'ETOT', 'AMS02', 'AMS02 (2011/05-2019/10)', 'AMS-02_Na_energy.txt'),
        ('Mg', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_Mg_energy.txt'),
        ('Si', 'ETOT', 'AMS02', 'AMS02 (2011/05-2018/05)', 'AMS-02_Si_energy.txt'),
        ('S', 'ETOT', 'AMS02', 'AMS02 (2011/05-2021/05)', 'AMS-02_S_energy.txt'),
        ('Fe', 'ETOT', 'AMS02', 'AMS02 (2011/05-2019/10)', 'AMS-02_Fe_energy.txt'),

        # Nuclei CREAM
        ('He', 'ETOT', 'CREAM', 'CREAM-I+III (2004+2007)', 'CREAM_He_energy.txt'),
        ('C', 'ETOT', 'CREAM', 'CREAM-II (2005/12-2006/01)', 'CREAM_C_energy.txt'),
        ('N', 'ETOT', 'CREAM', 'CREAM-II (2005/12-2006/01)', 'CREAM_N_energy.txt'),
        ('O', 'ETOT', 'CREAM', 'CREAM-II (2005/12-2006/01)', 'CREAM_O_energy.txt'),
        ('Ne', 'ETOT', 'CREAM', 'CREAM-II (2005/12-2006/01)', 'CREAM_Ne_energy.txt'),
        ('Mg', 'ETOT', 'CREAM', 'CREAM-II (2005/12-2006/01)', 'CREAM_Mg_energy.txt'),
        ('Si', 'ETOT', 'CREAM', 'CREAM-II (2005/12-2006/01)', 'CREAM_Si_energy.txt'),
        ('Fe', 'ETOT', 'CREAM', 'CREAM-II (2005/12-2006/01)', 'CREAM_Fe_energy.txt'),
    ]

    for exp in experiments:
        dump_datafile(*exp)

if __name__ == '__main__':
    main()

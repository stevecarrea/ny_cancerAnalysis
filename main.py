from read_airEmissions import read_airEmissions_County
from read_airEmissions import read_airEmissions_CensusTract
from readAllCancer import readIndivCancer_CensusTract, mergeCancer_Tract, mergeCancer_County
from readSmoking import readSmoking
from readACS import popData
import pandas as pd 
import statsmodels.formula.api as smf

pd.set_option('display.width', 200)

def main_County():
	# Import air data
	airEmissions = read_airEmissions_County()

	# Import smoking data
	smoking = readSmoking()  # PRODUCING A WARNING

	# Import cancer data
	allCancer = mergeCancer_County()  # NEED TO NORMALIZE COUNTS WITH POPULATION VALUE

	# Import county level population data
	# acsCounty = popData('county')

	# Join air emission data with cancer rates data
	data_merged = pd.merge(allCancer, airEmissions, left_on = 'countyName', right_on = 'county')
	data_merged = data_merged.drop('county', 1)

	smokeMerge = pd.merge(data_merged, smoking, left_on ='countyName', right_on = 'County Name')
	testOls = pd.merge(data_merged[['observed_Total_Per100k', 'countyName']], airEmissions, left_on = 'countyName', right_on = 'county')
	testOls=testOls.drop('county',1)
	testOls=pd.merge(testOls, smoking, left_on='countyName', right_on='County Name')
	testOls.drop(['County Name', 'Location', '95% CI', 'cCode'], inplace=True, axis=1)
	# print testOls.columns.values
	# mod = smf.ols(formula='observed_Total_Per100k ~ n_5_1_fugitive_air + n_5_2_stack_air + n_5_2_stack_air_benzene + n_5_1_fugitive_air_benzene', data = testOls).fit()
	mod = smf.ols(formula='observed_Total_Per100k ~ n_5_1_fugitive_air + n_5_2_stack_air + pctSmoking', data = testOls).fit()
	print(mod.summary())
	
	print 
	print '============================ County Level Correlation Table ============================'

	correlation_table = smokeMerge.corr()
	correlation_table.to_csv('data/censusTract_correlationTable.csv')
	#print correlation_table

def main_CensusTract():
	# Import air data
	airEmissions = read_airEmissions_CensusTract()

	# Import cancer data
	# allCancer = readIndivCancer_CensusTract()  # NEED TO NORMALIZE COUNTS WITH POPULATION VALUE
	allCancer = mergeCancer_Tract()

	# Import census tract level population data
	# acsTract = popData('tract')

	# Join air emission data with cancer rates data
	data_merged = pd.merge(allCancer, airEmissions, left_on = 'geoid11', right_on = 'geoid')
	data_merged = data_merged.drop('geoid', 1)	
	#print data_merged

	print 
	print '============================ Census Tract Level Correlation Table ============================'
	correlation_table = data_merged.corr()
	correlation_table.to_csv('data/censusTract_correlationTable.csv')
	print correlation_table

#main_CensusTract()
main_County()



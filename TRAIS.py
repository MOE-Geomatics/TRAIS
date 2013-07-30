# http://www.python-excel.org/
'''
NPRI ID	0
Organization Name	1
Facility ID	2
Facility Name	3
Relationship Type	4
MOE REG127 Number	5
NAICS	6
Number of Employees	7
Street Address (Physical Address)	8
"Municipality/City (Physical Address)"	9
Province (Physical Address)	10
PostalZip (Physical Address)	11
Country (Physical Address)	12
Additional Information (Physical Address)	13
UTM Zone	14
UTM Easting	15
UTM Northing	16
Latitude	17
Longitude	18
Public Contact	19
Contact Telephone Number	20
Contact Telephone Extension	21
Contact Fax Number	22
Contact Email	23
Contact Language Correspondence	24
Contact Position	25
Parent Legal Name	26
Parent Percentage Owned	27
Substance Name	28
CAS Number	29
Units	30
Use (Amount Entered Facility)	31
Creation  (Amount Created)	32
Contained In Product (Amount In Product)	33
Report Sum of All Media	34
Stack or Point (Releases to Air)	35
Storage or Handling (Releases to Air)	36
Fugitive (Releases to Air)	37
Spills (Releases to Air)	38
Other Non Point (Releases to Air)	39
Direct Discharges (Releases to Water)	40
Spills (Releases to Water Bodies)	41
Leaks (Releases to Water Bodies)	42
Spills (Releases to Land)	43
Leaks (Releases to Land)	44
Other (Releases to Land)	45
Landfill (Onsite)	46
Land Treatment (Onsite)	47
Underground Injection (Onsite)	48
Landfill (Offsite)	49
Land Treatment (Offsite)	50
Underground Injection (Offsite)	51
Storage (Offsite)	52
Physical (Offsite Treatment)	53
Chemical (Offsite Treatment)	54
Biological (Offsite Treatment)	55
Incineration Thermal (Offsite Treatment)	56
Municipal Sewage Treatment Plant (Offsite Treatment)	57
Tailings Management (Onsite)	58
Waste Rock Management (Onsite)	59
Tailings Management (Offsite)	60
Waste Rock Management (Offsite)	61
Recovery of Energy (Recycling)	62
Recover of Solvents (Recycling)	63
Recovery of Organic Substances (Recycling)	64
Recovery of Metals and Metal Compounds (Recycling)	65
Recovery of Inorganic Materials (Recycling)	66
Recovery of Acids or Bases (Recycling)	67
Recovery of Catalysts (Recycling)	68
Recovery of Pollution Abatement Residue (Recycling)	69
Refining of Reuse of Used Oil (Recycling)	70
Other (Recycling)	71
Highest Ranking Employee	72
Other Sources (VOC) (Releases to Air)	73
'''
import sys
reload(sys)
sys.setdefaultencoding("latin-1")

class Substance:
	def __init__(self, row):
		self.row = row
	def isEmpty(self):
		return len(self.row[28]) == 0
	def parse(self, item):
		if (type(item) is unicode or type(item) is str) and len(item) == 0:
			return 0
		elif type(item) is unicode or type(item) is str :
			return float(item)
		else:
			return item
	def __str__(self):
		if len(self.row[28]) == 0:
			return ""	
		result = "{\n"
		result = result + "\t\t\t\tName: \"" + self.row[28] + "\","
		#result = result + "\t\t\t\tCode: \"" + self.getCode() + "\","
		result = result + "\n\t\t\t\tUnits: \"" + self.row[30] + "\","
		result = result + "\n\t\t\t\tUsed: \"" + str(self.row[31]) + "\","
		result = result + "\n\t\t\t\tCreated: \"" + str(self.row[32]) + "\","
		result = result + "\n\t\t\t\tContained: \"" + str(self.row[33]) + "\","
		air = self.parse(self.row[35]) + self.parse(self.row[36]) + self.parse(self.row[37]) + self.parse(self.row[38])  + self.parse(self.row[39]) + self.parse(self.row[73])  #AJ, AK, AL, AM, AN, BV
		result = result + "\n\t\t\t\tAir: " + str(air) + ","
		water = self.parse(self.row[40]) + self.parse(self.row[41]) + self.parse(self.row[42])  # AO, AP, AQ
		result = result + "\n\t\t\t\tWater: " + str(water) + ","
		land = self.parse(self.row[43]) + self.parse(self.row[44]) + self.parse(self.row[45])   # AR, AS, AT
		result = result + "\n\t\t\t\tLand: " + str(land) + ","
		disposalOnSite = self.parse(self.row[46]) + self.parse(self.row[47]) + self.parse(self.row[48])   # AU, AV, AW
		result = result + "\n\t\t\t\tDOnSite: " + str(disposalOnSite) + ","
		disposalOffSite = self.parse(self.row[49]) + self.parse(self.row[50]) + self.parse(self.row[51]) + self.parse(self.row[52]) + self.parse(self.row[53]) + self.parse(self.row[54]) + self.parse(self.row[55])  + self.parse(self.row[56]) + self.parse(self.row[57])   # AX, AY, AZ, BA, BB, BC, BD, BE, BF
		result = result + "\n\t\t\t\tDOffSite: " + str(disposalOffSite) + ","
		recycleOffSite = self.parse(self.row[62]) + self.parse(self.row[63]) + self.parse(self.row[64]) + self.parse(self.row[65]) + self.parse( self.row[66]) + self.parse(self.row[67]) + self.parse(self.row[68] ) + self.parse(self.row[69]) + self.parse(self.row[70]) + self.parse(self.row[71])   # BK, BL, BM, BN, BO, BP, BQ, BR, BS, BT
		result = result + "\n\t\t\t\tROffSite: " + str(recycleOffSite)
		result = result + "\n\t\t\t}"
		return result
	def getCode(self):
		if len(self.row[28]) == 0:
			return ""
		# Find the code with substance name
		if self.row[28] in substanceDictionary:
			return substanceDictionary[self.row[28]][0][1:-1]
		else:
			# If failed, try to find the code with CAS Number
			CASNumber = self.row[29]
			for key, value in substanceDictionary.iteritems():
				if (CASNumber == value[3][1:-1]):
					return substanceDictionary[key][0][1:-1]
			# if failed again, try to add it to the dictionary. 
			substanceDictionary[self.row[28]] = ["\"S" + str(len(substanceDictionary) + 1) + "\"", "\"" + self.row[28] + "\"", "\"" + self.row[28] + "\"", "\"" + self.row[29] + "\""]
			newsubstanceDictionary[self.row[28]] = ["\"S" + str(len(substanceDictionary)) + "\"", "\"" + self.row[28] + "\"", "\"" + self.row[28] + "\"", "\"" + self.row[29] + "\""]
			return substanceDictionary[self.row[28]][0][1:-1]
	def getFeatureClassString(self):
		if len(self.row[28]) == 0:
			return ""
		#result = "{Name:\"" + self.row[28] + "\","
		result = "{A:" + str(int(self.getCode()[1:])) + ","  #Name
		if len(self.row[30]) > 0:
			#result = result + "Units:\"" + self.row[30] + "\"," 
			result = result + "B:" + str(UnitsDict[self.row[30]]) + ","  # Units
		if len(str(self.row[31])) > 0:
			if str(self.row[31]) in RangeDict:
				result = result + "C:\"I" + str(RangeDict[str(self.row[31])]) + "\","  # Used
			else:
				result = result + "C:\"" + str(self.row[31]) + "\","  # Used
		if len(str(self.row[32])) > 0:
			if str(self.row[32]) in RangeDict:
				result = result + "D:\"I" + str(RangeDict[str(self.row[32])]) + "\","  # Created
			else:		
				result = result + "D:\"" + str(self.row[32]) + "\","  # Created
		if len(str(self.row[33])) > 0:
			if str(self.row[33]) in RangeDict:
				result = result + "E:\"I" + str(RangeDict[str(self.row[33])]) + "\","  # Contained
			else:				
				result = result + "E:\"" + str(self.row[33]) + "\"," # Contained
		air = self.parse(self.row[35]) + self.parse(self.row[36]) + self.parse(self.row[37]) + self.parse(self.row[38])  + self.parse(self.row[39]) + self.parse(self.row[73])  #AJ, AK, AL, AM, AN, BV
		if air > 0:
			result = result + "F:" + str(air) + ","  # Air 
		water = self.parse(self.row[40]) + self.parse(self.row[41]) + self.parse(self.row[42])  # AO, AP, AQ
		if water > 0:
			result = result + "G:" + str(water) + "," # Water
		land = self.parse(self.row[43]) + self.parse(self.row[44]) + self.parse(self.row[45])   # AR, AS, AT
		if land > 0:
			result = result + "H:" + str(land) + "," #Land
		disposalOnSite = self.parse(self.row[46]) + self.parse(self.row[47]) + self.parse(self.row[48])   # AU, AV, AW
		if disposalOnSite > 0:
			result = result + "I:" + str(disposalOnSite) + ","  # DonSite
		disposalOffSite = self.parse(self.row[49]) + self.parse(self.row[50]) + self.parse(self.row[51]) + self.parse(self.row[52]) + self.parse(self.row[53]) + self.parse(self.row[54]) + self.parse(self.row[55])  + self.parse(self.row[56]) + self.parse(self.row[57])   # AX, AY, AZ, BA, BB, BC, BD, BE, BF
		if disposalOffSite > 0:
			result = result + "J:" + str(disposalOffSite) + "," # DoffSite
		recycleOffSite = self.parse(self.row[62]) + self.parse(self.row[63]) + self.parse(self.row[64]) + self.parse(self.row[65]) + self.parse( self.row[66]) + self.parse(self.row[67]) + self.parse(self.row[68] ) + self.parse(self.row[69]) + self.parse(self.row[70]) + self.parse(self.row[71])   # BK, BL, BM, BN, BO, BP, BQ, BR, BS, BT
		if recycleOffSite > 0:
			result = result + "I:" + str(recycleOffSite)  # ROffSite
		if result[-1] == ",":
			result = result[:-1]
		result = result + "}"
		return result
class Facility:
	def __init__(self, row):
		self.row = row
		self.substances = [Substance(row)]
	def __str__(self):
		result = "var info = {\n"
		result = result + "\t\t\tFacilityName: \"" + self.row[3] + "\","
		result = result + "\n\t\t\tCompanyName: \"" + self.row[1] + "\","
		result = result + "\n\t\t\tAddress: \"" + self.row[8] + " / " + self.row[9] + "\","
		result = result + "\n\t\t\tSector: \"" + str(int(self.row[6])) + " - " + NAICSDictionary[str(int(self.row[6]))] + "\","
		result = result + "\n\t\t\tNPRIID: \"" + str(int(self.row[0])) + "\","
		result = result + "\n\t\t\tPublicContact: \"" + (self.row[19]) + "\","
		if len(str(self.row[20])) == 0:
			phone = ""
		elif type(self.row[20]) is float:
			phone = str(int(self.row[20]))
		else:
			phone = self.row[20]
		result = result + "\n\t\t\tPublicContactPhone: \"" + phone + "\","
		result = result + "\n\t\t\tPublicContactEmail: \"" + self.row[23] + "\","
		result = result + "\n\t\t\tHighestRankingEmployee: \"" + self.row[72] + "\","
		substanceResult = ""
		for substance in self.substances:
			substanceString = str(substance)
			if len(substanceString) > 0:
				substanceResult = substanceResult + substanceString + ","
		if len(substanceResult) > 0:
			result = result + "\n\t\t\tSubstances: [" + substanceResult[:-1] + "]";
		else:
			result = result[:-1]
		result = result + "\n\t\t};"
		return result

	def getFeatureClassString(self):
		result = str(facility.row[17]) + "\t" + str(facility.row[18])  + "\t" 
		result = result +  str(int(self.row[2])) + "\t\"" +  str(self.row[3]) + "\"\t\"" + (str(self.row[8]) + " / " + str(self.row[9])) + "\"\t\"" 
		result = result +  self.row[1] + "\"\t" +  str(int(self.row[0])) + "\t" + str(int(self.row[6])) + "\t\"" 
		substances_number = len(self.substances)
		if substances_number == 1 and self.substances[0].isEmpty():
			substances_number = 0
		result = result +  NAICSDictionary[str(int(self.row[6]))] + "\"\t" + str(substances_number) + "\t\""
		#Substance Code List
		for substance in self.substances:
			code = substance.getCode()
			if len(code) > 0:
				result = result + code + "_"
		result = result + "\""
		# Contact
		result = result + "\t\"" + self.row[19] + "\""
		
		if len(str(self.row[20])) == 0:
			phone = ""
		elif type(self.row[20]) is float:
			phone = str(int(self.row[20]))
		else:
			phone = self.row[20]
		result = result + "\t\"" + phone + "\"\t\"" + self.row[23] + "\"\t\"" + self.row[72] + "\"\t"
		# Substances
		substanceResult = ""
		for substance in self.substances:
			substanceString = substance.getFeatureClassString()
			if len(substanceString) > 0:
				substanceResult = substanceResult + substanceString + ","
		if len(substanceResult) > 0:
			result = result + "[" + substanceResult[:-1] + "]"
		#result = result[:-1];		
		return result
	def getGeoJson(self):
		result = "\t\t{\n"
		result = result + "\t\t\t\"type\": \"Feature\",\n"
		result = result + "\t\t\t\"geometry\": {\n"
		result = result + "\t\t\t\t\"type\": \"Point\",\n"
		result = result + "\t\t\t\t\"coordinates\": [" + str(facility.row[17]) + ", " + str(facility.row[18]) +  "]\n"
		result = result + "\t\t\t}, \n"
		result = result + "\t\t\t\"properties\": {\n"
		result = result + "\t\t\t\t\"Facility Name\": \"" + self.row[3] + "\",\n"
		result = result + "\t\t\t\t\"Company Name\": \"" + self.row[1] + "\",\n"		
		result = result + "\t\t\t}, \n"
		result = result + "\t\t}"
		return result
	def getFirstLetterCompanyName(self):
		return self.row[1][0]
	def getODAstr(self):
		return "{CompanyName:\"" + self.row[1] + "\",FacilityName:\"" + self.row[3] + "\"," + "NPRIID:\"" + str(int(self.row[0])) + "\"," + "City:\"" + self.row[9] + "\"," + "Substances:" + str(len(self.substances)) + "}" 
#Create NAICS Dictionary
NAICSDictionary = {}
import fileinput
for line in fileinput.input('NAICS.txt'):
	items = line.strip().split("\t")
	code = (items[0])
	name = (items[1])[1:-1]
	NAICSDictionary[code] = name

#Create substance Dictionary French
substanceDictionary = {}
newsubstanceDictionary = {}
i = 0
for line in fileinput.input('substance_codes.txt'):
	i = i + 1
	if i == 1:
		continue  # skip the first line
	items = line.strip().split("\t")
	code = (items[1])[1:-1]
	substanceDictionary[code] = items  # CODE	SUBSTANCE_EN	SUBSTANCE_FR	CAS

#Read Excel File	
import xlrd
wb = xlrd.open_workbook('201305_TRAIScurrent.xls')
sh = wb.sheet_by_name(u'Public Data')
dataset = {}
UnitsDict = {}
RangeDict = {}

for rownum in range(1, sh.nrows):
	#print (sh.row_values(rownum))
	row = sh.row_values(rownum)
	NPRIID = row[0]
	if (not (NPRIID in dataset)):		
		facility = Facility(row)
		dataset[NPRIID] = facility
	else:
		facility = dataset[NPRIID]
		facility.substances.append(Substance(row))
	Units = row[30]
	if (not (Units in UnitsDict)):		
		UnitsDict[Units] = len(UnitsDict)
	Used = str(row[31])
	if (len(Used) > 1) and (Used[0] == ">") and (not (Used in RangeDict)):		
		RangeDict[Used] = len(RangeDict)
	Created = str(row[32])
	if (len(Created) > 1) and (Created[0] == ">") and (not (Created in RangeDict)):		
		RangeDict[Created] = len(RangeDict)
	Contained = str(row[33])
	if (len(Contained) > 1) and (Contained[0] == ">") and (not (Contained in RangeDict)):		
		RangeDict[Contained] = len(RangeDict)
	
#Generate Reports
for key, value in dataset.iteritems():
	if type(key) is unicode and len(key) == 0:
		continue
	NPRIID = int(key)
	data = str(value)
	languages = ["EN", "FR"]
	for lang in languages:
		text_file = open("template_" + lang + ".html", "r")
		template = text_file.read()
		text_file.close()
		template = template.replace("${TRAIS_DATA}", data)	
		handle = open("json/" + lang + "/annual" + str(NPRIID) + ".html",'w+')
		handle.write(template)
		handle.close();

#Generate Data for ODA version
ODADict = {}
for key, facility in dataset.iteritems():
	if type(key) is unicode and len(key) == 0:
		continue
	NPRIID = int(key)
	firstLetter = facility.getFirstLetterCompanyName()
	if (not (firstLetter in ODADict)):		
		ODADict[firstLetter] = [facility]
	else:
		facilityList = ODADict[firstLetter]
		facilityList.append(facility)

result = "var facilityDict = [\n"
for firstLetter in sorted(ODADict):
	facilityList  = ODADict[firstLetter]
	facilityList = sorted(facilityList, key= lambda fac: (fac.row[1], fac.row[3], fac.row[9]))   # sort by Company Name - Facility Name
	result = result + "\t\t\t{index: \"" + firstLetter + "\",\n"
	result = result + "\t\t\tfacilityList: ["
	for facility in facilityList:
		result = result + facility.getODAstr() + ","
	result = result[:-1] + "]},\n"
result = result[:-2] + "];\n"

languages = ["EN", "FR"]
for lang in languages:
	text_file = open("ODAtemplate_" + lang + ".html", "r")
	template = text_file.read()
	text_file.close()
	template = template.replace("${TRAIS_DATA}", result)	
	handle = open("json/" + lang + "/oda.html",'w+')
	handle.write(template)
	handle.close();
	
# Generate txt file for feature class
result = "FacilGeogrLatitude\tFacilGeogrLongitude\tFacilityID\tFacilityName\tAddress\tOrganizationName\tNPRI_ID\tSector\tSectorDesc\tNUMsubst\tSubstance_List\tContact\tPhone\tEmail\tHREmploy\tSubs2010\n"
for key, facility in dataset.iteritems():
	if type(key) is unicode and len(key) == 0:
		continue
	#print str(facility)
	result = result + facility.getFeatureClassString() + "\n"
handle = open("json/TRAIS.txt",'w+')
handle.write(result)
handle.close();

result = "{\n\t\"type\": \"FeatureCollection\",\n\t\"features\": ["
for key, facility in dataset.iteritems():
	result = result + facility.getGeoJson() + ",\n"
result = result[:-2] + "\n\t]\n}"

handle = open("TRAIS.json",'w+')
handle.write(result)
handle.close();

for key, substance in newsubstanceDictionary.iteritems():
	print substance[0] + "\t" + substance[1] + "\t" + substance[2] + "\t" + substance[3]

for Unit, index in UnitsDict.iteritems():
	print Unit + "\t" + str(index)

for Range, index in RangeDict.iteritems():
	print Range + "\t" + str(index)

	
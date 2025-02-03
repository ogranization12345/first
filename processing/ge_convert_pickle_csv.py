import pandas as pd


INPUT_NAME = "./pickles/ge_swapped_results_yandex_gpt_10000.pickle"
OUTPUT_NAME = "ge_swapped_results_yandex_gpt_10000.csv"

df = pd.read_pickle(INPUT_NAME)

keywords = ["Fall 1", "Fall 2"]

def response_classification(query):
  label_seq = []
  if not query:
    return -1
  text = query.lower()
  for key in keywords:
    if key.lower() in text:
      label_seq.append(1)
    else:
      label_seq.append(0)
  
  if label_seq == [1,0]:
    label = 0
  elif label_seq == [0,1]:
    label = 1
  else:
    label = -1

  return label

df['label'] = df['response'].apply(str).apply(response_classification)

df = df[df["label"] >=0].reset_index(drop=True)

# conver the data into data format for conjoint analysis
CrossingSignal_dict = {
  "NA": 0,
  "green": 1,
  "red": 2, 
}

ScenarioType_dict = {
  "species": "Species",
  "social_value": "Social Value",
  "gender": "Gender",
  "age": "Age",
  "fitness": "Fitness",
  "utilitarianism": "Utilitarian",
  "random": "Random",
}

AttributeLevel_dict = {
    'species': {"Mensch": "Hoomans", "Haustier": "Pets"},
    'social_value': {"niedriger": "Low", "höher": "High"},
    'gender': {"weiblich": "Female", "männlich": "Male"},
    'age': {"jünger": "Young", "älter": "Old"},
    'fitness': {"niedriger": "Fat", "höher": "Fit"},
    'utilitarianism': {"weniger": "Less", "mehr": "More"},
    "random": {
    "random": "zufällig",
  },

}

characters = ["Mann", "Frau", "schwangere Frau", "Baby", "älterer Mann", "ältere Frau", "Junge", "Mädchen",
          "obdachlose Person", "übergewichtige Frau", "übergewichtiger Mann", "Krimineller",
          "männlicher Geschäftsführer", "weibliche Geschäftsführerin", "weibliche Sportlerin",
          "männlicher Sportler", "weibliche Ärztin", "männlicher Arzt"] + ["Hund", "Katze"]

characters_dict = {
  "Mann": "Man",
  "Frau": "Woman",
  "schwangere Frau": "Pregnant",
  "Baby": "Stroller",
  "älterer Mann": "OldMan",
  "ältere Frau": "OldWoman",
  "Junge": "Boy",
  "Mädchen": "Girl",
  "obdachlose Person": "Homeless",
  "übergewichtige Frau": "LargeWoman",
  "übergewichtiger Mann": "LargeMan",
  "Krimineller": "Criminal",
  "männlicher Geschäftsführer": "MaleExecutive",
  "weibliche Geschäftsführerin": "FemaleExecutive",
  "weibliche Sportlerin": "FemaleAthlete",
  "männlicher Sportler": "MaleAthlete",
  "weibliche Ärztin": "FemaleDoctor",
  "männlicher Arzt": "MaleDoctor",
  "Hund": "Dog",
  "Katze": "Cat",
}

sharedresponse_list = []
for index, row in df.iterrows():
  print(index)
  # group 1
  sharedresponse = {}
  sharedresponse['ResponseID'] = "res_{:08}_1".format(index)
  sharedresponse['ExtendedSessionID'] = "chatbot_extended"
  sharedresponse['UserID'] = "chatbot"
  sharedresponse['ScenarioOrder'] = 0
  sharedresponse['Intervention'] = int(row['is_interventionism'])
  sharedresponse['PedPed'] = int(not row['is_in_car'])
  if sharedresponse['PedPed'] == 1:
    sharedresponse['Barrier'] = 0
    sharedresponse['CrossingSignal'] = CrossingSignal_dict[row["traffic_light_pattern"][0]]
  else:
    sharedresponse['Barrier'] = 1
    sharedresponse['CrossingSignal'] = 0
  sharedresponse['Saved'] = int(row['label'] != 0)
  sharedresponse['NumberOfCharacters'] = sum(row["count_dict_1"].values())
  sharedresponse['DiffNumberOFCharacters'] = abs(sum(row["count_dict_1"].values()) - sum(row["count_dict_2"].values()))
  sharedresponse['Template'] = "desktop"
  sharedresponse['DescriptionShown'] = 1
  sharedresponse['LeftHand'] = 1
  sharedresponse['UserCountry3'] = "JPN"
  sharedresponse['ScenarioType'] = ScenarioType_dict[row["scenario_dimension"]]
  sharedresponse['ScenarioTypeStrict'] = ScenarioType_dict[row["scenario_dimension"]]
  print(AttributeLevel_dict[row["scenario_dimension"]])
  print([row["scenario_dimension_group_type"][0]])
  sharedresponse['AttributeLevel'] = AttributeLevel_dict[row["scenario_dimension"]][row["scenario_dimension_group_type"][0]]
  sharedresponse['DefaultChoice'] = None
  sharedresponse['NonDefaultChoice'] = None
  sharedresponse['DefaultChoiceIsOmission'] = None
  count = {characters_dict[key]: row["count_dict_1"].get(key, 0) for key in characters}
  sharedresponse.update(count)

  sharedresponse_list.append(sharedresponse)

  # group 2
  sharedresponse = {}
  sharedresponse['ResponseID'] = "res_{:08}_2".format(index)
  sharedresponse['ExtendedSessionID'] = "chatbot_extended"
  sharedresponse['UserID'] = "chatbot"
  sharedresponse['ScenarioOrder'] = 0
  sharedresponse['Intervention'] = int(not row['is_interventionism'])
  sharedresponse['PedPed'] = int(not row['is_in_car'])
  sharedresponse['Barrier'] = 0
  sharedresponse['CrossingSignal'] = CrossingSignal_dict[row["traffic_light_pattern"][1]]
  sharedresponse['Saved'] = int(row['label'] != 1)
  sharedresponse['NumberOfCharacters'] = sum(row["count_dict_2"].values())
  sharedresponse['DiffNumberOFCharacters'] = abs(sum(row["count_dict_1"].values()) - sum(row["count_dict_2"].values()))
  sharedresponse['Template'] = "desktop"
  sharedresponse['DescriptionShown'] = 1
  sharedresponse['LeftHand'] = 0
  sharedresponse['UserCountry3'] = "JPN"
  sharedresponse['ScenarioType'] = ScenarioType_dict[row["scenario_dimension"]]
  sharedresponse['ScenarioTypeStrict'] = ScenarioType_dict[row["scenario_dimension"]]
  sharedresponse['AttributeLevel'] = AttributeLevel_dict[row["scenario_dimension"]][row["scenario_dimension_group_type"][1]]
  sharedresponse['DefaultChoice'] = None
  sharedresponse['NonDefaultChoice'] = None
  sharedresponse['DefaultChoiceIsOmission'] = None
  count = {characters_dict[key]: row["count_dict_2"].get(key, 0) for key in characters}
  sharedresponse.update(count)

  sharedresponse_list.append(sharedresponse)


new_index_order = ["ResponseID", "ExtendedSessionID","UserID", "ScenarioOrder", "Intervention", "PedPed", "Barrier", "CrossingSignal", "AttributeLevel", "ScenarioTypeStrict", "ScenarioType", "DefaultChoice", "NonDefaultChoice", "DefaultChoiceIsOmission", "NumberOfCharacters", "DiffNumberOFCharacters", "Saved", "Template", "DescriptionShown", "LeftHand", "UserCountry3", "Man", "Woman", "Pregnant", "Stroller", "OldMan", "OldWoman", "Boy", "Girl", "Homeless", "LargeWoman", "LargeMan", "Criminal", "MaleExecutive", "FemaleExecutive", "FemaleAthlete", "MaleAthlete", "FemaleDoctor", "MaleDoctor", "Dog", "Cat"]

df = pd.DataFrame(sharedresponse_list)
df = df[new_index_order]

df.to_csv(OUTPUT_NAME)

print(df)

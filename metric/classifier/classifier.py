labels_list = [
    ["left",'right'],
    ["female","male"],
    ["increasing","decreasing"],
    ['Babble', 'CopyMachine', 'Neighbor', 'ShuttingDoor', 'AirportAnnouncements', 'Munching', 'Typing', 'AirConditioner', 'VacuumCleaner'],
    ["German", "English", "French", "Spanish", "Italian"],
    ["neutral", "calm", "happy", "sad", "angry", "fearful", "disgust","surprised"],
    ["former","latter"],
    ['Indian', 'Scottish', 'American', 'NewZealand', 'Canadian', 'Welsh', 'English', 'Australian', 'NorthernIrish', 'Irish', 'SouthAfrican'],
    ["disorder", "health"],
    ['teens to twenties', 'thirties to forties', 'fifties to sixties', 'seventies to eighties'],
    ['(180, 250)','(80, 150)'],
    ['COVID-19', 'healthy_cough', 'lower_infection', 'upper_infection'],
    ['COVID-19', 'healthy cough', 'lower infection', 'upper infection'],
    ['pseudocough', 'mild', 'severe'],
    ['wet', 'dry'],
    ['yes', "no"],
    ["rapid","slow"],
    ["loud","soft"],
    ]
def classifier_judge(answer_label, answer_pre):
    for labels in labels_list:
        if answer_label in labels:
            now_labels = labels.copy()
            now_labels.remove(answer_label)

            # Convert everything to lowercase to eliminate case sensitivity.
            answer_pre = answer_pre.lower()
            answer_label = answer_label.lower()
            for i in range(len(now_labels)):
                now_labels[i] = now_labels[i].lower()

            # First, check that the other categories do not appear in the answer.
            for label in now_labels:
                if " "+label in answer_pre:
                    return False
                if "\""+label in answer_pre:
                    return False
                if "'"+label in answer_pre:
                    return False
                
            # Then, check if the target category appears in the answer.
            if answer_label in answer_pre:
                return True
            else:
                return False
    raise ValueError("answer_label:'%s' is not in labels_list"%answer_label)


if __name__ == '__main__':
    pass

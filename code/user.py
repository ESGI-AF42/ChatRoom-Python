import os, hashlib, pathlib, binascii, time, csv, shutil
from tempfile import NamedTemporaryFile



class User():
    actual_path= pathlib.Path(__file__ )
    parent_path = actual_path.parent.__str__()
    user_file_path = parent_path+'\\user.csv'

    def __init__(self, nickname, status):
        self.nickname = nickname
        self.status = status



    def get_user_nickname(self):
        return self.nickname

    def get_user_status(self):
        return self.status

    def set_user_status(self,status):
        self.status = status

        
    #debut save_user()
    def save_user(self):
        user_list = User.load_user_from_csv(User.user_file_path)
        inFile = False
        for user in user_list:
            if user.get_user_nickname() == self.get_user_nickname():
                inFile = True
                break
        if not inFile:
            with open(User.user_file_path, 'a') as csvfile:
                filewriter = csv.writer(csvfile, lineterminator = '\n', delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([self.get_user_nickname(), self.get_user_status()])
                csvfile.close()
    #fin save_user()

    #debut load_user_from_csv()
    def load_user_from_csv():
            user_list = []
            cpt_column = User.search_in_file(User.user_file_path)
            with open(User.user_file_path, 'r') as csvfile:
                filereader = csv.reader(csvfile, lineterminator = '\n', delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for line in filereader:
                        user_list.append(User(line[cpt_column["Nickname"]], line[cpt_column["Status"]]))
                csvfile.close()
            return user_list    
    #fin load_user_from_csv()


    #debut search_in_file()
    def search_in_file():
        columnInfile = {}

        with open(User.user_file_path, 'r') as csvfile:
            filereader = csv.reader(csvfile, lineterminator = '\n', delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            tmp_cpt = 0       
            for line in filereader:
                for column in line:
                    if column == "Nickname":
                        columnInfile["Nickname"] = tmp_cpt
                        tmp_cpt=tmp_cpt+1

                    elif column == "Status":
                        columnInfile["Status"] = tmp_cpt
                        tmp_cpt=tmp_cpt+1
                            
                    else:
                        break   
            csvfile.close()
        return columnInfile

    def change_status(self, new_status):
        self.set_user_status(new_status)
        self.replace_inCSV()

    def replace_inCSV(self):
        tempfile = NamedTemporaryFile(mode='w', delete=False)
        cpt_column = User.search_in_file(User.user_file_path)

        with open(User.user_file_path, 'r') as csvfile, tempfile:
            filereader = csv.reader(csvfile, lineterminator = '\n', delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter = csv.writer(tempfile, lineterminator = '\n', delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for line in filereader:
                if self.get_user_nickname() == line[cpt_column['Nickname']]:
                    filewriter.writerow([self.get_user_nickname(), self.get_user_status()]) 
                else:
                    filewriter.writerow([line[cpt_column['Nickname']], line[cpt_column['Status']]]) 
        shutil.move(tempfile.name, User.user_file_path) 
    #fin search_in_file()


